"""
Tests for the Noise factor.

This module tests the functionality of the Noise factor to ensure
it properly adds noise at the last stage of sales generation.
"""

import unittest
import numpy as np
import sys
import os

# Add the parent directory to the path to import fakedemand
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fakedemand.factors.noise import Noise
from fakedemand.core import Factor


class TestNoise(unittest.TestCase):
    """Test cases for the Noise factor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.noise_normal = Noise(noise_level=0.1, noise_type='normal')
        self.noise_uniform = Noise(noise_level=0.1, noise_type='uniform')
        self.noise_poisson = Noise(noise_level=0.1, noise_type='poisson')
    
    def test_noise_initialization(self):
        """Test that Noise factor initializes correctly."""
        self.assertEqual(self.noise_normal.name, 'noise')
        self.assertEqual(self.noise_normal.noise_level, 0.1)
        self.assertEqual(self.noise_normal.noise_type, 'normal')
        self.assertIsInstance(self.noise_normal, Factor)
    
    def test_build_own_values_normal(self):
        """Test normal distribution noise generation."""
        values = self.noise_normal.build_own_values()
        self.assertEqual(len(values), self.noise_normal.num_points)
        self.assertTrue(np.allclose(np.mean(values), 0, atol=0.1))
        self.assertTrue(np.allclose(np.std(values), 0.1, atol=0.05))
    
    def test_build_own_values_uniform(self):
        """Test uniform distribution noise generation."""
        values = self.noise_uniform.build_own_values()
        self.assertEqual(len(values), self.noise_uniform.num_points)
        self.assertTrue(np.all(values >= -0.1))
        self.assertTrue(np.all(values <= 0.1))
    
    def test_build_own_values_poisson(self):
        """Test Poisson distribution noise generation."""
        values = self.noise_poisson.build_own_values()
        self.assertEqual(len(values), self.noise_poisson.num_points)
        self.assertTrue(np.all(values >= 0))  # Poisson is always positive
    
    def test_invalid_noise_type(self):
        """Test that invalid noise type raises ValueError."""
        with self.assertRaises(ValueError):
            Noise(noise_level=0.1, noise_type='invalid')
    
    def test_noise_level_parameter(self):
        """Test different noise levels."""
        noise_low = Noise(noise_level=0.05, noise_type='normal')
        noise_high = Noise(noise_level=0.3, noise_type='normal')
        
        values_low = noise_low.build_own_values()
        values_high = noise_high.build_own_values()
        
        # Higher noise level should result in higher standard deviation
        self.assertGreater(np.std(values_high), np.std(values_low))
    
    def test_apply_method(self):
        """Test that the apply method works correctly."""
        # Mock some dependencies
        self.noise_normal.previous_plug_in_dependencies = []
        self.noise_normal.previous_plug_in_applier = {}
        
        result = self.noise_normal.apply()
        self.assertIsNotNone(result)
        self.assertEqual(len(result), self.noise_normal.num_points)
    
    def test_noise_reproducibility(self):
        """Test that noise generation is reproducible with same seed."""
        np.random.seed(42)
        noise1 = Noise(noise_level=0.1, noise_type='normal')
        values1 = noise1.build_own_values()
        
        np.random.seed(42)
        noise2 = Noise(noise_level=0.1, noise_type='normal')
        values2 = noise2.build_own_values()
        
        np.testing.assert_array_equal(values1, values2)


if __name__ == '__main__':
    unittest.main()
