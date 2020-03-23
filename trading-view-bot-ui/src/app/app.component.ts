import { Component, OnInit } from '@angular/core';
import { TickerService } from './ticker.service';
import { IndicatorService } from './indicator.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  chartOptions = {
    responsive: true,
    hoverMode: 'index',
    stacked: false,
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
    }
  };

  chartData = [];

  indicatorsLoaded = false;
  tickersLoaded = false;

  constructor(
    private tickerService: TickerService,
    private indicatorService: IndicatorService
  ) {}

  ngOnInit() {
    this.indicatorService
      .getIndicators('GEMINI:BTCUSD', 'all', '1h')
      .subscribe(response => {
        console.log(response);
        this.chartData.push({
          label: 'GEMINI:BTCUSD.all.1h',
          data: response,
          fill: false,
          yAxisID: 'indicator'
        });
        this.indicatorsLoaded = true;
      });

    this.tickerService.getIndicators('BTCUSDT').subscribe(response => {
      console.log(response);
      this.chartData.push({
        label: 'BTCUSDT',
        data: response,
        fill: false,
        yAxisID: 'ticker'
      });
      this.tickersLoaded = true;
    });
  }

  onChartClick(event) {
    console.log(event);
  }
}
