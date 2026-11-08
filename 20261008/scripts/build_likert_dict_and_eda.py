import pandas as pd
import numpy as np
import json
import os

excel_path = r"G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx"
out_dir = r"G:\マイドライブ\antigravity\IDM\20261008"

# 1. Load data
print("Loading data sheets...")
df_raw = pd.read_excel(excel_path, sheet_name="data", header=0)
labels_row = df_raw.iloc[0].to_dict()
df_data = df_raw.iloc[1:].copy()
df_data.reset_index(drop=True, inplace=True)

# Main survey subset (N=2,035) where Q1 is not null
df_main = df_data[df_data['Q1'].notna()].copy()
df_main.reset_index(drop=True, inplace=True)

print(f"Full screening records: {len(df_data)}")
print(f"Main survey records: {len(df_main)}")

# Load variable metadata from 見出し
with open(os.path.join(out_dir, "artifacts", "variables_metadata.json"), "r", encoding="utf-8") as f:
    vars_meta = json.load(f)

meta_by_id = {v["var_id"]: v for v in vars_meta}

# Also get labels for demographic variables (SEX, INCOME, EDUCATION, etc.) if available in data_text or 見出し
# Let's inspect 見出し for SEX, AGE, etc.
demo_meta = {}
for col in ["SEX", "AGE", "CHIIKI", "MARRIAGE", "CHILD", "JOB", "FAMILY", "EDUCATION", "INCOME"]:
    if col in meta_by_id:
        demo_meta[col] = meta_by_id[col]["options"]
    else:
        # Default mapping for known fields
        if col == "SEX":
            demo_meta[col] = {1: "男性", 2: "女性"}
        elif col == "MARRIAGE":
            demo_meta[col] = {1: "既婚", 2: "未婚"}
        elif col == "CHILD":
            demo_meta[col] = {1: "子供あり", 2: "子供なし"}
        elif col == "INCOME":
            demo_meta[col] = {
                1: "～400万円",
                2: "401万円～600万円",
                3: "601万円～800万円",
                4: "801万円～1000万円",
                5: "1001万円～1200万円",
                6: "1201万円～1500万円",
                7: "1501万円以上"
            }

