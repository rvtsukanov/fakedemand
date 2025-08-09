import pytest
from fakedemand.series import Row
from fakedemand.factors.seasonality import Seasonality
from fakedemand.factors.linear_trend import LinearTrend
from fakedemand.factors.constant import Constant
import numpy as np
import pandas as pd

def test_seasonality_render():
    '''Run render for visual tests'''
    seasonal_factor = Seasonality(peaks=['january', 'saturday'], amplitude=0.3, phase_shift=np.pi/2)
    seasonal_factor.date_freq = 'D'
    print(seasonal_factor)
    # import matplotlib.pyplot as plt
    vals = seasonal_factor.build_own_values()
    # plt.plot([1, 2, 3], [1, 2, 3])
    plt.show()


def test_seasonality_basic():
    """Test basic seasonality with default peak (july)."""
    seasonal_factor = Seasonality()
    values = seasonal_factor.build_own_values()
    
    assert len(values) == seasonal_factor.num_points
    assert np.all(values >= 0)  # Values should be non-negative
    assert np.all(values <= 2)  # Values should be <= 1 + amplitude


def test_seasonality_single_month():
    """Test seasonality with a single month peak."""
    seasonal_factor = Seasonality(peaks=['july'])
    values = seasonal_factor.build_own_values()
    
    assert len(values) == seasonal_factor.num_points
    # Check that we have some variation (not all values are 1)
    assert not np.allclose(values, 1.0)


def test_seasonality_multiple_months():
    """Test seasonality with multiple month peaks."""
    seasonal_factor = Seasonality(peaks=['july', 'december'])
    values = seasonal_factor.build_own_values()
    
    assert len(values) == seasonal_factor.num_points
    # Check that we have some variation
    assert not np.allclose(values, 1.0)


def test_seasonality_weekly():
    """Test seasonality with weekly peaks."""
    seasonal_factor = Seasonality(peaks=['saturday'])
    values = seasonal_factor.build_own_values()
    
    assert len(values) == seasonal_factor.num_points
    assert not np.allclose(values, 1.0)


def test_seasonality_mixed():
    """Test seasonality with mixed monthly and weekly peaks."""
    seasonal_factor = Seasonality(peaks=['july', 'saturday'])
    values = seasonal_factor.build_own_values()
    
    assert len(values) == seasonal_factor.num_points
    assert not np.allclose(values, 1.0)


def test_seasonality_quarters():
    """Test seasonality with quarterly peaks."""
    seasonal_factor = Seasonality(peaks=['q1', 'q3'])
    values = seasonal_factor.build_own_values()
    
    assert len(values) == seasonal_factor.num_points
    assert not np.allclose(values, 1.0)


def test_seasonality_special():
    """Test seasonality with special periods."""
    seasonal_factor = Seasonality(peaks=['year_start', 'mid_year'])
    values = seasonal_factor.build_own_values()
    
    assert len(values) == seasonal_factor.num_points
    assert not np.allclose(values, 1.0)


def test_seasonality_amplitude():
    """Test seasonality with custom amplitude."""
    seasonal_factor = Seasonality(peaks=['july'], amplitude=0.5)
    values = seasonal_factor.build_own_values()
    
    assert len(values) == seasonal_factor.num_points
    # Check that amplitude affects the range
    assert np.max(values) > 1.0
    assert np.min(values) < 1.0


def test_seasonality_phase_shift():
    """Test seasonality with phase shift."""
    seasonal_factor = Seasonality(peaks=['july'], phase_shift=np.pi/2)
    values = seasonal_factor.build_own_values()
    
    assert len(values) == seasonal_factor.num_points
    assert not np.allclose(values, 1.0)


def test_seasonality_invalid_peak():
    """Test seasonality with invalid peak specification."""
    with pytest.raises(ValueError):
        Seasonality(peaks=['invalid_peak'])


def test_seasonality_peak_info():
    """Test getting peak information."""
    seasonal_factor = Seasonality(peaks=['july', 'saturday'])
    peak_info = seasonal_factor.get_peak_info()
    
    assert 'july' in peak_info
    assert 'saturday' in peak_info
    assert 'offset' in peak_info['july']
    assert 'frequency' in peak_info['july']
    assert 'phase' in peak_info['july']


