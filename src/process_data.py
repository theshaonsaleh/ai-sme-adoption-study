"""
Process ONS BICS data on AI adoption - using proper weighted estimates.

This script extracts ONS's published weighted estimates for a single named wave,
avoiding pseudo-replication from pooling across rows or time points.

Data licensed under the Open Government Licence v3.0.
Source: ONS Business Insights and Conditions Survey
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import json
import warnings
warnings.filterwarnings('ignore')


def extract_wave_165_ai_adoption() -> pd.DataFrame:
    """
    Extract AI adoption rates from Wave 165 (Sept 2026) - most recent data.
    Uses ONS published weighted estimates for size bands directly.
    
    Returns DataFrame with: wave, date, size_band, uses_ai_rate
    """
    project_root = Path(__file__).parent.parent
    filepath = project_root / "data" / "raw" / "bics_wave_165_sept_2026.xlsx"
    
    df = pd.read_excel(filepath, sheet_name='AI Current Usage TS (WTD)', header=None)
    
    # Wave 165 data starts at row 6
    # Column 2 = Industry/Size Band
    # Column -1 = "Business does not currently use AI technologies"
    
    results = []
    
    # Extract size band rows for Wave 165
    for idx in range(6, 30):  # Wave 165 is in first block
        wave_str = df.iloc[idx, 1]
        if pd.isna(wave_str) or 'Wave 165' not in str(wave_str):
            break
            
        category = df.iloc[idx, 2]
        does_not_use = df.iloc[idx, -1]
        
        # Only extract size band rows
        if pd.notna(category) and any(x in str(category) for x in 
                                       ['0 - 9', '10 - 49', '50 - 99', 
                                        '100 - 249', '250', 'All']):
            if pd.notna(does_not_use) and does_not_use != '[c]':
                uses_ai = 1.0 - float(does_not_use)
                
                results.append({
                    'wave': 165,
                    'date': '21 September 2026 to 4 October 2026',
                    'category': str(category).strip(),
                    'does_not_use_ai': float(does_not_use),
                    'uses_ai_rate': uses_ai
                })
    
    return pd.DataFrame(results)


def extract_ai_adoption_trend() -> pd.DataFrame:
    """
    Extract AI adoption trend across multiple waves (165, 117, 105).
    
    Returns DataFrame with wave, date, size_band, uses_ai_rate for trend analysis.
    """
    project_root = Path(__file__).parent.parent
    
    all_data = []
    
    # Wave 165 (Sept 2026)
    filepath_165 = project_root / "data" / "raw" / "bics_wave_165_sept_2026.xlsx"
    df_165 = pd.read_excel(filepath_165, sheet_name='AI Current Usage TS (WTD)', header=None)
    
    for idx in range(6, 30):
        wave_str = df_165.iloc[idx, 1]
        if pd.isna(wave_str) or 'Wave 165' not in str(wave_str):
            break
        
        category = df_165.iloc[idx, 2]
        does_not_use = df_165.iloc[idx, -1]
        
        if pd.notna(category) and 'All businesses' in str(category):
            if pd.notna(does_not_use) and does_not_use != '[c]':
                all_data.append({
                    'wave': 165,
                    'date': 'Sept 2026',
                    'uses_ai_rate': 1.0 - float(does_not_use)
                })
                break
    
    # Wave 117 (Oct 2024) - extract from time series if available
    filepath_117 = project_root / "data" / "raw" / "bics_wave_117_oct_2024.xlsx"
    if filepath_117.exists():
        try:
            xls = pd.ExcelFile(filepath_117)
            ai_sheets = [s for s in xls.sheet_names if 'Artificial Intel TS' in s]
            if ai_sheets:
                df_117 = pd.read_excel(filepath_117, sheet_name=ai_sheets[0], header=None)
                
                for idx in range(6, 30):
                    category = df_117.iloc[idx, 2] if df_117.shape[1] > 2 else None
                    does_not_use = df_117.iloc[idx, -1]
                    
                    if pd.notna(category) and 'All' in str(category):
                        if pd.notna(does_not_use) and does_not_use != '[c]':
                            all_data.append({
                                'wave': 117,
                                'date': 'Oct 2024',
                                'uses_ai_rate': 1.0 - float(does_not_use)
                            })
                            break
        except Exception as e:
            print(f"Note: Could not extract Wave 117 trend data: {e}")
    
    # Wave 105 (April 2024)
    filepath_105 = project_root / "data" / "raw" / "bics_wave_105_april_2024.xlsx"
    if filepath_105.exists():
        try:
            xls = pd.ExcelFile(filepath_105)
            ai_sheets = [s for s in xls.sheet_names if 'Artificial Intel TS' in s]
            if ai_sheets:
                df_105 = pd.read_excel(filepath_105, sheet_name=ai_sheets[0], header=None)
                
                for idx in range(6, 30):
                    category = df_105.iloc[idx, 2] if df_105.shape[1] > 2 else None
                    does_not_use = df_105.iloc[idx, -1]
                    
                    if pd.notna(category) and 'All' in str(category):
                        if pd.notna(does_not_use) and does_not_use != '[c]':
                            all_data.append({
                                'wave': 105,
                                'date': 'April 2024',
                                'uses_ai_rate': 1.0 - float(does_not_use)
                            })
                            break
        except Exception as e:
            print(f"Note: Could not extract Wave 105 trend data: {e}")
    
    return pd.DataFrame(all_data)


def extract_ai_barriers_wave_165() -> pd.DataFrame:
    """
    Extract barriers to AI adoption from Wave 165.
    
    Returns DataFrame with: barrier, all_businesses_pct
    """
    project_root = Path(__file__).parent.parent
    filepath = project_root / "data" / "raw" / "bics_wave_165_sept_2026.xlsx"
    
    df = pd.read_excel(filepath, sheet_name='AI Prevent or Delayed TS (WTD)', header=None)
    
    # Get barrier column names from row 5
    barrier_cols = df.iloc[5, 3:].tolist()
    
    results = []
    
    # Extract "All businesses" row for Wave 165
    for idx in range(6, 30):
        wave_str = df.iloc[idx, 1]
        if pd.isna(wave_str) or 'Wave 165' not in str(wave_str):
            break
        
        category = df.iloc[idx, 2]
        
        if pd.notna(category) and 'All businesses' in str(category):
            # Extract barrier percentages
            for col_idx, barrier_name in enumerate(barrier_cols, start=3):
                if pd.notna(barrier_name) and barrier_name != '':
                    value = df.iloc[idx, col_idx]
                    if pd.notna(value) and value not in ['[c]', '[x]', '']:
                        try:
                            results.append({
                                'barrier': str(barrier_name),
                                'all_businesses_pct': float(value)
                            })
                        except (ValueError, TypeError):
                            pass
            break
    
    return pd.DataFrame(results)


def extract_ai_purposes_wave_165() -> pd.DataFrame:
    """
    Extract purposes for AI use from Wave 165.
    
    Returns DataFrame with: purpose, ai_adopters_pct
    (Note: base is businesses currently using AI, not all businesses)
    """
    project_root = Path(__file__).parent.parent
    filepath = project_root / "data" / "raw" / "bics_wave_165_sept_2026.xlsx"
    
    df = pd.read_excel(filepath, sheet_name='AI Current Purpose TS (WTD)', header=None)
    
    # Get purpose column names from row 5
    purpose_cols = df.iloc[5, 3:].tolist()
    
    results = []
    
    # Extract "All businesses" row for Wave 165
    for idx in range(6, 30):
        wave_str = df.iloc[idx, 1]
        if pd.isna(wave_str) or 'Wave 165' not in str(wave_str):
            break
        
        category = df.iloc[idx, 2]
        
        if pd.notna(category) and 'All businesses' in str(category):
            # Extract purpose percentages
            for col_idx, purpose_name in enumerate(purpose_cols, start=3):
                if pd.notna(purpose_name) and purpose_name != '':
                    value = df.iloc[idx, col_idx]
                    if pd.notna(value) and value not in ['[c]', '[x]', '']:
                        try:
                            results.append({
                                'purpose': str(purpose_name),
                                'ai_adopters_pct': float(value)
                            })
                        except (ValueError, TypeError):
                            pass
            break
    
    return pd.DataFrame(results)


def categorise_size_band(category: str) -> str:
    """Categorise firm size from category string."""
    category_str = str(category).strip()
    
    # Check in order from most specific to least specific
    if 'All size bands excluding' in category_str:
        return 'All 10+ employees'
    elif 'All businesses' in category_str:
        return 'All businesses'
    elif '250 +' in category_str or '250+' in category_str:
        return 'Large (250+)'
    elif '100 - 249' in category_str or '100-249' in category_str:
        return 'Medium (100-249)'
    elif '50 - 99' in category_str or '50-99' in category_str:
        return 'Medium (50-99)'
    elif '10 - 49' in category_str or '10-49' in category_str:
        return 'Small (10-49)'
    elif '0 - 9' in category_str:
        return 'Micro (0-9)'
    else:
        return 'Other'


def main():
    """Main processing pipeline - use Wave 165 weighted estimates."""
    project_root = Path(__file__).parent.parent
    processed_dir = project_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("Processing ONS BICS AI adoption data")
    print("Using Wave 165 (Sept 2026) weighted estimates")
    print("=" * 80)
    
    # Extract Wave 165 data
    print("\n1. Extracting Wave 165 AI adoption by size band...")
    adoption_w165 = extract_wave_165_ai_adoption()
    adoption_w165['size_band'] = adoption_w165['category'].apply(categorise_size_band)
    print(f"   Extracted {len(adoption_w165)} size bands")
    print("\n   Wave 165 AI adoption rates:")
    for _, row in adoption_w165.iterrows():
        if row['size_band'] != 'Other':
            print(f"     {row['size_band']:25s} {row['uses_ai_rate']:6.1%}")
    
    # Extract trend data
    print("\n2. Extracting AI adoption trend across waves...")
    trend = extract_ai_adoption_trend()
    print(f"   Extracted {len(trend)} time points")
    if len(trend) > 0:
        print("\n   Trend (All businesses):")
        for _, row in trend.iterrows():
            print(f"     Wave {row['wave']} ({row['date']:12s}): {row['uses_ai_rate']:6.1%}")
    
    # Extract barriers
    print("\n3. Extracting AI barriers (Wave 165)...")
    barriers = extract_ai_barriers_wave_165()
    print(f"   Extracted {len(barriers)} barriers")
    
    # Extract purposes
    print("\n4. Extracting AI purposes (Wave 165)...")
    purposes = extract_ai_purposes_wave_165()
    print(f"   Extracted {len(purposes)} purposes")
    
    # Save processed datasets
    print("\n5. Saving processed datasets...")
    adoption_w165.to_csv(processed_dir / "wave_165_adoption_by_size.csv", index=False)
    trend.to_csv(processed_dir / "adoption_trend.csv", index=False)
    barriers.to_csv(processed_dir / "wave_165_barriers.csv", index=False)
    purposes.to_csv(processed_dir / "wave_165_purposes.csv", index=False)
    
    # Save metadata
    metadata = {
        'primary_wave': 165,
        'primary_wave_date': '21 September 2026 to 4 October 2026',
        'data_source': 'ONS BICS Wave 165',
        'licence': 'Open Government Licence v3.0',
        'extraction_method': 'Direct extraction of published weighted estimates from named wave',
        'base_all_businesses': 'Adoption rates are % of all businesses',
        'base_ai_adopters': 'Purposes are % of businesses currently using AI',
        'note': 'No averaging across time points or mixed rows - single wave estimates only'
    }
    
    with open(processed_dir / "metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "=" * 80)
    print("Processing complete")
    print("=" * 80)
    print(f"\nFiles saved to: {processed_dir}")
    print(f"\nWave 165 summary:")
    print(f"  - All businesses: {adoption_w165[adoption_w165['size_band']=='All businesses']['uses_ai_rate'].iloc[0]:.1%} use AI")
    print(f"  - Businesses 10+ employees: {adoption_w165[adoption_w165['size_band']=='All 10+ employees']['uses_ai_rate'].iloc[0]:.1%} use AI")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