# 2. Canonical Likert scale dictionary
likert_groups = [
    {
        "group_id": "SC9",
        "name": "仕事スタイル・就労意識",
        "scale_type": "5件法リッカート尺度 (同意・合致度)",
        "original_coding": "1:非常に当てはまる, 2:やや当てはまる, 3:わからない・どちらともいえない, 4:あまり当てはまらない, 5:全く当てはまらない",
        "recommended_score_conversion": "肯定得点化 (5点=非常に当てはまる, 4点=やや当てはまる, 3点=どちらともいえない, 2点=あまり当てはまらない, 1点=全く当てはまらない : 式 `6 - code`)",
        "mapping": {
            1: "非常に当てはまる",
            2: "やや当てはまる",
            3: "わからない・どちらともいえない",
            4: "あまり当てはまらない",
            5: "全く当てはまらない"
        },
        "vars": [f"SC9.{i}" for i in range(1, 11)]
    },
    {
        "group_id": "SC14",
        "name": "デジタル技術による改善期待（ブルシット・ジョブ効率化）",
        "scale_type": "5件法評定尺度 (意向・評価)",
        "original_coding": "1:非常にそう思う, 2:そう思う, 3:あまりそう思わない, 4:まったくそう思わない, 5:わからない・そのような仕事はない",
        "recommended_score_conversion": "改善意欲得点化 (1:非常にそう思う=4点, 2:そう思う=3点, 3:あまりそう思わない=2点, 4:まったくそう思わない=1点, 5:非該当=欠損/0点)",
        "mapping": {
            1: "非常にそう思う",
            2: "そう思う",
            3: "あまりそう思わない",
            4: "まったくそう思わない",
            5: "わからない・そのような仕事はない"
        },
        "vars": ["SC14"]
    },
    {
        "group_id": "SC15",
        "name": "デジタル化の懸念（現場の心理的抵抗・懸念事項）",
        "scale_type": "5件法リッカート尺度 (懸念・抵抗度)",
        "original_coding": "1:非常に当てはまる, 2:やや当てはまる, 3:わからない・どちらともいえない, 4:あまり当てはまらない, 5:全く当てはまらない",
        "recommended_score_conversion": "懸念度得点化 (5点=非常に当てはまる ... 1点=全く当てはまらない : 式 `6 - code`)",
        "mapping": {
            1: "非常に当てはまる",
            2: "やや当てはまる",
            3: "わからない・どちらともいえない",
            4: "あまり当てはまらない",
            5: "全く当てはまらない"
        },
        "vars": [f"SC15.{i}" for i in range(1, 10)]
    },
    {
        "group_id": "SC18",
        "name": "DXに対する考え方（期待・インセンティブ・経営層評価）",
        "scale_type": "5件法リッカート尺度 (期待・信頼度)",
        "original_coding": "1:そう思う, 2:ややそう思う, 3:わからない・どちらともいえない, 4:あまりそう思わない, 5:まったくそう思わない",
        "recommended_score_conversion": "肯定得点化 (5点=そう思う ... 1点=まったくそう思わない : 式 `6 - code`)",
        "mapping": {
            1: "そう思う",
            2: "ややそう思う",
            3: "わからない・どちらともいえない",
            4: "あまりそう思わない",
            5: "まったくそう思わない"
        },
        "vars": [f"SC18.{i}" for i in range(1, 10)]
    },
    {
        "group_id": "SC20",
        "name": "DXの課題（組織的・技術的阻害要因）",
        "scale_type": "5件法リッカート尺度 (課題認知度)",
        "original_coding": "1:当てはまる, 2:ある程度当てはまる, 3:わからない・どちらともいえない, 4:あまり当てはまらない, 5:まったく当てはまらない",
        "recommended_score_conversion": "課題認知得点化 (5点=当てはまる ... 1点=まったく当てはまらない : 式 `6 - code`)",
        "mapping": {
            1: "当てはまる",
            2: "ある程度当てはまる",
            3: "わからない・どちらともいえない",
            4: "あまり当てはまらない",
            5: "まったく当てはまらない"
        },
        "vars": [f"SC20.{i}" for i in range(1, 11)]
    },
    {
        "group_id": "Q2",
        "name": "DXに期待する効果",
        "scale_type": "5件法リッカート尺度 (期待度)",
        "original_coding": "1:期待している, 2:ある程度期待している, 3:わからない・どちらともいえない, 4:あまり期待していない, 5:まったく期待していない",
        "recommended_score_conversion": "期待得点化 (5点=期待している ... 1点=まったく期待していない : 式 `6 - code`)",
        "mapping": {
            1: "期待している",
            2: "ある程度期待している",
            3: "わからない・どちらともいえない",
            4: "あまり期待していない",
            5: "まったく期待していない"
        },
        "vars": [f"Q2.{i}" for i in range(1, 11)]
    },
    {
        "group_id": "Q3",
        "name": "DXの実際の成果",
        "scale_type": "5件法リッカート尺度 (成果実感度)",
        "original_coding": "1:成果が出ている, 2:ある程度成果が出ている, 3:わからない・どちらともいえない, 4:あまり成果が出ていない, 5:まったく成果が出ていない",
        "recommended_score_conversion": "成果得点化 (5点=成果が出ている ... 1点=まったく成果が出ていない : 式 `6 - code`)",
        "mapping": {
            1: "成果が出ている",
            2: "ある程度成果が出ている",
            3: "わからない・どちらともいえない",
            4: "あまり成果が出ていない",
            5: "まったく成果が出ていない"
        },
        "vars": [f"Q3.{i}" for i in range(1, 11)]
    },
    {
        "group_id": "Q4",
        "name": "DXの成果の実感（総合評価）",
        "scale_type": "11段階レーティング尺度 (0:不十分 〜 10:十分)",
        "original_coding": "1:0(不十分である), 2:1, 3:2, ..., 11:10(十分である)",
        "recommended_score_conversion": "実得点化 (0点〜10点 : 式 `code - 1`)",
        "mapping": {
            1: "0（不十分である）",
            2: "1",
            3: "2",
            4: "3",
            5: "4",
            6: "5",
            7: "6",
            8: "7",
            9: "8",
            10: "9",
            11: "10（十分である）"
        },
        "vars": ["Q4"]
    },
    {
        "group_id": "Q6",
        "name": "今後の取組意向（総合継続評価）",
        "scale_type": "11段階レーティング尺度 (0:取組不要 〜 10:取組必要)",
        "original_coding": "1:0(今後は取組は不要), 2:1, 3:2, ..., 11:10(今後も取組が必要)",
        "recommended_score_conversion": "実得点化 (0点〜10点 : 式 `code - 1`)",
        "mapping": {
            1: "0（今後は取組は不要）",
            2: "1",
            3: "2",
            4: "3",
            5: "4",
            6: "5",
            7: "6",
            8: "7",
            9: "8",
            10: "9",
            11: "10（今後も取組が必要）"
        },
        "vars": ["Q6"]
    },
    {
        "group_id": "Q8",
        "name": "DX成功に必要な人材能力の重要度",
        "scale_type": "5件法リッカート尺度 (能力重要度)",
        "original_coding": "1:非常に重要, 2:ある程度重要, 3:わからない・どちらともいえない, 4:あまり重要ではない, 5:まったく重要ではない",
        "recommended_score_conversion": "重要度得点化 (5点=非常に重要 ... 1点=まったく重要ではない : 式 `6 - code`)",
        "mapping": {
            1: "非常に重要",
            2: "ある程度重要",
            3: "わからない・どちらともいえない",
            4: "あまり重要ではない",
            5: "まったく重要ではない"
        },
        "vars": [f"Q8.{i}" for i in range(1, 10)]
    },
    {
        "group_id": "Q9",
        "name": "DX成功に必要な人材能力の充足度",
        "scale_type": "5件法リッカート尺度 (能力充足度)",
        "original_coding": "1:非常に充足している, 2:ある程度充足している, 3:わからない・どちらともいえない, 4:あまり充足していない, 5:まったく充足していない",
        "recommended_score_conversion": "充足度得点化 (5点=非常に充足している ... 1点=まったく充足していない : 式 `6 - code`)",
        "mapping": {
            1: "非常に充足している",
            2: "ある程度充足している",
            3: "わからない・どちらともいえない",
            4: "あまり充足していない",
            5: "まったく充足していない"
        },
        "vars": [f"Q9.{i}" for i in range(1, 10)]
    }
]

