import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { TickerService, TickerRequest } from '../ticker.service';
import { ChartDataService } from '../../chart/chart-data.service';
import { CurrentFiltersService } from 'src/app/filtering/current-filters.service';

@Component({
  selector: 'app-add-ticker-form',
  templateUrl: './add-ticker-form.component.html',
  styleUrls: ['./add-ticker-form.component.css']
})
export class AddTickerFormComponent implements OnInit {
  tickerMarkets = [];
  addTickerForm: FormGroup;

  loading = false;

  constructor(
    private tickerService: TickerService,
    private formBuilder: FormBuilder,
    private currentFilterService: CurrentFiltersService,
    private chartDataService: ChartDataService
  ) {}

  ngOnInit(): void {
    this.tickerService.getOptions().subscribe(
      response => {
        this.tickerMarkets = response.market;
        this.currentFilterService.setTypes(response.filter_types);
      },
      error => {
        console.log(error);
      }
    );

    this.addTickerForm = this.formBuilder.group({
      market: '',
      common: this.formBuilder.group({
        dateSpan: this.formBuilder.group({
          start: '',
          end: ''
        }),
        step: 1,
        color: ''
      })
    });
  }

  onAddTicker(event) {
    this.loading = true;
    console.log(event);
    const request: TickerRequest = {
      market: event.market,
      start_date: event.common.dateSpan.start.toISOString(),
      end_date: event.common.dateSpan.end.toISOString(),
      filter: this.currentFilterService.getAll(),
      step: event.common.step
    };
    this.tickerService.getTickers(request).subscribe(
      response => {
        this.chartDataService.addChart(
          response,
          event.common.color,
          event.market
        );
        this.loading = false;
      },
      error => {
        console.log(error);
        this.loading = false;
      }
    );
  }
}
