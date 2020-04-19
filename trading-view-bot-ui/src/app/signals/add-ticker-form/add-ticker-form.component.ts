import { Component, OnInit, Inject } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { TickerService, TickerRequest } from '../ticker.service';
import { CurrentFiltersService } from 'src/app/filtering/current-filters.service';
import {
  SignalRegistryService,
  SignalType,
  SignalProperties
} from '../signal-registry.service';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

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
    public dialogRef: MatDialogRef<AddTickerFormComponent>,
    @Inject(MAT_DIALOG_DATA) public request: TickerRequest,
    private tickerService: TickerService,
    private signalRegistryService: SignalRegistryService,
    private formBuilder: FormBuilder,
    private currentFilterService: CurrentFiltersService
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
    const request: SignalProperties = {
      market: event.market,
      type: SignalType.Ticker,
      color: event.common.color,
      start_date: event.common.dateSpan.start.toISOString(),
      end_date: event.common.dateSpan.end.toISOString(),
      filter: this.currentFilterService.getAll(),
      step: event.common.step
    };
    this.signalRegistryService.register(request).subscribe(
      () => {
        this.loading = false;
      },
      error => {
        console.log(error);
        this.loading = false;
      }
    );
  }
}