likert_dictionary_full = {}
for g in likert_groups:
    for vid in g["vars"]:
        meta = meta_by_id.get(vid, {})
        likert_dictionary_full[vid] = {
            "var_id": vid,
            "group_id": g["group_id"],
            "group_name": g["name"],
            "scale_type": g["scale_type"],
            "q_text": meta.get("q_text", ""),
            "sub_text": meta.get("sub_text", ""),
            "mapping": g["mapping"],
            "original_coding": g["original_coding"],
            "recommended_score_conversion": g["recommended_score_conversion"]
        }

with open(os.path.join(out_dir, "artifacts", "likert_scale_dictionary_master.json"), "w", encoding="utf-8") as f:
    json.dump({
        "groups": likert_groups,
        "variables": likert_dictionary_full
    }, f, ensure_ascii=False, indent=2)

print(f"Master Likert dictionary written ({len(likert_dictionary_full)} items).")

# 3. EDA - Demographics for N=2,035
print("Running Demographics EDA...")

# SC7: 役職 (Position)
sc7_meta = meta_by_id.get("SC7", {}).get("options", {})
sc7_counts = df_main["SC7"].value_counts().sort_index()
sc7_summary = []
for code, cnt in sc7_counts.items():
    code_int = int(code) if pd.notna(code) else code
    lbl = sc7_meta.get(code_int, str(code))
    sc7_summary.append({
        "code": code_int,
        "label": lbl,
        "count": int(cnt),
        "pct": round(cnt / len(df_main) * 100, 2)
    })

# 3-tier Position
def classify_position_3tier(val):
    if pd.isna(val):
        return "Unknown"
    v = int(val)
    if 1 <= v <= 6:
        return "経営層"
    elif 7 <= v <= 14:
        return "管理職"
    elif v == 15:
        return "一般社員"
    else:
        return "その他"

df_main["Position_3tier"] = df_main["SC7"].apply(classify_position_3tier)
pos3_counts = df_main["Position_3tier"].value_counts().to_dict()

# SC2: 従業員規模 (SMO vs 大企業)
def classify_firm_size(val):
    if pd.isna(val):
        return "Unknown"
    v = int(val)
    if 1 <= v <= 11:
        return "SMO (<1,000人)"
    elif 12 <= v <= 15:
        return "大企業 (>=1,000人)"
    else:
        return "不明"

df_main["Firm_Size_2tier"] = df_main["SC2"].apply(classify_firm_size)
size2_counts = df_main["Firm_Size_2tier"].value_counts().to_dict()

# Crosstab: Position × Firm Size
ct = pd.crosstab(df_main["Position_3tier"], df_main["Firm_Size_2tier"], margins=True)
crosstab_pos_size = ct.to_dict()

