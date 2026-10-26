"""
Analyse AI adoption patterns in UK SMEs using ONS BICS data.

This script performs descriptive statistics and simple regression analysis
to identify drivers of AI adoption.

Data source: ONS Business Insights and Conditions Survey (BICS)
Licence: Open Government Licence v3.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import json

# Set plotting style
sns.set_style("whitegrid")
sns.set_palette("husl")


def load_processed_data(processed_dir: Path) -> dict:
    """Load all processed datasets."""
    return {
        'current_use': pd.read_csv(processed_dir / "ai_current_use.csv"),
        'purposes': pd.read_csv(processed_dir / "ai_purposes.csv"),
        'methods': pd.read_csv(processed_dir / "ai_adoption_methods.csv"),
        'planned': pd.read_csv(processed_dir / "ai_planned_adoption.csv"),
        'barriers': pd.read_csv(processed_dir / "ai_barriers.csv")
    }


def analyse_by_size(df: pd.DataFrame, rate_col: str = 'adoption_rate') -> pd.DataFrame:
    """
    Analyse AI adoption by firm size.
    
    Returns aggregated statistics by size band.
    """
    size_order = ['Micro (0-9)', 'Small (10-49)', 'Medium (50-249)', 
                  'Large (250+)', 'All businesses']
    
    # Filter for size band categories
    size_data = df[df['size_band'].isin(size_order)].copy()
    
    # Aggregate by size band
    agg_stats = size_data.groupby('size_band')[rate_col].agg([
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std'),
        ('count', 'count')
    ]).reset_index()
    
    # Order by size
    agg_stats['size_band'] = pd.Categorical(
        agg_stats['size_band'], 
        categories=size_order, 
        ordered=True
    )
    agg_stats = agg_stats.sort_values('size_band')
    
    return agg_stats


def plot_adoption_by_size(results_dir: Path):
    """
    Create visualisation of AI adoption by firm size.
    """
    processed_dir = results_dir.parent / "data" / "processed"
    current_use = pd.read_csv(processed_dir / "ai_current_use.csv")
    
    # Get aggregate stats
    size_stats = analyse_by_size(current_use)
    size_stats = size_stats[size_stats['size_band'] != 'All businesses']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar plot
    bars = ax.bar(range(len(size_stats)), size_stats['mean'], 
                   yerr=size_stats['std'], capsize=5, 
                   color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'])
    
    ax.set_xticks(range(len(size_stats)))
    ax.set_xticklabels(size_stats['size_band'], rotation=15, ha='right')
    ax.set_ylabel('Mean AI Adoption Rate', fontsize=12)
    ax.set_xlabel('Firm Size', fontsize=12)
    ax.set_title('AI Adoption by Firm Size\n(ONS BICS Wave 105, March 2024)', 
                 fontsize=14, fontweight='bold')
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, size_stats['mean'])):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1%}',
                ha='center', va='bottom', fontsize=10)
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    plt.tight_layout()
    
    output_path = results_dir / "figures" / "adoption_by_size.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()
    
    return size_stats


def plot_ai_purposes(results_dir: Path):
    """
    Create visualisation of what businesses use AI for.
    """
    processed_dir = results_dir.parent / "data" / "processed"
    purposes = pd.read_csv(processed_dir / "ai_purposes.csv")
    
    # Aggregate by purpose (across all categories)
    purpose_agg = purposes.groupby('purpose')['percentage'].mean().sort_values(ascending=True)
    
    # Take top purposes
    top_purposes = purpose_agg.tail(8)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.barh(range(len(top_purposes)), top_purposes.values, 
                    color='#3498db')
    
    ax.set_yticks(range(len(top_purposes)))
    ax.set_yticklabels([p[:50] for p in top_purposes.index], fontsize=10)
    ax.set_xlabel('Mean Percentage of AI-Using Businesses', fontsize=12)
    ax.set_title('What Do Businesses Use AI For?\n(ONS BICS Wave 105, March 2024)', 
                 fontsize=14, fontweight='bold')
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, top_purposes.values)):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f' {val:.1%}',
                va='center', fontsize=9)
    
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
    plt.tight_layout()
    
    output_path = results_dir / "figures" / "ai_purposes.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()
    
    return top_purposes


def plot_barriers(results_dir: Path):
    """
    Create visualisation of barriers to AI adoption.
    """
    processed_dir = results_dir.parent / "data" / "processed"
    barriers = pd.read_csv(processed_dir / "ai_barriers.csv")
    
    # Aggregate by barrier
    barrier_agg = barriers.groupby('barrier')['percentage'].mean().sort_values(ascending=True)
    
    # Take top barriers
    top_barriers = barrier_agg.tail(8)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.barh(range(len(top_barriers)), top_barriers.values, 
                    color='#e74c3c')
    
    ax.set_yticks(range(len(top_barriers)))
    # Shorten long labels
    labels = []
    for label in top_barriers.index:
        if len(label) > 50:
            labels.append(label[:47] + '...')
        else:
            labels.append(label)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel('Mean Percentage Reporting Barrier', fontsize=12)
    ax.set_title('Top Barriers to AI Adoption\n(ONS BICS Wave 105, March 2024)', 
                 fontsize=14, fontweight='bold')
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, top_barriers.values)):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f' {val:.1%}',
                va='center', fontsize=9)
    
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
    plt.tight_layout()
    
    output_path = results_dir / "figures" / "barriers.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()
    
    return top_barriers


def perform_size_correlation_test(current_use: pd.DataFrame) -> dict:
    """
    Test correlation between firm size and AI adoption.
    
    Returns correlation coefficient and p-value.
    """
    size_order = ['Micro (0-9)', 'Small (10-49)', 'Medium (50-249)', 'Large (250+)']
    
    # Filter and encode size as numeric
    size_data = current_use[current_use['size_band'].isin(size_order)].copy()
    size_data['size_numeric'] = size_data['size_band'].map({
        'Micro (0-9)': 1,
        'Small (10-49)': 2,
        'Medium (50-249)': 3,
        'Large (250+)': 4
    })
    
    # Calculate correlation
    corr, p_value = stats.spearmanr(size_data['size_numeric'], 
                                     size_data['adoption_rate'])
    
    return {
        'correlation': corr,
        'p_value': p_value,
        'interpretation': 'significant' if p_value < 0.05 else 'not significant'
    }


def generate_results_summary(data: dict, results_dir: Path) -> dict:
    """
    Generate summary of key findings.
    """
    summary = {
        'data_source': 'ONS BICS Wave 105 (18-31 March 2024)',
        'licence': 'Open Government Licence v3.0',
        'key_findings': {}
    }
    
    # Size analysis
    size_stats = analyse_by_size(data['current_use'])
    size_stats_clean = size_stats[size_stats['size_band'] != 'All businesses']
    
    summary['key_findings']['by_size'] = {
        'micro_mean': float(size_stats_clean[size_stats_clean['size_band'] == 'Micro (0-9)']['mean'].iloc[0]),
        'small_mean': float(size_stats_clean[size_stats_clean['size_band'] == 'Small (10-49)']['mean'].iloc[0]),
        'medium_mean': float(size_stats_clean[size_stats_clean['size_band'] == 'Medium (50-249)']['mean'].iloc[0]),
        'large_mean': float(size_stats_clean[size_stats_clean['size_band'] == 'Large (250+)']['mean'].iloc[0])
    }
    
    # Correlation test
    corr_result = perform_size_correlation_test(data['current_use'])
    summary['key_findings']['size_correlation'] = corr_result
    
    # Top barriers
    barriers_agg = data['barriers'].groupby('barrier')['percentage'].mean().sort_values(ascending=False)
    summary['key_findings']['top_barriers'] = {
        str(k): float(v) for k, v in barriers_agg.head(5).items()
    }
    
    # Top purposes
    purposes_agg = data['purposes'].groupby('purpose')['percentage'].mean().sort_values(ascending=False)
    summary['key_findings']['top_purposes'] = {
        str(k): float(v) for k, v in purposes_agg.head(5).items()
    }
    
    # Save summary
    output_path = results_dir / "analysis_summary.json"
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSaved summary: {output_path}")
    
    return summary


def main():
    """Main analysis pipeline."""
    project_root = Path(__file__).parent.parent
    processed_dir = project_root / "data" / "processed"
    results_dir = project_root / "results"
    figures_dir = results_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("Analysing AI adoption in UK SMEs")
    print("=" * 80)
    
    # Load data
    print("\n1. Loading processed data...")
    data = load_processed_data(processed_dir)
    
    # Generate visualisations
    print("\n2. Creating visualisations...")
    plot_adoption_by_size(results_dir)
    plot_ai_purposes(results_dir)
    plot_barriers(results_dir)
    
    # Perform statistical tests
    print("\n3. Performing statistical analysis...")
    corr_result = perform_size_correlation_test(data['current_use'])
    print(f"   Firm size vs AI adoption correlation: {corr_result['correlation']:.3f}")
    print(f"   P-value: {corr_result['p_value']:.4f} ({corr_result['interpretation']})")
    
    # Generate summary
    print("\n4. Generating results summary...")
    summary = generate_results_summary(data, results_dir)
    
    print("\n" + "=" * 80)
    print("Analysis complete")
    print("=" * 80)
    print(f"\nOutputs saved to: {results_dir}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
