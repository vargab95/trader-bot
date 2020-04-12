# Trading view bot

Bot for trading based on trading view technical summary.

## Run

```sh
python3 main.py conf.yml
```

## Initialze project

### On linux

```sh
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

## Start development

### On linux

```sh
source env/bin/activate
```

## Run tests

```
python3 -m coverage run --source=. \
                        --omit="*ut_*.py" \
                        -m unittest \
                        `find . -type f \
                                -name "ut_*.py" \
                                -printf "%P\n"`
python3 -m coverage report -m
```