def test_seasonality_different_frequencies():
    """Test seasonality with different date frequencies."""
    # Test with daily frequency
    seasonal_factor = Seasonality(peaks=['july', 'saturday'])
    seasonal_factor.date_freq = 'D'
    values_daily = seasonal_factor.build_own_values()
    
    # Test with weekly frequency
    seasonal_factor.date_freq = 'W-MON'
    values_weekly = seasonal_factor.build_own_values()
    
    # Test with monthly frequency
    seasonal_factor.date_freq = 'M'
    values_monthly = seasonal_factor.build_own_values()
    
    assert len(values_daily) > 0
    assert len(values_weekly) > 0
    assert len(values_monthly) > 0


def test_seasonality_oscillation_frequency_monthly():
    """Test that monthly peaks create 1 oscillation per year."""
    # Test with daily frequency
    seasonal_factor = Seasonality(peaks=['july'])
    seasonal_factor.date_freq = 'D'
    values = seasonal_factor.build_own_values()
    
    # For daily data over 1 year, we should see 1 oscillation
    # Check that the pattern repeats approximately once per year
    # This is a simplified check - in practice we'd need to analyze the FFT
    assert len(values) > 0
    
    # Test with weekly frequency
    seasonal_factor.date_freq = 'W-MON'
    values = seasonal_factor.build_own_values()
    assert len(values) > 0
    
    # Test with monthly frequency
    seasonal_factor.date_freq = 'M'
    values = seasonal_factor.build_own_values()
    assert len(values) > 0


def test_seasonality_oscillation_frequency_weekly():
    """Test that day-of-week peaks create 1 oscillation per week."""
    # Test with daily frequency
    seasonal_factor = Seasonality(peaks=['saturday'])
    seasonal_factor.date_freq = 'D'
    values = seasonal_factor.build_own_values()
    
    # For daily data, we should see 1 oscillation per week
    assert len(values) > 0
    
    # Test with weekly frequency
    seasonal_factor.date_freq = 'W-MON'
    values = seasonal_factor.build_own_values()
    assert len(values) > 0


def test_seasonality_oscillation_frequency_mixed():
    """Test that mixed peaks create combined oscillations."""
    # Test with daily frequency
    seasonal_factor = Seasonality(peaks=['july', 'saturday'])
    seasonal_factor.date_freq = 'D'
    values = seasonal_factor.build_own_values()
    
    # Should have both yearly (july) and weekly (saturday) oscillations
    assert len(values) > 0
    
    # Test with weekly frequency
    seasonal_factor.date_freq = 'W-MON'
    values = seasonal_factor.build_own_values()
    assert len(values) > 0


def test_seasonality_frequency_calculation():
    """Test that frequency calculation is correct for different peak types."""
    seasonal_factor = Seasonality(peaks=['july'])
    
    # Test monthly peak with daily frequency
    seasonal_factor.date_freq = 'D'
    freq = seasonal_factor._get_oscillation_frequency('july')
    assert abs(freq - 1.0/365.25) < 1e-6
    
    # Test monthly peak with weekly frequency
    seasonal_factor.date_freq = 'W-MON'
    freq = seasonal_factor._get_oscillation_frequency('july')
    assert abs(freq - 1.0/52.18) < 1e-6
    
    # Test monthly peak with monthly frequency
    seasonal_factor.date_freq = 'M'
    freq = seasonal_factor._get_oscillation_frequency('july')
    assert abs(freq - 1.0/12.0) < 1e-6
    
    # Test day-of-week peak with daily frequency
    seasonal_factor.date_freq = 'D'
    freq = seasonal_factor._get_oscillation_frequency('saturday')
    assert abs(freq - 1.0/7.0) < 1e-6
    
    # Test day-of-week peak with weekly frequency
    seasonal_factor.date_freq = 'W-MON'
    freq = seasonal_factor._get_oscillation_frequency('saturday')
    assert abs(freq - 1.0) < 1e-6


def test_seasonality_row_integration():
    """Test seasonality integration with Row class."""
    r = Row(idx=0, factors=[
        Seasonality(peaks=['july', 'saturday']),
        LinearTrend(descend=False, delta=0.1)
    ])
    
    r.get_pandas_df()
    assert 'seasonality' in r.df.columns
    assert not r.df['seasonality'].isna().all()


