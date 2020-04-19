import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AddIndicatorFormComponent } from '../signals/add-indicator-form/add-indicator-form.component';
import { AddTickerFormComponent } from '../signals/add-ticker-form/add-ticker-form.component';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit {
  constructor(public dialog: MatDialog) {}

  ngOnInit(): void {}

  onAddIndicator() {
    const dialogRef = this.dialog.open(AddIndicatorFormComponent, {
      width: '250px',
      data: null
    });
  }

  onAddTicker() {
    const dialogRef = this.dialog.open(AddTickerFormComponent, {
      width: '250px',
      data: null
    });
  }
}
