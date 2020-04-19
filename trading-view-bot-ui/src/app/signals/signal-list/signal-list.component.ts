import { Component, OnInit } from '@angular/core';
import {
  RegisteredSignal,
  SignalRegistryService
} from '../signal-registry.service';

@Component({
  selector: 'app-signal-list',
  templateUrl: './signal-list.component.html',
  styleUrls: ['./signal-list.component.css']
})
export class SignalListComponent implements OnInit {
  signals: RegisteredSignal[] = [];
  displayedColumns: string[] = ['id', 'type'];

  constructor(private signalRegistryService: SignalRegistryService) {
    this.signalRegistryService.signalsChanged.subscribe(signals => {
      this.signals = signals;
    });
  }

  ngOnInit(): void {}
}
