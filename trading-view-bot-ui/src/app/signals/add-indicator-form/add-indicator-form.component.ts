import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { IndicatorService, IndicatorRequest } from '../indicator.service';
import { ChartDataService } from '../../chart/chart-data.service';

@Component({
  selector: 'app-add-indicator-form',
  templateUrl: './add-indicator-form.component.html',
  styleUrls: ['./add-indicator-form.component.css']
})
export class AddIndicatorFormComponent implements OnInit {
  addIndicatorForm: FormGroup;

  indicatorMarkets = [];
  indicatorNames = [];
  indicatorCandleSizes = [];

  loading = false;
  filterTypes = [];

  constructor(
    private indicatorService: IndicatorService,
    private formBuilder: FormBuilder,
    private chartDataService: ChartDataService
  ) {}

  ngOnInit() {
    this.indicatorService.getOptions().subscribe(
      response => {
        this.indicatorMarkets = response.market;
        this.indicatorNames = response.indicator;
        this.indicatorCandleSizes = response.candle_size;
        this.filterTypes = response.filter_types;
      },
      error => {
        console.log(error);
      }
    );

    this.addIndicatorForm = this.formBuilder.group({
      market: '',
      indicator: '',
      candleSize: '',
      common: this.formBuilder.group({
        dateSpan: this.formBuilder.group({
          start: '',
          end: ''
        }),
        step: 1,
        color: '',
        filter: this.formBuilder.group({
          type: '',
          length: 0
        })
      })
    });
  }

  onAddIndicator(event) {
    this.loading = true;
    console.log(event);
    const request: IndicatorRequest = {
      market: event.market,
      indicator: event.indicator,
      candle_size: event.candleSize,
      start_date: event.common.dateSpan.start.toISOString(),
      end_date: event.common.dateSpan.end.toISOString(),
      ma_length: event.common.filter.length,
      ma_type: event.common.filter.type,
      step: event.common.step
    };
    this.indicatorService.getIndicators(request).subscribe(
      response => {
        this.chartDataService.addChart(
          response,
          event.common.color,
          event.market + '.' + event.indicator + '.' + event.candleSize
        );
        this.loading = false;
      },
      error => {
        this.loading = false;
        console.log(error);
      }
    );
  }
}
