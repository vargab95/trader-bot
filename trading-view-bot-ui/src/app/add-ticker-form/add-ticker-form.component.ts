import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { TickerService, TickerRequest } from '../ticker.service';
import { ChartDataService } from '../chart-data.service';

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
    private chartDataService: ChartDataService
  ) {}

  ngOnInit(): void {
    this.tickerService.getOptions().subscribe(response => {
      this.tickerMarkets = response.market;
    });

    this.addTickerForm = this.formBuilder.group({
      market: '',
      dateSpan: {
        start: '',
        end: ''
      },
      limit: -1,
      color: '225,10,20',
      sma: 0,
      step: 1
    });
  }

  onAddTicker(event) {
    this.loading = true;
    const request: TickerRequest = {
      market: event.market,
      start_date: event.dateSpan.start.toISOString(),
      end_date: event.dateSpan.end.toISOString(),
      sma: event.sma,
      step: event.step
    };
    this.tickerService.getTickers(request).subscribe(
      response => {
        this.chartDataService.addChart(response, event.color, event.market);
        this.loading = false;
      },
      error => {
        console.log(error);
        this.loading = false;
      }
    );
  }
}
