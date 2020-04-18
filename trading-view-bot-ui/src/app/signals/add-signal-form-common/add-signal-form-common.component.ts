import { Component, OnInit, forwardRef, Input } from '@angular/core';
import { FormGroup, FormBuilder, NG_VALUE_ACCESSOR } from '@angular/forms';

@Component({
  selector: 'app-add-signal-form-common',
  templateUrl: './add-signal-form-common.component.html',
  styleUrls: ['./add-signal-form-common.component.css']
})
export class AddSignalFormCommonComponent implements OnInit {
  @Input() group: FormGroup;
  @Input() filterTypes: string[];

  constructor() {}

  ngOnInit(): void {
    this.group.get('color').setValue(this.getRandomColor());
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
