#!/usr/bin/python

from datetime import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_MISSED, EVENT_JOB_ERROR, EVENT_JOB_MAX_INSTANCES

from mailing.error import ErrorMessage
from mailing.missed_job import MissedJobMessage

import applications.base


class TraderApplication(applications.base.ApplicationBase):
    def __init__(self):
        super().__init__()
        self.__scheduler = BlockingScheduler()

    def _initialize_application_logic(self):
        self._builder.build(self._configuration.components, self._configuration.testing.enabled)

    @staticmethod
    def __add_trader_schedule(scheduler, config, trader, listener):
        scheduler.add_job(lambda: trader.perform(listener.read_and_clear()),
                          "interval", seconds=config.check_interval,
                          next_run_time=datetime.now())

    def _run_application_logic(self):
        for fetcher_config in self._configuration.components.fetchers:
            self.__scheduler.add_job(self._builder.fetcher_publishers[fetcher_config.output_signal_id].publish,
                                     "interval",
                                     seconds=fetcher_config.check_interval,
                                     next_run_time=datetime.now())

        for trader_config in self._configuration.components.traders:
            trader = self._builder.traders[trader_config.input_signal_id]
            listener = self._builder.trader_listeners[trader_config.input_signal_id]
            self.__add_trader_schedule(self.__scheduler, trader_config, trader, listener)

        if self._configuration.mail.enabled:
            logging.info("Configuring mailing")
            self.__scheduler.add_listener(self.__handle_missed_job, EVENT_JOB_MISSED | EVENT_JOB_MAX_INSTANCES)
            self.__scheduler.add_listener(self.__handle_failed_job, EVENT_JOB_ERROR)
            self.__scheduler.add_job(self._postman.send_all, "interval", seconds=20)

        try:
            self.__scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logging.info("Keyboard interrup or system exit caught")

    def __handle_missed_job(self, event):
        job_name = str(self.__scheduler.get_job(event.job_id))
        logging.error("Missed job %s", job_name)
        message = MissedJobMessage()
        message.compose({"job_name": job_name})
        self._postman.add_message_to_queue(message)

    def __handle_failed_job(self, event):
        logging.exception(event.exception)
        message = ErrorMessage()
        message.compose({"error": str(event.exception) + "\n\n" + event.traceback})
        self._postman.add_message_to_queue(message)
