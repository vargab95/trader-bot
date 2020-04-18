import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { IndicatorService, IndicatorRequest } from '../indicator.service';
import { ChartDataService } from '../chart-data.service';

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
  filterTypes = [];

  loading = false;
  color = this.getRandomColor();

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
      dateSpan: {
        start: '',
        end: ''
      },
      limit: -1,
      color: this.getRandomColor(),
      maLength: 0,
      filterType: 'sma',
      step: 1
    });
  }

  getRandomSegment() {
    return Math.floor(Math.random() * 256).toString();
  }

  getRandomColor() {
    return (
      this.getRandomSegment() +
      ',' +
      this.getRandomSegment() +
      ',' +
      this.getRandomSegment()
    );
  }

  onAddIndicator(event) {
    this.loading = true;
    const request: IndicatorRequest = {
      market: event.market,
      indicator: event.indicator,
      candle_size: event.candleSize,
      start_date: event.dateSpan.start.toISOString(),
      end_date: event.dateSpan.end.toISOString(),
      ma_length: event.maLength,
      ma_type: event.filterType,
      step: event.step
    };
    this.indicatorService.getIndicators(request).subscribe(
      response => {
        this.chartDataService.addChart(
          response,
          event.color,
          event.market + '.' + event.indicator + '.' + event.candleSize
        );
        this.loading = false;
        this.color = this.getRandomColor();
      },
      error => {
        this.loading = false;
        console.log(error);
      }
    );
  }
}
