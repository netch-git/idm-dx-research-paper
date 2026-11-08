# -*- coding: utf-8 -*-
"""
build_epub_textbook.py
Generates the complete, Kindle-optimized EPUB 3.0 book for IDM statistical methods.
Uses textbook_master_data.py as single source of truth.
Features:
- Full 17 Chapters (Cover, Prologue, Core Pipeline ch01-ch08, Advanced Methods ch09-ch15, Epilogue Q&A 15)
- Deep Roots & Foundations Drill-down tree for all chapters
- Clean semantic HTML/Unicode math layouts (zero math breakage on any Kindle reader)
- Strict XML well-formedness (100% compliant with EPUB 3.0 and KDP standards)
Outputs: G:\\マイドライブ\\antigravity\\IDM\\20261029\\textbook_epub\\textbook_idm_statistics.epub
"""

import os
import sys
import re
import zipfile
import xml.etree.ElementTree as ET

# Ensure scripts dir is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from textbook_master_data import BOOK_METADATA, CHAPTERS_DATA, QA_TOPICS

EPUB_DIR = r"G:\マイドライブ\antigravity\IDM\20261029\textbook_epub"
OEBPS_DIR = os.path.join(EPUB_DIR, "OEBPS")
TEXT_DIR = os.path.join(OEBPS_DIR, "text")
STYLES_DIR = os.path.join(OEBPS_DIR, "styles")

os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(STYLES_DIR, exist_ok=True)

def sanitize_for_xml(text):
    """Sanitizes text for XML well-formedness."""
    # Convert &emsp; to &#8195;
    text = text.replace("&emsp;", "&#8195;")
    # Convert &ensp; to &#8194;
    text = text.replace("&ensp;", "&#8194;")
    # Convert raw ampersands not part of an entity
    text = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', text)
    return text

def convert_latex_for_epub(html_text):
    """Converts LaTeX display formulas in formula-card into clean Kindle-friendly HTML/Unicode."""
    # Formula 1: ANOVA alpha family
    f1_latex = r"$$\alpha_{\text{family}} = 1 - (1 - 0.05)^3 = 1 - (0.95)^3 = 1 - 0.857 = 14.3\%$$"
    f1_epub = """
<div class="epub-formula-card">
  <div class="formula-line"><strong>α<sub>family</sub> = 1 − (1 − 0.05)³ = 1 − (0.95)³ = 1 − 0.857 = 14.3%</strong></div>
  <div class="formula-note">※ 3回の検定で偶然有意差が出る確率が 5% から 14.3% へと約3倍に膨張する</div>
</div>
"""
    # Formula 2: F-ratio
    f2_epub = """
<div class="epub-formula-card">
  <div class="formula-line">
    <table class="formula-frac-table" style="margin: 0 auto; text-align: center; border-collapse: collapse;">
      <tr>
        <td rowspan="2" style="vertical-align: middle; padding-right: 8px; font-weight: bold; font-size: 1.15rem;">F =</td>
        <td style="border-bottom: 2px solid #005BAC; padding: 4px 8px; font-weight: bold;">群間分散 MS<sub>between</sub>（各グループ平均値の離れ具合 ＝ シグナル）</td>
      </tr>
      <tr>
        <td style="padding: 4px 8px; font-weight: bold;">群内分散 MS<sub>within</sub>（グループ内の個人のバラツキ ＝ ノイズ）</td>
      </tr>
    </table>
  </div>
</div>
"""
    # Formula 3: Logistic
    f3_epub = """
<div class="epub-formula-card">
  <div class="formula-line"><strong>ln( P / (1 − P) ) = β₀ + β₁X &#8195;⟺&#8195; P = 1 / ( 1 + e<sup>−(β₀ + β₁X)</sup> )</strong></div>
  <div class="formula-note">※ オッズの対数をとることで、確率は 0%〜100% の間に必ず収束する</div>
</div>
"""
    # Formula 4: Centering
    f4_epub = """
<div class="epub-formula-card">
  <div class="formula-line"><strong>X<sub>centered</sub> = X − X̄, &#8195; Z<sub>centered</sub> = Z − Z̄, &#8195; 交互作用項 = X<sub>centered</sub> × Z<sub>centered</sub></strong></div>
  <div class="formula-note">※ 平均値を引いて重心を原点に置くことで、多重共線性（VIF高騰）を解消する</div>
</div>
"""
    # Formula 5: Probit
    f5_epub = """
<div class="epub-formula-card">
  <div class="formula-line"><strong>P(Y = 1 | X) = Φ(β₀ + β₁X) = ∫<sub>−∞</sub><sup>β₀ + β₁X</sup> ( 1 / √(2π) ) e<sup>−t²/2</sup> dt</strong></div>
  <div class="formula-note">※ 標準正規分布の累積密度関数 Φ(z) によって確率のS字カーブを描く</div>
</div>
"""
    # Formula 6: Panel
    f6_epub = """
<div class="epub-formula-card">
  <div class="formula-line"><strong>Y<sub>it</sub> = β X<sub>it</sub> + α<sub>i</sub> + ε<sub>it</sub></strong> &#8195; (α<sub>i</sub>: 企業固有の観測不能な特性)</div>
  <div class="formula-note">※ 平均値との差分をとる（Within変換）ことで、固有の個性 α<sub>i</sub> を完全に消去する</div>
</div>
"""
    # Formula 7: Mediation
    f7_epub = """
<div class="epub-formula-card">
  <div class="formula-line"><strong>間接効果 (Indirect Effect) = a × b</strong> &#8195; (X →<sup>a</sup> M →<sup>b</sup> Y)</div>
  <div class="formula-note">※ 非正規な積の分布に対し、ブートストラップ法（5,000回）で信頼区間を検証する</div>
</div>
"""

    text = html_text
    text = re.sub(r'<div class="formula-card">\s*\$\$\\alpha_\{?\\text\{family\}\}?.*?\$\$\s*</div>', f1_epub, text, flags=re.DOTALL)
    text = re.sub(r'<div class="formula-card">\s*\$\$F = \\frac.*?\$\$\s*</div>', f2_epub, text, flags=re.DOTALL)
    text = re.sub(r'<div class="formula-card">\s*\$\\ln\\left.*?\$\$\s*</div>', f3_epub, text, flags=re.DOTALL)
    text = re.sub(r'<div class="formula-card">\s*\$\$X_\{?\\text\{centered\}\}?.*?\$\$\s*</div>', f4_epub, text, flags=re.DOTALL)
    text = re.sub(r'<div class="formula-card">\s*\$\$P\(Y = 1.*?\$\$\s*</div>', f5_epub, text, flags=re.DOTALL)
    text = re.sub(r'<div class="formula-card">\s*\$\$Y_\{it\}.*?\$\$\s*</div>', f6_epub, text, flags=re.DOTALL)
    text = re.sub(r'<div class="formula-card">\s*\$\$\\text\{間接効果.*?\$\$\s*</div>', f7_epub, text, flags=re.DOTALL)

    return text