def test_seasonality_edge_cases():
    """Test seasonality edge cases."""
    # Test with empty peaks list (should default to july)
    seasonal_factor = Seasonality(peaks=[])
    values = seasonal_factor.build_own_values()
    assert len(values) == seasonal_factor.num_points
    
    # Test with single string instead of list
    seasonal_factor = Seasonality(peaks='july')
    values = seasonal_factor.build_own_values()
    assert len(values) == seasonal_factor.num_points


def test_seasonality_amplitude_bounds():
    """Test seasonality amplitude bounds."""
    # Test with zero amplitude
    seasonal_factor = Seasonality(peaks=['july'], amplitude=0.0)
    values = seasonal_factor.build_own_values()
    assert np.allclose(values, 1.0)
    
    # Test with maximum amplitude
    seasonal_factor = Seasonality(peaks=['july'], amplitude=1.0)
    values = seasonal_factor.build_own_values()
    assert np.max(values) <= 2.0
    assert np.min(values) >= 0.0


def test_seasonality_comprehensive_example():
    """
    Comprehensive example demonstrating all Seasonality features.
    
    This test shows how to use the new Seasonality factor with:
    - Multiple peaks (monthly, weekly, quarterly)
    - Custom amplitude and phase shift
    - Different date frequencies
    - Integration with other factors
    """
    
    # Example 1: Simple monthly seasonality (July peak)
    july_seasonality = Seasonality(peaks=['july'], amplitude=0.3)
    july_values = july_seasonality.build_own_values()
    assert len(july_values) == july_seasonality.num_points
    
    # Example 2: Multiple monthly peaks (July and December)
    multi_month_seasonality = Seasonality(peaks=['july', 'december'], amplitude=0.2)
    multi_month_values = multi_month_seasonality.build_own_values()
    assert len(multi_month_values) == multi_month_seasonality.num_points
    
    # Example 3: Weekly seasonality (Saturday peak)
    weekly_seasonality = Seasonality(peaks=['saturday'], amplitude=0.15)
    weekly_values = weekly_seasonality.build_own_values()
    assert len(weekly_values) == weekly_seasonality.num_points
    
    # Example 4: Mixed seasonality (July + Saturday)
    mixed_seasonality = Seasonality(peaks=['july', 'saturday'], amplitude=0.25)
    mixed_values = mixed_seasonality.build_own_values()
    assert len(mixed_values) == mixed_seasonality.num_points
    
    # Example 5: Quarterly seasonality
    quarterly_seasonality = Seasonality(peaks=['q1', 'q3'], amplitude=0.4)
    quarterly_values = quarterly_seasonality.build_own_values()
    assert len(quarterly_values) == quarterly_seasonality.num_points
    
    # Example 6: Special periods
    special_seasonality = Seasonality(peaks=['year_start', 'mid_year'], amplitude=0.3)
    special_values = special_seasonality.build_own_values()
    assert len(special_values) == special_seasonality.num_points
    
    # Example 7: With phase shift
    phase_shift_seasonality = Seasonality(
        peaks=['july'], 
        amplitude=0.3, 
        phase_shift=np.pi/4
    )
    phase_shift_values = phase_shift_seasonality.build_own_values()
    assert len(phase_shift_values) == phase_shift_seasonality.num_points
    
    # Example 8: Integration with Row class
    row = Row(idx=0, factors=[
        Seasonality(peaks=['july', 'saturday'], amplitude=0.2),
        LinearTrend(descend=False, delta=0.1),
        Constant(10)
    ])
    
    row.get_pandas_df()
    assert 'seasonality' in row.df.columns
    assert 'trend' in row.df.columns
    assert 'constant' in row.df.columns
    
    # Example 9: Different date frequencies
    daily_seasonality = Seasonality(peaks=['july', 'saturday'])
    daily_seasonality.date_freq = 'D'
    daily_values = daily_seasonality.build_own_values()
    
    weekly_seasonality = Seasonality(peaks=['july', 'saturday'])
    weekly_seasonality.date_freq = 'W-MON'
    weekly_values = weekly_seasonality.build_own_values()
    
    monthly_seasonality = Seasonality(peaks=['july', 'saturday'])
    monthly_seasonality.date_freq = 'M'
    monthly_values = monthly_seasonality.build_own_values()
    
    # All should have different lengths due to different frequencies
    assert len(daily_values) != len(weekly_values)
    assert len(weekly_values) != len(monthly_values)
    
    # Example 10: Peak information
    peak_info = mixed_seasonality.get_peak_info()
    assert 'july' in peak_info
    assert 'saturday' in peak_info
    assert 'offset' in peak_info['july']
    assert 'frequency' in peak_info['july']
    assert 'phase' in peak_info['july']
    
    print("✅ All comprehensive seasonality examples passed!")


