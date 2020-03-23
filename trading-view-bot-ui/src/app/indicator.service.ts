import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class IndicatorService {
  private baseUrl = 'http://localhost:5000/indicator';

  constructor(private http: HttpClient) {}

  getIndicators(
    market: string,
    indicator: string,
    candleSize: string,
    startDate: Date = null,
    endDate: Date = null,
    limit: number = -1
  ) {
    const params: IndicatorRequest = {
      market,
      indicator,
      candle_size: candleSize,
      limit
    };

    if (startDate) {
      params.start_date = startDate.toISOString();
    }

    if (endDate) {
      params.end_date = endDate.toISOString();
    }

    return this.http
      .get(this.baseUrl, {
        params: params as any
      })
      .pipe(
        map((response: Array<IndicatorValue>) => {
          const indicators = [];

          for (const row of response) {
            indicators.push({
              x: new Date(row.date),
              y: row.value
            });
          }

          return indicators;
        })
      );
  }
}

interface IndicatorRequest {
  market: string;
  indicator: string;
  candle_size: string;
  start_date?: string;
  end_date?: string;
  limit?: number;
}

interface IndicatorValue {
  date: Date;
  value: number;
}