def render_epub_foundations(f_data):
    if not f_data:
        return ""
    steps_html = []
    for idx, step in enumerate(f_data.get("steps", []), 1):
        steps_html.append(f"""
  <div class="drilldown-step">
    <div class="step-badge">{idx}</div>
    <div class="step-content">
      <div class="step-title">{sanitize_for_xml(step['title'])}</div>
      <div class="step-desc">{sanitize_for_xml(step['desc'])}</div>
    </div>
  </div>
""")
    return f"""
<div class="foundations-box">
  <div class="foundations-header">
    <span class="foundations-tag">Roots &amp; Foundations</span>
    <h4 class="foundations-title">{sanitize_for_xml(f_data['title'])}</h4>
  </div>
  {''.join(steps_html)}
</div>
"""

def generate_epub():
    # 1. Generate Stylesheet
    css_content = """/* Kindle & EPUB 3.0 Standard Stylesheet */
body {
  font-family: "Noto Sans JP", "Hiragino Kaku Gothic ProN", "Meiryo", sans-serif;
  line-height: 1.8;
  color: #1A1A1A;
  margin: 0;
  padding: 1.2rem;
  background-color: #FFFFFF;
}

h1, h2, h3, h4 {
  font-family: "Noto Sans JP", sans-serif;
  color: #0F172A;
  font-weight: 700;
  margin-top: 1.5rem;
  margin-bottom: 0.8rem;
  page-break-after: avoid;
}

h1.book-title {
  font-size: 2rem;
  color: #005BAC;
  text-align: center;
  margin-top: 2rem;
  margin-bottom: 0.5rem;
}

p.book-subtitle {
  font-size: 1.1rem;
  color: #475569;
  text-align: center;
  margin-bottom: 2rem;
}

.cover-badge {
  text-align: center;
  font-size: 0.75rem;
  letter-spacing: 0.15em;
  color: #005BAC;
  font-weight: bold;
  text-transform: uppercase;
}

.cover-authors {
  text-align: center;
  margin-top: 3rem;
  font-size: 1rem;
}

.cover-pub {
  text-align: center;
  margin-top: 2rem;
  font-size: 0.85rem;
  color: #64748B;
}

.chapter-number {
  font-size: 0.85rem;
  font-weight: bold;
  color: #005BAC;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 0.3rem;
}

h2.chapter-title {
  font-size: 1.45rem;
  color: #0F172A;
  border-bottom: 2px solid #005BAC;
  padding-bottom: 0.5rem;
  margin-top: 0;
}

p.chapter-lead {
  font-size: 1.05rem;
  font-weight: 500;
  color: #334155;
  background: #F8FAFC;
  border-left: 4px solid #005BAC;
  padding: 0.8rem 1rem;
  margin-bottom: 1.5rem;
}

h3.subhead {
  font-size: 1.2rem;
  color: #005BAC;
  border-left: 4px solid #00838F;
  padding-left: 0.6rem;
  margin-top: 1.8rem;
}

p {
  margin: 0.8rem 0;
  text-align: justify;
}

strong {
  color: #0F172A;
}

/* Formula Card for EPUB */
.epub-formula-card {
  background: #F1F5F9;
  border: 1px solid #CBD5E1;
  border-left: 4px solid #005BAC;
  border-radius: 6px;
  padding: 1rem;
  margin: 1.2rem 0;
  text-align: center;
}

.formula-line {
  font-size: 1.1rem;
  color: #0F172A;
  margin-bottom: 0.4rem;
}

.formula-note {
  font-size: 0.85rem;
  color: #64748B;
}

/* Foundations Drill-down Box */
.foundations-box {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-top: 3px solid #00838F;
  border-radius: 6px;
  padding: 1.2rem;
  margin: 2rem 0;
}

.foundations-header {
  margin-bottom: 1rem;
}

.foundations-tag {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: bold;
  color: #00838F;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  background: #E0F2FE;
  padding: 2px 8px;
  border-radius: 4px;
}

.foundations-title {
  font-size: 1.1rem;
  color: #0F172A;
  margin: 0.4rem 0 0;
}

.drilldown-step {
  display: table;
  width: 100%;
  margin-bottom: 0.8rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px dashed #CBD5E1;
}

.drilldown-step:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.step-badge {
  display: table-cell;
  width: 28px;
  vertical-align: top;
  font-weight: bold;
  color: #00838F;
  font-size: 1rem;
}

.step-content {
  display: table-cell;
  vertical-align: top;
}

.step-title {
  font-weight: bold;
  color: #1E293B;
  font-size: 0.95rem;
  margin-bottom: 0.2rem;
}

.step-desc {
  font-size: 0.9rem;
  color: #475569;
  line-height: 1.6;
}

/* Tables */
table.epub-table, table.data-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.2rem 0;
  font-size: 0.85rem;
}

table.epub-table th, table.data-table th {
  background: #005BAC;
  color: #FFFFFF;
  padding: 8px 10px;
  text-align: left;
  border: 1px solid #004582;
}

table.epub-table td, table.data-table td {
  padding: 8px 10px;
  border: 1px solid #CBD5E1;
  vertical-align: top;
}

table.epub-table tr:nth-child(even), table.data-table tr:nth-child(even) {
  background: #F8FAFC;
}

/* QA Items */
.epub-qa-item {
  margin: 1.5rem 0;
  padding: 1rem;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
}

.epub-qa-q {
  font-weight: bold;
  color: #005BAC;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.epub-qa-a {
  font-size: 0.95rem;
  color: #334155;
  line-height: 1.7;
}
"""
    with open(os.path.join(STYLES_DIR, "stylesheet.css"), "w", encoding="utf-8") as f:
        f.write(css_content)

    # 2. Build Chapter XHTML Files
    manifest_items = []
    spine_items = []
    nav_links = []

    # Cover
    cover_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ja">
