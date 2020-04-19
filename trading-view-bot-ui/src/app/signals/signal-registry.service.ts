import { Injectable } from '@angular/core';
import {
  IndicatorResponse,
  IndicatorRequest,
  IndicatorService
} from './indicator.service';
import { TickerResponse, TickerRequest, TickerService } from './ticker.service';
import { Subject } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SignalRegistryService {
  signals: Array<RegisteredSignal> = [];
  signalsChanged = new Subject<Array<RegisteredSignal>>();

  constructor(
    private indicatorService: IndicatorService,
    private tickerService: TickerService
  ) {}

  register(type: SignalType, request: IndicatorRequest | TickerRequest) {
    const id = this.signals.push({
      id: this.signals.length + 1,
      isHidden: false,
      type,
      data: null,
      request
    });

    return this.modify(id - 1, request);
  }

  remove(id: number) {
    delete this.signals[id];

    for (let i = 0; i < this.signals.length; i++) {
      this.signals[i].id = i + 1;
    }

    this.signalsChanged.next([...this.signals]);
  }

  modify(id: number, request: IndicatorRequest | TickerRequest) {
    this.signals[id].request = request;

    if (this.signals[id].type === SignalType.Indicator) {
      return this.indicatorService
        .getIndicators(this.signals[id].request as IndicatorRequest)
        .pipe(
          map((response: IndicatorResponse) => {
            this.signals[id].data = response;
            this.signalsChanged.next([...this.signals]);
          })
        );
    } else {
      return this.tickerService.getTickers(this.signals[id].request).pipe(
        map((response: TickerResponse) => {
          this.signals[id].data = response;
          this.signalsChanged.next([...this.signals]);
        })
      );
    }
  }
}

export enum SignalType {
  Indicator,
  Ticker
}

export interface RegisteredSignal {
  id: number;
  isHidden: boolean;
  type: SignalType;
  data: IndicatorResponse | TickerResponse;
  request: IndicatorRequest | TickerRequest;
}
