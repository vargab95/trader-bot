FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc libffi-dev

RUN groupadd -g 1000 appgroup && useradd -u 1000 -g appgroup -s /bin/sh -m appuser
USER appuser

ENV PATH="${PATH}:/home/appuser/.local/bin"

WORKDIR /app
COPY ./requirements.txt ./requirements.txt
COPY ./requirements.test.txt ./requirements.test.txt

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

ARG include_testing_tools=false
RUN if [ "$include_testing_tools" = "true" ]; then python3 -m pip install -r requirements.test.txt; fi

ENV TRADER_APPLICATION_TYPE=
ENV TRADER_CONFIG_FILE=

COPY . .

USER root
RUN chmod +x *.sh

USER appuser
