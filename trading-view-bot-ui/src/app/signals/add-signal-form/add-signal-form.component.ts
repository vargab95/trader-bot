import { Component, OnInit, Inject } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import {
  SignalRegistryService,
  SignalType,
  SignalProperties,
  RegisteredSignal,
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
  isModify = false;
  type: SignalType = null;

  constructor(
    public dialogRef: MatDialogRef<AddSignalFormComponent>,
    @Inject(MAT_DIALOG_DATA) public signal: RegisteredSignal,
    private signalRegistryService: SignalRegistryService,
    private filterService: FilterService,
    private formBuilder: FormBuilder
  ) {
    if (!this.signal) {
      this.isModify = false;
      this.signal = {
        id: 0,
        properties: {
          market: "",
          type: SignalType.Indicator,
          color: "",
        },
        data: [],
      };
    } else {
      this.isModify = true;
      this.type = this.signal.properties.type;
    }
    dialogRef.disableClose = true;
  }

  ngOnInit() {
    if (this.isModify) {
      this.generateForm(this.type);

      this.signalRegistryService.getOptions(this.type).subscribe(
        (response) => {
          this.markets = response.market;
          this.names = response.indicator;
          this.candleSizes = response.candle_size;
          this.filterService.types = response.filter_types;
          this.loading = false;

          this.form.controls.market.setValue(this.signal.properties.market);
          if (this.signal.properties.type === SignalType.Indicator) {
            this.form.controls.indicator.setValue(
              this.signal.properties.indicator
            );
            this.form.controls.candleSize.setValue(
              this.signal.properties.candleSize
            );
          }
          this.form.controls.dateSpan.setValue(this.signal.properties.dateSpan);
          this.filterService.filters = this.signal.properties.filter;
          this.form.controls.step.setValue(this.signal.properties.step);
          this.form.controls.color.setValue(this.signal.properties.color);
        },
        (error) => {
          console.log(error);
        }
      );
    } else {
      this.form = this.formBuilder.group({
        type: ["", Validators.required],
      });
      this.form.controls.type.valueChanges.subscribe(
        (signalType: SignalType) => {
          this.type = signalType;
          this.loading = true;

          this.generateForm(signalType);

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
        }
      );
    }
  }

  private generateForm(signalType: SignalType) {
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
          start: [new Date(), Validators.required],
          end: [new Date(), Validators.required],
        }),
        filter: [],
        step: [1, Validators.required],
        color: [this.getRandomColor(), Validators.required],
      });
    }
  }

  onSubmit() {
    this.loading = true;
    this.signal.properties = {
      ...this.signal.properties,
      ...this.form.value,
      filter: [...this.filterService.filters],
    };
    this.signal.properties.type = this.type;
    if (this.isModify) {
      this.signalRegistryService
        .modify(this.signal.id, this.signal.properties)
        .subscribe(
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
    } else {
      this.signalRegistryService.register(this.signal.properties).subscribe(
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
