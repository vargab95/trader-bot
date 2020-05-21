import { Injectable } from "@angular/core";
import { Subject, Observable } from "rxjs";
import { map } from "rxjs/operators";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { environment } from "src/environments/environment";
import { Filter } from "./filter.entity";

@Injectable({
  providedIn: "root",
})
export class FilterService {
  private _filters: Array<Filter> = [];
  private _types: Array<string> = [];
  private lastId: number = 0;
  filtersChanged = new Subject<Array<Filter>>();
  typesChanged = new Subject<Array<string>>();

  get types(): Array<string> {
    return [...this._types];
  }

  set types(types: Array<string>) {
    console.log(types);
    this._types = [...types];
    this.typesChanged.next(this.types);
  }

  get filters(): Array<Filter> {
    return [...this._filters];
  }

  set filters(filters: Array<Filter>) {
    this._filters = [...filters];
    this.filtersChanged.next(this.filters);
  }

  addFilter(filter: Filter) {
    ++this.lastId;
    filter.no = this.lastId;
    this._filters.push({ ...filter });
    this.filtersChanged.next(this.filters);
  }

  reset() {
    this.filters = [];
    this.types = [];
    this.lastId = 0;
  }
}
