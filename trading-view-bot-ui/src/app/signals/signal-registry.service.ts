import { Injectable } from '@angular/core';
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

  constructor(private http: HttpClient) {}

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
      map((response: SignalResponse) => {
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
    return this.http.get<SignalOptions>(this.getBaseUrl(type, '/options'));
  }

  getBaseUrl(type: SignalType, subUrl: string = ''): string {
    return (
      environment.apiBaseUrl +
      (type === SignalType.Indicator ? 'indicator' : 'ticker') +
      subUrl
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
