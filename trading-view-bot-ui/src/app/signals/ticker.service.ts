import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { Filter } from '../filtering/filter.entity';

@Injectable({
  providedIn: 'root'
})
export class TickerService {
  private baseUrl = environment.apiBaseUrl + 'ticker';

  constructor(private http: HttpClient) {}

  getTickers(request: TickerRequest): Observable<TickerResponse> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<TickerResponse>(this.baseUrl, request, httpOptions);
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
  filter: Array<Filter>;
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
