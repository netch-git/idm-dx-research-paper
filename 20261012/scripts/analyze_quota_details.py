import pandas as pd
import numpy as np

path = r'G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx'
df = pd.read_excel(path, sheet_name='data', header=0)
df_data = df.iloc[1:].copy()

flag_col = 'SC_MAIN'
df_eligible = df_data[df_data['SC19'].isin([1, 2, 3])].copy()
df_eligible['SEQ'] = pd.to_numeric(df_eligible['SEQ'])
df_eligible['SC7'] = pd.to_numeric(df_eligible['SC7'])
df_eligible['SC2'] = pd.to_numeric(df_eligible['SC2'])

# Position category:
# 役員: 1..6
# 管理職: 7..11, 14 (支店長/工場長)
# 一般社員/非管理職: 12, 13, 15
def categorize_pos(sc7):
    if sc7 in [1, 2, 3, 4, 5, 6]:
        return '役員・経営層'
    elif sc7 in [7, 8, 9, 10, 11, 14]:
        return '管理職'
    elif sc7 in [12, 13, 15]:
        return '一般社員・係長クラス'
    return 'その他'

df_eligible['pos_cat'] = df_eligible['SC7'].apply(categorize_pos)

# Company size category (as standard in IDM project):
# 大企業: 1000人以上 (12..15)
# 中堅企業: 300〜999人 (10, 11)
# 中小企業: 300人未満 (1..9)
def categorize_size(sc2):
    if sc2 in [12, 13, 14, 15]:
        return '大企業(1000人以上)'
    elif sc2 in [10, 11]:
        return '中堅企業(300-999人)'
    elif sc2 in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        return '中小企業(300人未満)'
    return '不明'

df_eligible['size_cat'] = df_eligible['SC2'].apply(categorize_size)

print("=== 9 Cells (Size x Position) breakdown in eligible sample (N=2,845) ===")
cell_summary = df_eligible.groupby(['size_cat', 'pos_cat', flag_col]).size().unstack(fill_value=0)
cell_summary.columns = ['SC終了', '本調査終了']
cell_summary['合計'] = cell_summary['SC終了'] + cell_summary['本調査終了']
cell_summary['本調査率(%)'] = (cell_summary['本調査終了'] / cell_summary['合計'] * 100).round(1)
print(cell_summary)

print("\n=== SEQ distribution by Position category and SC_MAIN ===")
for pcat in ['役員・経営層', '管理職', '一般社員・係長クラス']:
    sub = df_eligible[df_eligible['pos_cat'] == pcat]
    print(f"\n--- {pcat} ---")
    print(sub.groupby(flag_col)['SEQ'].describe().round(1))

