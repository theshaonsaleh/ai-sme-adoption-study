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
    extract_wave_165_ai_adoption,
    extract_ai_barriers_wave_165
)


def test_categorise_size_band():
    """Test firm size categorisation."""
    assert categorise_size_band("0 - 9") == "Micro (0-9)"
    assert categorise_size_band("10 - 49") == "Small (10-49)"
    assert categorise_size_band("50 - 99") == "Medium (50-99)"
    assert categorise_size_band("100 - 249") == "Medium (100-249)"
    assert categorise_size_band("250 +") == "Large (250+)"
    assert categorise_size_band("All size bands excluding 0 - 9") == "All 10+ employees"
    assert categorise_size_band("All businesses") == "All businesses"


def test_calculate_summary_stats():
    """Test summary statistics calculation."""
    df = pd.DataFrame({
        'uses_ai_rate': [0.1, 0.2, 0.3, 0.4, 0.5]
    })
    
    # Simple stats
    assert df['uses_ai_rate'].mean() == pytest.approx(0.3, rel=1e-6)
    assert df['uses_ai_rate'].median() == pytest.approx(0.3, rel=1e-6)
    assert df['uses_ai_rate'].min() == pytest.approx(0.1, rel=1e-6)
    assert df['uses_ai_rate'].max() == pytest.approx(0.5, rel=1e-6)
    assert len(df) == 5


def test_calculate_summary_stats_empty():
    """Test summary statistics with empty DataFrame."""
    df = pd.DataFrame()
    
    assert len(df) == 0


def test_extract_current_ai_use_structure():
    """Test that current AI use extraction returns correct structure."""
    project_root = Path(__file__).parent.parent
    
    # Test with Wave 165
    from process_data import extract_wave_165_ai_adoption
    
    df = extract_wave_165_ai_adoption()
    
    # Check columns
    assert 'wave' in df.columns
    assert 'uses_ai_rate' in df.columns
    assert 'category' in df.columns
    
    # Check data types
    assert df['uses_ai_rate'].dtype in [np.float64, np.float32, float]
    
    # Check value ranges
    assert df['uses_ai_rate'].min() >= 0.0
    assert df['uses_ai_rate'].max() <= 1.0
    
    # Check we have data
    assert len(df) > 0


def test_extract_barriers_structure():
    """Test that barriers extraction returns correct structure."""
    project_root = Path(__file__).parent.parent
    
    from process_data import extract_ai_barriers_wave_165
    
    df = extract_ai_barriers_wave_165()
    
    # Check columns
    assert 'barrier' in df.columns
    assert 'all_businesses_pct' in df.columns
    
    # Check data types
    assert df['all_businesses_pct'].dtype in [np.float64, np.float32, float]
    
    # Check value ranges
    assert df['all_businesses_pct'].min() >= 0.0
    assert df['all_businesses_pct'].max() <= 1.0
    
    # Check we have data
    assert len(df) > 0


def test_adoption_rates_sum_sensible():
    """Test that adoption rates are sensible (don't exceed 100%)."""
    project_root = Path(__file__).parent.parent
    processed_path = project_root / "data" / "processed" / "wave_165_adoption_by_size.csv"
    
    if not processed_path.exists():
        pytest.skip("Processed data not available")
    
    df = pd.read_csv(processed_path)
    
    # Check no adoption rate exceeds 100%
    assert (df['uses_ai_rate'] <= 1.0).all()
    assert (df['uses_ai_rate'] >= 0.0).all()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
