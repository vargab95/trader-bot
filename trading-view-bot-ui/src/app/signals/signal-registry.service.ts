import { Injectable } from "@angular/core";
import { Subject, Observable } from "rxjs";
import { map } from "rxjs/operators";
import { Filter } from "../filtering/filter.entity";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { environment } from "src/environments/environment";
import { DateSpan } from "./date-span-picker/date-span-picker.component";

@Injectable({
  providedIn: "root",
})
export class SignalRegistryService {
  signals: Array<RegisteredSignal> = [];
  signalsChanged = new Subject<Array<RegisteredSignal>>();

  constructor(private http: HttpClient) {}

  get(id: number) {
    return { ...this.signals[id] };
  }

  register(properties: SignalProperties) {
    const id = this.signals.push({
      id: this.signals.length,
      data: null,
      properties,
    });

    return this.modify(id - 1, properties);
  }

  remove(id: number) {
    this.signals.splice(id, 1);

    for (let i = 0; i < this.signals.length; i++) {
      this.signals[i].id = i;
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
        "Content-Type": "application/json",
      }),
    };
    return this.http.post<SignalResponse>(
      this.getBaseUrl(properties.type),
      properties,
      httpOptions
    );
  }

  getOptions(type: SignalType): Observable<SignalOptions> {
    return this.http.get<SignalOptions>(this.getBaseUrl(type, "/options"));
  }

  getBaseUrl(type: SignalType, subUrl: string = ""): string {
    return (
      environment.apiBaseUrl +
      (type === SignalType.Indicator ? "indicator" : "ticker") +
      subUrl
    );
  }
}

export enum SignalType {
  Indicator,
  Ticker,
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
  candleSize?: string;
  dateSpan?: DateSpan;
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
