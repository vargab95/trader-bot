import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TickerService {
  private baseUrl = environment.apiBaseUrl + 'ticker';

  constructor(private http: HttpClient) {}

  getTickers(request: TickerRequest) {
    return this.http.get(this.baseUrl, { params: request as any }).pipe(
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

  getOptions() {
    return this.http.get(this.baseUrl + '/options').pipe(
      map(response => {
        return response;
      })
    );
  }
}

export interface TickerRequest {
  market: string;
  start_date?: string;
  end_date?: string;
  limit?: number;
}

interface TickerValue {
  date: Date;
  price: number;
}
