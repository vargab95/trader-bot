import { Component, OnInit, Input, forwardRef } from '@angular/core';
import {
  FormControl,
  FormGroup,
  FormBuilder,
  ControlValueAccessor,
  NG_VALUE_ACCESSOR
} from '@angular/forms';

@Component({
  selector: 'app-date-span-picker',
  templateUrl: './date-span-picker.component.html',
  styleUrls: ['./date-span-picker.component.css'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => DateSpanPickerComponent),
      multi: true
    }
  ]
})
export class DateSpanPickerComponent implements OnInit, ControlValueAccessor {
  @Input() start = new Date();
  @Input() end = new Date();

  dateSpanForm: FormGroup;
  propagateChange = (_: DateSpan) => {};

  constructor(private formBuilder: FormBuilder) {}

  ngOnInit(): void {
    this.dateSpanForm = new FormGroup({
      startDate: new FormControl(),
      endDate: new FormControl()
    });

    this.dateSpanForm.get('startDate').valueChanges.subscribe(value => {
      this.start = value;
      this.propagateChange({ start: this.start, end: this.end } as DateSpan);
    });

    this.dateSpanForm.get('endDate').valueChanges.subscribe(value => {
      this.end = value;
      this.propagateChange({ start: this.start, end: this.end } as DateSpan);
    });
  }

  writeValue(value: DateSpan) {
    this.start = value.start;
    this.end = value.end;
  }

  registerOnChange(fn) {
    this.propagateChange = fn;
  }

  registerOnTouched() {}
}

export interface DateSpan {
  start: Date;
  end: Date;
}
