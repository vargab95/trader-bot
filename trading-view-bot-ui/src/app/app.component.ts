import { Component, NgZone, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { FormBuilder } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
import * as _moment from 'moment';
import { TickerService, TickerRequest } from './signals/ticker.service';
import {
  IndicatorService,
  IndicatorRequest
} from './signals/indicator.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  constructor() {}

  ngOnInit() {}
}
