# ICT-Quant

Small educational example of a quantitative trading workflow. The repository
contains:

* A sample price history under `data/sample_prices.csv`.
* A lightweight toolkit in `ict_quant/` for loading price data, computing
  moving averages, generating strategy signals, and running a simple
  backtest.
* A `main.py` script that wires everything together and prints a short
  performance summary.

## Quick start

Create a virtual environment (optional) and install the test dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

To run the example backtest:

```bash
python main.py
```

To execute the automated tests:

```bash
pytest
```
