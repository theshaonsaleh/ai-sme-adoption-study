"""
Process and analyse ONS BICS data on AI adoption in UK SMEs.

This script:
1. Extracts AI adoption data from BICS waves
2. Cleans and structures the data
3. Produces analysis-ready datasets
4. Calculates key statistics

Data licensed under the Open Government Licence v3.0.
Source: ONS Business Insights and Conditions Survey
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple
import json
import warnings
warnings.filterwarnings('ignore')


def parse_ai_sheet(df: pd.DataFrame, skip_rows: int = 4) -> pd.DataFrame:
    """
    Parse an AI data sheet from BICS with proper headers.
    
    Args:
        df: Raw DataFrame from Excel
        skip_rows: Number of metadata rows to skip
        
    Returns:
        Cleaned DataFrame with proper column names
    """
    # Use row after skipping as column names
    new_df = df.iloc[skip_rows:].copy()
    new_df.columns = df.iloc[skip_rows - 1].fillna('Unknown')
    new_df = new_df.reset_index(drop=True)
    
    # Remove any remaining metadata rows
    new_df = new_df[new_df.iloc[:, 0].notna()]
    
    return new_df


def extract_current_ai_use_by_size(filepath: Path) -> pd.DataFrame:
    """
    Extract current AI usage rates by firm size from BICS Wave 105.
    
    Returns DataFrame with columns: size_band, technology, adoption_rate
    """
    # Read the weighted time series sheet
    df = pd.read_excel(filepath, sheet_name='Artificial Intel TS (WTD) (1)', header=None)
    
    # Column 2 contains Industry/Size Band labels
    # Row 5 onwards contains data
    # Technology columns start from column 3 onwards
    
    # Get column headers from row 5
    tech_columns = df.iloc[5, 3:].values
    
    data_rows = []
    
    # Process data rows (starting from row 6)
    for idx in range(6, len(df)):
        category = df.iloc[idx, 2]  # Industry/Size band is in column 2
        
        if pd.isna(category) or category == '':
            continue
        
        # Process each technology column
        for col_idx, tech in enumerate(tech_columns, start=3):
            if pd.isna(tech) or tech == '':
                continue
                
            value = df.iloc[idx, col_idx]
            
            if pd.notna(value) and value != '[c]' and value != '':
                try:
                    rate = float(value)
                    data_rows.append({
                        'category': category,
                        'technology': tech,
                        'adoption_rate': rate
                    })
                except (ValueError, TypeError):
                    pass
    
    return pd.DataFrame(data_rows)


def extract_ai_purposes(filepath: Path) -> pd.DataFrame:
    """
    Extract what businesses use AI for from BICS Wave 105.
    
    Returns DataFrame with columns: category, purpose, percentage
    """
    # Read the weighted time series sheet for AI purposes
    df = pd.read_excel(filepath, sheet_name='Artificial Intel TS (WTD) (2)', header=None)
    
    # Get column headers from row 5
    purpose_columns = df.iloc[5, 3:].values
    
    data_rows = []
    
    # Process data rows (starting from row 6)
    for idx in range(6, len(df)):
        category = df.iloc[idx, 2]  # Industry/Size band is in column 2
        
        if pd.isna(category) or category == '':
            continue
        
        # Process each purpose column
        for col_idx, purpose in enumerate(purpose_columns, start=3):
            if pd.isna(purpose) or purpose == '':
                continue
                
            value = df.iloc[idx, col_idx]
            
            if pd.notna(value) and value != '[c]' and value != '':
                try:
                    rate = float(value)
                    data_rows.append({
                        'category': category,
                        'purpose': purpose,
                        'percentage': rate
                    })
                except (ValueError, TypeError):
                    pass
    
    return pd.DataFrame(data_rows)


def extract_ai_adoption_methods(filepath: Path) -> pd.DataFrame:
    """
    Extract how businesses adopted AI technologies.
    
    Returns DataFrame with columns: category, method, percentage
    """
    df = pd.read_excel(filepath, sheet_name='Artificial Intel TS (WTD) (3)', header=None)
    
    # Get column headers from row 5
    method_columns = df.iloc[5, 3:].values
    
    data_rows = []
    
    # Process data rows (starting from row 6)
    for idx in range(6, len(df)):
        category = df.iloc[idx, 2]  # Industry/Size band is in column 2
        
        if pd.isna(category) or category == '':
            continue
        
        # Process each method column
        for col_idx, method in enumerate(method_columns, start=3):
            if pd.isna(method) or method == '':
                continue
                
            value = df.iloc[idx, col_idx]
            
            if pd.notna(value) and value != '[c]' and value != '':
                try:
                    rate = float(value)
                    data_rows.append({
                        'category': category,
                        'method': method,
                        'percentage': rate
                    })
                except (ValueError, TypeError):
                    pass
    
    return pd.DataFrame(data_rows)


def extract_planned_ai_adoption(filepath: Path) -> pd.DataFrame:
    """
    Extract planned AI adoption within next 3 months.
    
    Returns DataFrame with columns: category, technology, planned_rate
    """
    df = pd.read_excel(filepath, sheet_name='Artificial Intel TS (WTD) (4)', header=None)
    
    # Get column headers from row 5
    tech_columns = df.iloc[5, 3:].values
    
    data_rows = []
    
    # Process data rows (starting from row 6)
    for idx in range(6, len(df)):
        category = df.iloc[idx, 2]  # Industry/Size band is in column 2
        
        if pd.isna(category) or category == '':
            continue
        
        # Process each technology column
        for col_idx, tech in enumerate(tech_columns, start=3):
            if pd.isna(tech) or tech == '':
                continue
                
            value = df.iloc[idx, col_idx]
            
            if pd.notna(value) and value != '[c]' and value != '':
                try:
                    rate = float(value)
                    data_rows.append({
                        'category': category,
                        'technology': tech,
                        'planned_rate': rate
                    })
                except (ValueError, TypeError):
                    pass
    
    return pd.DataFrame(data_rows)


def extract_ai_barriers(filepath: Path) -> pd.DataFrame:
    """
    Extract barriers to AI adoption.
    
    Returns DataFrame with columns: category, barrier, percentage
    """
    df = pd.read_excel(filepath, sheet_name='Artificial Intel TS (WTD) (6)', header=None)
    
    # Get column headers from row 5
    barrier_columns = df.iloc[5, 3:].values
    
    data_rows = []
    
    # Process data rows (starting from row 6)
    for idx in range(6, len(df)):
        category = df.iloc[idx, 2]  # Industry/Size band is in column 2
        
        if pd.isna(category) or category == '':
            continue
        
        # Process each barrier column
        for col_idx, barrier in enumerate(barrier_columns, start=3):
            if pd.isna(barrier) or barrier == '':
                continue
                
            value = df.iloc[idx, col_idx]
            
            if pd.notna(value) and value != '[c]' and value != '':
                try:
                    rate = float(value)
                    data_rows.append({
                        'category': category,
                        'barrier': barrier,
                        'percentage': rate
                    })
                except (ValueError, TypeError):
                    pass
    
    return pd.DataFrame(data_rows)


def categorise_size_band(category: str) -> str:
    """Categorise firm size from category string."""
    category_str = str(category).strip()
    
    # Check in order from longest to shortest to avoid substring matches
    if '250 +' in category_str or '250+' in category_str:
        return 'Large (250+)'
    elif '100 - 249' in category_str or '100-249' in category_str:
        return 'Medium (50-249)'
    elif '50 - 99' in category_str or '50-99' in category_str:
        return 'Medium (50-249)'
    elif '10 - 49' in category_str or '10-49' in category_str:
        return 'Small (10-49)'
    elif '0 - 9' in category_str or '0-9' in category_str:
        return 'Micro (0-9)'
    elif 'All' in category_str or 'Total' in category_str:
        return 'All businesses'
    else:
        # Industries
        return 'Industry'


def calculate_summary_stats(df: pd.DataFrame) -> Dict:
    """Calculate summary statistics from processed data."""
    stats = {
        'mean': df['adoption_rate'].mean() if 'adoption_rate' in df.columns else None,
        'median': df['adoption_rate'].median() if 'adoption_rate' in df.columns else None,
        'std': df['adoption_rate'].std() if 'adoption_rate' in df.columns else None,
        'min': df['adoption_rate'].min() if 'adoption_rate' in df.columns else None,
        'max': df['adoption_rate'].max() if 'adoption_rate' in df.columns else None,
        'count': len(df)
    }
    return stats


def main():
    """Main processing pipeline."""
    project_root = Path(__file__).parent.parent
    raw_data_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("Processing ONS BICS AI adoption data")
    print("=" * 80)
    
    wave_105_path = raw_data_dir / "bics_wave_105_april_2024.xlsx"
    
    if not wave_105_path.exists():
        print(f"Error: {wave_105_path} not found")
        return 1
    
    # Extract all datasets
    print("\n1. Extracting current AI usage by size...")
    current_use = extract_current_ai_use_by_size(wave_105_path)
    current_use['size_band'] = current_use['category'].apply(categorise_size_band)
    print(f"   Extracted {len(current_use)} records")
    
    print("\n2. Extracting AI purposes...")
    purposes = extract_ai_purposes(wave_105_path)
    purposes['size_band'] = purposes['category'].apply(categorise_size_band)
    print(f"   Extracted {len(purposes)} records")
    
    print("\n3. Extracting AI adoption methods...")
    methods = extract_ai_adoption_methods(wave_105_path)
    methods['size_band'] = methods['category'].apply(categorise_size_band)
    print(f"   Extracted {len(methods)} records")
    
    print("\n4. Extracting planned AI adoption...")
    planned = extract_planned_ai_adoption(wave_105_path)
    planned['size_band'] = planned['category'].apply(categorise_size_band)
    print(f"   Extracted {len(planned)} records")
    
    print("\n5. Extracting AI barriers...")
    barriers = extract_ai_barriers(wave_105_path)
    barriers['size_band'] = barriers['category'].apply(categorise_size_band)
    print(f"   Extracted {len(barriers)} records")
    
    # Save processed datasets
    print("\n6. Saving processed datasets...")
    current_use.to_csv(processed_dir / "ai_current_use.csv", index=False)
    purposes.to_csv(processed_dir / "ai_purposes.csv", index=False)
    methods.to_csv(processed_dir / "ai_adoption_methods.csv", index=False)
    planned.to_csv(processed_dir / "ai_planned_adoption.csv", index=False)
    barriers.to_csv(processed_dir / "ai_barriers.csv", index=False)
    
    # Calculate and save summary statistics
    print("\n7. Calculating summary statistics...")
    stats = {
        'current_use': calculate_summary_stats(current_use),
        'planned': calculate_summary_stats(planned),
        'data_extracted_from': 'ONS BICS Wave 105 (March 2024)',
        'licence': 'Open Government Licence v3.0',
        'source_url': 'https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/businessinsightsandimpactontheukeconomy'
    }
    
    with open(processed_dir / "summary_stats.json", 'w') as f:
        json.dump(stats, f, indent=2)
    
    print("\n" + "=" * 80)
    print("Processing complete")
    print("=" * 80)
    print(f"\nFiles saved to: {processed_dir}")
    print("\nSummary:")
    print(f"  - Current AI use: {len(current_use)} records")
    print(f"  - AI purposes: {len(purposes)} records")
    print(f"  - Adoption methods: {len(methods)} records")
    print(f"  - Planned adoption: {len(planned)} records")
    print(f"  - Barriers: {len(barriers)} records")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
