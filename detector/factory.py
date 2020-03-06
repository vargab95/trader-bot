#!/usr/bin/python3

import config.market
import spider
import detector.interface
import detector.crossover
import detector.reverse_crossover
import detector.moving_threshold

class DetectorFactory:
    @classmethod
    def create(cls,
               configuration: config.market.MarketConfig,
               spider: spider.TradingViewSpider = None) -> detector.interface.DetectorInterface:
        if spider:
            return detector.moving_threshold.MovingThresholdCrossOverDetector(configuration.bearish_threshold,
                                                                              configuration.bullish_threshold,
                                                                              spider)
        if configuration.bullish_threshold > configuration.bearish_threshold:
            return detector.crossover.CrossOverDetector(configuration.bearish_threshold,
                                                        coniguration.bullish_threshold)
        return detector.reverse_crossover.ReverseCrossOverDetector(configuration.bearish_threshold,
                                                                   configuration.bullish_threshold)
