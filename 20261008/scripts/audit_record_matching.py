import pandas as pd
import numpy as np
import json
import os

cleaned_path = r"G:\マイドライブ\antigravity\IDM\data\data[企業規模-職制カラム追加].xlsx"
raw_path = r"G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx"
out_dir = r"G:\マイドライブ\antigravity\IDM\20261008"

print("Loading cleaned file...")
df_cleaned = pd.read_excel(cleaned_path, sheet_name="data_utf8")
print(f"Cleaned file shape: rows={df_cleaned.shape[0]}, cols={df_cleaned.shape[1]}")

print("Loading raw file data_text...")
df_raw_text = pd.read_excel(raw_path, sheet_name="data_text", header=0)
raw_labels_text = df_raw_text.iloc[0].to_dict()
df_raw_text_data = df_raw_text.iloc[1:].copy()
df_raw_text_data.reset_index(drop=True, inplace=True)

# Main survey subset in raw
df_raw_main = df_raw_text_data[df_raw_text_data['Q1'].notna()].copy()
df_raw_main.reset_index(drop=True, inplace=True)
print(f"Raw main survey rows: {len(df_raw_main)}")

# Compare K_ID
cleaned_kids = df_cleaned['K_ID'].tolist()
raw_kids = df_raw_main['K_ID'].tolist()

print(f"Unique K_IDs in cleaned: {len(set(cleaned_kids))}")
print(f"Unique K_IDs in raw main: {len(set(raw_kids))}")

# Check matching
kids_in_both = set(cleaned_kids).intersection(set(raw_kids))
print(f"K_IDs present in both: {len(kids_in_both)}")

kids_only_cleaned = set(cleaned_kids) - set(raw_kids)
kids_only_raw = set(raw_kids) - set(cleaned_kids)
print(f"K_IDs only in cleaned: {len(kids_only_cleaned)}")
print(f"K_IDs only in raw: {len(kids_only_raw)}")

# Check row ordering
order_identical = (cleaned_kids == raw_kids)
print(f"Row ordering identical: {order_identical}")

audit_res = {
    "cleaned_shape": [int(df_cleaned.shape[0]), int(df_cleaned.shape[1])],
    "raw_main_shape": [int(df_raw_main.shape[0]), int(df_raw_main.shape[1])],
    "kids_in_both": len(kids_in_both),
    "kids_only_cleaned": list(kids_only_cleaned),
    "kids_only_raw": list(kids_only_raw),
    "order_identical": bool(order_identical)
}

with open(os.path.join(out_dir, "artifacts", "audit_record_matching.json"), "w", encoding="utf-8") as f:
    json.dump(audit_res, f, ensure_ascii=False, indent=2)

print("Saved audit_record_matching.json")
