"""
Download ONS Business Insights and Conditions Survey (BICS) data on AI adoption.

This script downloads publicly available data from the ONS on business use of AI
and related technologies. All data is licensed under the Open Government Licence v3.0.

Data sources:
- ONS Business Insights and Conditions Survey (BICS)
- ONS business demographics and characteristics
"""

import os
import sys
import requests
from datetime import datetime
from pathlib import Path
import pandas as pd


def download_file(url: str, output_path: Path, description: str = "") -> bool:
    """
    Download a file from a URL and save it to the output path.
    
    Args:
        url: URL to download from
        output_path: Path to save the file
        description: Description of the file being downloaded
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Downloading {description or url}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(response.content)
        
        print(f"✓ Downloaded to {output_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False


def create_metadata_file(data_dir: Path) -> None:
    """Create a metadata file documenting data sources and download date."""
    metadata = {
        "download_date": datetime.now().isoformat(),
        "sources": [
            {
                "name": "ONS Business Insights and Conditions Survey (BICS) - AI adoption",
                "url": "https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/datasets/businessinsightsandconditionssurvey",
                "description": "Survey data on business adoption of AI technologies",
                "licence": "Open Government Licence v3.0",
                "licence_url": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
            }
        ]
    }
    
    metadata_path = data_dir / "metadata.json"
    import json
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✓ Metadata saved to {metadata_path}")


def main():
    """Download all required datasets."""
    # Set up paths
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("Downloading ONS data on AI adoption in UK businesses")
    print("=" * 80)
    print(f"Download date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output directory: {data_dir}")
    print()
    
    # Note: ONS BICS data is typically published as Excel files with multiple sheets
    # The actual URLs need to point to specific published datasets
    # As of 2024-2026, BICS Wave data on AI is available but URLs change with releases
    
    # For this research project, we'll use the ONS API or direct links to published files
    # Example: BICS Wave data on business characteristics and technology use
    
    success_count = 0
    total_count = 0
    
    # Download ONS BICS data with AI questions
    # AI questions were introduced in Wave 92 (Sept 2023) and continued through recent waves
    # We'll download several key waves to track AI adoption trends
    datasets = [
        {
            "url": "https://www.ons.gov.uk/file?uri=/economy/economicoutputandproductivity/output/datasets/businessinsightsandimpactontheukeconomy/bicswave105/bicswave1052final.xlsx",
            "filename": "bics_wave_105_april_2024.xlsx",
            "description": "BICS Wave 105 (April 2024) - includes AI adoption data"
        },
        {
            "url": "https://www.ons.gov.uk/file?uri=/economy/economicoutputandproductivity/output/datasets/businessinsightsandimpactontheukeconomy/bicswave117/bicswave1172final.xlsx",
            "filename": "bics_wave_117_oct_2024.xlsx",
            "description": "BICS Wave 117 (October 2024) - includes AI adoption data"
        },
        {
            "url": "https://www.ons.gov.uk/file?uri=/economy/economicoutputandproductivity/output/adhocs/1953businessinsightsandconditionssurveybicswave105capitalexpenditureandartificialintelligenceadhoctables/beiswave105capitalexpenditureandartificialintelligence.xlsx",
            "filename": "bics_wave_105_ai_adhoc_tables.xlsx",
            "description": "BICS Wave 105 AI ad hoc tables (by sector and size)"
        }
    ]
    
    for dataset in datasets:
        total_count += 1
        output_path = data_dir / dataset["filename"]
        if download_file(dataset["url"], output_path, dataset["description"]):
            success_count += 1
    
    # Create metadata file
    create_metadata_file(data_dir)
    
    print()
    print("=" * 80)
    print(f"Download complete: {success_count}/{total_count} files downloaded successfully")
    print("=" * 80)
    
    if success_count < total_count:
        print("\nNote: Some downloads failed. This may be due to:")
        print("  - Changed URLs (ONS updates dataset locations)")
        print("  - Network connectivity issues")
        print("  - Files no longer available")
        print("\nPlease check the ONS website for the latest data:")
        print("https://www.ons.gov.uk/businessindustryandtrade/business/businessservices/datasets/businessinsightsandconditionssurvey")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
