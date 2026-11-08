import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 生Excelから直接
df = pd.read_excel('data/data[企業規模-職制カラム追加].xlsx')
likert = {
    'そう思う': 5, 'ややそう思う': 4, 'どちらともいえない': 3,
    'あまりそう思わない': 2, 'まったくそう思わない': 1, '全くそう思わない': 1
}
import re

def find_col(d, prefix, num=None):
    for c in d.columns:
        if num is not None:
            pats = [f"{prefix}[_-]{num}[^0-9]", f"{prefix}[_-]{num}$", f"{prefix}_{num}", f"{prefix}-{num}"]
            if any(re.search(p, str(c)) for p in pats):
                return c
        else:
            if str(c).startswith(prefix) or f"_{prefix}" in str(c):
                return c
    return None

for i in range(1, 10):
    c18 = find_col(df, "SC18", i)
    c15 = find_col(df, "SC15", i)
    if c18: df[f'sc18_{i}'] = df[c18].map(likert)
    if c15: df[f'sc15_{i}'] = df[c15].map(likert)

# 定義A（論文本文の定義）
own_A = df[[f'sc18_{i}' for i in range(1, 6)]].mean(axis=1)
fr_A = df[['sc15_1', 'sc15_2', 'sc15_4', 'sc15_5', 'sc15_6']].mean(axis=1)
dj_low = 6.0 - df[['sc18_1', 'sc18_4']].mean(axis=1)

# 主分析
Z = StandardScaler().fit_transform(pd.DataFrame({'own': own_A, 'fr': fr_A}))
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(Z)
c = pd.DataFrame({'own': own_A, 'fr': fr_A, 'cl': km.labels_}).groupby('cl').mean()
print('Main Cluster Centers:\n', c)
alien_id = c['own'].idxmin()
is_al = (km.labels_ == alien_id).astype(int)
print(f'Alienated n = {is_al.sum()} ({is_al.mean()*100:.1f}%)')

# 感度分析 (SC18-2, 3, 5)
own_3 = df[['sc18_2', 'sc18_3', 'sc18_5']].mean(axis=1)
Z3 = StandardScaler().fit_transform(pd.DataFrame({'own': own_3, 'fr': fr_A}))
km3 = KMeans(n_clusters=3, random_state=42, n_init=10).fit(Z3)
c3 = pd.DataFrame({'own': own_3, 'fr': fr_A, 'cl': km3.labels_}).groupby('cl').mean()
print('Sensitivity 3-item Cluster Centers:\n', c3)
alien3_id = c3['own'].idxmin()
is_al3 = (km3.labels_ == alien3_id).astype(int)
print(f'Sensitivity Alienated n = {is_al3.sum()} ({is_al3.mean()*100:.1f}%)')

# 統制変数
ctrl = pd.DataFrame({
    'age': 53.306,
    'female': (df['性別'] == '女性').astype(int),
    'large': (df['SC2-2_大企業・中小企業・官公庁・公的団体等の区分'] == '大企業').astype(int),
    'mid': (df['SC7-2_役職'] == '2.部課長クラス').astype(int),
    'gen': (df['SC7-2_役職'] == '3.一般社員').astype(int),
    'dj': dj_low
})
m3 = sm.Logit(is_al3, sm.add_constant(ctrl)).fit(disp=0)
print('Sensitivity OR:', np.exp(m3.params['dj']), 'B:', m3.params['dj'], 'p:', m3.pvalues['dj'])