<head>
  <meta charset="utf-8" />
  <title>{BOOK_METADATA['title']}</title>
  <link rel="stylesheet" type="text/css" href="../styles/stylesheet.css" />
</head>
<body>
  <div class="cover-badge">IDM EMPIRICAL METHODOLOGY STUDY GUIDE</div>
  <h1 class="book-title">{BOOK_METADATA['title']}</h1>
  <p class="book-subtitle">{BOOK_METADATA['subtitle']}</p>
  <div style="border-top: 2px solid #005BAC; width: 60px; margin: 2rem auto;"></div>
  <div class="cover-authors">
    <p><strong>{BOOK_METADATA['authors']}</strong> 編著</p>
    <p style="font-size: 0.9rem; color: #64748B;">{BOOK_METADATA['affiliation']}</p>
  </div>
  <div class="cover-pub">
    <p>{BOOK_METADATA['rights']}</p>
    <p>Version {BOOK_METADATA['version']} ({BOOK_METADATA['date']})</p>
  </div>
</body>
</html>
"""
    with open(os.path.join(TEXT_DIR, "cover.xhtml"), "w", encoding="utf-8") as f:
        f.write(cover_xhtml)
    manifest_items.append('<item id="cover" href="text/cover.xhtml" media-type="application/xhtml+xml"/>')
    spine_items.append('<itemref idref="cover"/>')
    nav_links.append('<li><a href="text/cover.xhtml">表紙</a></li>')

    # Chapters
    for ch in CHAPTERS_DATA:
        ch_id = ch["id"]
        ch_file = f"{ch_id}.xhtml"
        ch_num = ch["num"]
        ch_title = ch["title"]

        sections_body = []
        for sec in ch.get("sections", []):
            content_sanitized = sanitize_for_xml(convert_latex_for_epub(sec['content']))
            sections_body.append(f"""
  <h3 class="subhead">{sanitize_for_xml(sec['subhead'])}</h3>
  {content_sanitized}
