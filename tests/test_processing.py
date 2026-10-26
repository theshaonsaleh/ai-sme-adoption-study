"""
Tests for data processing functions.

Run with: pytest tests/test_processing.py
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from process_data import (
    categorise_size_band,
    calculate_summary_stats,
    extract_current_ai_use_by_size,
    extract_ai_barriers
)


def test_categorise_size_band():
    """Test firm size categorisation."""
    assert categorise_size_band("0 - 9") == "Micro (0-9)"
    assert categorise_size_band("10 - 49") == "Small (10-49)"
    assert categorise_size_band("50 - 99") == "Medium (50-249)"
    assert categorise_size_band("100 - 249") == "Medium (50-249)"
    assert categorise_size_band("250 +") == "Large (250+)"
    assert categorise_size_band("Manufacturing") == "Industry"
    assert categorise_size_band("All") == "All businesses"


def test_calculate_summary_stats():
    """Test summary statistics calculation."""
    df = pd.DataFrame({
        'adoption_rate': [0.1, 0.2, 0.3, 0.4, 0.5]
    })
    
    stats = calculate_summary_stats(df)
    
    assert stats['mean'] == pytest.approx(0.3, rel=1e-6)
    assert stats['median'] == pytest.approx(0.3, rel=1e-6)
    assert stats['min'] == pytest.approx(0.1, rel=1e-6)
    assert stats['max'] == pytest.approx(0.5, rel=1e-6)
    assert stats['count'] == 5


def test_calculate_summary_stats_empty():
    """Test summary statistics with empty DataFrame."""
    df = pd.DataFrame()
    
    stats = calculate_summary_stats(df)
    
    assert stats['mean'] is None
    assert stats['count'] == 0


def test_extract_current_ai_use_structure():
    """Test that current AI use extraction returns correct structure."""
    project_root = Path(__file__).parent.parent
    wave_105_path = project_root / "data" / "raw" / "bics_wave_105_april_2024.xlsx"
    
    if not wave_105_path.exists():
        pytest.skip("Test data not available")
    
    df = extract_current_ai_use_by_size(wave_105_path)
    
    # Check columns
    assert 'category' in df.columns
    assert 'technology' in df.columns
    assert 'adoption_rate' in df.columns
    
    # Check data types
    assert df['adoption_rate'].dtype in [np.float64, np.float32, float]
    
    # Check value ranges
    assert df['adoption_rate'].min() >= 0.0
    assert df['adoption_rate'].max() <= 1.0
    
    # Check we have data
    assert len(df) > 0


def test_extract_barriers_structure():
    """Test that barriers extraction returns correct structure."""
    project_root = Path(__file__).parent.parent
    wave_105_path = project_root / "data" / "raw" / "bics_wave_105_april_2024.xlsx"
    
    if not wave_105_path.exists():
        pytest.skip("Test data not available")
    
    df = extract_ai_barriers(wave_105_path)
    
    # Check columns
    assert 'category' in df.columns
    assert 'barrier' in df.columns
    assert 'percentage' in df.columns
    
    # Check data types
    assert df['percentage'].dtype in [np.float64, np.float32, float]
    
    # Check value ranges
    assert df['percentage'].min() >= 0.0
    assert df['percentage'].max() <= 1.0
    
    # Check we have data
    assert len(df) > 0


def test_adoption_rates_sum_sensible():
    """Test that adoption rates are sensible (don't exceed 100%)."""
    project_root = Path(__file__).parent.parent
    processed_path = project_root / "data" / "processed" / "ai_current_use.csv"
    
    if not processed_path.exists():
        pytest.skip("Processed data not available")
    
    df = pd.read_csv(processed_path)
    
    # Check no adoption rate exceeds 100%
    assert (df['adoption_rate'] <= 1.0).all()
    assert (df['adoption_rate'] >= 0.0).all()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
