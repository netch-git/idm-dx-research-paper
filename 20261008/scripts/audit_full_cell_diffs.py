import pandas as pd
import numpy as np
import json
import os

cleaned_path = r"G:\マイドライブ\antigravity\IDM\data\data[企業規模-職制カラム追加].xlsx"
raw_path = r"G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx"
out_dir = r"G:\マイドライブ\antigravity\IDM\20261008"

# Load cleaned
df_cleaned = pd.read_excel(cleaned_path, sheet_name="data_utf8")

# Load raw text and raw num
df_raw_text = pd.read_excel(raw_path, sheet_name="data_text", header=0)
df_raw_text_data = df_raw_text.iloc[1:].copy()
df_raw_text_data.reset_index(drop=True, inplace=True)

df_raw_num = pd.read_excel(raw_path, sheet_name="data", header=0)
df_raw_num_data = df_raw_num.iloc[1:].copy()
df_raw_num_data.reset_index(drop=True, inplace=True)

# 1. Investigate the 19 diffs in SC1
sc1_clean_col = [c for c in df_cleaned.columns if 'SC1.' in c][0]
s_clean_sc1 = df_cleaned[sc1_clean_col].astype(str).replace('nan', '')
s_raw_text_sc1 = df_raw_text_data['SC1'].astype(str).replace('nan', '')
s_raw_num_sc1 = df_raw_num_data['SC1'].astype(str).replace('nan', '')

diff_sc1_mask = (s_clean_sc1 != s_raw_text_sc1)
diff_indices = np.where(diff_sc1_mask)[0]
print(f"Total diffs in SC1: {len(diff_indices)}")

sc1_diff_samples = []
for idx in diff_indices:
    kid = df_cleaned.iloc[idx]['K_ID']
    clean_val = s_clean_sc1.iloc[idx]
    raw_text_val = s_raw_text_sc1.iloc[idx]
    raw_num_val = s_raw_num_sc1.iloc[idx]
    raw_other_val = str(df_raw_text_data.iloc[idx].get('SC1-22', ''))
    sc1_diff_samples.append({
        "row_idx": int(idx),
        "K_ID": kid,
        "clean_val": clean_val,
        "raw_text_val": raw_text_val,
        "raw_num_val": raw_num_val,
        "raw_other_text (SC1-22)": raw_other_val
    })

print("Sample SC1 diffs (first 10):")
for s in sc1_diff_samples[:10]:
    print(s)

# 2. Check full survey columns cell diffs
# Align all remaining question columns
raw_cols = list(df_raw_text.columns)
cleaned_cols = list(df_cleaned.columns)

all_col_diffs = []

for rc in raw_cols:
    if rc in ['SEQ', 'K_ID']:
        continue
    # find matching cleaned col
    matches = [cc for cc in cleaned_cols if cc.strip().startswith(rc.strip() + '.') or cc.strip() == rc.strip() or (rc.strip() in cc.strip() and not any(k in cc for k in ['-2', 'グループ', '×']))]
    if not matches:
        continue
    cc = matches[0]
    
    s_raw = df_raw_text_data[rc].astype(str).replace('nan', '')
    s_clean = df_cleaned[cc].astype(str).replace('nan', '')
    
    # Normalize numbering prefix if any (e.g. "1. " or "1.")
    import re
    s_clean_norm = s_clean.apply(lambda x: re.sub(r'^[0-9１２３４５６７８９０]+[\.．\s]+', '', x))
    s_raw_norm = s_raw.apply(lambda x: re.sub(r'^[0-9１２３４５６７８９０]+[\.．\s]+', '', x))
    
    # Strip float formatting (e.g. '6.0' -> '6')
    s_clean_norm = s_clean_norm.apply(lambda x: x[:-2] if x.endswith('.0') else x)
    s_raw_norm = s_raw_norm.apply(lambda x: x[:-2] if x.endswith('.0') else x)
    
    diff_mask = (s_raw_norm != s_clean_norm)
    n_diff = diff_mask.sum()
    if n_diff > 0:
        all_col_diffs.append({
            "raw_col": rc,
            "cleaned_col": cc,
            "diff_count": int(n_diff),
            "sample_raw": s_raw[diff_mask].head(3).tolist(),
            "sample_clean": s_clean[diff_mask].head(3).tolist()
        })

print(f"\nTotal columns with normalized differences: {len(all_col_diffs)}")
for d in all_col_diffs:
    print(f"Col {d['raw_col']} vs {d['cleaned_col']}: {d['diff_count']} diffs (Sample Raw: {d['sample_raw'][:2]} vs Clean: {d['sample_clean'][:2]})")

# Save diff details
with open(os.path.join(out_dir, "artifacts", "audit_cell_diffs_complete.json"), "w", encoding="utf-8") as f:
    json.dump({
        "sc1_diffs": sc1_diff_samples,
        "normalized_col_diffs": all_col_diffs
    }, f, ensure_ascii=False, indent=2)

print("Saved audit_cell_diffs_complete.json")
