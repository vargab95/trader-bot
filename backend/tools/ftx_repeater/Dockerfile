FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y

RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -s /bin/sh -m appuser
USER appuser

ENV PATH="${PATH}:/home/appuser/.local/bin"

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

COPY ./ftx_repeater.py .

CMD ["python3", "ftx_repeater.py", "0.0.0.0"]
