#!/usr/bin/python3

import sys

from applications.factory import ApplicationFactory, \
                                 InvalidApplicationException


def main(argc, argv):
    if argc < 2:
        available = ', '.join(ApplicationFactory.get_available_applications())
        print("Usage: {} <application>".format(argv[0]))
        print("\nAvailable application: {}".format(available))
        return 1

    try:
        application = ApplicationFactory.create(argv[1])

        application.initialize()
        application.run()
    except InvalidApplicationException:
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))  # pragma: no cover
