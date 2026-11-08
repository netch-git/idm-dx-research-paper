import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. 生データ読み込み
df = pd.read_parquet('20261008/artifacts/analysis_data_n2035_final.parquet')

# 3項目版の変革当事者意識（SC18-2: 残業削減, SC18-3: 負担軽減, SC18-5: 市場価値向上）
# SC18-1 (給与増) と SC18-4 (適正評価) を完全除外
own_3 = df[['sc18_2', 'sc18_3', 'sc18_5']].mean(axis=1)

# 組織内摩擦認知 (SC15-1, 2, 4, 5, 6)
fr = df[['sc15_1', 'sc15_2', 'sc15_4', 'sc15_5', 'sc15_6']].mean(axis=1)

# 分配的公正の低認知スコア: 6 - mean(SC18-1, SC18-4)
dj_low = 6.0 - df[['sc18_1', 'sc18_4']].mean(axis=1)

# 標準化
X = pd.DataFrame({'own': own_3, 'fr': fr})
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# k-means (k=3, random_state=42, n_init=10)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cl_labels = kmeans.fit_predict(X_scaled)
df_cl = pd.DataFrame({'own': own_3, 'fr': fr, 'cl': cl_labels})
prof = df_cl.groupby('cl').agg(count=('own', 'count'), own_mean=('own', 'mean'), fr_mean=('fr', 'mean'))
print('=== Cluster Profiles (3 items) ===')
print(prof)

# クラスタ1が最低当事者意識（M=2.13）・最高摩擦（M=3.29）＝心理的離反層
alien_id = prof['own_mean'].idxmin()

ctrl_df = pd.DataFrame({
    'age': df['age'].astype(float),
    'female': (df['gender_code'] == 2).astype(int),
    'large': df['is_large_firm'].astype(int),
    'mid': (df['tier_a'] == '管理職').astype(int),
    'gen': (df['tier_a'] == '一般職').astype(int),
    'dj_low': dj_low
})

# 二項ロジスティック回帰（主分析と同一仕様：離反層 vs その他）
bin1 = (cl_labels == alien_id).astype(int)
X_bin = sm.add_constant(ctrl_df)
m_bin = sm.Logit(bin1, X_bin).fit(disp=0)

b_dj = m_bin.params['dj_low']
se_dj = m_bin.bse['dj_low']
or_dj = np.exp(b_dj)
ci_low = np.exp(b_dj - 1.96 * se_dj)
ci_high = np.exp(b_dj + 1.96 * se_dj)
p_dj = m_bin.pvalues['dj_low']

print('\n=== Binary Logit Model (Alienated Cluster vs Others) ===')
print(f'N = {len(df)}, Alienated N = {bin1.sum()} ({bin1.mean()*100:.1f}%)')
print(f'B = {b_dj:.4f}, SE = {se_dj:.4f}')
print(f'OR = {or_dj:.3f}, 95% CI [{ci_low:.3f}, {ci_high:.3f}]')
print(f'p-value = {p_dj:.4e}')
print(f'McFadden Pseudo R2 = {m_bin.prsquared:.4f}, AIC = {m_bin.aic:.1f}')

# 多項ロジスティック回帰（クラスタ0: 変革牽引層 を基準群とした場合）
mnlogit = sm.MNLogit(cl_labels, X_bin).fit(disp=0)
b_mn = mnlogit.params.loc['dj_low', alien_id]
se_mn = mnlogit.bse.loc['dj_low', alien_id]
or_mn = np.exp(b_mn)
p_mn = mnlogit.pvalues.loc['dj_low', alien_id]
ci_mn_low = np.exp(b_mn - 1.96 * se_mn)
ci_mn_high = np.exp(b_mn + 1.96 * se_mn)

print('\n=== Multinomial Logit Model (Alienated vs Leader Cluster 0) ===')
print(f'B = {b_mn:.4f}, SE = {se_mn:.4f}')
print(f'OR = {or_mn:.3f}, 95% CI [{ci_mn_low:.3f}, {ci_mn_high:.3f}]')
print(f'p-value = {p_mn:.4e}')