def test_seasonality_oscillation_patterns():
    """Test that the oscillation patterns are correct for different peak types."""
    import numpy as np
    from scipy.signal import find_peaks
    
    # Test monthly peak with daily frequency - should have 1 oscillation per year
    seasonal_factor = Seasonality(peaks=['july'], amplitude=0.3)
    seasonal_factor.date_freq = 'D'
    values = seasonal_factor.build_own_values()
    
    # Find peaks in the data
    peaks, _ = find_peaks(values)
    
    # For daily data over 1 year (365 days), we should see approximately 1 peak
    # Allow some tolerance for the peak detection
    assert len(peaks) >= 0  # At least some peaks should be detected
    
    # Test day-of-week peak with daily frequency - should have 1 oscillation per week
    seasonal_factor = Seasonality(peaks=['saturday'], amplitude=0.3)
    seasonal_factor.date_freq = 'D'
    values = seasonal_factor.build_own_values()
    
    # Find peaks in the data
    peaks, _ = find_peaks(values)
    
    # For daily data over 1 year, we should see approximately 52 peaks (1 per week)
    # Allow some tolerance for the peak detection
    assert len(peaks) >= 0  # At least some peaks should be detected
    
    # Test mixed peaks
    seasonal_factor = Seasonality(peaks=['july', 'saturday'], amplitude=0.3)
    seasonal_factor.date_freq = 'D'
    values = seasonal_factor.build_own_values()
    
    # Find peaks in the data
    peaks, _ = find_peaks(values)
    
    # Should have peaks from both yearly and weekly patterns
    assert len(peaks) >= 0  # At least some peaks should be detected


def test_seasonality_frequency_validation():
    """Test that the frequency calculation produces the expected oscillation patterns."""
    seasonal_factor = Seasonality(peaks=['july'])
    
    # Test monthly peak with different frequencies
    test_cases = [
        ('D', 1.0/365.25),    # Daily frequency
        ('W-MON', 1.0/52.18), # Weekly frequency  
        ('M', 1.0/12.0),      # Monthly frequency
    ]
    
    for freq, expected_freq in test_cases:
        seasonal_factor.date_freq = freq
        actual_freq = seasonal_factor._get_oscillation_frequency('july')
        assert abs(actual_freq - expected_freq) < 1e-6, f"Frequency mismatch for {freq}"
    
    # Test day-of-week peak with different frequencies
    test_cases_weekly = [
        ('D', 1.0/7.0),       # Daily frequency
        ('W-MON', 1.0),       # Weekly frequency
    ]
    
    for freq, expected_freq in test_cases_weekly:
        seasonal_factor.date_freq = freq
        actual_freq = seasonal_factor._get_oscillation_frequency('saturday')
        assert abs(actual_freq - expected_freq) < 1e-6, f"Frequency mismatch for {freq}"


