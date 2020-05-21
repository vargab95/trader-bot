import { Component, OnInit, Inject } from "@angular/core";
import { FormGroup, FormBuilder } from "@angular/forms";
import {
  SignalRegistryService,
  SignalType,
  SignalProperties,
} from "../signal-registry.service";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { FilterService } from "src/app/filtering/filter.service";

@Component({
  selector: "app-add-indicator-form",
  templateUrl: "./add-indicator-form.component.html",
  styleUrls: ["./add-indicator-form.component.css"],
})
export class AddIndicatorFormComponent implements OnInit {
  public signalTypes = SignalType;
  form: FormGroup;

  indicatorMarkets = [];
  indicatorNames = [];
  indicatorCandleSizes = [];

  loading = false;
  type: SignalType = null;

  constructor(
    public dialogRef: MatDialogRef<AddIndicatorFormComponent>,
    @Inject(MAT_DIALOG_DATA) public properties: SignalProperties,
    private signalRegistryService: SignalRegistryService,
    private filterService: FilterService,
    private formBuilder: FormBuilder
  ) {
    if (!this.properties) {
      this.properties = {
        market: "",
        type: SignalType.Indicator,
        color: "",
      };
    }
    dialogRef.disableClose = true;
  }

  ngOnInit() {
    this.form = this.formBuilder.group({
      type: "",
      market: "",
      indicator: "",
      candleSize: "",
      dateSpan: this.formBuilder.group({
        start: "",
        end: "",
      }),
      filter: [],
      step: 1,
      color: this.getRandomColor(),
    });

    this.form.controls.type.valueChanges.subscribe((signalType: SignalType) => {
      this.type = signalType;
      this.loading = true;
      this.signalRegistryService.getOptions(this.type).subscribe(
        (response) => {
          this.indicatorMarkets = response.market;
          this.indicatorNames = response.indicator;
          this.indicatorCandleSizes = response.candle_size;
          this.filterService.types = response.filter_types;
          this.loading = false;
        },
        (error) => {
          console.log(error);
        }
      );
    });
  }

  onAddSignal() {
    this.loading = true;
    this.properties = {
      ...this.properties,
      ...this.form.value,
      filter: [...this.filterService.filters],
    };
    console.log(this.properties);
    this.signalRegistryService.register(this.properties).subscribe(
      () => {
        this.loading = false;
        this.filterService.reset();
        this.dialogRef.close();
      },
      (error) => {
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
      "," +
      this.getRandomSegment() +
      "," +
      this.getRandomSegment()
    );
  }
}
