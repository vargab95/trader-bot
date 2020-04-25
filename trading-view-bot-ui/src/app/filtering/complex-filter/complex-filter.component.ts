import { Component, OnInit, Input } from "@angular/core";
import { Filter } from "../filter.entity";
import { FormGroup, FormControl } from "@angular/forms";

@Component({
  selector: "app-complex-filter",
  templateUrl: "./complex-filter.component.html",
  styleUrls: ["./complex-filter.component.css"],
})
export class ComplexFilterComponent implements OnInit {
  @Input() types: string[];
  @Input() filters = [];
  addFilterFormGroup: FormGroup;
  displayedColumns: string[] = ["no", "type", "length"];
  empty = false;

  constructor() {}

  ngOnInit(): void {
    this.addFilterFormGroup = new FormGroup({
      type: new FormControl(),
      length: new FormControl(),
    });
  }

  onAddFilter(): void {
    console.log(this.addFilterFormGroup.value);
    this.filters.push(this.addFilterFormGroup.value as Filter);
  }
}
