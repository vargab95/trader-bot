import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TickerService {
  private baseUrl = environment.apiBaseUrl + 'ticker';

  constructor(private http: HttpClient) {}

  getTickers(request: TickerRequest): Observable<TickerResponse> {
    return this.http.get(this.baseUrl, {
      params: request as any
    }) as Observable<TickerResponse>;
  }

  getOptions(): Observable<TickerOptions> {
    return this.http.get(this.baseUrl + '/options') as Observable<
      TickerOptions
    >;
  }
}

export interface TickerRequest {
  market: string;
  start_date?: string;
  end_date?: string;
  limit?: number;
  sma?: number;
  step?: number;
}

export interface Ticker {
  date: Date;
  price: number;
}

export type TickerResponse = Array<Ticker>;

export interface TickerOptions {
  market: Array<string>;
  filter_types: Array<string>;
}
