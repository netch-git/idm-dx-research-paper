import re

def latex_to_html(latex_str):
    s = latex_str.strip()
    
    # 特殊な積・乗号・記号 (HTML Entities)
    s = s.replace(r"\times", "&times;")
    s = s.replace(r"\pm", "&plusmn;")
    s = s.replace(r"\sim", "&sim;")
    s = s.replace(r"\%", "%")
    s = s.replace(r"\le", "&le;")
    s = s.replace(r"\ge", "&ge;")
    s = s.replace(r"\ne", "&ne;")

    # ギリシャ文字 (HTML Entities)
    s = s.replace(r"\alpha", "&alpha;")
    s = s.replace(r"\beta", "&beta;")
    s = s.replace(r"\eta_p^2", "<em>&eta;</em><sub>p</sub><sup>2</sup>")
    s = s.replace(r"\eta^2", "<em>&eta;</em><sup>2</sup>")
    s = s.replace(r"\eta", "<em>&eta;</em>")
    
    # 上付き・下付き
    s = re.sub(r'\^\{([^}]+)\}', r'<sup>\1</sup>', s)
    s = re.sub(r'\^([0-9a-zA-Z+-]+)', r'<sup>\1</sup>', s)
    s = re.sub(r'_\{([^}]+)\}', r'<sub>\1</sub>', s)
    s = re.sub(r'_([0-9a-zA-Z]+)', r'<sub>\1</sub>', s)
    
    # 統計変数（APAスタイル: 斜体イタリック）
    def italicize_vars(m):
        return f"<em>{m.group(0)}</em>"
    
    # 変数名 (F, p, t, n, N, M, SD, r, g, d, k, z, R)
    s = re.sub(r'\b(F|p|t|n|N|M|SD|r|g|d|k|z|R)\b', italicize_vars, s)
    
    # マイナス記号の視覚的改善 (−: &minus;)
    s = re.sub(r'(?<=\s)-([0-9])', r'&minus;\1', s)
    s = re.sub(r'(?<==\s)-([0-9])', r'&minus;\1', s)
    s = re.sub(r'(?<==)-([0-9])', r'&minus;\1', s)
    s = re.sub(r'^-([0-9])', r'&minus;\1', s)

    return f'<span class="math-expr">{s}</span>'

test_cases = [
    "n = 745",
    "\\alpha = 0.859",
    "F(1, 2029) = 8.04, p = 0.0046, \\eta_p^2 = 0.0039",
    "3.60 \\times 10^{-17}",
    "M = 3.77",
    "p < 0.001, g = 0.79",
    "r = -0.0901",
    "2.69 \\pm 0.67",
    "0.392 \\sim 0.651",
    "+0.40, t(35.63) = 3.01, p_{raw} = 0.0048, p_{holm} = 0.0145, g = 0.60"
]

for t in test_cases:
    print(f"INPUT : ${t}$")
    print(f"OUTPUT: {latex_to_html(t)}")
    print()
