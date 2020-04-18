import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { TickerService, TickerRequest } from '../ticker.service';
import { ChartDataService } from '../../chart/chart-data.service';

@Component({
  selector: 'app-add-ticker-form',
  templateUrl: './add-ticker-form.component.html',
  styleUrls: ['./add-ticker-form.component.css']
})
export class AddTickerFormComponent implements OnInit {
  tickerMarkets = [];
  filterTypes = [];
  addTickerForm: FormGroup;

  loading = false;
  color = this.getRandomColor();

  constructor(
    private tickerService: TickerService,
    private formBuilder: FormBuilder,
    private chartDataService: ChartDataService
  ) {}

  ngOnInit(): void {
    this.tickerService.getOptions().subscribe(
      response => {
        this.tickerMarkets = response.market;
        this.filterTypes = response.filter_types;
      },
      error => {
        console.log(error);
      }
    );

    this.addTickerForm = this.formBuilder.group({
      market: '',
      dateSpan: {
        start: '',
        end: ''
      },
      limit: -1,
      color: '225,10,20',
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

  onAddTicker(event) {
    this.loading = true;
    const request: TickerRequest = {
      market: event.market,
      start_date: event.dateSpan.start.toISOString(),
      end_date: event.dateSpan.end.toISOString(),
      ma_length: event.maLength,
      ma_type: event.filterType,
      step: event.step
    };
    this.tickerService.getTickers(request).subscribe(
      response => {
        this.chartDataService.addChart(response, event.color, event.market);
        this.loading = false;
        this.color = this.getRandomColor();
      },
      error => {
        console.log(error);
        this.loading = false;
      }
    );
  }
}
