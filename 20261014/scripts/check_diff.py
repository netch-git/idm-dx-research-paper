import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. parquet からの計算
pq = pd.read_parquet('20261008/artifacts/analysis_data_n2035_final.parquet')
own3_pq = pq[['sc18_2', 'sc18_3', 'sc18_5']].mean(axis=1)
fr_pq = pq[['sc15_1', 'sc15_2', 'sc15_4', 'sc15_5', 'sc15_6']].mean(axis=1)
dj_pq = 6.0 - pq[['sc18_1', 'sc18_4']].mean(axis=1)

Z_pq = StandardScaler().fit_transform(pd.DataFrame({'o': own3_pq, 'f': fr_pq}))
km_pq = KMeans(n_clusters=3, random_state=42, n_init=10).fit(Z_pq)
c_pq = pd.DataFrame({'o': own3_pq, 'f': fr_pq, 'cl': km_pq.labels_}).groupby('cl').mean()
print('Parquet cluster centers:\n', c_pq)
alien_pq = c_pq['o'].idxmin()
is_al_pq = (km_pq.labels_ == alien_pq).astype(int)
print(f'Parquet Alienated N = {is_al_pq.sum()} ({is_al_pq.mean()*100:.1f}%)')

X_pq = sm.add_constant(pd.DataFrame({
    'age': pq['age'].astype(float),
    'female': (pq['gender_code'] == 2).astype(int),
    'large': pq['is_large_firm'].astype(int),
    'mid': (pq['tier_a'] == '管理職').astype(int),
    'gen': (pq['tier_a'] == '一般職').astype(int),
    'dj': dj_pq
}))
m_pq = sm.Logit(is_al_pq, X_pq).fit(disp=0)
print('Parquet OR:', np.exp(m_pq.params['dj']), 'B:', m_pq.params['dj'])

# 2. ノートブック内の生データ処理
# ノートブック内では df['friction'] がどう計算されているか？
print('Parquet friction_prevention M, SD:', pq['friction_prevention'].mean(), pq['friction_prevention'].std())
print('fr_pq M, SD:', fr_pq.mean(), fr_pq.std())
