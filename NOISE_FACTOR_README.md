# Noise Factor

The Noise factor is designed to add realistic variability at the last stage of sales generation to avoid heteroscedasticity and make synthetic data more realistic.

## Overview

Heteroscedasticity occurs when the variance of errors is not constant across different levels of the independent variable. In sales data, this often manifests as larger variations during peak periods (e.g., holiday seasons) and smaller variations during low periods. The Noise factor addresses this by adding controlled randomness at the final stage of data generation.

## Features

- **Configurable noise level**: Control the intensity of noise added
- **Multiple noise types**: Support for normal, uniform, and Poisson distributions
- **Last-stage application**: Ensures noise is applied after all other factors
- **Reproducible results**: Consistent output with the same random seed

## Usage

### Basic Usage

```python
from fakedemand import Noise, Sales, Seasonality, Row

# Create base factors
sales = Sales(level=100, scale=20)
seasonality = Seasonality(peaks=['july', 'december'], amplitude=0.3)

# Create noise factor - this will be applied last
noise = Noise(noise_level=0.15, noise_type='normal')

# Create row with factors in specific order
# Noise should be last to ensure it's applied at the final stage
factors = [sales, seasonality, noise]
row = Row(idx=1, factors=factors)
```

### Parameters

- **`noise_level`** (float): Standard deviation of the noise as a fraction of the signal
  - For normal/uniform: represents the scale of variation
  - For Poisson: represents the mean of the distribution
  - Recommended range: 0.05 to 0.3 (5% to 30% of signal)

- **`noise_type`** (str): Type of noise distribution
  - `'normal'`: Gaussian distribution (default)
  - `'uniform'`: Uniform distribution between [-level, +level]
  - `'poisson'`: Poisson distribution (always positive)

### Integration with RowSet

The Noise factor is automatically included in RowSet configurations:

```python
from fakedemand import RowSet

# Create a RowSet with default configurations including noise
rowset = RowSet(num_groups=3, rows_per_group=5)
rowset.generate_groups()

# The default configuration includes:
# - Seasonality (40% weight)
# - LinearTrend (30% weight) 
# - Promo (20% weight)
# - Noise (10% weight)
```

## Why Add Noise at the Last Stage?

1. **Avoids heteroscedasticity**: By adding noise after all other factors, we ensure consistent variability across all sales levels
2. **Realistic data**: Real sales data always contains some random variation
3. **Proper integration**: Noise is applied to the final processed values, not just individual factors
4. **Controlled randomness**: The noise level can be tuned to match expected real-world variability

## Examples

### Different Noise Types

```python
# Normal distribution (most common for sales data)
noise_normal = Noise(noise_level=0.1, noise_type='normal')

# Uniform distribution (bounded variation)
noise_uniform = Noise(noise_level=0.1, noise_type='uniform')

# Poisson distribution (positive-only variation)
noise_poisson = Noise(noise_level=0.1, noise_type='poisson')
```

### Adjusting Noise Levels

```python
# Low noise for stable products
noise_low = Noise(noise_level=0.05, noise_type='normal')

# High noise for volatile products
noise_high = Noise(noise_level=0.25, noise_type='normal')
```

## Best Practices

1. **Order matters**: Always place the Noise factor last in your factors list
2. **Start small**: Begin with noise_level=0.1 and adjust based on your needs
3. **Consider your data**: Use normal distribution for most cases, uniform for bounded scenarios
4. **Test different levels**: Experiment with various noise levels to find the right balance
5. **Reproducibility**: Set random seeds when you need consistent results

## Technical Details

The Noise factor inherits from the base `Factor` class and overrides the `apply()` method to ensure noise is added at the final stage. It integrates seamlessly with the existing factor system and follows the same patterns as other factors in the library.

## See Also

- [Main README](README.md) - Overview of the fakedemand library
- [Factor System](fakedemand/core.py) - Understanding how factors work
- [RowSet Documentation](ROWSET_README.md) - Using RowSet for batch generation
- [Examples](examples/) - More usage examples
