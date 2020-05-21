import { Component, OnInit } from "@angular/core";
import { MatDialog } from "@angular/material/dialog";
import { AddSignalFormComponent } from "../signals/add-signal-form/add-signal-form.component";

@Component({
  selector: "app-graph",
  templateUrl: "./graph.component.html",
  styleUrls: ["./graph.component.css"],
})
export class GraphComponent implements OnInit {
  constructor(public dialog: MatDialog) {}

  ngOnInit(): void {}

  onAddSignal() {
    const dialogRef = this.dialog.open(AddSignalFormComponent, {
      maxWidth: "90%",
      minWidth: "20%",
    });
  }
}
