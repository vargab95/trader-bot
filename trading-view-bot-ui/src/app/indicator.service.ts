import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class IndicatorService {
  private baseUrl = environment.apiBaseUrl + 'indicator';

  constructor(private http: HttpClient) {}

  getIndicators(request: IndicatorRequest): Observable<IndicatorResponse> {
    return this.http.get(this.baseUrl, {
      params: request as any
    }) as Observable<IndicatorResponse>;
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
  ma_length?: number;
  ma_type?: string;
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