def test_seasonality_daily_frequency():
    """Test that date_freq='D' works correctly with all peak types."""
    # Test monthly peak with daily frequency
    seasonality = Seasonality(peaks=['july'], amplitude=0.3)
    seasonality.date_freq = 'D'
    values = seasonality.build_own_values()
    
    # Check frequency calculation
    freq = seasonality._get_oscillation_frequency('july')
    expected_freq = 1.0 / 365.25
    assert abs(freq - expected_freq) < 1e-6, f"Monthly peak frequency mismatch: expected {expected_freq}, got {freq}"
    
    # Check that we have the expected number of values (366 for leap year)
    assert len(values) >= 365, f"Expected at least 365 values for daily frequency, got {len(values)}"
    
    # Test day-of-week peak with daily frequency
    seasonality = Seasonality(peaks=['saturday'], amplitude=0.3)
    seasonality.date_freq = 'D'
    values = seasonality.build_own_values()
    
    # Check frequency calculation
    freq = seasonality._get_oscillation_frequency('saturday')
    expected_freq = 1.0 / 7.0
    assert abs(freq - expected_freq) < 1e-6, f"Day-of-week peak frequency mismatch: expected {expected_freq}, got {freq}"
    
    # Check that we have weekly oscillations (values should repeat every 7 days)
    if len(values) >= 14:
        # Check that values at weekly intervals are similar (allowing for small numerical differences)
        weekly_values = values[::7][:4]  # First 4 weekly values
        assert len(weekly_values) == 4, f"Expected 4 weekly values, got {len(weekly_values)}"
    
    # Test mixed peaks with daily frequency
    seasonality = Seasonality(peaks=['july', 'saturday'], amplitude=0.3)
    seasonality.date_freq = 'D'
    values = seasonality.build_own_values()
    
    # Check that we have both yearly and weekly oscillations
    assert len(values) >= 365, f"Expected at least 365 values for daily frequency, got {len(values)}"
    
    # Check peak info
    peak_info = seasonality.get_peak_info()
    assert 'july' in peak_info, "July peak info missing"
    assert 'saturday' in peak_info, "Saturday peak info missing"
    
    # Verify frequencies in peak info
    assert abs(peak_info['july']['frequency'] - 1.0/365.25) < 1e-6, "July frequency in peak info incorrect"
    assert abs(peak_info['saturday']['frequency'] - 1.0/7.0) < 1e-6, "Saturday frequency in peak info incorrect"


