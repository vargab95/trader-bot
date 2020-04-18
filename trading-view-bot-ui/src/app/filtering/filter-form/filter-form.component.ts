import { Component, OnInit } from '@angular/core';
import { TickerService } from '../../signals/ticker.service';
import { FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-filter-form',
  templateUrl: './filter-form.component.html',
  styleUrls: ['./filter-form.component.css']
})
export class FilterFormComponent implements OnInit {
  filterTypes = [];

  constructor(
    private tickerService: TickerService,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.tickerService.getOptions().subscribe(
      response => {
        this.filterTypes = response.filter_types;
      },
      error => {
        console.log(error);
      }
    );
  }
}
