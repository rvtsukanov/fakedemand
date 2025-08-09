# Fakedemand

A Python library for generating synthetic demand data with various factors and seasonality patterns.

## Features

- **Multiple Factors**: Linear trends, change points, seasonality, sales patterns, and more
- **Flexible Seasonality**: Custom peaks for months, weeks, quarters, and special periods
- **Date Frequency Support**: Works with any pandas-style date frequency
- **Comprehensive Testing**: Agent-based testing framework included

## Installation

### Development Installation (Recommended)

For development and testing, install the package in editable mode:

```bash
# Clone the repository
git clone <repository-url>
cd fakedemand

# Install in development mode
pip install -e .

# Or use the provided script
./install_dev.sh
```

### Production Installation

For production use, install from PyPI (when available):

```bash
pip install fakedemand
```

## Usage

### Running Examples

After installation, you can run the example:

```bash
# Run the main example
python -m fakedemand

# Or run the specific example file
python -m fakedemand.fakedemand
```

### Importing Factors

You can import factors in several ways:

#### 1. Individual Factor Imports (Recommended)

```python
from fakedemand.factors.seasonality import Seasonality
from fakedemand.factors.linear_trend import LinearTrend
from fakedemand.factors.change_points import ChangePoints
from fakedemand.factors.oos import OOS
from fakedemand.factors.sales import Sales
from fakedemand.factors.constant import Constant, Multiplier
from fakedemand.factors.new_trend import NewTrend
```

#### 2. Package-Level Imports

```python
from fakedemand.factors import (
    Seasonality,
    LinearTrend,
    ChangePoints,
    OOS,
    Sales,
    Constant,
    Multiplier,
    NewTrend
)
```

#### 3. Main Package Imports (Backward Compatibility)

```python
from fakedemand import (
    Seasonality,
    LinearTrend,
    ChangePoints,
    OOS,
    Sales,
    Constant,
    Multiplier,
    NewTrend
)
```

## Seasonality Factor

The Seasonality factor has been enhanced to support custom peaks and multiple seasonality types.

### Basic Usage

```python
from fakedemand.factors.seasonality import Seasonality

# Basic seasonality with July peak
seasonality = Seasonality(peaks=['july'], amplitude=0.3)

# Multiple peaks - July and December
seasonality = Seasonality(peaks=['july', 'december'], amplitude=0.2)

# Weekly seasonality - Saturday peak
seasonality = Seasonality(peaks=['saturday'], amplitude=0.15)

# Mixed seasonality - July + Saturday
seasonality = Seasonality(peaks=['july', 'saturday'], amplitude=0.25)
```

### Supported Peak Types

#### Monthly Peaks
- `'january'`, `'february'`, `'march'`, `'april'`, `'may'`, `'june'`
- `'july'`, `'august'`, `'september'`, `'october'`, `'november'`, `'december'`

#### Weekly Peaks
- `'monday'`, `'tuesday'`, `'wednesday'`, `'thursday'`, `'friday'`, `'saturday'`, `'sunday'`

#### Quarterly Peaks
- `'q1'`, `'q2'`, `'q3'`, `'q4'`

#### Special Periods
- `'year_start'`, `'mid_year'`, `'year_end'`

### Advanced Features

#### Custom Amplitude and Phase Shift
```python
# Custom amplitude (0.0 to 1.0)
seasonality = Seasonality(peaks=['july'], amplitude=0.5)

# Phase shift in radians (0.0 to 2*pi)
seasonality = Seasonality(peaks=['july'], amplitude=0.3, phase_shift=np.pi/4)
```

#### Different Date Frequencies
```python
# Daily frequency
seasonality = Seasonality(peaks=['july', 'saturday'])
seasonality.date_freq = 'D'

# Weekly frequency
seasonality.date_freq = 'W-MON'

# Monthly frequency
seasonality.date_freq = 'M'
```

#### Peak Information
```python
seasonality = Seasonality(peaks=['july', 'saturday'])
peak_info = seasonality.get_peak_info()
print(peak_info)
# Output:
# {
#     'july': {'offset': 0.5, 'frequency': 12.0, 'phase': 3.142},
#     'saturday': {'offset': 0.714, 'frequency': 7.0, 'phase': 4.487}
# }
```

### Integration with Row Class

```python
from fakedemand.series import Row
from fakedemand.factors.seasonality import Seasonality
from fakedemand.factors.linear_trend import LinearTrend
from fakedemand.factors.constant import Constant

# Create a row with multiple factors including seasonality
row = Row(idx=0, factors=[
    Seasonality(peaks=['july', 'saturday'], amplitude=0.2),
    LinearTrend(descend=False, delta=0.1),
    Constant(10)
])

# Get the dataframe
row.get_pandas_df()
print(row.df.head())
```

## Development

### Project Structure

```
fakedemand/
├── fakedemand/
│   ├── __init__.py              # Main package initialization
│   ├── __main__.py              # Entry point for python -m fakedemand
│   ├── core.py                  # Core Factor class
│   ├── series.py                # Row class
│   ├── _types.py                # Type definitions
│   ├── fakedemand.py            # Example usage
│   └── factors/                 # Factor modules
│       ├── __init__.py          # Factors package initialization
│       ├── seasonality.py       # Seasonality factor
│       ├── linear_trend.py      # LinearTrend factor
│       ├── change_points.py     # ChangePoints factor
│       ├── oos.py              # OOS factor
│       ├── sales.py            # Sales factor
│       ├── constant.py         # Constant and Multiplier factors
│       └── new_trend.py        # NewTrend factor
├── tests/                       # Test suite
├── examples/                    # Example scripts
├── setup.py                     # Package setup
├── pyproject.toml              # Modern Python packaging
└── README.md                   # This file
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run seasonality tests only
pytest tests/test_seasonality.py -v

# Run with coverage
pytest tests/ --cov=fakedemand
```

### Code Quality

```bash
# Format code
black fakedemand/ tests/

# Lint code
flake8 fakedemand/ tests/

# Type checking
mypy fakedemand/
```

## Examples

See `examples/seasonality_examples.py` for comprehensive examples of the new Seasonality functionality.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Add your license information here]