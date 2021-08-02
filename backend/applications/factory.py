#!/usr/bin/python3

import logging

import applications.exporter
import applications.gatherer
import applications.server
import applications.trader
import applications.simulator


class InvalidApplicationException(Exception):
    pass


class ApplicationFactory:
    __available_applications = ["trader", "exporter", "gatherer", "server", "simulator"]

    @classmethod
    def create(cls, application_name):
        if application_name == "exporter":
            return applications.exporter.ExporterApplication()

        if application_name == "gatherer":
            return applications.gatherer.GathererApplication()

        if application_name == "trader":
            return applications.trader.TraderApplication()

        if application_name == "server":
            return applications.server.ServerApplication()

        if application_name == "simulator":
            return applications.simulator.SimulatorApplication()

        logging.critical("There is no such application %s. Use one of %s",
                         application_name,
                         ", ".join(cls.__available_applications))
        raise InvalidApplicationException()

    @classmethod
    def get_available_applications(cls):
        return cls.__available_applications
