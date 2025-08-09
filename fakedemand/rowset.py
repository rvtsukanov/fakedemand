"""
RowSet module for fakedemand.

This module provides functionality to gather several Row objects into a dataset
with randomly sampled groups that have similar properties in terms of factor configurations.
"""

import random
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

from .series import Row
from .factors import (
    Seasonality, LinearTrend, ChangePoints, 
    NewTrend, Sales, Constant, Multiplier, Promo, Noise
)


@dataclass
class FactorConfig:
    """Configuration template for a factor with parameter ranges."""
    factor_class: type
    param_ranges: Dict[str, Tuple[Any, Any]]
    weight: float = 1.0  # Probability weight for this factor type


class RowSet:
    """
    A collection of Row objects organized into groups with similar factor configurations.
    
    This class allows you to create datasets where each group of rows has similar
    factor patterns, making it useful for testing different scenarios or creating
    training datasets with controlled variations.
    """
    
    def __init__(self, 
                 num_groups: int = 3,
                 rows_per_group: int = 5,
                 random_seed: Optional[int] = None):
        """
        Initialize a RowSet.
        
        Args:
            num_groups: Number of distinct groups to create
            rows_per_group: Number of rows in each group
            random_seed: Random seed for reproducible results
        """
        self.num_groups = num_groups
        self.rows_per_group = rows_per_group
        self.total_rows = num_groups * rows_per_group
        
        if random_seed is not None:
            random.seed(random_seed)
            np.random.seed(random_seed)
        
        self.groups: Dict[int, List[Row]] = {}
        self.group_configs: Dict[int, Dict[str, Any]] = {}
        self.factor_configs: List[FactorConfig] = []
        
        # Initialize with default factor configurations
        self._setup_default_configs()
    
    def _setup_default_configs(self):
        """Set up default factor configurations with reasonable parameter ranges."""
        self.factor_configs = [
            FactorConfig(
                Seasonality,
                {
                    'peaks': (['july'], ['december'], ['saturday'], ['july', 'december']),
                    'amplitude': (0.1, 0.5),
                    'phase_shift': (0, 2 * np.pi)
                },
                weight=0.4
            ),
            FactorConfig(
                LinearTrend,
                {
                    'descend': (True, False),
                    'delta': (0.1, 0.8)
                },
                weight=0.3
            ),
            FactorConfig(
                Promo,
                {
                    'promo_value': (1.5, 3.0),
                    'num_random_promos': (2, 6)
                },
                weight=0.2
            ),
            FactorConfig(
                Noise,
                {
                    'noise_level': (0.05, 0.2),
                    'noise_type': ('normal', 'uniform')
                },
                weight=0.1
            )
        ]
    
    def add_factor_config(self, config: FactorConfig):
        """Add a custom factor configuration."""
        self.factor_configs.append(config)
    
    def generate_groups(self):
        """Generate all groups with similar factor configurations."""
        for group_id in range(self.num_groups):
            # Generate a base configuration for this group
            base_config = self._generate_base_config()
            self.group_configs[group_id] = base_config
            
            # Create rows for this group with variations
            group_rows = []
            for row_idx in range(self.rows_per_group):
                row_id = group_id * self.rows_per_group + row_idx
                row = self._create_row_from_config(row_id, base_config)
                group_rows.append(row)
            
            self.groups[group_id] = group_rows
    
    def _generate_base_config(self) -> Dict[str, Any]:
        """Generate a base configuration for a group."""
        config = {}
        
        # Select factors for this group based on weights
        selected_factors = self._select_factors_for_group()
        
        for factor_type, factor_class in selected_factors:
            # Find the config for this factor type
            factor_config = next(fc for fc in self.factor_configs 
                               if fc.factor_class == factor_class)
            
            # Generate parameters for this factor
            factor_params = {}
            for param_name, param_range in factor_config.param_ranges.items():
                if isinstance(param_range, tuple):
                    if isinstance(param_range[0], (int, float)):
                        # Numeric range
                        value = np.random.uniform(param_range[0], param_range[1])
                        
                        # Check if the original range was integers and convert accordingly
                        if isinstance(param_range[0], int) and isinstance(param_range[1], int):
                            factor_params[param_name] = int(round(value))
                        else:
                            factor_params[param_name] = value
                    else:
                        # List of options
                        factor_params[param_name] = random.choice(param_range)
                else:
                    # Single value
                    factor_params[param_name] = param_range
            
            config[factor_type] = {
                'class': factor_class,
                'params': factor_params
            }
        
        return config
    
    def _select_factors_for_group(self) -> List[Tuple[str, type]]:
        """Select which factors to include in a group based on weights."""
        selected = []
        
        for config in self.factor_configs:
            if random.random() < config.weight:
                factor_name = config.factor_class.__name__.lower()
                selected.append((factor_name, config.factor_class))
        
        # Ensure at least one factor is selected
        if not selected:
            # Fallback to seasonality if nothing selected
            seasonality_config = next(fc for fc in self.factor_configs 
                                    if fc.factor_class == Seasonality)
            selected.append(('seasonality', Seasonality))
        
        return selected
    
    def _create_row_from_config(self, row_id: int, base_config: Dict[str, Any]) -> Row:
        """Create a Row object from a group configuration with small variations."""
        factors = []
        
        # Create modifier factors FIRST (they will be dependencies for Sales)
        for factor_name, factor_info in base_config.items():
            factor_class = factor_info['class']
            base_params = factor_info['params'].copy()
            
            # Add small variations to parameters
            varied_params = self._add_parameter_variations(base_params)
            
            # Create factor instance
            try:
                factor = factor_class(**varied_params)
                factors.append(factor)
            except Exception as e:
                # Fallback to default parameters if variation fails
                try:
                    factor = factor_class(**base_params)
                    factors.append(factor)
                except Exception as e2:
                    print(f"Warning: Could not create {factor_name} factor: {e2}")
                    continue
        
        # Create Sales factor LAST so it can receive all other factors as dependencies
        sales_params = {
            'level': np.random.uniform(50, 200),
            'scale': 0
        }
        sales_factor = Sales(**sales_params)
        factors.append(sales_factor)
        
        # Create the row - Row.activate_factors will handle the dependencies
        row = Row(idx=row_id, factors=factors)
        return row
    
    def _add_parameter_variations(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add small random variations to parameters."""
        varied_params = params.copy()
        
        for param_name, param_value in varied_params.items():
            if isinstance(param_value, (int, float)):
                # Add ±10% variation for numeric parameters
                variation = param_value * 0.1
                new_value = param_value + np.random.uniform(-variation, variation)
                
                # Preserve integer type for parameters that should be integers
                if isinstance(param_value, int):
                    varied_params[param_name] = int(round(new_value))
                else:
                    varied_params[param_name] = new_value
            elif isinstance(param_value, list):
                # For list parameters, keep the same but maybe shuffle
                if random.random() < 0.3:  # 30% chance to shuffle
                    varied_params[param_name] = param_value.copy()
                    random.shuffle(varied_params[param_name])
        
        return varied_params
    
    def get_all_rows(self) -> List[Row]:
        """Get all rows from all groups as a flat list."""
        all_rows = []
        for group_rows in self.groups.values():
            all_rows.extend(group_rows)
        return all_rows
    
    def get_group_rows(self, group_id: int) -> List[Row]:
        """Get rows from a specific group."""
        return self.groups.get(group_id, [])
    
    def get_group_config(self, group_id: int) -> Dict[str, Any]:
        """Get the configuration for a specific group."""
        return self.group_configs.get(group_id, {})
    
    def to_dataframe(self, include_group_info: bool = True) -> pd.DataFrame:
        """Convert all rows to a single pandas DataFrame."""
        all_dfs = []
        
        for group_id, group_rows in self.groups.items():
            for row in group_rows:
                # Ensure the row has processed data and dependencies are applied
                # This is crucial for getting the properly scaled sales values
                row.get_pandas_df()
                
                # Start with required columns
                df_data = {
                    'date': row.date_range,
                    'id': row.idx,
                    'sales': None  # Will be filled from Sales factor
                }
                
                if include_group_info:
                    df_data['group_id'] = group_id
                    df_data['group_config'] = str(self.group_configs[group_id])
                
                # Process each factor
                for factor in row.factors:
                    if factor.name == 'sales':
                        # Sales factor provides the base sales values
                        # Make sure processed_values are available and dependencies are applied
                        if factor.processed_values is None:
                            # Force re-application of dependencies
                            factor.apply()
                        
                        # Use the processed values which include all dependency effects
                        df_data['sales'] = factor.processed_values
                    else:
                        # Other factors may provide additional features via feature_view
                        try:
                            if hasattr(factor, 'feature_view') and callable(factor.feature_view):
                                feature_values = factor.feature_view()
                                if feature_values is not None and len(feature_values) > 0:
                                    # Use factor name as column name
                                    df_data[factor.name] = feature_values
                        except Exception as e:
                            # Skip factors that don't have feature_view or fail
                            continue
                
                # Create DataFrame for this row
                df = pd.DataFrame(df_data)
                all_dfs.append(df)
        
        if all_dfs:
            return pd.concat(all_dfs, ignore_index=True)
        else:
            return pd.DataFrame()
    
    def get_group_summary(self) -> pd.DataFrame:
        """Get a summary of all groups and their configurations."""
        summary_data = []
        
        for group_id in range(self.num_groups):
            config = self.group_configs.get(group_id, {})
            row_count = len(self.groups.get(group_id, []))
            
            # Extract factor information
            factors_info = []
            for factor_name, factor_info in config.items():
                factor_class = factor_info['class'].__name__
                params_str = str(factor_info['params'])
                factors_info.append(f"{factor_class}: {params_str}")
            
            summary_data.append({
                'group_id': group_id,
                'num_rows': row_count,
                'factors': '; '.join(factors_info),
                'config': str(config)
            })
        
        return pd.DataFrame(summary_data)
    
    def render_group(self, group_id: int, column: str = 'sales'):
        """Render all rows in a specific group."""
        group_rows = self.get_group_rows(group_id)
        if not group_rows:
            print(f"No rows found in group {group_id}")
            return
        
        print(f"Rendering group {group_id} with {len(group_rows)} rows")
        print(f"Group configuration: {self.group_configs[group_id]}")
        
        for row in group_rows:
            row.render_pandas_df(column)
    
    def render_all_groups(self, column: str = 'sales'):
        """Render all groups."""
        for group_id in range(self.num_groups):
            self.render_group(group_id, column)
    
    def save_to_csv(self, filepath: str, include_group_info: bool = True):
        """Save the dataset to a CSV file."""
        df = self.to_dataframe(include_group_info)
        df.to_csv(filepath, index=False)
        print(f"Dataset saved to {filepath}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistical information about the dataset."""
        stats = {
            'total_rows': self.total_rows,
            'num_groups': self.num_groups,
            'rows_per_group': self.rows_per_group,
            'group_sizes': {gid: len(rows) for gid, rows in self.groups.items()},
            'factor_distribution': self._get_factor_distribution()
        }
        return stats
    
    def _get_factor_distribution(self) -> Dict[str, int]:
        """Get distribution of factors across all groups."""
        factor_counts = defaultdict(int)
        
        for config in self.group_configs.values():
            for factor_name in config.keys():
                factor_counts[factor_name] += 1
        
        return dict(factor_counts)


def create_sample_rowset(num_groups: int = 3, 
                        rows_per_group: int = 5,
                        random_seed: Optional[int] = None) -> RowSet:
    """
    Create a sample RowSet with predefined configurations.
    
    This is a convenience function to quickly create a RowSet with
    reasonable default configurations for testing and demonstration.
    """
    rowset = RowSet(num_groups, rows_per_group, random_seed)
    rowset.generate_groups()
    return rowset


if __name__ == "__main__":
    # Example usage
    print("Creating a sample RowSet...")
    rowset = create_sample_rowset(num_groups=2, rows_per_group=3, random_seed=42)
    
    print(f"Created RowSet with {rowset.total_rows} total rows")
    print("\nGroup summary:")
    print(rowset.get_group_summary())
    
    print("\nDataset statistics:")
    print(rowset.get_statistics())
    
    # Convert to DataFrame
    df = rowset.to_dataframe()
    print(f"\nDataFrame shape: {df.shape}")
    print(f"DataFrame columns: {df.columns.tolist()}")
