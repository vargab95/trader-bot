import { Component, OnInit, Input } from '@angular/core';
import { Filter } from '../filter.entity';
import { CurrentFiltersService } from '../current-filters.service';

@Component({
  selector: 'app-filter-list',
  templateUrl: './filter-list.component.html',
  styleUrls: ['./filter-list.component.css']
})
export class FilterListComponent implements OnInit {
  filters: Filter[] = [];
  displayedColumns: string[] = ['no', 'type', 'length'];
  empty = false;

  constructor(private currentFilterService: CurrentFiltersService) {}

  ngOnInit(): void {
    this.currentFilterService.filtersChanged.subscribe((filters: Filter[]) => {
      this.filters = filters;
    });
  }
}
