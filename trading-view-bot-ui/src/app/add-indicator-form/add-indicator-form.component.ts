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

  constructor(
    private indicatorService: IndicatorService,
    private formBuilder: FormBuilder,
    private chartDataService: ChartDataService
  ) {}

  ngOnInit() {
    this.indicatorService.getOptions().subscribe(response => {
      this.indicatorMarkets = response.market;
      this.indicatorNames = response.indicator;
      this.indicatorCandleSizes = response.candle_size;
    });

    this.addIndicatorForm = this.formBuilder.group({
      market: '',
      indicator: '',
      candleSize: '',
      dateSpan: {
        start: '',
        end: ''
      },
      limit: -1,
      color: '225,10,20',
      sma: 0
    });
  }

  onAddIndicator(event) {
    console.log(event);

    const request: IndicatorRequest = {
      market: event.market,
      indicator: event.indicator,
      candle_size: event.candleSize,
      start_date: event.dateSpan.start.toISOString(),
      end_date: event.dateSpan.end.toISOString(),
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
}