# SC1: 業種 (Industry)
sc1_meta = meta_by_id.get("SC1", {}).get("options", {})
sc1_counts = df_main["SC1"].value_counts().sort_index()
sc1_summary = []
for code, cnt in sc1_counts.items():
    code_int = int(code) if pd.notna(code) else code
    lbl = sc1_meta.get(code_int, str(code))
    sc1_summary.append({
        "code": code_int,
        "label": lbl,
        "count": int(cnt),
        "pct": round(cnt / len(df_main) * 100, 2)
    })

# SEX
sex_meta = demo_meta.get("SEX", {1: "男性", 2: "女性"})
sex_counts = df_main["SEX"].value_counts().sort_index()
sex_summary = [{
    "code": int(k),
    "label": sex_meta.get(int(k), str(k)),
    "count": int(v),
    "pct": round(v / len(df_main) * 100, 2)
} for k, v in sex_counts.items()]

# AGE
df_main["Age_num"] = pd.to_numeric(df_main["AGE"], errors="coerce")
age_desc = df_main["Age_num"].describe().to_dict()

# Age Groups (20代, 30代, 40代, 50代, 60代以上)
def age_bracket(age):
    if pd.isna(age):
        return "不明"
    if age < 30:
        return "20代以下"
    elif age < 40:
        return "30代"
    elif age < 50:
        return "40代"
    elif age < 60:
        return "50代"
    else:
        return "60代以上"

df_main["Age_bracket"] = df_main["Age_num"].apply(age_bracket)
age_group_counts = df_main["Age_bracket"].value_counts().to_dict()

# INCOME
inc_meta = demo_meta.get("INCOME", {})
inc_counts = df_main["INCOME"].value_counts().sort_index()
inc_summary = [{
    "code": int(k),
    "label": inc_meta.get(int(k), str(k)),
    "count": int(v),
    "pct": round(v / len(df_main) * 100, 2)
} for k, v in inc_counts.items() if pd.notna(k)]

# 4. Descriptive Statistics for Likert Items
print("Running Likert Descriptives...")
likert_stats = []

for vid, vinfo in likert_dictionary_full.items():
    if vid not in df_main.columns:
        continue
    
    s = pd.to_numeric(df_main[vid], errors="coerce")
    n_valid = int(s.count())
    n_miss = int(s.isna().sum())
    
    # Raw stats (1 to 5)
    raw_mean = float(s.mean()) if n_valid > 0 else 0.0
    raw_std = float(s.std()) if n_valid > 1 else 0.0
    raw_median = float(s.median()) if n_valid > 0 else 0.0
    
    # Converted score (if 5-point Likert: 6 - raw, if 11-point: raw - 1)
    if "5点" in vinfo["recommended_score_conversion"]:
        conv_s = 6 - s
    elif "実得点化" in vinfo["recommended_score_conversion"]:
        conv_s = s - 1
    else:
        conv_s = s
        
    conv_mean = float(conv_s.mean()) if n_valid > 0 else 0.0
    conv_std = float(conv_s.std()) if n_valid > 1 else 0.0
    
    # Frequencies
    freq = s.value_counts().sort_index().to_dict()
    freq_pct = {int(k): round(v / n_valid * 100, 2) for k, v in freq.items() if pd.notna(k)}
    
    likert_stats.append({
        "var_id": vid,
        "group_id": vinfo["group_id"],
        "group_name": vinfo["group_name"],
        "sub_text": vinfo["sub_text"],
        "n_valid": n_valid,
        "n_missing": n_miss,
        "raw_mean": round(raw_mean, 3),
        "raw_std": round(raw_std, 3),
        "raw_median": raw_median,
        "converted_mean": round(conv_mean, 3),
        "converted_std": round(conv_std, 3),
        "freq_pct": freq_pct
    })

# Save full results
eda_output = {
    "sample_summary": {
        "screening_n": len(df_data),
        "main_survey_n": len(df_main),
        "pass_rate_pct": round(len(df_main) / len(df_data) * 100, 2)
    },
    "position_3tier": pos3_counts,
    "firm_size_2tier": size2_counts,
    "crosstab_pos_size": crosstab_pos_size,
    "sc7_positions": sc7_summary,
    "sc1_industries": sc1_summary,
    "sex": sex_summary,
    "age": {
        "summary": {k: round(v, 2) for k, v in age_desc.items()},
        "brackets": age_group_counts
    },
    "income": inc_summary,
    "likert_stats": likert_stats
}

with open(os.path.join(out_dir, "artifacts", "eda_complete_results.json"), "w", encoding="utf-8") as f:
    json.dump(eda_output, f, ensure_ascii=False, indent=2)

print("Saved eda_complete_results.json")
