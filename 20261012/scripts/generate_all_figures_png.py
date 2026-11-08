# -*- coding: utf-8 -*-
"""
generate_all_figures_png.py: 8大実証図表を300 DPI PNGで完全自動生成
企業規模2区分（大企業 vs SMO）および真のマスターデータ数値完全準拠版
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['Meiryo', 'Yu Gothic', 'MS Gothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

out_dir = r'G:\マイドライブ\antigravity\IDM\20261012\figures'
os.makedirs(out_dir, exist_ok=True)

# DADSカラー
C_BLUE = '#005BAC'
C_TEAL = '#00838F'
C_GREEN = '#228543'
C_RED = '#D32F2F'
C_GRAY = '#666666'
C_LIGHT_GRAY = '#F0F2F5'

# ----------------------------------------------------
# 図 4-1: 企業規模（大企業 vs SMO）× 組織階層 交互作用プロット
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)
categories = ['役員・経営層', '中間管理職', '一般社員・非管理職']
large_means = [3.852, 3.400, 3.227]
smo_means = [3.519, 3.306, 3.243]

x = np.arange(len(categories))
ax.plot(x, large_means, marker='o', linewidth=2.5, markersize=8, color=C_BLUE, label='大企業 (従業員1,000人以上: n = 745)')
ax.plot(x, smo_means, marker='^', linewidth=2.5, markersize=8, color=C_RED, label='SMO (従業員1,000人未満: n = 1,290)')

for i, (lv, sv) in enumerate(zip(large_means, smo_means)):
    ax.annotate(f"{lv:.3f}", (x[i], lv + 0.025), ha='center', fontsize=9.5, fontweight='bold', color=C_BLUE)
    offset_y = -0.045 if i < 2 else 0.025
    ax.annotate(f"{sv:.3f}", (x[i], sv + offset_y), ha='center', fontsize=9.5, fontweight='bold', color=C_RED)

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
ax.set_ylabel('変革当事者意識 平均スコア (1〜5点)', fontsize=11)
ax.set_ylim(3.10, 4.00)
ax.set_title('図 4-1: 企業規模（大企業 vs SMO）× 組織階層別 変革当事者意識の交互作用\n(F(2, 2029) = 4.619, p = 0.010*, partial η² = 0.0045)', fontsize=11.5, fontweight='bold', pad=12)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=10)
plt.tight_layout()
fig1_path = os.path.join(out_dir, 'Figure4_1_Interaction.png')
plt.savefig(fig1_path)
plt.close()
print("Saved:", fig1_path)

# ----------------------------------------------------
# 図 4-2: k-means 3群のプロファイル比較
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=300)
clusters = [
    'クラスタ1: 変革牽引層 (17.3%)',
    'クラスタ2: 受動的追随層 (36.9%)',
    'クラスタ3: 心理的離反層 (45.8%)'
]
commitment = [4.160, 3.465, 2.790]
friction = [3.059, 2.728, 3.374]
dist_justice = [3.679, 3.077, 2.390]

y = np.arange(len(clusters))
height = 0.25

ax.barh(y - height, commitment, height, label='変革当事者意識 (形成変数)', color=C_BLUE)
ax.barh(y, friction, height, label='組織内摩擦認知 (形成変数)', color=C_RED)
ax.barh(y + height, dist_justice, height, label='分配的公正 (外部変数)', color=C_GREEN)

ax.set_yticks(y)
ax.set_yticklabels(clusters, fontsize=10, fontweight='bold')
ax.set_xlabel('平均スコア (1〜5点)', fontsize=11)
ax.set_xlim(0, 4.6)
ax.set_title('図 4-2: k-means クラスタリングによる3類型の主要指標比較 (N = 2,035)', fontsize=12, fontweight='bold', pad=12)
ax.grid(True, axis='x', linestyle=':', alpha=0.6)
ax.legend(loc='lower right', frameon=True, fontsize=9.5)
ax.invert_yaxis()
plt.tight_layout()
fig2_path = os.path.join(out_dir, 'Figure4_2_Clusters.png')
plt.savefig(fig2_path)
plt.close()
print("Saved:", fig2_path)

# ----------------------------------------------------
# 図 4-3: 手続的公正の調整効果 単純傾斜プロット
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(6.8, 4.2), dpi=300)
friction_vals = np.array([-0.630, 0.0, 0.630]) # ±1SD (SD=0.630)
low_pj = 3.341 + (-0.0692) * friction_vals
high_pj = 3.342 + (0.0515) * friction_vals

ax.plot(friction_vals, low_pj, marker='o', linewidth=2.5, color=C_RED, label='手続的公正 低水準 (-1SD): B = -0.0692* (p = 0.0148)')
ax.plot(friction_vals, high_pj, marker='s', linewidth=2.5, color=C_BLUE, label='手続的公正 高水準 (+1SD): B = +0.0515* (p = 0.0349)')

ax.set_xticks(friction_vals)
ax.set_xticklabels(['低摩擦 (-1SD: 2.45)', '平均 (3.08)', '高摩擦 (+1SD: 3.71)'], fontsize=10.5)
ax.set_xlabel('組織内摩擦認知 (SC15)', fontsize=11)
ax.set_ylabel('変革当事者意識 推定値', fontsize=11)
ax.set_ylim(3.25, 3.43)
ax.set_title('図 4-3: 手続的公正の水準別 単純傾斜プロット\n(交互作用 B = +0.0826, t = 3.66, p < 0.001)', fontsize=12, fontweight='bold', pad=12)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)
plt.tight_layout()
fig3_path = os.path.join(out_dir, 'Figure4_3_SimpleSlopes.png')
plt.savefig(fig3_path)
plt.close()
print("Saved:", fig3_path)

# ----------------------------------------------------
# 図 4-4: 人材能力9項目の需給ギャップ
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=300)
skills = [
    '3. 現場課題の抽出能力',
    '4. 業務プロセスデザイン能力',
    '6. 要件定義・外注管理力',
    '7. 現場の抵抗を乗り越える推進力',
    '5. システム・サービス選定力',
    '8. 部門間利害調整能力',
    '9. ロードマップ策定企画力',
    '2. 経営層への説明・予算獲得力',
    '1. デジタル技術知識・スキル'
]
gaps = [1.083, 1.003, 0.993, 0.991, 0.982, 0.980, 0.954, 0.897, 0.799]

y = np.arange(len(skills))
ax.barh(y, gaps, height=0.6, color=C_BLUE, alpha=0.85)

for i, v in enumerate(gaps):
    ax.text(v + 0.02, i, f"+{v:.3f}", va='center', fontsize=9.5, fontweight='bold', color='#1A1A1A')

ax.set_yticks(y)
ax.set_yticklabels(skills, fontsize=10)
ax.set_xlabel('需給ギャップ (重要度 Q8 - 充足度 Q9)', fontsize=11)
ax.set_xlim(0, 1.25)
ax.set_title('図 4-4: DX推進に必要な9大能力項目の需給ギャップランキング (N = 2,035)', fontsize=12, fontweight='bold', pad=12)
ax.grid(True, axis='x', linestyle=':', alpha=0.6)
ax.invert_yaxis()
plt.tight_layout()
fig4_path = os.path.join(out_dir, 'Figure4_4_CapabilityGaps.png')
plt.savefig(fig4_path)
plt.close()
print("Saved:", fig4_path)

# ----------------------------------------------------
# 図 4-5: DX成果に対する回帰係数 (β) の比較
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(6.8, 3.6), dpi=300)
features = [
    '変革推進 (PMO) 機能 (Q9-3,4,8)',
    '企業規模 (大企業ダミー)',
    'デジタル技術知識 (Q9-1)',
    '組織階層 (中間管理職ダミー)',
    '組織階層 (一般社員ダミー)'
]
betas = [0.439, 0.079, 0.047, 0.001, -0.018]
colors = [C_BLUE, C_TEAL, C_GRAY, C_GRAY, C_GRAY]

y = np.arange(len(features))
ax.barh(y, betas, height=0.55, color=colors)

for i, v in enumerate(betas):
    sig = '***' if i==0 else ('***' if i==1 else ('† (n.s.)' if i==2 else 'n.s.'))
    pos_x = max(v, 0) + 0.012
    ax.text(pos_x, i, f"β = {v:.3f} {sig}", va='center', fontsize=9.5, fontweight='bold')

ax.set_yticks(y)
ax.set_yticklabels(features, fontsize=10, fontweight='bold')
ax.set_xlabel('標準化偏回帰係数 (β)', fontsize=11)
ax.set_xlim(-0.06, 0.58)
ax.axvline(x=0, color='#333333', linewidth=0.8)
ax.set_title('図 4-5: DX総合成果 (Q4) に対する説明変数の標準化係数比較 (R² = 0.233)', fontsize=11.5, fontweight='bold', pad=12)
ax.grid(True, axis='x', linestyle=':', alpha=0.6)
ax.invert_yaxis()
plt.tight_layout()
fig5_path = os.path.join(out_dir, 'Figure4_5_RegressionBeta.png')
plt.savefig(fig5_path)
plt.close()
print("Saved:", fig5_path)

# ----------------------------------------------------
# 図 4-6: 成果実感 vs 推進継続意向の組織的乖離 (2要因6セル + 全社平均)
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=300)
cells = [
    '全社平均 (N = 2,035)',
    '大企業 経営層 (n = 31)',
    '大企業 中間管理職 (n = 295)',
    '大企業 一般社員 (n = 419)',
    'SMO 経営層 (n = 298)',
    'SMO 中間管理職 (n = 511) ★管理・現場層最大',
    'SMO 一般社員 (n = 481)'
]
diffs = [1.254, 1.677, 1.078, 1.167, 1.339, 1.446, 1.154]
bar_colors = [C_TEAL if i == 0 else (C_RED if '★' in c else C_BLUE) for i, c in enumerate(cells)]

y = np.arange(len(cells))
ax.barh(y, diffs, height=0.6, color=bar_colors, alpha=0.85)

for i, v in enumerate(diffs):
    ax.text(v + 0.02, i, f"+{v:.3f}", va='center', fontsize=9.5, fontweight='bold')

ax.set_yticks(y)
ax.set_yticklabels(cells, fontsize=9.5, fontweight='bold')
ax.set_xlabel('平均乖離スコア (推進継続意向 Q6 - 成果実感 Q4)', fontsize=10.5)
ax.set_xlim(0, 1.90)
ax.set_title('図 4-6: 企業規模（大企業 vs SMO）× 組織階層別 成果実感と推進継続意向の乖離幅', fontsize=11.5, fontweight='bold', pad=12)
ax.grid(True, axis='x', linestyle=':', alpha=0.6)
ax.invert_yaxis()
plt.tight_layout()
fig6_path = os.path.join(out_dir, 'Figure4_6_CognitiveGap.png')
plt.savefig(fig6_path)
plt.close()
print("Saved:", fig6_path)

# ----------------------------------------------------
# 図 5-1: 8大感度分析モデルのF値/p値比較
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(7.4, 4.0), dpi=300)
models = [
    'モデル1: 主分析 (Type II ANOVA)',
    'モデル2: Type III SS ANOVA',
    'モデル3: 共変量統制 ANCOVA',
    'モデル4: 全9項目平均尺度',
    'モデル5: EFA第1因子得点モデル',
    'モデル6: 職階分類定義B (監督職編入)',
    'モデル7: HC3不均一分散頑健回帰',
    'モデル8: 順序ロジット (LR χ²=5.45)'
]
p_vals = [0.0100, 0.0100, 0.0128, 0.0134, 0.0146, 0.0380, 0.0092, 0.0655]

y = np.arange(len(models))
bar_c = [C_TEAL if p < 0.05 else C_GRAY for p in p_vals]
ax.barh(y, p_vals, height=0.55, color=bar_c, alpha=0.85)
ax.axvline(x=0.05, color=C_RED, linestyle='--', linewidth=1.5, label='有意水準 α = 0.05')

for i, v in enumerate(p_vals):
    mark = '**' if v < 0.01 else ('*' if v < 0.05 else '†')
    ax.text(v + 0.001, i, f"p = {v:.4f} {mark}", va='center', fontsize=9, fontweight='bold')

ax.set_yticks(y)
ax.set_yticklabels(models, fontsize=9.5)
ax.set_xlabel('交互作用効果の p値', fontsize=10.5)
ax.set_xlim(0, 0.080)
ax.set_title('図 5-1: 8大感度分析モデルにおける交互作用効果の統計的有意性比較', fontsize=11.5, fontweight='bold', pad=12)
ax.grid(True, axis='x', linestyle=':', alpha=0.6)
ax.legend(loc='lower right', frameon=True, fontsize=9.5)
ax.invert_yaxis()
plt.tight_layout()
fig7_path = os.path.join(out_dir, 'Figure5_1_RobustnessPValues.png')
plt.savefig(fig7_path)
plt.close()
print("Saved:", fig7_path)

# ----------------------------------------------------
# 図 5-2: SC18個別9項目の交互作用F値ランキング
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=300)
items = [
    'SC18-8: 経営層リーダーシップ発揮',
    'SC18-6: 会社の将来のために必要',
    'SC18-1: 給料が増える',
    'SC18-7: 経営層はよく学んでいる',
    'SC18-3: 仕事が楽になる',
    'SC18-2: 残業時間が減る',
    'SC18-5: 自分の市場価値向上',
    'SC18-9: 経営層は現場の声を聞く',
    'SC18-4: 会社から評価される'
]
f_vals = [5.57, 3.73, 3.62, 2.66, 2.58, 2.38, 1.93, 1.52, 1.46]
f_colors = [C_RED if i==0 else (C_BLUE if i<3 else C_GRAY) for i in range(len(items))]

y = np.arange(len(items))
ax.barh(y, f_vals, height=0.6, color=f_colors, alpha=0.85)

for i, v in enumerate(f_vals):
    sig = ' (Holm p=0.034*)' if i==0 else (' (未補正 p<0.05)' if i<3 else '')
    ax.text(v + 0.1, i, f"F = {v:.2f}{sig}", va='center', fontsize=9, fontweight='bold')

ax.set_yticks(y)
ax.set_yticklabels(items, fontsize=9.5)
ax.set_xlabel('交互作用 F値 (大企業・SMO × 3職階)', fontsize=10.5)
ax.set_xlim(0, 7.5)
ax.set_title('図 5-2: SC18 個別9項目における二元配置交互作用 F値ランキング', fontsize=11.5, fontweight='bold', pad=12)
ax.grid(True, axis='x', linestyle=':', alpha=0.6)
ax.invert_yaxis()
plt.tight_layout()
fig8_path = os.path.join(out_dir, 'Figure5_2_ItemFValues.png')
plt.savefig(fig8_path)
plt.close()
print("Saved:", fig8_path)

print("All 8 figures generated successfully at 300 DPI!")
