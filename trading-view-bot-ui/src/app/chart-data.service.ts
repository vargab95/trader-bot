import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { IndicatorResponse } from './indicator.service';
import { TickerResponse, Ticker } from './ticker.service';

@Injectable({
  providedIn: 'root'
})
export class ChartDataService {
  private charts = {};
  private lastChartId = 0;
  chartsChanged = new Subject<Array<ChartData>>();

  constructor() {}

  addChart(
    data: IndicatorResponse | TickerResponse,
    color: string,
    name: string
  ) {
    // FIXME Find a proper solution for checking data type
    const chart: ChartData = {
      id: this.lastChartId,
      data: this.convertToChartPoints(data),
      color,
      name,
      type: 'price' in data[0] ? 'ticker' : 'indicator'
    };

    this.charts[this.lastChartId] = chart;
    this.lastChartId++;

    this.chartsChanged.next(Object.values(this.charts));
  }

  deleteChart(id: number) {
    if (id in this.charts) {
      delete this.charts[id];
    }
  }

  private convertToChartPoints(
    data: IndicatorResponse | TickerResponse
  ): Array<ChartDataPoint> {
    const chart = new Array<ChartDataPoint>();

    for (const row of data) {
      chart.push({
        x: new Date(row.date),
        y: 'price' in row ? row.price : row.value
      } as ChartDataPoint);
    }

    return chart;
  }
}

export interface ChartDataPoint {
  x: Date;
  y: number;
}

export interface ChartData {
  data: Array<ChartDataPoint>;
  id: number;
  color: string;
  name: string;
  type: string;
}
