import { Component, OnInit, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { CurrentFiltersService } from '../current-filters.service';

@Component({
  selector: 'app-filter-form',
  templateUrl: './filter-form.component.html',
  styleUrls: ['./filter-form.component.css']
})
export class FilterFormComponent implements OnInit {
  @Input() group: FormGroup;
  types: string[] = [];

  constructor(private currentFilterService: CurrentFiltersService) {}

  ngOnInit(): void {
    this.currentFilterService.typesChanged.subscribe(types => {
      this.types = types;
    });
  }
}
