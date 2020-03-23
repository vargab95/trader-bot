import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class TickerService {
  private baseUrl = 'http://localhost:5000/ticker';

  constructor(private http: HttpClient) {}

  getIndicators(
    market: string,
    startDate: Date = null,
    endDate: Date = null,
    limit: number = -1
  ) {
    const params: TickerRequest = {
      market,
      limit
    };

    if (startDate) {
      params.start_date = startDate.toISOString();
    }

    if (endDate) {
      params.end_date = endDate.toISOString();
    }

    return this.http.get(this.baseUrl, { params: params as any }).pipe(
      map((response: Array<TickerValue>) => {
        const indicators = [];

        for (const row of response) {
          indicators.push({
            x: new Date(row.date),
            y: row.price
          });
        }

        return indicators;
      })
    );
  }
}

interface TickerRequest {
  market: string;
  start_date?: string;
  end_date?: string;
  limit?: number;
}

interface TickerValue {
  date: Date;
  price: number;
}
