import { Component, Input } from "@angular/core";
import { FormGroup } from "@angular/forms";
import { Subscription } from "rxjs";

@Component({
  selector: "app-filter-form",
  templateUrl: "./filter-form.component.html",
  styleUrls: ["./filter-form.component.css"],
})
export class FilterFormComponent {
  @Input() group: FormGroup;
  @Input() types: string[] = [];
  filterSubscription: Subscription;

  constructor() {}
}
