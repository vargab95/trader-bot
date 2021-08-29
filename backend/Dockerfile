FROM python:3.9

WORKDIR /app
COPY ./requirements.txt ./requirements.txt

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

ENV TRADER_APPLICATION_TYPE=
ENV TRADER_CONFIG_FILE=

COPY . .

ENTRYPOINT ["./run.sh"]
