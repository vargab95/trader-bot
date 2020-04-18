import { Component, OnInit, OnDestroy } from '@angular/core';
import { ChartDataService, ChartDataPoint } from '../chart-data.service';
import { Subscription } from 'rxjs';

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

  constructor(private chartDataService: ChartDataService) {}

  ngOnInit(): void {
    this.subscription = this.chartDataService.chartsChanged.subscribe(
      charts => {
        this.chartData = new Array<Array<ChartDataPoint>>();

        console.log(charts);

        for (const chart of charts) {
          this.chartData.push({
            label: '(' + chart.id.toString() + ') ' + chart.name,
            data: chart.data,
            fill: false,
            yAxisID: chart.type,
            borderColor: 'rgba(' + chart.color + ',1)'
          });
        }

        this.anyChartLoaded = this.chartData.length > 0;
      }
    );
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
}
