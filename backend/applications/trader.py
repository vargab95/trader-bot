#!/usr/bin/python

from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

import applications.base


class TraderApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self.__last_sent_time: datetime
        self.__first_mail_sent: bool = False

    def _initialize_application_logic(self):
        self._builder.build(self._configuration.components)

    @staticmethod
    def __add_trader_schedule(scheduler, config, trader, listener):
        scheduler.add_job(lambda: trader.perform(listener.read_and_clear()),
                          "interval", seconds=config.check_interval)

    def _run_application_logic(self):
        scheduler = BlockingScheduler()

        for fetcher_config in self._configuration.components.fetchers:
            scheduler.add_job(self._builder.fetcher_publishers[fetcher_config.output_signal_id].publish,
                              "interval",
                              seconds=fetcher_config.check_interval)

        for trader_config in self._configuration.components.traders:
            trader = self._builder.traders[trader_config.input_signal_id]
            listener = self._builder.trader_listeners[trader_config.input_signal_id]
            self.__add_trader_schedule(scheduler, trader_config, trader, listener)

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
