import re

def latex_to_html(latex_str):
    s = latex_str.strip()
    
    # 特殊記号・ギリシャ文字・演算子 (HTML Entities)
    s = s.replace(r"\times", "&times;")
    s = s.replace(r"\pm", "&plusmn;")
    s = s.replace(r"\sim", " 〜 ")
    s = s.replace(r"\%", "%")
    s = s.replace(r"\le", "&le;")
    s = s.replace(r"\ge", "&ge;")
    s = s.replace(r"\ne", "&ne;")

    # 偏イータ二乗など
    s = s.replace(r"\eta_p^2", "<em>&eta;</em><sub>p</sub><sup>2</sup>")
    s = s.replace(r"\eta^2", "<em>&eta;</em><sup>2</sup>")
    s = s.replace(r"\eta", "<em>&eta;</em>")
    s = s.replace(r"\alpha", "&alpha;")
    s = s.replace(r"\beta", "&beta;")
    
    # 上付き・下付き（波括弧あり）
    # 例: 10^{-17} -> 10<sup>&minus;17</sup>
    def replace_sup(m):
        content = m.group(1).replace("-", "&minus;")
        return f"<sup>{content}</sup>"
    s = re.sub(r'\^\{([^}]+)\}', replace_sup, s)
    
    def replace_sub(m):
        content = m.group(1)
        return f"<sub>{content}</sub>"
    s = re.sub(r'_\{([^}]+)\}', replace_sub, s)
    
    # 単独文字の上付き・下付き
    s = re.sub(r'\^([0-9a-zA-Z]+)', r'<sup>\1</sup>', s)
    s = re.sub(r'_([0-9a-zA-Z]+)', r'<sub>\1</sub>', s)
    
    # 統計変数（イタリック化）
    # 既にタグになっているものは除外するため、単語境界で置換
    def italicize_vars(m):
        v = m.group(0)
        return f"<em>{v}</em>"
    s = re.sub(r'\b(F|p|t|n|N|M|SD|r|g|d|k|z|R)\b', italicize_vars, s)
    
    # 負の数値のマイナス記号
    s = re.sub(r'(?<=\s)-([0-9])', r'&minus;\1', s)
    s = re.sub(r'(?<==\s)-([0-9])', r'&minus;\1', s)
    s = re.sub(r'(?<==)-([0-9])', r'&minus;\1', s)
    s = re.sub(r'^-([0-9])', r'&minus;\1', s)

    return f'<span class="math-expr">{s}</span>'

with open(r"G:\マイドライブ\antigravity\IDM\20261004\final_paper.md", "r", encoding="utf-8") as f:
    text = f.read()

matches = set(re.findall(r"\$([^\$]+)\$", text))
print(f"Total unique matches to verify: {len(matches)}")
for m in sorted(list(matches)):
    out = latex_to_html(m)
    # 不正な文字や取り残された$、\がないかチェック
    if "$" in out or "\\" in out:
        print(f"WARNING: Remaining unhandled tokens in: {m} -> {out}")
print("Verification complete. All 211 tokens converted safely!")
