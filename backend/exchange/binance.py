#!/usr/bin/python3

import logging
import datetime

import binance.client

import exchange.base
import exchange.interface
import exchange.guard
import config.exchange

from signals.trading_signal import TradingSignal, TickerSignalDescriptor, TradingSignalPoint


class BinanceController(exchange.base.ExchangeBase):
    def __init__(self, configuration: config.exchange.ExchangeConfig):
        super().__init__(configuration)
        self.client = binance.client.Client(self._public_key,
                                            self._private_key)
        exchange_info = self.client.get_exchange_info()
        logging.debug("Min quantities:")
        for market_info in exchange_info["symbols"]:
            for filter_info in market_info["filters"]:
                if filter_info["filterType"] == "LOT_SIZE":
                    min_quantity = float(filter_info["minQty"])
                if filter_info["filterType"] == "MIN_NOTIONAL":
                    min_notional = float(filter_info["minNotional"])
            symbol = market_info["symbol"]
            self._min_amount[symbol] = min_quantity
            self._min_notional[symbol] = min_notional
            logging.debug("    %s: LOT_SIZE: %f MIN_NOTIONAL: %f", symbol,
                          min_quantity, min_notional)

    @exchange.guard.exchange_guard()
    def buy(self, market: exchange.interface.Market, amount: float) -> bool:
        if amount <= 0.0:
            return False

        corrected_amount = self._check_and_log_corrected_amount(
            market, amount, "buy")

        if corrected_amount <= 0.0:
            return False

        self.client.create_order(
            symbol=self.get_market_key(market),
            side=binance.client.Client.SIDE_BUY,
            type=binance.client.Client.ORDER_TYPE_MARKET,
            quantity="{:.12f}".format(corrected_amount).rstrip('0'))
        logging.info("%.10f %s was successfully bought", corrected_amount,
                     self.get_market_key(market))
        return True

    @exchange.guard.exchange_guard()
    def sell(self, market: exchange.interface.Market, amount: float) -> bool:
        if amount <= 0.0:
            return False

        corrected_amount = self._check_and_log_corrected_amount(
            market, amount, "sell")

        if corrected_amount <= 0.0:
            return False

        self.client.create_order(
            symbol=self.get_market_key(market),
            side=binance.client.Client.SIDE_SELL,
            type=binance.client.Client.ORDER_TYPE_MARKET,
            quantity="{:.12f}".format(corrected_amount).rstrip('0'))
        logging.info("%.10f %s was successfully sold", corrected_amount,
                     self.get_market_key(market))
        return True

    @exchange.guard.exchange_guard()
    def get_balances(self) -> exchange.interface.Balances:
        account_information = self.client.get_account()
        binance_balances = account_information["balances"]
        balances = exchange.interface.Balances()

        for balance in binance_balances:
            free = float(balance["free"])
            if free > 1e-7:
                balances[balance["asset"]] = free

        return balances

    @exchange.guard.exchange_guard()
    def get_balance(self, market: str) -> float:
        return float(self.client.get_asset_balance(asset=market)["free"])

    @exchange.guard.exchange_guard()
    def get_price(self, market: exchange.interface.Market, keyword: str = "lastPrice", future: bool = False) -> float:
        response = self.client.get_ticker(symbol=self.get_market_key(market))
        return float(response[keyword])

    __resolution_map = {
        60:             binance.client.Client.KLINE_INTERVAL_1MINUTE,
        60 * 3:         binance.client.Client.KLINE_INTERVAL_3MINUTE,
        60 * 5:         binance.client.Client.KLINE_INTERVAL_5MINUTE,
        60 * 15:        binance.client.Client.KLINE_INTERVAL_15MINUTE,
        60 * 30:        binance.client.Client.KLINE_INTERVAL_30MINUTE,
        3600:           binance.client.Client.KLINE_INTERVAL_1HOUR,
        3600 * 2:       binance.client.Client.KLINE_INTERVAL_2HOUR,
        3600 * 4:       binance.client.Client.KLINE_INTERVAL_4HOUR,
        3600 * 6:       binance.client.Client.KLINE_INTERVAL_6HOUR,
        3600 * 8:       binance.client.Client.KLINE_INTERVAL_8HOUR,
        3600 * 12:      binance.client.Client.KLINE_INTERVAL_12HOUR,
        3600 * 24:      binance.client.Client.KLINE_INTERVAL_1DAY,
        3600 * 24 * 3:  binance.client.Client.KLINE_INTERVAL_3DAY,
        3600 * 24 * 7:  binance.client.Client.KLINE_INTERVAL_1WEEK,
        3600 * 24 * 30: binance.client.Client.KLINE_INTERVAL_1MONTH
    }

    __result_map = {
        "time": 0,
        "open": 1,
        "high": 2,
        "low": 3,
        "close": 4,
        "volume": 5
    }

    @exchange.guard.exchange_guard()
    def get_price_history(self, descriptor: TickerSignalDescriptor, keyword: str = "") -> TradingSignal:
        if descriptor.resolution.total_seconds() not in list(self.__resolution_map.keys()):
            raise ValueError(
                "Resolution time gap should be in " + str(list(self.__resolution_map.keys())))

        resolution = self.__resolution_map[
            descriptor.resolution.total_seconds()]

        result = self.client.get_historical_klines(
            symbol=self.get_market_key(descriptor.market),
            interval=str(resolution),
            start_str=int((descriptor.start_date
                           - datetime.datetime(1970, 1, 1)).total_seconds() * 1000) if descriptor.start_date else 0,
            end_str=int((descriptor.end_date -
                         datetime.datetime(1970, 1, 1)).total_seconds())
            * 1000 if descriptor.end_date else None,
            limit=descriptor.limit if descriptor.limit > 0 else 500
        )

        logging.debug("Binance price history request result: %s", str(result))

        history = []
        for item in result:
            point = TradingSignalPoint()
            point.value = float(item[self.__result_map[keyword]])
            point.date = datetime.datetime.fromtimestamp(item[0] / 1000)
            history.append(point)

        return TradingSignal(history, descriptor)

    def get_positions(self) -> exchange.interface.Balances:
        raise NotImplementedError

    def get_position(self, market: str) -> float:
        raise NotImplementedError
