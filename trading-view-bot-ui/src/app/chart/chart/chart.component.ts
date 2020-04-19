import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import {
  SignalRegistryService,
  SignalType,
  SignalResponse
} from 'src/app/signals/signal-registry.service';
import { TickerResponse } from 'src/app/signals/ticker.service';
import { IndicatorResponse } from 'src/app/signals/indicator.service';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent implements OnInit, OnDestroy {
  chartOptions = {
    responsive: true,
    hoverMode: 'index',
    stacked: false,
    elements: { point: { radius: 0 } },
    title: {
      display: true,
      text: 'Trading view bot test data'
    },
    scales: {
      xAxes: [
        {
          type: 'time',
          time: {
            displayFormats: {
              quarter: 'MMM YYYY'
            }
          }
        }
      ],
      yAxes: [
        {
          type: 'linear',
          display: true,
          position: 'left',
          id: 'indicator'
        },
        {
          type: 'linear',
          display: true,
          position: 'right',
          id: 'ticker',

          gridLines: {
            drawOnChartArea: false
          }
        }
      ]
    },
    plugins: {
      zoom: {
        pan: {
          enabled: true,
          mode: 'xy',

          rangeMin: {
            x: null,
            y: null
          },
          rangeMax: {
            x: null,
            y: null
          },

          speed: 20,

          threshold: 10
        },

        zoom: {
          enabled: true,
          drag: false,
          mode: 'xy',

          rangeMin: {
            x: null,
            y: null
          },
          rangeMax: {
            x: null,
            y: null
          },

          speed: 0.1,
          sensitivity: 3
        }
      }
    }
  };

  chartData = [];
  anyChartLoaded = false;
  subscription: Subscription;

  constructor(private signalRegistryService: SignalRegistryService) {}

  ngOnInit(): void {
    this.subscription = this.signalRegistryService.signalsChanged.subscribe(
      signals => {
        this.chartData = new Array<Array<ChartDataPoint>>();

        for (const signal of signals) {
          this.chartData.push({
            label: '(' + signal.id.toString() + ') ',
            data: this.convertToChartPoints(signal.data),
            fill: false,
            yAxisID:
              signal.properties.type === SignalType.Indicator
                ? 'indicator'
                : 'ticker',
            borderColor: 'rgba(' + signal.properties.color + ',1)'
          });
        }

        this.anyChartLoaded = this.chartData.length > 0;
      }
    );
  }

  private convertToChartPoints(data: SignalResponse): Array<ChartDataPoint> {
    const chart = new Array<ChartDataPoint>();

    for (const row of data) {
      chart.push({
        x: new Date(row.date),
        y: 'price' in row ? row.price : row.value
      } as ChartDataPoint);
    }

    return chart;
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
}

export interface ChartDataPoint {
  x: Date;
  y: number;
}
