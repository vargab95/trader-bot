import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class IndicatorService {
  private baseUrl = 'http://localhost:5000/indicator';

  constructor(private http: HttpClient) {}

  getIndicators(request: IndicatorRequest) {
    return this.http
      .get(this.baseUrl, {
        params: request as any
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

  getOptions() {
    return this.http.get(this.baseUrl + '/options').pipe(
      map(response => {
        return response;
      })
    );
  }
}

export interface IndicatorRequest {
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
