import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { Filter } from '../filtering/filter.entity';

@Injectable({
  providedIn: 'root'
})
export class IndicatorService {
  private baseUrl = environment.apiBaseUrl + 'indicator';

  constructor(private http: HttpClient) {}

  getIndicators(request: IndicatorRequest): Observable<IndicatorResponse> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<IndicatorResponse>(
      this.baseUrl,
      request,
      httpOptions
    );
  }

  getOptions(): Observable<IndicatorOptions> {
    return this.http.get(this.baseUrl + '/options') as Observable<
      IndicatorOptions
    >;
  }
}

export interface IndicatorRequest {
  market: string;
  indicator: string;
  candle_size: string;
  start_date?: string;
  end_date?: string;
  limit?: number;
  filter: Array<Filter>;
  step?: number;
}

export interface Indicator {
  date: Date;
  value: number;
}

export type IndicatorResponse = Array<Indicator>;

export interface IndicatorOptions {
  market: Array<string>;
  candle_size: Array<string>;
  indicator: Array<string>;
  filter_types: Array<string>;
}
