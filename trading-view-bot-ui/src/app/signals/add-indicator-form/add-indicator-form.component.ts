import { Component, OnInit, Inject } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { IndicatorService, IndicatorRequest } from '../indicator.service';
import { CurrentFiltersService } from 'src/app/filtering/current-filters.service';
import { SignalRegistryService, SignalType } from '../signal-registry.service';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

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

  constructor(
    public dialogRef: MatDialogRef<AddIndicatorFormComponent>,
    @Inject(MAT_DIALOG_DATA) public request: IndicatorRequest,
    private indicatorService: IndicatorService,
    private signalRegistryService: SignalRegistryService,
    private currentFilterService: CurrentFiltersService,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit() {
    this.indicatorService.getOptions().subscribe(
      response => {
        this.indicatorMarkets = response.market;
        this.indicatorNames = response.indicator;
        this.indicatorCandleSizes = response.candle_size;
        this.currentFilterService.setTypes(response.filter_types);
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
        color: ''
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
      filter: this.currentFilterService.getAll(),
      step: event.common.step
    };
    this.signalRegistryService
      .register(SignalType.Indicator, request)
      .subscribe(
        /*response => {
          this.chartDataService.addChart(
            response,
            event.common.color,
            event.market + '.' + event.indicator + '.' + event.candleSize
          );
          this.loading = false;
        },*/
        () => {
          this.loading = false;
        },
        error => {
          this.loading = false;
          console.log(error);
        }
      );
  }
}
