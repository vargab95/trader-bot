import { Injectable } from '@angular/core';
import { Filter } from './filter.entity';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CurrentFiltersService {
  filtersChanged = new Subject<Array<Filter>>();
  typesChanged = new Subject<Array<string>>();
  private filters: Filter[] = [];
  private types: string[] = [];

  constructor() {}

  add(newFilter: Filter): void {
    const newFilterCopy = { ...newFilter };
    newFilterCopy.no = this.filters.length + 1;
    this.filters.push(newFilterCopy);
    this.filtersChanged.next(this.getAll());
  }

  remove(no: number): void {
    delete this.filters[no];

    for (let i = 0; i < this.filters.length; i++) {
      this.filters[i].no = i;
    }

    this.filtersChanged.next(this.getAll());
  }

  getAll(): Filter[] {
    return [...this.filters];
  }

  clear(): void {}

  setTypes(types: string[]): void {
    this.types = [...types];
    this.typesChanged.next(this.getTypes());
  }

  getTypes(): string[] {
    return [...this.types];
  }
}
