import { Component, NgZone, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { FormBuilder } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
import * as _moment from 'moment';
import { TickerService, TickerRequest } from './ticker.service';
import { IndicatorService, IndicatorRequest } from './indicator.service';

// tslint:disable-next-line:no-duplicate-imports
import { Moment, MomentFormatSpecification, MomentInput } from 'moment';
const moment = _moment;

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

  indicatorsLoaded = false;
  tickersLoaded = false;

  indicatorSignalList: Array<IndicatorRequest> = [];
  tickerSignalList: Array<TickerRequest> = [];

  addIndicatorForm;
  addTickerForm;

  constructor(
    private tickerService: TickerService,
    private indicatorService: IndicatorService,
    private formBuilder: FormBuilder
  ) {
    this.addIndicatorForm = this.formBuilder.group({
      market: '',
      indicator: '',
      candleSize: '',
      startDate: '',
      endDate: '',
      limit: -1,
      color: '225,10,20',
      sma: 0
    });

    this.addTickerForm = this.formBuilder.group({
      market: '',
      startDate: '',
      endDate: '',
      limit: -1,
      color: '225,10,20',
      sma: 0
    });
  }

  @ViewChild('picker') picker: any;

  public date: Moment;
  public disabled = false;
  public showSpinners = true;
  public showSeconds = false;
  public touchUi = false;
  public enableMeridian = false;
  public minDate: Moment;
  public maxDate: Moment;
  public stepHour = 1;
  public stepMinute = 1;
  public stepSecond = 1;
  public color: ThemePalette = 'primary';

  public formGroup = new FormGroup({
    date: new FormControl(
      moment()
        .utc()
        .utcOffset(5),
      [Validators.required]
    ),
    date2: new FormControl(null, [Validators.required])
  });
  public dateControl = new FormControl(moment());
  public dateControlMinMax = new FormControl(moment());

  public options = [
    { value: true, label: 'True' },
    { value: false, label: 'False' }
  ];

  public listColors = ['primary', 'accent', 'warn'];

  public stepHours = [1, 2, 3, 4, 5];
  public stepMinutes = [1, 5, 10, 15, 20, 25];
  public stepSeconds = [1, 5, 10, 15, 20, 25];

  indicatorMarkets = [];
  indicatorNames = [];
  indicatorCandleSizes = [];
  tickerMarkets = [];

  ngOnInit() {
    this.tickerService.getOptions().subscribe(response => {
      this.tickerMarkets = response['market'];
    });

    this.indicatorService.getOptions().subscribe(response => {
      this.indicatorMarkets = response['market'];
      this.indicatorNames = response['indicator'];
      this.indicatorCandleSizes = response['candle_size'];
    });
  }

  onAddIndicator(event) {
    console.log(event);

    const request: IndicatorRequest = {
      market: event.market,
      indicator: event.indicator,
      candle_size: event.candleSize,
      start_date: event.startDate.toISOString(),
      end_date: event.endDate.toISOString(),
      sma: event.sma
    };
    this.indicatorService.getIndicators(request).subscribe(response => {
      console.log(response);
      this.chartData.push({
        label: event.market + '.' + event.indicator + '.' + event.candleSize,
        data: response,
        fill: false,
        yAxisID: 'indicator',
        borderColor: 'rgba(' + event.color + ',1)'
      });
      this.indicatorSignalList.push(request);
      this.indicatorsLoaded = true;
    });
  }

  onAddTicker(event) {
    console.log(event);

    const request: TickerRequest = {
      market: event.market,
      start_date: event.startDate.toISOString(),
      end_date: event.endDate.toISOString(),
      sma: event.sma
    };
    this.tickerService.getTickers(request).subscribe(response => {
      console.log(response);
      this.chartData.push({
        label: 'BTCUSDT',
        data: response,
        fill: false,
        yAxisID: 'ticker',
        borderColor: 'rgba(' + event.color + ',1)'
      });
      this.tickerSignalList.push(request);
      this.tickersLoaded = true;
    });
  }

  onDeleteSignal(event) {
    console.log(event);
  }

  onAddSMA(event) {
    console.log(event);
  }
}