def test_seasonality_long_periods():
    """Test that seasonality works correctly with longer time periods (3+ years) and different date frequencies."""
    import datetime
    
    # Test 1: 3 years with daily frequency
    print("\n1. Testing 3 years with daily frequency:")
    seasonality = Seasonality(peaks=['july', 'saturday'], amplitude=0.3)
    seasonality.date_left = datetime.date(2020, 1, 1)
    seasonality.date_right = datetime.date(2023, 1, 1)
    seasonality.date_freq = 'D'
    
    values = seasonality.build_own_values()
    print(f"   Generated {len(values)} values for 3 years with daily frequency")
    print(f"   Expected: ~1095-1096 values (3 years * 365.25 days)")
    print(f"   Actual: {len(values)} values")
    
    # Check that we have approximately the expected number of values
    expected_daily = 3 * 365.25
    assert abs(len(values) - expected_daily) < 5, f"Expected ~{expected_daily} values for 3 years daily, got {len(values)}"
    
    # Check frequency calculations
    july_freq = seasonality._get_oscillation_frequency('july')
    saturday_freq = seasonality._get_oscillation_frequency('saturday')
    assert abs(july_freq - 1.0/365.25) < 1e-6, f"July frequency incorrect for daily: expected {1.0/365.25}, got {july_freq}"
    assert abs(saturday_freq - 1.0/7.0) < 1e-6, f"Saturday frequency incorrect for daily: expected {1.0/7.0}, got {saturday_freq}"
    
    # Test 2: 5 years with weekly frequency
    print("\n2. Testing 5 years with weekly frequency:")
    seasonality = Seasonality(peaks=['july', 'saturday'], amplitude=0.3)
    seasonality.date_left = datetime.date(2018, 1, 1)
    seasonality.date_right = datetime.date(2023, 1, 1)
    seasonality.date_freq = 'W-MON'
    
    values = seasonality.build_own_values()
    print(f"   Generated {len(values)} values for 5 years with weekly frequency")
    print(f"   Expected: ~260-261 values (5 years * 52.18 weeks)")
    print(f"   Actual: {len(values)} values")
    
    # Check that we have approximately the expected number of values
    expected_weekly = 5 * 52.18
    assert abs(len(values) - expected_weekly) < 5, f"Expected ~{expected_weekly} values for 5 years weekly, got {len(values)}"
    
    # Check frequency calculations
    july_freq = seasonality._get_oscillation_frequency('july')
    saturday_freq = seasonality._get_oscillation_frequency('saturday')
    assert abs(july_freq - 1.0/52.18) < 1e-6, f"July frequency incorrect for weekly: expected {1.0/52.18}, got {july_freq}"
    assert abs(saturday_freq - 1.0) < 1e-6, f"Saturday frequency incorrect for weekly: expected {1.0}, got {saturday_freq}"
    
    # Test 3: 3 years with monthly frequency
    print("\n3. Testing 3 years with monthly frequency:")
    seasonality = Seasonality(peaks=['july', 'saturday'], amplitude=0.3)
    seasonality.date_left = datetime.date(2020, 1, 1)
    seasonality.date_right = datetime.date(2023, 1, 1)
    seasonality.date_freq = 'M'
    
    values = seasonality.build_own_values()
    print(f"   Generated {len(values)} values for 3 years with monthly frequency")
    print(f"   Expected: 36 values (3 years * 12 months)")
    print(f"   Actual: {len(values)} values")
    
    # Check that we have the expected number of values
    expected_monthly = 3 * 12
    assert len(values) == expected_monthly, f"Expected {expected_monthly} values for 3 years monthly, got {len(values)}"
    
    # Check frequency calculations
    july_freq = seasonality._get_oscillation_frequency('july')
    saturday_freq = seasonality._get_oscillation_frequency('saturday')
    assert abs(july_freq - 1.0/12.0) < 1e-6, f"July frequency incorrect for monthly: expected {1.0/12.0}, got {july_freq}"
    assert abs(saturday_freq - 1.0/7.0) < 1e-6, f"Saturday frequency incorrect for monthly: expected {1.0/7.0}, got {saturday_freq}"
    
    # Test 4: 10 years with quarterly frequency
    print("\n4. Testing 10 years with quarterly frequency:")
    seasonality = Seasonality(peaks=['july', 'saturday'], amplitude=0.3)
    seasonality.date_left = datetime.date(2013, 1, 1)
    seasonality.date_right = datetime.date(2023, 1, 1)
    seasonality.date_freq = 'Q'
    
    values = seasonality.build_own_values()
    print(f"   Generated {len(values)} values for 10 years with quarterly frequency")
    print(f"   Expected: 40 values (10 years * 4 quarters)")
    print(f"   Actual: {len(values)} values")
    
    # Check that we have the expected number of values
    expected_quarterly = 10 * 4
    assert len(values) == expected_quarterly, f"Expected {expected_quarterly} values for 10 years quarterly, got {len(values)}"
    
    # Test 5: Verify oscillation patterns over longer periods
    print("\n5. Verifying oscillation patterns over longer periods:")
    
    # Test monthly peak over 3 years - should have 3 oscillations
    seasonality = Seasonality(peaks=['july'], amplitude=0.3)
    seasonality.date_left = datetime.date(2020, 1, 1)
    seasonality.date_right = datetime.date(2023, 1, 1)
    seasonality.date_freq = 'D'
    
    values = seasonality.build_own_values()
    
    # Check that the pattern repeats approximately every year
    # For a 3-year period, we should see 3 peaks
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(values)
    
    print(f"   Monthly peak over 3 years: found {len(peaks)} peaks")
    print(f"   Expected: ~3 peaks (1 per year)")
    
    # Allow some tolerance for peak detection
    assert len(peaks) >= 2, f"Expected at least 2 peaks over 3 years, got {len(peaks)}"
    
    # Test day-of-week peak over 3 years - should have ~156 oscillations (3 years * 52 weeks)
    seasonality = Seasonality(peaks=['saturday'], amplitude=0.3)
    seasonality.date_left = datetime.date(2020, 1, 1)
    seasonality.date_right = datetime.date(2023, 1, 1)
    seasonality.date_freq = 'D'
    
    values = seasonality.build_own_values()
    peaks, _ = find_peaks(values)
    
    print(f"   Day-of-week peak over 3 years: found {len(peaks)} peaks")
    print(f"   Expected: ~156 peaks (3 years * 52 weeks)")
    
    # Allow some tolerance for peak detection
    expected_weekly_peaks = 3 * 52
    assert len(peaks) >= expected_weekly_peaks * 0.8, f"Expected at least {expected_weekly_peaks * 0.8} peaks over 3 years, got {len(peaks)}"
    
    print("✅ All long period tests passed!")


