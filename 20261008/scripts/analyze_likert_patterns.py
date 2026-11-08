import json
import os

dict_path = r"G:\マイドライブ\antigravity\IDM\20261008\artifacts\likert_scales_dict.json"
with open(dict_path, "r", encoding="utf-8") as f:
    likert_dict = json.load(f)

print(f"Total Likert variables: {len(likert_dict)}")

# Group by option patterns
patterns = {}
for var_id, item in likert_dict.items():
    opts = item["options_mapping"]
    pattern_key = " | ".join([f"{k}:{v}" for k, v in sorted(opts.items(), key=lambda x: int(x[0]))])
    if pattern_key not in patterns:
        patterns[pattern_key] = []
    patterns[pattern_key].append(var_id)

print(f"\nUnique Likert Scale Patterns: {len(patterns)}\n")
for idx, (pat, vars_list) in enumerate(patterns.items()):
    print(f"--- Pattern {idx+1} (Variables count: {len(vars_list)}) ---")
    print(f"Scale: {pat}")
    print(f"Variables: {vars_list[:10]} ...\n")
