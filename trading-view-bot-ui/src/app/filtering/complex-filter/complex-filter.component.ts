import { Component, OnInit, Input } from '@angular/core';
import { Filter } from '../filter.entity';
import { FormGroup, FormControl } from '@angular/forms';
import { CurrentFiltersService } from '../current-filters.service';

@Component({
  selector: 'app-complex-filter',
  templateUrl: './complex-filter.component.html',
  styleUrls: ['./complex-filter.component.css']
})
export class ComplexFilterComponent implements OnInit {
  @Input() types: string[];
  addFilterFormGroup: FormGroup;

  constructor(private currentFilterService: CurrentFiltersService) {}

  ngOnInit(): void {
    this.addFilterFormGroup = new FormGroup({
      type: new FormControl(),
      length: new FormControl()
    });
  }

  onAddFilter(): void {
    this.currentFilterService.add(this.addFilterFormGroup.value as Filter);
  }
}