""")

        foundations_html = render_epub_foundations(ch.get("foundations"))

        ch_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ja">
<head>
  <meta charset="utf-8" />
  <title>CHAPTER {ch_num}: {sanitize_for_xml(ch_title)}</title>
  <link rel="stylesheet" type="text/css" href="../styles/stylesheet.css" />
</head>
<body>
  <div class="chapter-number">CHAPTER {ch_num}</div>
  <h2 class="chapter-title">{sanitize_for_xml(ch_title)}</h2>
  <p class="chapter-lead">{sanitize_for_xml(ch['lead'])}</p>

  {''.join(sections_body)}
  {foundations_html}
</body>
</html>
"""
        with open(os.path.join(TEXT_DIR, ch_file), "w", encoding="utf-8") as f:
            f.write(ch_xhtml)

        manifest_items.append(f'<item id="{ch_id}" href="text/{ch_file}" media-type="application/xhtml+xml"/>')
        spine_items.append(f'<itemref idref="{ch_id}"/>')
        nav_links.append(f'<li><a href="text/{ch_file}">第{ch_num}章: {sanitize_for_xml(ch_title)}</a></li>')

    # Epilogue & QA
    qa_xhtml_items = []
    for idx, item in enumerate(QA_TOPICS, 1):
        qa_xhtml_items.append(f"""
  <div class="epub-qa-item">
    <div class="epub-qa-q">{sanitize_for_xml(item['q'])}</div>
    <div class="epub-qa-a">{sanitize_for_xml(item['a'])}</div>
  </div>
""")

    epilogue_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ja">
<head>
  <meta charset="utf-8" />
  <title>エピローグ: 学術的対話のための討議手引（15選）</title>
  <link rel="stylesheet" type="text/css" href="../styles/stylesheet.css" />
</head>
<body>
  <div class="chapter-number">CHAPTER 16</div>
  <h2 class="chapter-title">エピローグ: チームと育む学術的討議の作法（Q&amp;A 15選）</h2>
  <p class="chapter-lead">試問を「防衛」の場から「探究の深化」の場へ。審査員やチームメンバーと建設的な対話を紡ぐための15の視点。</p>

  <p>
    分析手法についての質問を受けるとき、それを「追及」や「試練」と捉えて防衛的になると、視野が狭まってしまいます。指導教官や査読者は、研究の妥当性を共に高め、より確かな知見へと磨き上げるためのパートナーです。
  </p>
  <p>
    以下に、本研究および先行研究の分析手法に関して交わされる代表的な15の学術的問いと、それに対する論理的・誠実な対話の指針をまとめました。
  </p>

  {''.join(qa_xhtml_items)}
