# -*- coding: utf-8 -*-
"""
extract_likert_dictionary.py
リッカート尺度（Likert scale）を用いた質問項目と回答選択肢、および数値化辞書を網羅的に抽出・定義するスクリプト
"""
import os
import sys
import json
import pandas as pd
from collections import OrderedDict

DATA_PATH = r"G:\マイドライブ\IDM\data-cross.xlsx"

def main():
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.")
        return

    print("Loading data...")
    df = pd.read_excel(DATA_PATH)
    print(f"Loaded shape: {df.shape}")

    # 本調査終了者 (N=2,035) に限定
    df_main = df[df["終了判定"] == "本調査終了"].copy()
    print(f"Valid main survey respondents: {len(df_main)}")

    # 各列のユニーク値と質問内容を調査
    results = OrderedDict()

    # リッカート尺度と判定するキーワード
    likert_keys = ["当てはまる", "そう思う", "重要", "満足", "賛成", "反対", "効率化"]

    for col in df_main.columns:
        vals = [v for v in df_main[col].dropna().unique() if isinstance(v, str)]
        
        # 単一選択肢のダミー列（「上記に当てはまるものはない」のみ等）は除外
        if len(vals) < 2:
            continue

        # リッカート的な多段階評価尺度か判定
        is_likert = False
        for v in vals:
            if any(k in v for k in likert_keys):
                is_likert = True
                break

        # かつ選択肢数が 7 個以下（リッカート尺度は通常 3〜7 段階）
        if is_likert and len(vals) <= 7:
            # プレフィックスの抽出 (例: SC9, SC14, SC15, SC18, SC20, Q8 等)
            parts = col.split(".", 1)
            prefix = parts[0].strip()
            
            if prefix not in results:
                results[prefix] = {
                    "question_block": col.split(":")[0] if ":" in col else col,
                    "items": [],
                    "unique_values": set()
                }
            
            # 各項目のサブタイトル
            sub_item = col.split(":", 1)[1] if ":" in col else col
            results[prefix]["items"].append({
                "column_name": col,
                "item_label": sub_item,
                "value_counts": df_main[col].value_counts().to_dict()
            })
            for v in vals:
                results[prefix]["unique_values"].add(v)

    # 出力構造の整理
    output_summary = {}
    for p, data in results.items():
        unique_vals = sorted(list(data["unique_values"]))
        output_summary[p] = {
            "prefix": p,
            "block_title": data["question_block"],
            "num_items": len(data["items"]),
            "items": [it["item_label"] for it in data["items"]],
            "unique_values": unique_vals,
            "sample_counts": data["items"][0]["value_counts"]
        }

    # JSON出力
    out_dir = r"G:\マイドライブ\antigravity\IDM\20261007\artifacts"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "likert_scales_inventory.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_summary, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(output_summary)} Likert blocks.")
    for p, info in output_summary.items():
        print(f"\n[{p}] {info['block_title']} ({info['num_items']} items)")
        print(f"  Values: {info['unique_values']}")

if __name__ == "__main__":
    main()
