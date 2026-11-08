# -*- coding: utf-8 -*-
"""
Step 2: Publication-Quality Visualization Script (APA 7th Compliant)
Target: Figure1_Interaction, Figure2_Distribution, Figure3_Cluster_Analysis
Guarantees:
  - Identical visual vocabulary (colors, markers, error bar caps, line weights)
  - 300 DPI raster PNG and vector PDF outputs
  - Type-II ANOVA effect size and test statistic annotations
"""

import sys
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"G:\マイドライブ\antigravity\IDM\20261004"
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
os.makedirs(FIGURES_DIR, exist_ok=True)

# 1. Setup typography and theme
plt.rcParams['font.sans-serif'] = ['Meiryo', 'Yu Gothic', 'BIZ UDPGothic', 'MS Gothic', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 10.5
plt.rcParams['lines.linewidth'] = 2.2
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Colors and marker specs (STRICTLY UNIFIED ACROSS ALL FIGURES)
COLOR_LARGE = "#1B365D"  # Oxford Navy Blue
COLOR_SMO = "#C0392B"    # Rich Vermilion Crimson
MARKER_LARGE = "o"       # Circle
MARKER_SMO = "s"         # Square
LINE_LARGE = "-"         # Solid
LINE_SMO = "--"          # Dashed
CAP_SIZE = 5
CAP_THICK = 1.5

# Load summary json and cohort data
with open(os.path.join(ARTIFACTS_DIR, "results_summary.json"), "r", encoding="utf-8") as f:
    summary_data = json.load(f)

# Dataset columns: ['row_index', 'size', 'position', 'dv_SC18', 'dv_SC15']
df = pd.read_csv(os.path.join(ARTIFACTS_DIR, "analysis_dataset_scores.csv"), encoding="utf-8-sig")

# Position order
POS_ORDER = ["1.経営層", "2.部課長クラス", "3.一般社員"]
POS_LABELS_JP = ["経営層\n(Executives)", "部課長クラス\n(Managers)", "一般社員\n(Staff)"]

print(f"Loaded {len(df)} records for visualization.")

# -------------------------------------------------------------
# FIGURE 1: TWO-PANEL INTERACTION PLOT (APA 7th STYLE)
# -------------------------------------------------------------
def generate_figure1():
    print("Generating Figure 1: Two-Panel Interaction Plot...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.2), sharey=True)
    
    panels = [
        {
            "ax": axes[0],
            "var": "SC18",
            "title": "(A) DX推進意識・心理的所有感 (SC18)",
            "ylabel": "リッカート合成平均スコア (1〜5点)",
            "anova": summary_data["analyses"]["SC18"]["anova_type2"],
            "cells": summary_data["analyses"]["SC18"]["cells"]
        },
        {
            "ax": axes[1],
            "var": "SC15",
            "title": "(B) DXリスク懸念・組織摩擦 (SC15)",
            "ylabel": "リッカート合成平均スコア (1〜5点)",
            "anova": summary_data["analyses"]["SC15"]["anova_type2"],
            "cells": summary_data["analyses"]["SC15"]["cells"]
        }
    ]
    
    for p in panels:
        ax = p["ax"]
        cells = p["cells"]
        
        # Split into Large and SMO
        large_cells = {c["position"]: c for c in cells if c["size"] == "Large"}
        smo_cells = {c["position"]: c for c in cells if c["size"] == "SMO"}
        
        x_vals = [0, 1, 2]
        
        # Means and 95% CIs
        large_means = [large_cells[pos]["mean"] for pos in POS_ORDER]
        large_ci_low = [large_cells[pos]["ci95_low"] for pos in POS_ORDER]
        large_ci_high = [large_cells[pos]["ci95_high"] for pos in POS_ORDER]
        large_err = [
            np.array(large_means) - np.array(large_ci_low),
            np.array(large_ci_high) - np.array(large_means)
        ]
        
        smo_means = [smo_cells[pos]["mean"] for pos in POS_ORDER]
        smo_ci_low = [smo_cells[pos]["ci95_low"] for pos in POS_ORDER]
        smo_ci_high = [smo_cells[pos]["ci95_high"] for pos in POS_ORDER]
        smo_err = [
            np.array(smo_means) - np.array(smo_ci_low),
            np.array(smo_ci_high) - np.array(smo_means)
        ]
        
        # Plot Large
        ax.errorbar(
            x_vals, large_means, yerr=large_err,
            fmt=MARKER_LARGE + LINE_LARGE, color=COLOR_LARGE,
            ecolor=COLOR_LARGE, elinewidth=1.6, capsize=CAP_SIZE, capthick=CAP_THICK,
            markersize=8, markerfacecolor=COLOR_LARGE, markeredgecolor='white', markeredgewidth=1.2,
            label="大企業 (Large: 1,000人以上, n=745)", zorder=4
        )
        
        # Plot SMO
        ax.errorbar(
            x_vals, smo_means, yerr=smo_err,
            fmt=MARKER_SMO + LINE_SMO, color=COLOR_SMO,
            ecolor=COLOR_SMO, elinewidth=1.6, capsize=CAP_SIZE, capthick=CAP_THICK,
            markersize=8, markerfacecolor=COLOR_SMO, markeredgecolor='white', markeredgewidth=1.2,
            label="中小企業 (SMO: 1,000人未満, n=1,290)", zorder=3
        )
        
        # Value callout text
        for i, (lm, sm) in enumerate(zip(large_means, smo_means)):
            ax.annotate(f"{lm:.2f}", (x_vals[i], lm), textcoords="offset points",
                        xytext=(-20 if lm >= sm else 20, 8),
                        fontsize=9.5, fontweight='bold', color=COLOR_LARGE)
            ax.annotate(f"{sm:.2f}", (x_vals[i], sm), textcoords="offset points",
                        xytext=(20 if sm > lm else -20, -15),
                        fontsize=9.5, fontweight='bold', color=COLOR_SMO)
            
        ax.set_xticks(x_vals)
        ax.set_xticklabels(POS_LABELS_JP, fontweight='medium')
        ax.set_ylim(2.5, 4.2)
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
        ax.grid(axis='y', linestyle=':', alpha=0.6, color='gray')
        ax.set_title(p["title"], pad=14, fontweight='bold')
        
        if ax == axes[0]:
            ax.set_ylabel(p["ylabel"], fontweight='bold', labelpad=8)
            ax.legend(frameon=True, facecolor='#f8f9fa', edgecolor='#d0d7de', loc='upper right')
        else:
            ax.legend(frameon=True, facecolor='#f8f9fa', edgecolor='#d0d7de', loc='lower right')
            
        # Add Statistical Test Annotation Box
        a = p["anova"]
        stat_box_text = (
            f"二元配置分散分析 (Type II ANOVA):\n"
            f"• 規模主効果: F({a['size']['df']}, {a['residual']['df']}) = {a['size']['F']:.2f}, "
            f"p = {a['size']['p']:.4f}, ηp² = {a['size']['partial_eta_sq']:.4f}\n"
            f"• 職制主効果: F({a['position']['df']}, {a['residual']['df']}) = {a['position']['F']:.2f}, "
            f"p < 0.001, ηp² = {a['position']['partial_eta_sq']:.4f}\n"
            f"• 交互作用: F({a['interaction']['df']}, {a['residual']['df']}) = {a['interaction']['F']:.2f}, "
            f"p = {a['interaction']['p']:.4f}, ηp² = {a['interaction']['partial_eta_sq']:.4f}"
        )
        props = dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.95)
        if p["var"] == "SC18":
            ax.text(0.04, 0.05, stat_box_text, transform=ax.transAxes, fontsize=8.8,
                    verticalalignment='bottom', bbox=props)
        else:
            ax.text(0.04, 0.72, stat_box_text, transform=ax.transAxes, fontsize=8.8,
                    verticalalignment='top', bbox=props)

    plt.suptitle("図1: 企業規模 × 職制グループにおけるDX意識の二元配置分散分析交互作用プロット (N = 2,035)",
                 fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save composite outputs
    png_path = os.path.join(FIGURES_DIR, "Figure1_Interaction.png")
    pdf_path = os.path.join(FIGURES_DIR, "Figure1_Interaction.pdf")
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.close()
    print(f"Saved {png_path} and {pdf_path}")

# -------------------------------------------------------------
# FIGURE 2: DISTRIBUTION VIOLIN & BOX PLOTS
# -------------------------------------------------------------
def generate_figure2():
    print("Generating Figure 2: Distribution Violin & Box Plots...")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5), sharey=True)
    
    # Stratum labels
    stratum_map = {
        ('Large', '1.経営層'): "大企業\n経営層",
        ('Large', '2.部課長クラス'): "大企業\n部課長",
        ('Large', '3.一般社員'): "大企業\n一般社員",
        ('SMO', '1.経営層'): "中小企業\n経営層",
        ('SMO', '2.部課長クラス'): "中小企業\n部課長",
        ('SMO', '3.一般社員'): "中小企業\n一般社員",
    }
    df_plot = df.copy()
    df_plot['stratum'] = [stratum_map[(s, p)] for s, p in zip(df_plot['size'], df_plot['position'])]
    
    order = [
        "大企業\n経営層", "大企業\n部課長", "大企業\n一般社員",
        "中小企業\n経営層", "中小企業\n部課長", "中小企業\n一般社員"
    ]
    palette = [
        COLOR_LARGE, "#2b5c8f", "#417bb8",
        COLOR_SMO, "#d35400", "#e67e22"
    ]
    
    # Panel A: SC18
    sns.violinplot(
        data=df_plot, x="stratum", y="dv_SC18", hue="stratum", order=order, palette=palette,
        ax=axes[0], inner=None, cut=0, linewidth=1.2, alpha=0.4, legend=False
    )
    sns.boxplot(
        data=df_plot, x="stratum", y="dv_SC18", order=order,
        ax=axes[0], width=0.25, color="white", boxprops=dict(alpha=0.9, edgecolor='#2c3e50', linewidth=1.2),
        whiskerprops=dict(color='#2c3e50', linewidth=1.2),
        capprops=dict(color='#2c3e50', linewidth=1.2),
        medianprops=dict(color='#c0392b', linewidth=2.0)
    )
    axes[0].set_title("(A) DX推進意識・心理的所有感 分布 (SC18)", fontweight='bold', pad=12)
    axes[0].set_ylabel("リッカート合成平均スコア (1〜5点)", fontweight='bold')
    axes[0].set_xlabel("分析層 (企業規模 × 職制グループ)", fontweight='bold')
    axes[0].grid(axis='y', linestyle=':', alpha=0.6)
    axes[0].set_ylim(0.8, 5.2)
    
    # Panel B: SC15
    sns.violinplot(
        data=df_plot, x="stratum", y="dv_SC15", hue="stratum", order=order, palette=palette,
        ax=axes[1], inner=None, cut=0, linewidth=1.2, alpha=0.4, legend=False
    )
    sns.boxplot(
        data=df_plot, x="stratum", y="dv_SC15", order=order,
        ax=axes[1], width=0.25, color="white", boxprops=dict(alpha=0.9, edgecolor='#2c3e50', linewidth=1.2),
        whiskerprops=dict(color='#2c3e50', linewidth=1.2),
        capprops=dict(color='#2c3e50', linewidth=1.2),
        medianprops=dict(color='#1b365d', linewidth=2.0)
    )
    axes[1].set_title("(B) DXリスク懸念・組織摩擦 分布 (SC15)", fontweight='bold', pad=12)
    axes[1].set_ylabel("", fontweight='bold')
    axes[1].set_xlabel("分析層 (企業規模 × 職制グループ)", fontweight='bold')
    axes[1].grid(axis='y', linestyle=':', alpha=0.6)
    
    # Add sample sizes on bottom
    counts = df_plot['stratum'].value_counts()
    for ax in axes:
        for i, cat in enumerate(order):
            n_val = counts.get(cat, 0)
            ax.text(i, 0.95, f"n={n_val}", ha='center', va='bottom', fontsize=9, color='#475569')

    plt.suptitle("図2: 企業規模別・職制別のDX意識およびリスク懸念スコア分布 (N = 2,035)",
                 fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    png_path = os.path.join(FIGURES_DIR, "Figure2_Distribution.png")
    pdf_path = os.path.join(FIGURES_DIR, "Figure2_Distribution.pdf")
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.close()
    print(f"Saved {png_path} and {pdf_path}")

# -------------------------------------------------------------
# FIGURE 3: BIVARIATE 2D PROFILE / CLUSTER DYNAMICS
# -------------------------------------------------------------
def generate_figure3():
    print("Generating Figure 3: Bivariate 2D Profile Plot...")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Calculate cell means for SC18 and SC15
    summary_sc18 = {c["size"] + "_" + c["position"]: c["mean"] for c in summary_data["analyses"]["SC18"]["cells"]}
    summary_sc15 = {c["size"] + "_" + c["position"]: c["mean"] for c in summary_data["analyses"]["SC15"]["cells"]}
    
    # Scatter background individuals with alpha
    ax.scatter(df[df['size']=='Large']['dv_SC18'],
               df[df['size']=='Large']['dv_SC15'],
               alpha=0.08, color=COLOR_LARGE, s=18, label="_nolegend_")
    ax.scatter(df[df['size']=='SMO']['dv_SC18'],
               df[df['size']=='SMO']['dv_SC15'],
               alpha=0.08, color=COLOR_SMO, s=18, label="_nolegend_")
    
    # Grand means reference lines
    gm_18 = summary_data["analyses"]["SC18"]["grand_mean"]
    gm_15 = summary_data["analyses"]["SC15"]["grand_mean"]
    ax.axvline(gm_18, linestyle=':', color='#94a3b8', linewidth=1.5, label=f"全体平均 (推進意識: {gm_18:.2f})")
    ax.axhline(gm_15, linestyle=':', color='#94a3b8', linewidth=1.5, label=f"全体平均 (リスク懸念: {gm_15:.2f})")
    
    # Quadrant Labels
    ax.text(4.8, 4.8, "【高推進・高摩擦】\n変革推進・摩擦直面層", ha='right', va='top', fontsize=10,
            color='#b91c1c', bbox=dict(boxstyle='round,pad=0.4', facecolor='#fee2e2', alpha=0.8, edgecolor='none'))
    ax.text(1.2, 4.8, "【低推進・高摩擦】\nDX警戒・組織防衛層", ha='left', va='top', fontsize=10,
            color='#64748b', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f1f5f9', alpha=0.8, edgecolor='none'))
    ax.text(4.8, 1.2, "【高推進・低摩擦】\n全社牽引・理想推進層", ha='right', va='bottom', fontsize=10,
            color='#047857', bbox=dict(boxstyle='round,pad=0.4', facecolor='#d1fae5', alpha=0.8, edgecolor='none'))
    ax.text(1.2, 1.2, "【低推進・低摩擦】\n現状維持・低関心層", ha='left', va='bottom', fontsize=10,
            color='#475569', bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8fafc', alpha=0.8, edgecolor='none'))
    
    # Connect Large and SMO trajectory points
    large_pts_x = [summary_sc18["Large_" + pos] for pos in POS_ORDER]
    large_pts_y = [summary_sc15["Large_" + pos] for pos in POS_ORDER]
    smo_pts_x = [summary_sc18["SMO_" + pos] for pos in POS_ORDER]
    smo_pts_y = [summary_sc15["SMO_" + pos] for pos in POS_ORDER]
    
    # Plot trajectories
    ax.plot(large_pts_x, large_pts_y, color=COLOR_LARGE, linewidth=2.5, linestyle='-', zorder=5,
            label="大企業 職制遷移 (経営層 → 部課長 → 一般社員)")
    ax.plot(smo_pts_x, smo_pts_y, color=COLOR_SMO, linewidth=2.5, linestyle='--', zorder=5,
            label="中小企業 職制遷移 (経営層 → 部課長 → 一般社員)")
    
    # Point labels
    pos_short = ["経営層", "部課長", "一般社員"]
    for i in range(3):
        # Large
        ax.scatter(large_pts_x[i], large_pts_y[i], color=COLOR_LARGE, s=140, marker=MARKER_LARGE,
                   edgecolor='white', linewidth=1.8, zorder=6)
        ax.annotate(f"大企業・{pos_short[i]}\n({large_pts_x[i]:.2f}, {large_pts_y[i]:.2f})",
                    (large_pts_x[i], large_pts_y[i]), textcoords="offset points",
                    xytext=(10, 10 if i!=1 else -25), fontsize=9.5, fontweight='bold', color=COLOR_LARGE)
        
        # SMO
        ax.scatter(smo_pts_x[i], smo_pts_y[i], color=COLOR_SMO, s=140, marker=MARKER_SMO,
                   edgecolor='white', linewidth=1.8, zorder=6)
        ax.annotate(f"中小・{pos_short[i]}\n({smo_pts_x[i]:.2f}, {smo_pts_y[i]:.2f})",
                    (smo_pts_x[i], smo_pts_y[i]), textcoords="offset points",
                    xytext=(-15, -20 if i!=0 else 12), ha='right' if i==0 else 'center',
                    fontsize=9.5, fontweight='bold', color=COLOR_SMO)
        
    ax.set_xlabel("DX推進意識・心理的所有感 スコア (SC18)", fontweight='bold', fontsize=12)
    ax.set_ylabel("DXリスク懸念・組織摩擦 スコア (SC15)", fontweight='bold', fontsize=12)
    ax.set_title("図3: 企業規模・職制別 DX推進意欲 vs リスク懸念 2次元ダイナミクス (N = 2,035)",
                 fontsize=13, fontweight='bold', pad=14)
    ax.set_xlim(1.0, 5.0)
    ax.set_ylim(1.0, 5.0)
    ax.grid(linestyle=':', alpha=0.5)
    ax.legend(frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', loc='upper left')
    
    plt.tight_layout()
    png_path = os.path.join(FIGURES_DIR, "Figure3_Cluster_Analysis.png")
    pdf_path = os.path.join(FIGURES_DIR, "Figure3_Cluster_Analysis.pdf")
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.close()
    print(f"Saved {png_path} and {pdf_path}")

if __name__ == "__main__":
    generate_figure1()
    generate_figure2()
    generate_figure3()
    print("All Step 2 visualizations generated successfully.")
