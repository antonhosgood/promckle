# Promckle

Promckle is a Python package for reading Prometheus TSDB blocks.

## Description

Promckle allows you to read Prometheus TSDB blocks so that you can process or analyse them in Python.
Promckle is great if you have TSDB dumps and would like to get a feel for what time series are present.

Prometheus TSDB blocks are structured as
shown [here](https://github.com/prometheus/prometheus/tree/main/tsdb/docs/format).

## Installation

### Prerequisites

You will need to have [Go](https://go.dev/doc/install) installed to build
the [prometheus-tsdb-dump](https://github.com/ryotarai/prometheus-tsdb-dump) binary.

Additionally, ensure that you have **Python 3.10 or higher** installed.

### Setup

Clone or download the repo to where you would like to use promckle and run the setup.

```bash
cd promckle
make setup
```

Make sure you have a Python environment ready with all the necessary packages installed.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```python3
from promckle import DataLoader

# Initialise dataloader
dataloader = DataLoader()

# Read a block
dataloader.read_block('/path/to/tsdb/block')

# Promckle can read multiple blocks
dataloader.read_block('/path/to/tsdb/block2')

# And store the data in a single dataframe
df = dataloader.to_dataframe()

# Or write directly to disk
dataloader.to_parquet('/path/to/output.parquet')
```
