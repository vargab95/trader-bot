import { Component, NgZone, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { FormBuilder } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
import * as _moment from 'moment';
import { TickerService, TickerRequest } from './ticker.service';
import { IndicatorService, IndicatorRequest } from './indicator.service';
import { ChartDataService } from './chart-data.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  indicatorSignalList: Array<IndicatorRequest> = [];
  tickerSignalList: Array<TickerRequest> = [];

  addIndicatorForm;
  addTickerForm;

  constructor(
    private tickerService: TickerService,
    private indicatorService: IndicatorService,
    private formBuilder: FormBuilder,
    private chartDataService: ChartDataService
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
      this.chartDataService.addChart(
        response,
        event.color,
        event.market + '.' + event.indicator + '.' + event.candleSize
      );
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
      this.chartDataService.addChart(response, event.color, event.market);
    });
  }
}
