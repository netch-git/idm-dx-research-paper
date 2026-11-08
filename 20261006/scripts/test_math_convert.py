import re

def latex_to_html(latex_str):
    s = latex_str.strip()
    
    # ギリシャ文字
    s = s.replace(r"\alpha", "α")
    s = s.replace(r"\beta", "β")
    s = s.replace(r"\eta_p^2", "<em>η</em><sub>p</sub><sup>2</sup>")
    s = s.replace(r"\eta^2", "<em>η</em><sup>2</sup>")
    s = s.replace(r"\eta", "<em>η</em>")
    
    # 記号
    s = s.replace(r"\times", "×")
    s = s.replace(r"\pm", "±")
    s = s.replace(r"\sim", "〜")
    s = s.replace(r"\%", "%")
    s = s.replace(r"\le", "≤")
    s = s.replace(r"\ge", "≥")
    s = s.replace(r"\ne", "≠")
    
    # 上付き・下付き: 10^{-17} -> 10<sup>-17</sup>
    s = re.sub(r'\^\{([^}]+)\}', r'<sup>\1</sup>', s)
    s = re.sub(r'\^([0-9a-zA-Z]+)', r'<sup>\1</sup>', s)
    s = re.sub(r'_\{([^}]+)\}', r'<sub>\1</sub>', s)
    s = re.sub(r'_([0-9a-zA-Z]+)', r'<sub>\1</sub>', s)
    
    # 学術統計変数 (イタリック化): F, p, t, n, N, M, SD, r, g, d, k, z
    # 単語境界かつタグでないアルファベット
    def italicize_vars(match):
        v = match.group(0)
        return f"<em>{v}</em>"
    
    # 変数名のイタリック置換 (F, p, t, n, N, M, SD, r, g, d, k, z, R)
    s = re.sub(r'\b(F|p|t|n|N|M|SD|r|g|d|k|z|R)\b', italicize_vars, s)
    
    # マイナス記号をハイフンマイナスから見栄えの良いマイナス記号 (−) に置換（負の数値）
    s = re.sub(r'(?<=\s)-([0-9])', r'−\1', s)
    s = re.sub(r'(?<==\s)-([0-9])', r'−\1', s)
    s = re.sub(r'(?<==)-([0-9])', r'−\1', s)
    
    return f'<span class="math-tex">{s}</span>'

# テスト
with open(r"G:\マイドライブ\antigravity\IDM\20261004\final_paper.md", "r", encoding="utf-8") as f:
    text = f.read()

matches = set(re.findall(r"\$([^\$]+)\$", text))
for m in sorted(list(matches))[:30]:
    converted = latex_to_html(m)
    print(f"ORIGINAL : ${m}$")
    print(f"CONVERTED: {converted}")
    print("-" * 50)
