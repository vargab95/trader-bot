import { Component, OnInit } from "@angular/core";
import {
  RegisteredSignal,
  SignalRegistryService,
} from "../signal-registry.service";
import { AddSignalFormComponent } from "../add-signal-form/add-signal-form.component";
import { MatDialog } from "@angular/material/dialog";

@Component({
  selector: "app-signal-list",
  templateUrl: "./signal-list.component.html",
  styleUrls: ["./signal-list.component.css"],
})
export class SignalListComponent implements OnInit {
  signals: RegisteredSignal[] = [];
  displayedColumns: string[] = [
    "id",
    "type",
    "market",
    "startDate",
    "endDate",
    "color",
    "step",
    "controls",
  ];

  constructor(
    public dialog: MatDialog,
    private signalRegistryService: SignalRegistryService
  ) {
    this.signalRegistryService.signalsChanged.subscribe((signals) => {
      this.signals = signals;
    });
  }

  ngOnInit(): void {}

  onAddSignal() {
    const dialogRef = this.dialog.open(AddSignalFormComponent, {
      maxWidth: "90%",
      minWidth: "20%",
    });
  }

  editSignal(id: number) {
    const dialogRef = this.dialog.open(AddSignalFormComponent, {
      maxWidth: "90%",
      minWidth: "20%",
      data: this.signalRegistryService.get(id),
    });
  }

  deleteSignal(id: number) {
    this.signalRegistryService.remove(id);
  }
}
