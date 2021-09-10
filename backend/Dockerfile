FROM python:3.9

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

ENTRYPOINT ["./run.sh"]