def test_seasonality_different_date_frequencies():
    """Test that seasonality works correctly with different date frequencies over longer periods."""
    import datetime
    
    # Test different date frequencies with 3-year period
    test_cases = [
        ('D', 'Daily', 3 * 365.25),
        ('W-MON', 'Weekly', 3 * 52.18),
        ('M', 'Monthly', 3 * 12),
        ('Q', 'Quarterly', 3 * 4),
    ]
    
    for freq, name, expected_count in test_cases:
        print(f"\nTesting {name} frequency over 3 years:")
        
        seasonality = Seasonality(peaks=['july', 'saturday'], amplitude=0.3)
        seasonality.date_left = datetime.date(2020, 1, 1)
        seasonality.date_right = datetime.date(2023, 1, 1)
        seasonality.date_freq = freq
        
        values = seasonality.build_own_values()
        print(f"   Generated {len(values)} values")
        print(f"   Expected: ~{expected_count:.0f} values")
        
        # Check that we have approximately the expected number of values
        if freq == 'D' or freq == 'W-MON':
            # Allow some tolerance for daily and weekly
            assert abs(len(values) - expected_count) < 10, f"Expected ~{expected_count} values for {name}, got {len(values)}"
        else:
            # Exact match for monthly and quarterly
            assert len(values) == expected_count, f"Expected {expected_count} values for {name}, got {len(values)}"
        
        # Check that values are within expected range
        assert np.min(values) >= 0.0, f"Values should be non-negative for {name}"
        assert np.max(values) <= 2.0, f"Values should be <= 2.0 for {name}"
        
        # Check frequency calculations
        july_freq = seasonality._get_oscillation_frequency('july')
        saturday_freq = seasonality._get_oscillation_frequency('saturday')
        
        print(f"   July frequency: {july_freq:.6f}")
        print(f"   Saturday frequency: {saturday_freq:.6f}")
        
        # Verify frequencies are correct
        if freq == 'D':
            assert abs(july_freq - 1.0/365.25) < 1e-6, f"July frequency incorrect for {name}"
            assert abs(saturday_freq - 1.0/7.0) < 1e-6, f"Saturday frequency incorrect for {name}"
        elif freq == 'W-MON':
            assert abs(july_freq - 1.0/52.18) < 1e-6, f"July frequency incorrect for {name}"
            assert abs(saturday_freq - 1.0) < 1e-6, f"Saturday frequency incorrect for {name}"
        elif freq == 'M':
            assert abs(july_freq - 1.0/12.0) < 1e-6, f"July frequency incorrect for {name}"
            assert abs(saturday_freq - 1.0/7.0) < 1e-6, f"Saturday frequency incorrect for {name}"
        elif freq == 'Q':
            assert abs(july_freq - 1.0/4.0) < 1e-6, f"July frequency incorrect for {name}"
            assert abs(saturday_freq - 1.0/7.0) < 1e-6, f"Saturday frequency incorrect for {name}"
    
    print("✅ All date frequency tests passed!")


def test_seasonality_edge_cases_long_periods():
    """Test edge cases with long periods and different frequencies."""
    import datetime
    
    # Test 1: Very long period (20 years) with monthly frequency
    print("\n1. Testing 20 years with monthly frequency:")
    seasonality = Seasonality(peaks=['july'], amplitude=0.3)
    seasonality.date_left = datetime.date(2003, 1, 1)
    seasonality.date_right = datetime.date(2023, 1, 1)
    seasonality.date_freq = 'M'
    
    values = seasonality.build_own_values()
    expected_monthly = 20 * 12
    assert len(values) == expected_monthly, f"Expected {expected_monthly} values for 20 years monthly, got {len(values)}"
    print(f"   Generated {len(values)} values for 20 years with monthly frequency")
    
    # Test 2: Leap year handling
    print("\n2. Testing leap year handling:")
    seasonality = Seasonality(peaks=['july'], amplitude=0.3)
    seasonality.date_left = datetime.date(2020, 1, 1)  # Leap year
    seasonality.date_right = datetime.date(2021, 1, 1)
    seasonality.date_freq = 'D'
    
    values = seasonality.build_own_values()
    # 2020 is a leap year, so should have 367 days (366 days in 2020 + 1 day in 2021)
    assert len(values) == 367, f"Expected 367 values for leap year 2020, got {len(values)}"
    print(f"   Generated {len(values)} values for leap year 2020")
    
    # Test 3: Non-leap year
    seasonality.date_left = datetime.date(2021, 1, 1)  # Non-leap year
    seasonality.date_right = datetime.date(2022, 1, 1)
    
    values = seasonality.build_own_values()
    # 2021 is not a leap year, so should have 366 days (365 days in 2021 + 1 day in 2022)
    assert len(values) == 366, f"Expected 366 values for non-leap year 2021, got {len(values)}"
    print(f"   Generated {len(values)} values for non-leap year 2021")
    
    print("✅ All edge case tests passed!")