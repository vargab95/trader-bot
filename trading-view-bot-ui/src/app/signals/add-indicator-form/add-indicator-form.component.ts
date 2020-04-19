import { Component, OnInit, Inject } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { CurrentFiltersService } from 'src/app/filtering/current-filters.service';
import {
  SignalRegistryService,
  SignalType,
  SignalProperties
} from '../signal-registry.service';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-add-indicator-form',
  templateUrl: './add-indicator-form.component.html',
  styleUrls: ['./add-indicator-form.component.css']
})
export class AddIndicatorFormComponent implements OnInit {
  form: FormGroup;

  indicatorMarkets = [];
  indicatorNames = [];
  indicatorCandleSizes = [];

  loading = false;

  constructor(
    public dialogRef: MatDialogRef<AddIndicatorFormComponent>,
    @Inject(MAT_DIALOG_DATA) public properties: SignalProperties,
    private signalRegistryService: SignalRegistryService,
    private currentFilterService: CurrentFiltersService,
    private formBuilder: FormBuilder
  ) {
    if (!this.properties) {
      this.properties = {
        market: '',
        type: SignalType.Indicator,
        color: ''
      };
    }
  }

  ngOnInit() {
    this.signalRegistryService.getOptions(this.properties.type).subscribe(
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

    this.form = this.formBuilder.group({
      market: '',
      indicator: '',
      candleSize: '',
      dateSpan: this.formBuilder.group({
        start: '',
        end: ''
      }),
      step: 1,
      color: this.getRandomColor()
    });
  }

  onAddSignal() {
    this.loading = true;
    this.properties = { ...this.properties, ...this.form.value };
    console.log(this.properties);
    this.signalRegistryService.register(this.properties).subscribe(
      () => {
        this.loading = false;
      },
      error => {
        this.loading = false;
        console.log(error);
      }
    );
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
}
