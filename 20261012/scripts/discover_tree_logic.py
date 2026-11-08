import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text

path = r'G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx'
df = pd.read_excel(path, sheet_name='data', header=0)
df_data = df.iloc[1:].copy()

flag_col = 'SC_MAIN'
y = (df_data[flag_col] == 2).astype(int)

# Candidate features from SC and Demographics
feature_cols = [c for c in df_data.columns if c.startswith('SC') and c != 'SC_MAIN'] + \
               ['SEX', 'AGE', 'CHIIKI', 'MARRIAGE', 'CHILD', 'JOB', 'FAMILY', 'EDUCATION', 'INCOME', 'HOME', 'LICENSE', 'CAR']

X = pd.DataFrame()
for c in feature_cols:
    X[c] = pd.to_numeric(df_data[c], errors='coerce').fillna(-999)

# Fit decision tree
dt = DecisionTreeClassifier(max_depth=5, min_samples_leaf=20, random_state=42)
dt.fit(X, y)

print("Decision Tree Accuracy:", dt.score(X, y))
tree_rules = export_text(dt, feature_names=list(X.columns))
print("\n--- Decision Tree Rules ---")
print(tree_rules)

# Top feature importances
importances = pd.Series(dt.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\n--- Top 10 Feature Importances ---")
print(importances.head(10))