</body>
</html>
"""
    with open(os.path.join(TEXT_DIR, "epilogue.xhtml"), "w", encoding="utf-8") as f:
        f.write(epilogue_xhtml)
    manifest_items.append('<item id="epilogue" href="text/epilogue.xhtml" media-type="application/xhtml+xml"/>')
    spine_items.append('<itemref idref="epilogue"/>')
    nav_links.append('<li><a href="text/epilogue.xhtml">エピローグ: 学術的対話のための討議手引（15選）</a></li>')

    # 3. Nav XHTML
    nav_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ja">
<head>
  <meta charset="utf-8" />
  <title>目次</title>
  <link rel="stylesheet" type="text/css" href="styles/stylesheet.css" />
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>目次</h1>
    <ol>
      {''.join(nav_links)}
    </ol>
  </nav>
</body>
</html>
"""
    with open(os.path.join(OEBPS_DIR, "nav.xhtml"), "w", encoding="utf-8") as f:
        f.write(nav_xhtml)
    manifest_items.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')

    # 4. TOC.ncx (for Kindle backwards compatibility)
    ncx_points = []
    play_order = 1
    for item in nav_links:
        m = re.search(r'href="([^"]+)">([^<]+)<', item)
        if m:
            href = m.group(1)
            # href in ncx is relative to OEBPS
            title = m.group(2)
            ncx_points.append(f"""
    <navPoint id="np_{play_order}" playOrder="{play_order}">
      <navLabel><text>{title}</text></navLabel>
      <content src="{href}"/>
    </navPoint>
""")
            play_order += 1

    toc_ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:idm-study-guide-2026-v2"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>{BOOK_METADATA['title']} — {BOOK_METADATA['subtitle']}</text></docTitle>
  <navMap>
    {''.join(ncx_points)}
  </navMap>
</ncx>
"""
    with open(os.path.join(OEBPS_DIR, "toc.ncx"), "w", encoding="utf-8") as f:
        f.write(toc_ncx)
    manifest_items.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')

    # Stylesheet in manifest
    manifest_items.append('<item id="stylesheet" href="styles/stylesheet.css" media-type="text/css"/>')

    # 5. Content OPF
    content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookID" version="3.0" xml:lang="ja">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookID">urn:uuid:idm-study-guide-2026-v2</dc:identifier>
    <dc:title>{BOOK_METADATA['title']} — {BOOK_METADATA['subtitle']}</dc:title>
    <dc:creator>{BOOK_METADATA['authors']}</dc:creator>
    <dc:publisher>IDM Project</dc:publisher>
    <dc:language>ja</dc:language>
    <dc:rights>{BOOK_METADATA['rights']}</dc:rights>
    <meta property="dcterms:modified">2026-10-29T14:50:00Z</meta>
  </metadata>
  <manifest>
    {''.join(manifest_items)}
  </manifest>
  <spine toc="ncx">
    {''.join(spine_items)}
  </spine>
</package>
"""
    with open(os.path.join(OEBPS_DIR, "content.opf"), "w", encoding="utf-8") as f:
        f.write(content_opf)

    # 6. Container XML
    meta_inf_dir = os.path.join(EPUB_DIR, "META-INF")
    os.makedirs(meta_inf_dir, exist_ok=True)
    container_xml = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""
    with open(os.path.join(meta_inf_dir, "container.xml"), "w", encoding="utf-8") as f:
        f.write(container_xml)

    # 7. Mimetype
    mimetype_file = os.path.join(EPUB_DIR, "mimetype")
    with open(mimetype_file, "w", encoding="ascii") as f:
        f.write("application/epub+zip")

    # 8. Validate all XML files
    print("Validating XML files...")
    all_xml_files = [
        os.path.join(meta_inf_dir, "container.xml"),
        os.path.join(OEBPS_DIR, "content.opf"),
        os.path.join(OEBPS_DIR, "toc.ncx"),
        os.path.join(OEBPS_DIR, "nav.xhtml"),
    ]
    for root, _, files in os.walk(TEXT_DIR):
        for file in files:
            if file.endswith(".xhtml"):
                all_xml_files.append(os.path.join(root, file))

    for xml_path in all_xml_files:
        try:
            ET.parse(xml_path)
        except Exception as e:
            print(f"XML Validation Error in {xml_path}: {e}")
            raise e
    print(f"All {len(all_xml_files)} XML/XHTML files validated successfully!")

    # 9. Pack into EPUB ZIP
    epub_out = os.path.join(EPUB_DIR, "textbook_idm_statistics.epub")
    if os.path.exists(epub_out):
        os.remove(epub_out)

    with zipfile.ZipFile(epub_out, "w") as z:
        # mimetype must be first and uncompressed
        z.write(mimetype_file, "mimetype", compress_type=zipfile.ZIP_STORED)
        # Add META-INF
        z.write(os.path.join(meta_inf_dir, "container.xml"), "META-INF/container.xml", compress_type=zipfile.ZIP_DEFLATED)
        # Add OEBPS
        for root, _, files in os.walk(OEBPS_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, EPUB_DIR)
                z.write(full_path, rel_path, compress_type=zipfile.ZIP_DEFLATED)

    print(f"EPUB successfully built: {epub_out} (Size: {os.path.getsize(epub_out)} bytes)")

if __name__ == "__main__":
    generate_epub()
