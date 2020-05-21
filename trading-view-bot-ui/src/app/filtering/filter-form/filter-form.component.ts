import { Component, Input, OnDestroy, OnInit } from "@angular/core";
import { FormGroup } from "@angular/forms";
import { Subscription } from "rxjs";
import { FilterService } from "../filter.service";

@Component({
  selector: "app-filter-form",
  templateUrl: "./filter-form.component.html",
  styleUrls: ["./filter-form.component.css"],
})
export class FilterFormComponent implements OnInit, OnDestroy {
  @Input() group: FormGroup;
  types: string[] = [];
  filterSubscription: Subscription;

  constructor(private filterService: FilterService) {}

  ngOnInit() {
    this.types = this.filterService.types;
    this.filterSubscription = this.filterService.typesChanged.subscribe(
      (types) => {
        console.log("Types changed in filter form");
        this.types = types;
      }
    );
  }

  ngOnDestroy() {
    this.filterSubscription.unsubscribe();
  }
}
