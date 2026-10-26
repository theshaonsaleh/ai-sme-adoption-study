"""
Analyse AI adoption patterns in UK SMEs using ONS BICS Wave 165 data.

This script performs descriptive analysis of published weighted estimates
from a single named wave, avoiding pseudo-replication.

Data source: ONS Business Insights and Conditions Survey (BICS) Wave 165
Licence: Open Government Licence v3.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

# Set plotting style
sns.set_style("whitegrid")
sns.set_palette("husl")


def plot_adoption_by_size_wave_165(results_dir: Path):
    """
    Visualise AI adoption by firm size from Wave 165.
    """
    processed_dir = results_dir.parent / "data" / "processed"
    df = pd.read_csv(processed_dir / "wave_165_adoption_by_size.csv")
    
    # Filter to individual size bands (not aggregates)
    size_order = ['Micro (0-9)', 'Small (10-49)', 'Medium (50-99)', 
                  'Medium (100-249)', 'Large (250+)']
    df_plot = df[df['size_band'].isin(size_order)].copy()
    df_plot['size_band'] = pd.Categorical(df_plot['size_band'], 
                                          categories=size_order, ordered=True)
    df_plot = df_plot.sort_values('size_band')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 7))
    
    bars = ax.bar(range(len(df_plot)), df_plot['uses_ai_rate'], 
                   color=['#3498db', '#2ecc71', '#f39c12', '#e67e22', '#e74c3c'])
    
    ax.set_xticks(range(len(df_plot)))
    ax.set_xticklabels(df_plot['size_band'], rotation=20, ha='right')
    ax.set_ylabel('AI Adoption Rate', fontsize=13)
    ax.set_xlabel('Firm Size (employees)', fontsize=13)
    ax.set_title('AI Adoption by Firm Size\nONS BICS Wave 165 (21 Sept–4 Oct 2026)', 
                 fontsize=15, fontweight='bold', pad=20)
    
    # Add value labels
    for bar, val in zip(bars, df_plot['uses_ai_rate']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1%}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    ax.set_ylim(0, 0.85)
    
    # Add source note
    ax.text(0.99, -0.15, 'Source: ONS BICS Wave 165\nWeighted estimates, all businesses', 
            transform=ax.transAxes, ha='right', va='top', fontsize=9, 
            style='italic', color='#666666')
    
    plt.tight_layout()
    
    output_path = results_dir / "figures" / "adoption_by_size_wave165.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()


def plot_adoption_trend(results_dir: Path):
    """
    Visualise AI adoption trend across waves.
    """
    processed_dir = results_dir.parent / "data" / "processed"
    df = pd.read_csv(processed_dir / "adoption_trend.csv")
    
    if len(df) == 0:
        print("  Skipped trend plot (no data)")
        return
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(df['wave'], df['uses_ai_rate'], marker='o', linewidth=2.5, 
            markersize=10, color='#2ecc71')
    
    # Add value labels
    for _, row in df.iterrows():
        ax.text(row['wave'], row['uses_ai_rate'] + 0.015, 
                f"{row['uses_ai_rate']:.1%}",
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('BICS Wave', fontsize=13)
    ax.set_ylabel('AI Adoption Rate', fontsize=13)
    ax.set_title('AI Adoption Trend in UK Businesses\n(All businesses)', 
                 fontsize=15, fontweight='bold', pad=20)
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    ax.set_ylim(0.15, 0.45)
    ax.grid(True, alpha=0.3)
    
    # Add wave dates as secondary labels
    wave_labels = []
    for _, row in df.iterrows():
        wave_labels.append(f"Wave {int(row['wave'])}\n{row['date']}")
    ax.set_xticks(df['wave'])
    ax.set_xticklabels(wave_labels, fontsize=9)
    
    # Add source note
    ax.text(0.99, -0.18, 'Source: ONS BICS Waves 105, 117, 165\nWeighted estimates', 
            transform=ax.transAxes, ha='right', va='top', fontsize=9, 
            style='italic', color='#666666')
    
    plt.tight_layout()
    
    output_path = results_dir / "figures" / "adoption_trend.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()


def plot_barriers_wave_165(results_dir: Path):
    """
    Visualise top barriers to AI adoption from Wave 165.
    """
    processed_dir = results_dir.parent / "data" / "processed"
    df = pd.read_csv(processed_dir / "wave_165_barriers.csv")
    
    # Exclude meta-categories
    df_sub = df[~df['barrier'].str.contains(
        'not attempted|not been prevented|Not sure|Not applicable', 
        case=False, na=False)]
    
    # Sort and take top 8
    df_sub = df_sub.sort_values('all_businesses_pct', ascending=True).tail(8)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 7))
    
    bars = ax.barh(range(len(df_sub)), df_sub['all_businesses_pct'], 
                    color='#e74c3c')
    
    ax.set_yticks(range(len(df_sub)))
    # Wrap long labels
    labels = []
    for label in df_sub['barrier']:
        if len(label) > 55:
            # Split at word boundary
            words = label.split()
            line1, line2 = [], []
            for word in words:
                if len(' '.join(line1)) < 45:
                    line1.append(word)
                else:
                    line2.append(word)
            labels.append(' '.join(line1) + '\n' + ' '.join(line2))
        else:
            labels.append(label)
    ax.set_yticklabels(labels, fontsize=10)
    
    ax.set_xlabel('% of All Businesses Reporting Barrier', fontsize=13)
    ax.set_title('Top Barriers to AI Adoption\nONS BICS Wave 165 (21 Sept–4 Oct 2026)', 
                 fontsize=15, fontweight='bold', pad=20)
    
    # Add value labels
    for bar, val in zip(bars, df_sub['all_businesses_pct']):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f' {val:.1%}',
                va='center', fontsize=10, fontweight='bold')
    
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
    
    # Add source note
    ax.text(0.99, -0.10, 'Source: ONS BICS Wave 165\nBase: All businesses', 
            transform=ax.transAxes, ha='right', va='top', fontsize=9, 
            style='italic', color='#666666')
    
    plt.tight_layout()
    
    output_path = results_dir / "figures" / "barriers_wave165.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()


def plot_purposes_wave_165(results_dir: Path):
    """
    Visualise purposes for AI use from Wave 165.
    """
    processed_dir = results_dir.parent / "data" / "processed"
    df = pd.read_csv(processed_dir / "wave_165_purposes.csv")
    
    # Exclude meta-categories
    df_sub = df[~df['purpose'].str.contains('Not sure|Not applicable|Other', 
                                            case=False, na=False)]
    
    # Sort
    df_sub = df_sub.sort_values('ai_adopters_pct', ascending=True)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.barh(range(len(df_sub)), df_sub['ai_adopters_pct'], 
                    color='#3498db')
    
    ax.set_yticks(range(len(df_sub)))
    ax.set_yticklabels(df_sub['purpose'], fontsize=11)
    
    ax.set_xlabel('% of AI-Adopting Businesses', fontsize=13)
    ax.set_title('What Do Businesses Use AI For?\nONS BICS Wave 165 (21 Sept–4 Oct 2026)', 
                 fontsize=15, fontweight='bold', pad=20)
    
    # Add value labels
    for bar, val in zip(bars, df_sub['ai_adopters_pct']):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f' {val:.1%}',
                va='center', fontsize=10, fontweight='bold')
    
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
    
    # Add source note
    ax.text(0.99, -0.13, 'Source: ONS BICS Wave 165\nBase: Businesses currently using AI', 
            transform=ax.transAxes, ha='right', va='top', fontsize=9, 
            style='italic', color='#666666')
    
    plt.tight_layout()
    
    output_path = results_dir / "figures" / "purposes_wave165.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.close()


def generate_summary_wave_165(results_dir: Path) -> dict:
    """
    Generate summary of key findings from Wave 165.
    """
    processed_dir = results_dir.parent / "data" / "processed"
    
    adoption = pd.read_csv(processed_dir / "wave_165_adoption_by_size.csv")
    barriers = pd.read_csv(processed_dir / "wave_165_barriers.csv")
    purposes = pd.read_csv(processed_dir / "wave_165_purposes.csv")
    trend = pd.read_csv(processed_dir / "adoption_trend.csv")
    
    summary = {
        'data_source': 'ONS BICS Wave 165 (21 September–4 October 2026)',
        'licence': 'Open Government Licence v3.0',
        'extraction_method': 'Direct extraction of published weighted estimates',
        'note': 'No pseudo-replication - single wave estimates only',
        'key_findings': {}
    }
    
    # Adoption by size
    summary['key_findings']['by_size'] = {}
    for _, row in adoption.iterrows():
        if row['size_band'] not in ['Other', 'All 10+ employees']:
            summary['key_findings']['by_size'][row['size_band']] = float(row['uses_ai_rate'])
    
    # Trend
    if len(trend) > 0:
        summary['key_findings']['trend'] = []
        for _, row in trend.sort_values('wave').iterrows():
            summary['key_findings']['trend'].append({
                'wave': int(row['wave']),
                'date': row['date'],
                'adoption_rate': float(row['uses_ai_rate'])
            })
    
    # Top barriers (substantive only)
    barriers_sub = barriers[~barriers['barrier'].str.contains(
        'not attempted|not been prevented|Not sure', case=False, na=False)]
    barriers_sorted = barriers_sub.sort_values('all_businesses_pct', ascending=False)
    summary['key_findings']['top_barriers'] = {
        str(row['barrier']): float(row['all_businesses_pct'])
        for _, row in barriers_sorted.head(5).iterrows()
    }
    
    # Top purposes
    purposes_sub = purposes[~purposes['purpose'].str.contains(
        'Not sure|Not applicable|Other', case=False, na=False)]
    purposes_sorted = purposes_sub.sort_values('ai_adopters_pct', ascending=False)
    summary['key_findings']['top_purposes'] = {
        str(row['purpose']): float(row['ai_adopters_pct'])
        for _, row in purposes_sorted.iterrows()
    }
    
    # Save
    output_path = results_dir / "analysis_summary_wave165.json"
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSaved summary: {output_path}")
    return summary


def main():
    """Main analysis pipeline."""
    project_root = Path(__file__).parent.parent
    results_dir = project_root / "results"
    figures_dir = results_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("Analysing AI adoption in UK SMEs")
    print("Using ONS BICS Wave 165 (Sept 2026) weighted estimates")
    print("=" * 80)
    
    # Generate visualisations
    print("\n1. Creating visualisations...")
    plot_adoption_by_size_wave_165(results_dir)
    plot_adoption_trend(results_dir)
    plot_barriers_wave_165(results_dir)
    plot_purposes_wave_165(results_dir)
    
    # Generate summary
    print("\n2. Generating results summary...")
    summary = generate_summary_wave_165(results_dir)
    
    print("\n" + "=" * 80)
    print("Analysis complete")
    print("=" * 80)
    print(f"\nOutputs saved to: {results_dir}")
    print("\nKey findings from Wave 165:")
    print(f"  - All businesses: {summary['key_findings']['by_size']['All businesses']:.1%} use AI")
    print(f"  - Micro (0-9): {summary['key_findings']['by_size']['Micro (0-9)']:.1%}")
    print(f"  - Large (250+): {summary['key_findings']['by_size']['Large (250+)']:.1%}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
