# Trader bot

Bot for trading with crypto currencies.

# Features

The current implementation supports the following main features
    - Trading with different type of pairs on different exchanges
    - Simulation of trading strategies
    - Sending email notifications (nice when executing on a VPS)
    - Composition of complex filters and detection logic
    - Scraping Tradingview to be able to trade based on trading view "gauges"

Some features were discontinued due to the lack of time, like
    - UI for trading simulation
    - (Storing and serving indicators with timestamps in mongodb
    - Some features are only working with FTX exchange as it was recently used by me

PRs are welcomed for any new features, making current ones better or updating discontinued ones.

# Configuration

## Generate default configuration

Configuration is done via yaml files. A default file with the default
settings can be generated with the following command.
```python3
cd backend
python3 tools/generate_config.py conf.yml
```

For details on configuration options in general, please check the comments
in the comments module.

## Components

Trader-bot uses "message buses" to communicate between components. Two major
message buses are used. This first one is for the analogue signals, like
input signals and the other one is for detector signals. Analogue signals
are provided by fetchers and filters and consumed by detectors. Detector
signals are provided by detectors and detector combinations and consumed by
traders. So to set up a properly functioning bot, you'll have to define all
these components and the connection between them. This additional complexity
was added to be able to set up arbitrary filter and detector sequences.

# Running

It can be run in a container, using the following commands.

```bash
cd backend
docker image build -t traderbot .
docker container run \
	--restart=always \
	-d \
	-v `pwd`/conf.yml:/app/conf.yml \
	--name traderbotinstance \
	traderbot:master ./run.sh trader conf.yml
```
