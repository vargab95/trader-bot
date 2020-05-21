import { Component, OnInit, Inject } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import {
  SignalRegistryService,
  SignalType,
  SignalProperties,
} from "../signal-registry.service";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { FilterService } from "src/app/filtering/filter.service";

@Component({
  selector: "app-add-signal-form",
  templateUrl: "./add-signal-form.component.html",
  styleUrls: ["./add-signal-form.component.css"],
})
export class AddSignalFormComponent implements OnInit {
  public signalTypes = SignalType;
  form: FormGroup;

  markets = [];
  names = [];
  candleSizes = [];

  loading = false;
  type: SignalType = null;

  constructor(
    public dialogRef: MatDialogRef<AddSignalFormComponent>,
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
      type: ["", Validators.required],
    });
    this.form.controls.type.valueChanges.subscribe((signalType: SignalType) => {
      this.type = signalType;
      this.loading = true;

      if (signalType == SignalType.Ticker) {
        this.form = this.formBuilder.group({
          market: ["", Validators.required],
          dateSpan: this.formBuilder.group({
            start: [new Date(), Validators.required],
            end: [new Date(), Validators.required],
          }),
          filter: [],
          step: [1, Validators.required],
          color: [this.getRandomColor(), Validators.required],
        });
      } else {
        this.form = this.formBuilder.group({
          market: ["", Validators.required],
          indicator: ["", Validators.required],
          candleSize: ["", Validators.required],
          dateSpan: this.formBuilder.group({
            start: ["", Validators.required],
            end: ["", Validators.required],
          }),
          filter: [],
          step: [1, Validators.required],
          color: [this.getRandomColor(), Validators.required],
        });
      }

      this.signalRegistryService.getOptions(this.type).subscribe(
        (response) => {
          this.markets = response.market;
          this.names = response.indicator;
          this.candleSizes = response.candle_size;
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
    this.properties.type = this.type;
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
