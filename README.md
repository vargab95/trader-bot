# Trader bot

Bot for trading with crypto currencies.

# Features

The current implementation supports the following main features
- Trading with different type of pairs on different exchanges
- Simulation of trading strategies
- Sending email notifications (nice when executing on a VPS)
- Composition of complex filters and detection logic (multiple filters applied to the same signal and
  complex logic between detection logics with AND, OR and NOT relationship)
- Scraping Tradingview to be able to trade based on trading view "gauges"
- Cross exchange detection (for example trading on FTX based on prices on Binance)
- Cross pair detection (for example trading ETH-USDT based on BTC-USDT price)

Some features were discontinued due to the lack of time, like
- UI for trading simulation
- (Storing and serving indicators with timestamps in mongodb
- Some features are only working with FTX exchange

# Configuration

## Generate default configuration

Configuration is done via a yaml file. A default file with the default
settings can be generated with the following command.
```python3
cd backend
python3 tools/generate_config.py conf.yml
```

For details on configuration options in general, please check the comments
in the config module.

# Components

Trader-bot uses "message buses" to communicate between components. Two major
message buses are used. This first one is for the analogue signals, like
input signals and the other one is for detector signals. Analogue signals
are provided by fetchers and filters and consumed by detectors. Detector
signals are provided by detectors and detector combinations and consumed by
traders. So to set up a properly functioning bot, you'll have to define all
these components and the connection between them. This additional complexity
was added to be able to set up arbitrary filter, detector, exchange and 
trader connections.

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
	traderbot ./run.sh trader conf.yml
```

# Contribution

PRs are welcomed in any topics. This bot was implemented and used by only me for several years
and now I've just made it public. Due to this fact it does not have an extensive
documentation yet and there are several discontinued features due to the lack of spare time.
I'll try to add some documentation and make the project more complete. If you're interested
please create a PR or contact me and let's create a great bot together.

# Disclaimer

As it's described by the licence as well, there is no warranty on using this bot. It's only a
hobby project, there can be bugs in the trading algorithm and even in the simulation logic.
It can only be used at your own risk.
