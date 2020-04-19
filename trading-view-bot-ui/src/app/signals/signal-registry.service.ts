import { Injectable } from '@angular/core';
import {
  IndicatorResponse,
  IndicatorRequest,
  IndicatorService
} from './indicator.service';
import { TickerResponse, TickerRequest, TickerService } from './ticker.service';
import { Subject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Filter } from '../filtering/filter.entity';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SignalRegistryService {
  signals: Array<RegisteredSignal> = [];
  signalsChanged = new Subject<Array<RegisteredSignal>>();

  constructor(
    private http: HttpClient,
    private indicatorService: IndicatorService,
    private tickerService: TickerService
  ) {}

  register(properties: SignalProperties) {
    const id = this.signals.push({
      id: this.signals.length + 1,
      data: null,
      properties
    });

    return this.modify(id - 1, properties);
  }

  remove(id: number) {
    delete this.signals[id];

    for (let i = 0; i < this.signals.length; i++) {
      this.signals[i].id = i + 1;
    }

    this.signalsChanged.next([...this.signals]);
  }

  modify(id: number, properties: SignalProperties) {
    this.signals[id].properties = properties;

    return this.getSignal(properties).pipe(
      map((response: IndicatorResponse) => {
        this.signals[id].data = response;
        this.signalsChanged.next([...this.signals]);
      })
    );
  }

  getSignal(properties: SignalProperties): Observable<SignalResponse> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<SignalResponse>(
      this.getBaseUrl(properties.type),
      properties,
      httpOptions
    );
  }

  getOptions(type: SignalType): Observable<SignalOptions> {
    return this.http.get<SignalOptions>(this.getBaseUrl(type));
  }

  getBaseUrl(type: SignalType): string {
    return (
      environment.apiBaseUrl +
      (type === SignalType.Indicator ? 'indicator' : 'ticker')
    );
  }
}

export enum SignalType {
  Indicator,
  Ticker
}

export interface RegisteredSignal {
  id: number;
  data: SignalResponse;
  properties: SignalProperties;
}

export interface SignalProperties {
  market: string;
  type: SignalType;
  color: string;
  indicator?: string;
  candle_size?: string;
  start_date?: string;
  end_date?: string;
  limit?: number;
  filter?: Array<Filter>;
  step?: number;
}

export interface SignalPoint {
  date: Date;
  value?: number;
  price?: number;
}

export type SignalResponse = Array<SignalPoint>;

export interface SignalOptions {
  market: Array<string>;
  candle_size?: Array<string>;
  indicator?: Array<string>;
  filter_types: Array<string>;
}
