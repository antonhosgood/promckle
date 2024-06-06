# Promckle

Promckle is a Python library for reading Prometheus TSDB blocks.

## Description

Promckle allows you to read Prometheus TSDB blocks so that you can process or analyze them in Python. Promckle is great if you have dumped TSDB blocks and would like to get a feel for what time series are present.

Prometheus TSDB blocks are structured as shown [here](https://github.com/prometheus/prometheus/tree/main/tsdb/docs/format).

## Installation

Clone or download the repo to where you would like to use promckle.

```bash
cd promckle
make setup
```

Note: you will need to have Go installed to build the prometheus-tsdb-dump binary.

## Usage

```python
from promckle import DataLoader

# Initialize dataloader
dataloader = DataLoader()

# Read a block
dataloader.read_block('/path/to/tsdb/block')

# Promckle can read multiple blocks
dataloader.read_block('/path/to/tsdb/block2')

# And store the data in a single dataframe
df = dataloader.to_dataframe()

# Or write directly to disk
dataloader.to_tsv('/path/to/output.tsv')
```

## Acknowledgment

Promckle is built on top of [prometheus-tsdb-dump](https://github.com/ryotarai/prometheus-tsdb-dump).
