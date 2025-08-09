"""
Example demonstrating the Noise factor usage.

This example shows how to add noise at the last stage of sales generation
to avoid heteroscedasticity and make the data more realistic.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fakedemand import Row, Noise, Sales, Seasonality, LinearTrend
import matplotlib.pyplot as plt
import numpy as np

def create_sales_with_noise():
    """Create a sales series with noise applied at the last stage."""
    
    # Create base factors
    sales = Sales(level=100, scale=20)
    seasonality = Seasonality(peaks=['july', 'december'], amplitude=0.3)
    trend = LinearTrend(descend=False, delta=0.1)
    
    # Create noise factor - this will be applied last
    noise = Noise(noise_level=0.15, noise_type='normal')
    
    # Create row with factors in specific order
    # Noise should be last to ensure it's applied at the final stage
    factors = [sales, seasonality, trend, noise]
    row = Row(idx=1, factors=factors)
    
    return row

def compare_with_without_noise():
    """Compare sales with and without noise."""
    
    # Sales without noise
    sales_no_noise = Sales(level=100, scale=20)
    seasonality = Seasonality(peaks=['july', 'december'], amplitude=0.3)
    trend = LinearTrend(descend=False, delta=0.1)
    
    row_no_noise = Row(idx=1, factors=[sales_no_noise, seasonality, trend])
    
    # Sales with noise
    row_with_noise = create_sales_with_noise()
    
    # Plot comparison
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8))
    
    # Without noise
    row_no_noise.get_pandas_df()
    df_no_noise = row_no_noise.df
    ax1.plot(df_no_noise['date'], df_no_noise['sales'], 'b-', label='Sales without noise')
    ax1.set_title('Sales without Noise')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # With noise
    row_with_noise.get_pandas_df()
    df_with_noise = row_with_noise.df
    ax2.plot(df_with_noise['date'], df_with_noise['sales'], 'r-', label='Sales with noise')
    ax2.set_title('Sales with Noise (Heteroscedasticity avoided)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return row_no_noise, row_with_noise

def demonstrate_noise_types():
    """Demonstrate different types of noise."""
    
    # Base factors
    sales = Sales(level=100, scale=20)
    seasonality = Seasonality(peaks=['july'], amplitude=0.2)
    
    # Different noise types
    noise_normal = Noise(noise_level=0.1, noise_type='normal')
    noise_uniform = Noise(noise_level=0.1, noise_type='uniform')
    noise_poisson = Noise(noise_level=0.1, noise_type='poisson')
    
    # Create rows
    row_normal = Row(idx=1, factors=[sales, seasonality, noise_normal])
    row_uniform = Row(idx=2, factors=[sales, seasonality, noise_uniform])
    row_poisson = Row(idx=3, factors=[sales, seasonality, noise_poisson])
    
    # Plot comparison
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 10))
    
    # Normal noise
    row_normal.get_pandas_df()
    df_normal = row_normal.df
    ax1.plot(df_normal['date'], df_normal['sales'], 'b-', label='Normal noise')
    ax1.set_title('Normal Distribution Noise')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Uniform noise
    row_uniform.get_pandas_df()
    df_uniform = row_uniform.df
    ax2.plot(df_uniform['date'], df_uniform['sales'], 'g-', label='Uniform noise')
    ax2.set_title('Uniform Distribution Noise')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Poisson noise
    row_poisson.get_pandas_df()
    df_poisson = row_poisson.df
    ax3.plot(df_poisson['date'], df_poisson['sales'], 'r-', label='Poisson noise')
    ax3.set_title('Poisson Distribution Noise')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return row_normal, row_uniform, row_poisson

if __name__ == "__main__":
    print("Demonstrating Noise factor usage...")
    
    # Basic example
    print("\n1. Creating sales with noise...")
    row_with_noise = create_sales_with_noise()
    row_with_noise.get_pandas_df()
    df = row_with_noise.df
    print(f"Created row with {len(df)} data points")
    print(f"Sales range: {df['sales'].min():.2f} to {df['sales'].max():.2f}")
    
    # Comparison
    print("\n2. Comparing with and without noise...")
    row_no_noise, row_with_noise = compare_with_without_noise()
    
    # Different noise types
    print("\n3. Demonstrating different noise types...")
    row_normal, row_uniform, row_poisson = demonstrate_noise_types()
    
    print("\nNoise factor demonstration completed!")
    print("\nKey benefits:")
    print("- Adds realistic variability to avoid heteroscedasticity")
    print("- Applied at the last stage for proper integration")
    print("- Configurable noise level and type")
    print("- Supports normal, uniform, and Poisson distributions")
