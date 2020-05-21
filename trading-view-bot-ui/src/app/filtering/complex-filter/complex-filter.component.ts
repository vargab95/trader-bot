import { Component, OnInit, Input, OnDestroy } from "@angular/core";
import { Filter } from "../filter.entity";
import { FormGroup, FormControl } from "@angular/forms";
import { FilterService } from "../filter.service";
import { Subscription } from "rxjs";

@Component({
  selector: "app-complex-filter",
  templateUrl: "./complex-filter.component.html",
  styleUrls: ["./complex-filter.component.css"],
})
export class ComplexFilterComponent implements OnInit, OnDestroy {
  filters = [];
  addFilterFormGroup: FormGroup;
  displayedColumns: string[] = ["no", "type", "length"];
  empty = true;
  filterSubscription: Subscription;

  constructor(private filterService: FilterService) {}

  ngOnInit(): void {
    this.addFilterFormGroup = new FormGroup({
      type: new FormControl(),
      length: new FormControl(),
    });

    this.filterSubscription = this.filterService.filtersChanged.subscribe(
      (filters) => {
        this.filters = filters;
        if (this.filters.length > 0) {
          this.empty = false;
        } else {
          this.empty = true;
        }
      }
    );
  }

  ngOnDestroy() {
    this.filterSubscription.unsubscribe();
  }

  onAddFilter(): void {
    this.filterService.addFilter(this.addFilterFormGroup.value as Filter);
  }
}
