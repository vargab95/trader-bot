import { Component, OnInit, Input } from '@angular/core';
import { TickerService } from '../../signals/ticker.service';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'app-filter-form',
  templateUrl: './filter-form.component.html',
  styleUrls: ['./filter-form.component.css']
})
export class FilterFormComponent {
  @Input() types: string[];
  @Input() group: FormGroup;

  constructor() {}
}
