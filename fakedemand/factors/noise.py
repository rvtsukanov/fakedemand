"""
Noise factor for fakedemand.

This factor adds random noise at the last stage of sales generation
to avoid heteroscedasticity and make the data more realistic.
"""

from fakedemand.core import Factor
import numpy as np


class Noise(Factor):
    name = 'noise'
    
    def __init__(self, noise_level: float = 0.1, noise_type: str = 'normal'):
        """
        Initialize the Noise factor.
        
        Args:
            noise_level: Standard deviation of the noise (as a fraction of the signal)
            noise_type: Type of noise ('normal', 'uniform', 'poisson')
        """
        self.noise_level = noise_level
        self.noise_type = noise_type
        super().__init__()

    def build_own_values(self):
        """Generate noise values based on the specified type and level."""
        if self.noise_type == 'normal':
            # Normal distribution noise
            return np.random.normal(0, self.noise_level, self.num_points)
        elif self.noise_type == 'uniform':
            # Uniform distribution noise
            return np.random.uniform(-self.noise_level, self.noise_level, self.num_points)
        elif self.noise_type == 'poisson':
            # Poisson distribution noise (always positive)
            return np.random.poisson(self.noise_level, self.num_points)
        else:
            raise ValueError(f"Unknown noise type: {self.noise_type}. Use 'normal', 'uniform', or 'poisson'")

    def apply(self):
        """
        Override apply method to add noise to the final processed values.
        This ensures noise is applied at the very last stage.
        """
        # First apply any dependencies
        self.validate_dependencies()
        own_values = self.build_own_values()

        # Apply transformations from dependencies
        for transform in self.previous_plug_in_dependencies:
            if type(transform) in self.previous_plug_in_applier:
                own_values = self.previous_plug_in_applier[type(transform)](
                    transform.processed_values, own_values
                )
        
        # Add noise to the final values
        self.processed_values = own_values
        return self.processed_values
