import { Component, OnInit, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'app-date-span-picker',
  templateUrl: './date-span-picker.component.html',
  styleUrls: ['./date-span-picker.component.css']
})
export class DateSpanPickerComponent implements OnInit {
  @Input() start = new Date();
  @Input() end = new Date();
  @Input() group: FormGroup;

  constructor() {}

  ngOnInit(): void {}
}

export interface DateSpan {
  start: Date;
  end: Date;
}
