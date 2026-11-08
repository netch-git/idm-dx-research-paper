import pandas as pd
import numpy as np
import json
import os

out_dir = r"G:\マイドライブ\antigravity\IDM\20261008"
csv_path = os.path.join(out_dir, "artifacts", "analysis_dataset_n2035.csv")
dict_path = os.path.join(out_dir, "artifacts", "corrected_scoring_dictionary_master.json")
map_path = os.path.join(out_dir, "artifacts", "column_short_name_map.json")

df = pd.read_csv(csv_path)
with open(dict_path, "r", encoding="utf-8") as f:
    scoring_dict = json.load(f)
with open(map_path, "r", encoding="utf-8") as f:
    col_map = json.load(f)

# Helper function to map text response to numeric score (5-point scale: 5=Strongly Agree ... 1=Strongly Disagree)
# Original coding in data: 1=非常に当てはまる -> 5点, 2=やや -> 4点, 3=どちらとも -> 3点, 4=あまり -> 2点, 5=全く -> 1点
text_to_5pt_map = {
    # 当てはまる系 (SC9, SC15, SC20)
    "非常に当てはまる": 5, "やや当てはまる": 4, "わからない・どちらともいえない": 3, "あまり当てはまらない": 2, "全く当てはまらない": 1,
    "当てはまる": 5, "ある程度当てはまる": 4, "あまり当てはまらない": 2, "まったく当てはまらない": 1,
    # そう思う系 (SC18, SC14)
    "非常にそう思う": 5, "そう思う": 5, "ややそう思う": 4, "あまりそう思わない": 2, "まったくそう思わない": 1,
    # 重要系 (Q8)
    "非常に重要": 5, "ある程度重要": 4, "あまり重要ではない": 2, "まったく重要ではない": 1,
    # 充足系 (Q9)
    "非常に充足している": 5, "ある程度充足している": 4, "あまり充足していない": 2, "まったく充足していない": 1,
    # 成果系 (Q3)
    "成果が出ている": 5, "ある程度成果が出ている": 4, "あまり成果が出ていない": 2, "まったく成果が出ていない": 1,
    # 期待系 (Q2)
    "期待している": 5, "ある程度期待している": 4, "あまり期待していない": 2, "まったく期待していない": 1
}

def get_5pt_score(series):
    # Try mapping text first, if already numeric handle it
    s = series.map(text_to_5pt_map)
    # If not mapped (already numeric or floats)
    if s.isna().all() and not series.isna().all():
        num_s = pd.to_numeric(series, errors='coerce')
        return 6 - num_s
    return s

# Create scored columns
# 1. SC9 Subscales
df['SCORE_SC9_組織エンゲージメント'] = df[[col_map[f"SC9.{i}"] for i in [1, 4, 5, 7, 10]]].apply(get_5pt_score).mean(axis=1).round(3)
df['SCORE_SC9_分配的不公正感'] = df[[col_map[f"SC9.{i}"] for i in [2, 3]]].apply(get_5pt_score).mean(axis=1).round(3)
df['SCORE_SC9_変革抵抗業務逼迫'] = df[[col_map[f"SC9.{i}"] for i in [8, 9]]].apply(get_5pt_score).mean(axis=1).round(3)

# 2. SC15 Resistance
sc15_cols = [col_map[f"SC15.{i}"] for i in range(1, 10)]
df['SCORE_SC15_デジタル化心理的抵抗'] = df[sc15_cols].apply(get_5pt_score).mean(axis=1).round(3)

# 3. SC18 Subscales
df['SCORE_SC18_個人的インセンティブ'] = df[[col_map[f"SC18.{i}"] for i in range(1, 6)]].apply(get_5pt_score).mean(axis=1).round(3)
df['SCORE_SC18_滅私奉公義務感'] = get_5pt_score(df[col_map["SC18.6"]]).round(3)
df['SCORE_SC18_経営層リーダーシップ'] = df[[col_map[f"SC18.{i}"] for i in [7, 8, 9]]].apply(get_5pt_score).mean(axis=1).round(3)

# 4. Q4 Outcome & Q6 Intent
# Extract numeric rating (0 to 10)
def extract_rating(series):
    return series.astype(str).str.extract(r'(\d+)')[0].astype(float)

df['SCORE_Q4_DX成果総合実感'] = extract_rating(df[col_map["Q4"]])
df['SCORE_Q6_DX取組継続意向'] = extract_rating(df[col_map["Q6"]])
df['GAP_Q6_Q4_推進プレッシャー'] = (df['SCORE_Q6_DX取組継続意向'] - df['SCORE_Q4_DX成果総合実感']).round(3)

# 5. Q8 vs Q9 Capability Gaps
cap_names = [
    "1_技術知識", "2_PMO説得力", "3_PMO発見力", "4_PMO設計力",
    "5_PMO選定力", "6_PMO折衝力", "7_PMO推進力", "8_権限調整力", "9_戦略企画力"
]

for i in range(1, 10):
    imp = get_5pt_score(df[col_map[f"Q8.{i}"]])
    suf = get_5pt_score(df[col_map[f"Q9.{i}"]])
    df[f"SCORE_Q8_重要度_{cap_names[i-1]}"] = imp.round(3)
    df[f"SCORE_Q9_充足度_{cap_names[i-1]}"] = suf.round(3)
    df[f"GAP_人材不足_{cap_names[i-1]}"] = (imp - suf).round(3)

print("Computed all psychological scale scores and GAP variables.")
print(df[['SCORE_SC9_組織エンゲージメント', 'SCORE_SC9_分配的不公正感', 'SCORE_SC18_個人的インセンティブ', 'GAP_人材不足_3_PMO発見力']].describe())

out_scored_csv = os.path.join(out_dir, "artifacts", "analysis_dataset_n2035_scored.csv")
out_scored_xlsx = os.path.join(out_dir, "artifacts", "analysis_dataset_n2035_scored.xlsx")

df.to_csv(out_scored_csv, index=False, encoding='utf-8-sig')
df.to_excel(out_scored_xlsx, index=False, sheet_name="n2035_scored")

print(f"Saved {out_scored_csv} and {out_scored_xlsx}")
