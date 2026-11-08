import pandas as pd
import numpy as np
import json
import os
import re

out_dir = r"G:\マイドライブ\antigravity\IDM\20261008"
csv_path = os.path.join(out_dir, "artifacts", "analysis_dataset_n2035.csv")
dict_path = os.path.join(out_dir, "artifacts", "corrected_scoring_dictionary_master.json")

df = pd.read_csv(csv_path)
with open(dict_path, "r", encoding="utf-8") as f:
    scoring_dict = json.load(f)

# Build a bidirectional column mapping between short code (e.g., SC9.1) and full column name
column_map = {}
for col in df.columns:
    # Match patterns like SC9.*:1.* or SC15.*:2.* or Q8.*:3.* or SC1. or Q1.
    # Check if starts with SC\d+ or Q\d+ or SC\d+-\d+
    m_sub = re.match(r'^(SC\d+|Q\d+|SC\d+-\d+)[^:]*:([0-9]+)\.', col)
    if m_sub:
        short_name = f"{m_sub.group(1)}.{m_sub.group(2)}"
        column_map[short_name] = col
    else:
        m_single = re.match(r'^(SC\d+|Q\d+|SC\d+-\d+)\.', col)
        if m_single:
            short_name = m_single.group(1)
            column_map[short_name] = col

print(f"Mapped {len(column_map)} short variable codes to full column headers.")
sample_mapped = list(column_map.items())[:10]
for k, v in sample_mapped:
    print(f"  {k} -> {v[:50]}...")

# Save column mapping dictionary
with open(os.path.join(out_dir, "artifacts", "column_short_name_map.json"), "w", encoding="utf-8") as f:
    json.dump(column_map, f, ensure_ascii=False, indent=2)

print("Saved column_short_name_map.json")
