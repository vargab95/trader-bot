#!/usr/bin/python3

import sys  # pragma: no cover

import yaml  # pragma: no cover

import config.application  # pragma: no cover


def main():  # pragma: no cover
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], " [config file path]")
        sys.exit(1)
    configuration = config.application.ApplicationConfig({})
    with open(sys.argv[1], "w") as generated:
        yaml.dump(configuration, generated)


if __name__ == "__main__":  # pragma: no cover
    main()
