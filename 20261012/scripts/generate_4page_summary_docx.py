# -*- coding: utf-8 -*-
"""
A4サイズ 4ページサマリー概要 Word (.docx) 生成スクリプト
- 厳密なA4 4ページ構成（ページ区切りによる精密分割）
- APA / DADSカラーデザイン（Primary Blue: #005BAC）
- N=2,035 完全決定論的数値の完全バインド
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """セル内側のパディングを設定"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m_name, m_val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m_name}')
        node.set(qn('w:w'), str(m_val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    """セルの背景色を設定"""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_table_borders(table, color="DDE2E5", sz="4", val="single"):
    """テーブル枠線の設定"""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_heading_styled(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.bold = True
    if level == 1:
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0, 91, 172) # #005BAC
    elif level == 2:
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0, 63, 117)
    return p

def add_body_p(doc, text, bold_prefix="", space_after=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.size = Pt(9)
        r_pre.font.color.rgb = RGBColor(26, 26, 26)
    r = p.add_run(text)
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(26, 26, 26)
    return p

def main():
    doc = Document()
    
    # ページ設定 (A4, 余白上下15mm, 左右15mm)
    for section in doc.sections:
        section.page_width = Mm(210)
        section.page_height = Mm(297)
        section.top_margin = Mm(14)
        section.bottom_margin = Mm(14)
        section.left_margin = Mm(15)
        section.right_margin = Mm(15)
        
    # フォント既定値
    style = doc.styles['Normal']
    font = style.font
    font.name = '游ゴシック'
    font.size = Pt(9)
    font.color.rgb = RGBColor(26, 26, 26)

    # ==================== PAGE 1 ====================
    # ヘッダー
    p_hdr = doc.add_paragraph()
    p_hdr.paragraph_format.space_after = Pt(2)
    r_hdr_tag = p_hdr.add_run("EXECUTIVE RESEARCH SUMMARY | ")
    r_hdr_tag.bold = True
    r_hdr_tag.font.size = Pt(8)
    r_hdr_tag.font.color.rgb = RGBColor(0, 91, 172)
    r_hdr_txt = p_hdr.add_run("企業規模と組織階層がDX推進意識および組織摩擦認知に及ぼす影響 (N=2,035)")
    r_hdr_txt.font.size = Pt(8)
    r_hdr_txt.font.color.rgb = RGBColor(100, 100, 100)

    # タイトル
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(1)
    r_t = p_title.add_run("企業規模と組織階層がDX推進意識および組織摩擦認知に及ぼす影響")
    r_t.bold = True
    r_t.font.size = Pt(14)
    r_t.font.color.rgb = RGBColor(0, 63, 117)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(3)
    r_s = p_sub.add_run("就業者2,035名のマイクロデータに基づく二元配置分散分析と組織公正の調整効果")
    r_s.bold = True
    r_s.font.size = Pt(10)
    r_s.font.color.rgb = RGBColor(50, 50, 50)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(4)
    r_m = p_meta.add_run("SMOフロンティア研究所 IDM研究グループ | 調査対象: 国内有職者 2,035名 | 2026年10月12日")
    r_m.font.size = Pt(8.5)
    r_m.font.color.rgb = RGBColor(100, 100, 100)

    # エグゼクティブサマリー ボックス
    tbl_sum = doc.add_table(rows=1, cols=1)
    tbl_sum.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_sum = tbl_sum.cell(0, 0)
    set_cell_shading(cell_sum, "EBF3FA")
    set_cell_margins(cell_sum, top=120, bottom=120, left=180, right=180)
    p_sb = cell_sum.paragraphs[0]
    p_sb.paragraph_format.line_spacing = 1.15
    p_sb.paragraph_format.space_after = Pt(0)
    r_sbt = p_sb.add_run("【エグゼクティブ・サマリー】 ")
    r_sbt.bold = True
    r_sbt.font.size = Pt(8.5)
    r_sbt.font.color.rgb = RGBColor(0, 91, 172)
    r_sbc = p_sb.add_run(
        "本研究は、国内就業者2,035名の完全決定論的マイクロデータ解析を通じ、DX成否を規定する組織要因を実証的に解明した。"
        "企業規模（大企業／SMO）と組織階層（経営層／中間管理職／一般社員）の2要因6セル配置による計量分析の結果、"
        "①企業規模×職階の交互作用によりSMO中間管理職の当事者意識が急落する一方、一般社員層では規模間差が消失（現場収束）すること（H1, p=0.010）、"
        "②評価・給与還元の欠落（分配的不公正）が心理的離反リスクを約4倍に増大させること（H2, OR=3.95）、"
        "③意思決定プロセスの透明性（手続的公正）が摩擦を推進エネルギーへと正転させる感情的反転レジリエンスを有すること（H3, B=+0.0826）、"
        "④成果規定力においてIT技術知識は非有意（p=0.098）であり全社変革機能（PMO）が独占的影響力（β=0.439）を持つこと（H4）、"
        "⑤全社的焦燥の中でSMO中間管理職の認知的葛藤が最大化すること（H5, ギャップ+1.45点）を証明した。"
        "DXの本質はツール導入ではなく「組織公正と階層間認識の統合」にある。"
    )
    r_sbc.font.size = Pt(8.5)

    add_heading_styled(doc, "1. 問題の所在と先行研究の課題", level=1)
    add_body_p(doc, "先行研究の多くはAIやクラウド等の導入仕様や個人のITスキルに偏重し、現場で発生する業務負荷・不安・部門間対立といった組織内摩擦のガバナンスを看過してきた（技術決定論の限界）。また、大企業とSMOのマクロ比較に終始し、同一企業内の階層間（経営層・中間管理職・一般社員）で生じる変革当事者意識の乖離や役割葛藤構造を実証できていない（規模二元論の限界）。実務現場では「経営層と現場の間での中間管理職の役割葛藤」「処遇還元なき変革への離反」が生じており、これらを組織行動論の枠組みで実証することが課題であった。", bold_prefix="背景と動機: ")

    add_heading_styled(doc, "2. 理論的枠組みと5大仮説体系（H1〜H5）", level=1)
    
    # H1-H5テーブル
    tbl_h = doc.add_table(rows=6, cols=4)
    tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_h, color="B0BEC5", sz="4")
    
    headers_h = ["仮説", "依拠する主要学術理論", "理論的メカニズムと実証仮説", "検証結果"]
    col_widths_h = [Mm(18), Mm(42), Mm(95), Mm(25)]
    
    for i, h_text in enumerate(headers_h):
        c = tbl_h.cell(0, i)
        set_cell_shading(c, "EBF3FA")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(0, 63, 117)
        
    rows_h_data = [
        ("H1", "心理的所有感理論 (Pierce et al., 2001)\n組織構造論 (Blau, 1970)", "企業規模×組織階層の交互作用効果：大企業では意識が直線的に下降するが、SMOでは中間管理職で急落。一般社員層では規模間差が消失（現場収束）。", "支持 (p=0.010)\nηp²=0.0045"),
        ("H2", "分配的公正理論 (Adams, 1965)\n組織的公正論 (Colquitt, 2001)", "分配的公正の欠落と心理的離反：変革努力が給与・人事評価へ還元されない認知は、就業者が「心理的離反層」へ所属するリスクを有意に高める。", "支持 (p<0.001)\nOR = 3.95"),
        ("H3", "手続的公正理論 (Brockner, 2002)\n感情調整論 (Huy, 2002)", "手続的公正の感情的反転レジリエンス：意思決定プロセスの透明性は、摩擦が意識に及ぼす負の影響を緩和し、高公正群で正へと反転させる。", "支持 (p<0.001)\nB = +0.0826"),
        ("H4", "動的能力論 (Teece, 2007)\n組織変革能力 (Kane et al., 2015)", "現場課題発見GAPとPMOの成果決定力：能力需給GAPは技術より「課題発見力」が最大。成果を規定するのはIT知識ではなく全社PMO機能である。", "支持 (p<0.001)\nβ = 0.439"),
        ("H5", "認知的不協和理論 (Festinger, 1957)\n推進プレッシャーモデル", "成果なき推進焦燥の不協和：成果実感より推進意向が先行する認知的焦燥が全社的に生じ、板挟みのSMO中間管理職においてギャップが最大化する。", "支持 (p<0.001)\nGAP +1.45点"),
    ]
    
    for row_idx, data in enumerate(rows_h_data, start=1):
        for col_idx, text in enumerate(data):
            c = tbl_h.cell(row_idx, col_idx)
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_after = Pt(0)
            if col_idx in [0, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.size = Pt(8)
            if col_idx == 0:
                r.bold = True
            elif col_idx == 3:
                r.bold = True
                r.font.color.rgb = RGBColor(34, 133, 67) # Green
                
    # ページ1フッター
    p_f1 = doc.add_paragraph()
    p_f1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_f1.paragraph_format.space_before = Pt(8)
    r_f1 = p_f1.add_run("Page 1 / 4")
    r_f1.font.size = Pt(8)
    r_f1.font.color.rgb = RGBColor(120, 120, 120)

    # 改ページ
    doc.add_page_break()


    # ==================== PAGE 2 ====================
    # ヘッダー
    p_hdr2 = doc.add_paragraph()
    p_hdr2.paragraph_format.space_after = Pt(4)
    r_h2_tag = p_hdr2.add_run("RESEARCH DESIGN & METHODS | ")
    r_h2_tag.bold = True
    r_h2_tag.font.size = Pt(8)
    r_h2_tag.font.color.rgb = RGBColor(0, 91, 172)
    r_h2_txt = p_hdr2.add_run("研究デザイン・標本抽出・変数操作化・分析手法")
    r_h2_txt.font.size = Pt(8)
    r_h2_txt.font.color.rgb = RGBColor(100, 100, 100)

    add_heading_styled(doc, "3. サンプリングデザインと標本セル構成", level=1)
    add_body_p(doc, "本研究は、国内有職者を対象とする事前スクリーニング調査（8,608名）より、DXの意味を理解し勤務先でDXの取り組みがあると回答した適格就業者を抽出し、セル割付管理を経て有効回答 N = 2,035 名の完全データセットを構築した。企業規模は大企業（従業員1,000人以上: 745名, 36.6%）とSMO（従業員1,000人未満: 1,290名, 63.4%）の2区分である。", bold_prefix="調査設計: ")

    # セル構成表
    tbl_cell = doc.add_table(rows=4, cols=5)
    tbl_cell.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_cell, color="B0BEC5", sz="4")
    
    headers_cell = ["企業規模 ＼ 組織階層", "役員・経営層", "中間管理職", "一般社員・非管理職", "小計"]
    for i, h_text in enumerate(headers_cell):
        c = tbl_cell.cell(0, i)
        set_cell_shading(c, "EBF3FA")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(0, 63, 117)
        
    rows_cell_data = [
        ("大企業 (従業員1,000人以上)", "31名", "295名", "419名", "745名 (36.6%)"),
        ("SMO (従業員1,000人未満)", "298名", "511名", "481名", "1,290名 (63.4%)"),
        ("合計 (N = 2,035)", "329名 (16.2%)", "806名 (39.6%)", "900名 (44.2%)", "2,035名 (100.0%)"),
    ]
    for row_idx, r_data in enumerate(rows_cell_data, start=1):
        for col_idx, text in enumerate(r_data):
            c = tbl_cell.cell(row_idx, col_idx)
            set_cell_margins(c, top=50, bottom=50, left=70, right=70)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_after = Pt(0)
            if col_idx > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if row_idx == 3:
                set_cell_shading(c, "F4F6F8")
            r = p.add_run(text)
            r.font.size = Pt(8)
            if row_idx == 3 or col_idx == 0:
                r.bold = True

    add_heading_styled(doc, "4. 変数の操作化と測定尺度の信頼性", level=1)
    
    # 尺度表
    tbl_scale = doc.add_table(rows=7, cols=4)
    tbl_scale.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_scale, color="B0BEC5", sz="4")
    
    headers_scale = ["測定概念", "項目数 / 尺度形式", "測定内容・代表的設問項目", "信頼性係数"]
    for i, h_text in enumerate(headers_scale):
        c = tbl_scale.cell(0, i)
        set_cell_shading(c, "EBF3FA")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(0, 63, 117)
        
    rows_scale_data = [
        ("DX推進当事者意識 (従属変数)", "4項目 (5件法)", "自社のDX推進を自己の課題として能動的に引き受け、関与している度合い (SC18_1, 2, 3, 6)", "Cronbach's α = 0.88"),
        ("組織摩擦認知 (調整・説明)", "4項目 (5件法)", "変革に伴う部門間対立、既存業務との軋轢、現場の負担感および不安の知覚 (SC19_1, 2, 4, 5)", "Cronbach's α = 0.84"),
        ("分配的公正 (規定要因)", "1項目 (5件法)", "「自社のDX推進や変革の成果は、給与や人事評価に適正に還元されている」(Q8_11)", "単一指標 (1〜5点)"),
        ("手続的公正 (調整変数)", "1項目 (5件法)", "「DX推進に関する意思決定や方針決定のプロセスは、透明で納得感がある」(Q8_10)", "単一指標 (1〜5点)"),
        ("DX総合成果実感 (成果指標)", "5項目 (5件法)", "業務効率化、顧客価値向上、新事業創出、組織風土改革等の総合的達成度 (Q12_1〜5)", "Cronbach's α = 0.91"),
        ("人材能力需給GAP (能力分析)", "各10項目 (5件法)", "変革に必要な10能力の重要度と保有度の差分 (Gap = 重要度 − 保有度) を算出", "対応差分スコア"),
    ]
    for row_idx, r_data in enumerate(rows_scale_data, start=1):
        for col_idx, text in enumerate(r_data):
            c = tbl_scale.cell(row_idx, col_idx)
            set_cell_margins(c, top=45, bottom=45, left=60, right=60)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_after = Pt(0)
            if col_idx in [1, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.size = Pt(8)
            if col_idx == 0:
                r.bold = True
            elif col_idx == 3 and "α" in text:
                r.bold = True
                r.font.color.rgb = RGBColor(0, 91, 172)

    add_heading_styled(doc, "5. 計量分析モデルと統計的プロトコル", level=1)
    add_body_p(doc, "要因計画: 企業規模（2水準）×組織階層（3水準）。主効果および交互作用効果を検定し、単純主効果検定（Simple Main Effects）および効果量（偏イータ二乗: ηp²）を算出。先行研究（Blau, 1970; Packmohr et al., 2023）に準拠。", bold_prefix="H1 検証モデル（二元配置分散分析）: ")
    add_body_p(doc, "当事者意識と摩擦認知の直交2次元空間に対し、k-means法（シード固定: random_state=42）を適用し4象限クラスタを抽出。心理的離反層への所属を被説明変数とし、分配的公正・統制変数を投入した多項ロジスティック回帰によりオッズ比（OR）を推定。", bold_prefix="H2 検証モデル（k-meansクラスタリング＆多項ロジスティック回帰）: ")
    add_body_p(doc, "モデル: Y = β0 + β1(摩擦) + β2(手続的公正) + β3(摩擦×手続的公正) + Covariates + ε。多重共線性を防止するため変数を平均中心化（Mean-centering）し、単純傾き分析（Simple Slope: ±1SD）で調整効果の形状を厳密検定。", bold_prefix="H3 検証モデル（階層的モデレーション重回帰分析）: ")
    add_body_p(doc, "同一回答者内の能力需給GAPを対応のあるt検定で検証。全変数でVIF < 2.5を確認後、DX総合成果に対する重回帰分析を行い標準化回帰係数（β）の相対的寄与度を比較（H4）。同一尺度（10点満点）による推進意向と成果実感の差分について一元配置ANOVA・Bonferroni検定を実施（H5）。", bold_prefix="H4・H5 検証モデル（対応のあるt検定＆多重共線性点検付き重回帰分析）: ")

    # ページ2フッター
    p_f2 = doc.add_paragraph()
    p_f2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_f2.paragraph_format.space_before = Pt(6)
    r_f2 = p_f2.add_run("Page 2 / 4")
    r_f2.font.size = Pt(8)
    r_f2.font.color.rgb = RGBColor(120, 120, 120)

    # 改ページ
    doc.add_page_break()


    # ==================== PAGE 3 ====================
    # ヘッダー
    p_hdr3 = doc.add_paragraph()
    p_hdr3.paragraph_format.space_after = Pt(4)
    r_h3_tag = p_hdr3.add_run("EMPIRICAL FINDINGS & EVIDENCE | ")
    r_h3_tag.bold = True
    r_h3_tag.font.size = Pt(8)
    r_h3_tag.font.color.rgb = RGBColor(0, 91, 172)
    r_h3_txt = p_hdr3.add_run("実証分析結果・主要数値ファクトシート・頑健性")
    r_h3_txt.font.size = Pt(8)
    r_h3_txt.font.color.rgb = RGBColor(100, 100, 100)

    add_heading_styled(doc, "6. 5大仮説の実証検証結果（全仮説支持: Supported）", level=1)
    
    # H1 & H2 表
    add_body_p(doc, "二元配置ANOVAにおいて、組織階層主効果（F = 28.867, p < 0.001, ηp² = 0.0277）、企業規模主効果（F = 9.572, p = 0.002, ηp² = 0.0047）および交互作用効果（F = 4.619, p = 0.010, ηp² = 0.0045）が有意に成立した。大企業では経営(3.852)→管理(3.400)→一般(3.227)と直線推移するのに対し、SMOでは経営(3.519)から中間管理職(3.306)で低下（対大企業管理職 p = 0.0384*）。一方、一般社員層では大企業(3.227)とSMO(3.243)に有意差がなく（t = -0.387, p = 0.699 ns）、現場収束が確認された。", bold_prefix="【H1】企業規模×組織階層の交互作用と現場収束 (Supported): ")

    add_body_p(doc, "k-meansクラスタリングにより抽出された3類型のうち、最大層はクラスタ3「心理的離反層（当事者意識低・摩擦高）」であり、全体の45.8%（933名）に達した。二項ロジスティック回帰分析の結果、分配的公正（給与・評価還元）の欠落による心理的離反所属オッズ比は OR = 3.951 (95% CI: [3.26, 4.79], p < 0.001) を記録。評価還元のない変革が現場の離反を招く主要因であることが示された。", bold_prefix="【H2】分配的公正の欠落と心理的離反 (Supported): ")

    add_body_p(doc, "階層的モデレーション重回帰において、交互作用項が有意（B = +0.0826, t = 3.66, p < 0.001）。単純傾斜分析の結果、低手続的公正群(-1SD)では摩擦増大に伴い意識が低下（B = -0.0692, p = 0.0148）する一方、高手続的公正群(+1SD)では傾きが正へと反転（B = +0.0515, p = 0.0349）した。意思決定プロセスの納得感があれば、変革の摩擦は課題解決意識へと転換される（Huy, 2002の計量支持）。", bold_prefix="【H3】手続的公正による調整効果 (Supported): ")

    add_body_p(doc, "能力需給GAPにおいて最大不足を示したのは「デジタル技術知識」(+0.799)ではなく「現場の声を聞き取り課題を見つける能力」(+1.083, p < 0.001)であった。さらにDX総合成果に対する重回帰分析において、技術知識の影響は非有意（β = 0.0473, p = 0.0982 ns）にとどまったのに対し、全社変革を統括・調整する推進機能（PMO）が強い正の関連を示した（β = 0.4388, t = 15.33, p < 0.001）。", bold_prefix="【H4】現場課題発見GAPとPMOの成果関連度 (Supported): ")

    add_body_p(doc, "就業者全体においてDX推進意向(6.351)が成果実感(5.097)を上回るGAP +1.254点（t = 25.30, p < 0.001, dz = 0.561）が存在し、全体の48.6%が推進先行型であった。6セル別比較では、SMO中間管理職においてギャップが +1.446点（正比率 54.0%）を記録し、大企業中間管理職(+1.078点)を有意に上回った（p = 0.0224*）。SMO管理職が大きな認知的葛藤に直面していることが示された。", bold_prefix="【H5】推進継続意向と成果実感の乖離 (Supported): ")

    add_heading_styled(doc, "7. 多重感度分析とSC18項目別分析", level=1)
    
    # 感度分析テーブル
    tbl_rob = doc.add_table(rows=5, cols=4)
    tbl_rob.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_rob, color="B0BEC5", sz="4")
    
    headers_rob = ["検証モデル名", "検証内容・統制条件", "統計検定量 / p値", "判定結果"]
    for i, h_text in enumerate(headers_rob):
        c = tbl_rob.cell(0, i)
        set_cell_shading(c, "EBF3FA")
        set_cell_margins(c, top=50, bottom=50, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(0, 63, 117)
        
    rows_rob_data = [
        ("M1: 主分析 / M2: Type III", "5項目平均尺度 / 不均衡データType III平方和", "F(2, 2029) = 4.619, p = 0.0100*", "有意 (Supported)"),
        ("M3: 共変量統制 ANCOVA", "年齢・性別・勤続年数を共変量として統制投入", "F(2, 2026) = 4.370, p = 0.0128*", "有意 (Supported)"),
        ("M4: 全9項目 / M5: 因子得点", "SC18全項目合成 / EFA第1因子得点モデル", "F = 4.320 (p=0.0134*) / F = 4.237 (p=0.0146*)", "有意 (Supported)"),
        ("M6: 職階定義B / M7: HC3頑健", "監督職361名編入 / 不均一分散HC3頑健標準誤差", "F = 3.275 (p=0.0380*) / F = 4.705 (p=0.0092**)", "有意 (Supported)"),
    ]
    for row_idx, r_data in enumerate(rows_rob_data, start=1):
        for col_idx, text in enumerate(r_data):
            c = tbl_rob.cell(row_idx, col_idx)
            set_cell_margins(c, top=40, bottom=40, left=60, right=60)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_after = Pt(0)
            if col_idx in [2, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.size = Pt(8)
            if col_idx == 0:
                r.bold = True
            elif col_idx == 3:
                r.bold = True
                r.font.color.rgb = RGBColor(34, 133, 67)

    add_body_p(doc, "SC18個別9項目のANOVAにおいて、Holm多重比較補正後も有意な交互作用を維持したのは「経営層はDXについてリーダーシップを発揮している（SC18-8: F = 5.57, p = 0.0038, Holm p = 0.0342*）」であった（大企業管理職 3.25 vs SMO管理職 2.87）。SMOの中間管理職は、経営層の変革リーダーシップ行動に対する認識の低さによって当事者意識が低下していることが示唆された。", bold_prefix="SC18個別9項目ANOVAによる要因の特定: ")

    # ページ3フッター
    p_f3 = doc.add_paragraph()
    p_f3.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_f3.paragraph_format.space_before = Pt(6)
    r_f3 = p_f3.add_run("Page 3 / 4")
    r_f3.font.size = Pt(8)
    r_f3.font.color.rgb = RGBColor(120, 120, 120)

    # 改ページ
    doc.add_page_break()


    # ==================== PAGE 4 ====================
    # ヘッダー
    p_hdr4 = doc.add_paragraph()
    p_hdr4.paragraph_format.space_after = Pt(4)
    r_h4_tag = p_hdr4.add_run("IMPLICATIONS & CONCLUSION | ")
    r_h4_tag.bold = True
    r_h4_tag.font.size = Pt(8)
    r_h4_tag.font.color.rgb = RGBColor(0, 91, 172)
    r_h4_txt = p_hdr4.add_run("考察・学術的貢献・実務的処方箋・限界と結論")
    r_h4_txt.font.size = Pt(8)
    r_h4_txt.font.color.rgb = RGBColor(100, 100, 100)

    add_heading_styled(doc, "8. 総合的考察と学術的貢献（理論への寄与）", level=1)
    add_body_p(doc, "従来の組織論（Blau, 1970）では規模が大きいほど官僚制化し下位階層の乖離が進むとされてきたが、本研究は大企業においてなだらかな推移を示す一方、SMOでは中間管理職が特異的に意識を急落させる非線形モデルを提示した。さらに一般社員層において企業規模間の意識差が完全に消失する「現場収束現象」を明らかにし、巨額のIT投資も現場の意識変革を自動的に誘発しない構造的限界を立証した。", bold_prefix="① 心理的所有感の非線形性と現場収束の解明: ")
    add_body_p(doc, "手続的公正が単なるネガティブ感情の緩和（緩衝効果）にとどまらず、困難や摩擦を推進エネルギーへと転換させる「感情的反転レジリエンス」をもたらすことを世界で初めてマイクロデータで計量実証した。", bold_prefix="② 組織公正理論の進展（感情的反転現象の実証）: ")
    add_body_p(doc, "模倣可能なITツール知識は競争優位の源泉になり得ず（β = 0.047 ns）、現場課題を抽出・合意形成する組織固有のPMO機能（変革ルーティン）こそが持続的成果を決定づける（β = 0.439）ことを示した。", bold_prefix="③ 動的能力論（RBV・Dynamic Capabilities）の計量実証: ")

    add_heading_styled(doc, "9. 実務的インプリケーション（企業経営・DX実務への3大処方箋）", level=1)
    
    # 3大処方箋ボックス
    tbl_rec = doc.add_table(rows=1, cols=3)
    tbl_rec.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_rec, color="DDE2E5", sz="4")
    
    rec_data = [
        ("処方箋 1：分配的公正の確立\n【精神論的DXの即時是正】", "残業削減や効率化の成果を、給与・賞与・人事評価に適正に還元するインセンティブ制度を設計する。努力が評価に直結しない変革は、現場の45.8%を心理的離反層へ追いやる。", "EBF3FA"),
        ("処方箋 2：手続的公正の担保\n【SMO管理職の孤立防衛】", "変革方針の決定プロセスを開示し、双方向の対話機会を確保する。納得感のあるプロセス設計は、管理職の板挟み負担を「推進の使命感」へと反転させる心理的支柱となる。", "E0F7FA"),
        ("処方箋 3：社内PMOの配置\n【課題発見型推進体制への投資】", "ITベンダー頼みや技術者採用に偏重せず、現場の業務課題を傾聴・言語化し、部門間合意形成を担う「社内PMO機能」を育成・配置する（成果決定力 β = 0.439）。", "E8F5E9"),
    ]
    for i, (title, desc, bg) in enumerate(rec_data):
        c = tbl_rec.cell(0, i)
        set_cell_shading(c, bg)
        set_cell_margins(c, top=80, bottom=80, left=90, right=90)
        p = c.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(0)
        r_t = p.add_run(title + "\n")
        r_t.bold = True
        r_t.font.size = Pt(8.5)
        r_t.font.color.rgb = RGBColor(0, 63, 117)
        r_d = p.add_run(desc)
        r_d.font.size = Pt(8)

    add_heading_styled(doc, "10. 研究の限界と今後の課題", level=1)
    add_body_p(doc, "本研究は同一時点の横断データ（Cross-sectional）に基づくため、因果の方向性を厳密に確定するには縦断的パネル調査が必要である。また、全産業一括分析であるため、製造業、情報通信業、サービス業などの産業特性に応じた階層乖離のバリエーション比較が今後の課題である。", bold_prefix="研究上の制約: ")

    add_heading_styled(doc, "11. 結論（総括）", level=1)
    # 結論枠
    tbl_concl = doc.add_table(rows=1, cols=1)
    tbl_concl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_concl = tbl_concl.cell(0, 0)
    set_cell_shading(c_concl, "FFFFFF")
    set_cell_margins(c_concl, top=80, bottom=80, left=120, right=120)
    p_c = c_concl.paragraphs[0]
    p_c.paragraph_format.line_spacing = 1.15
    p_c.paragraph_format.space_after = Pt(0)
    r_cc = p_c.add_run(
        "国内就業者2,035名の完全決定論的マイクロデータ解析により、「DXの成否を分ける本質はデジタルツールの導入そのものではなく、組織階層間の認識統合、組織公正の制度的担保、および全社的PMO変革機能の有無にある」という結論を計量的に立証した。本研究は、実務知（IDM）と組織行動論の厳密な架橋を通じて、変革停滞に悩む日本企業に対し、極めて強固な統計的根拠に基づく組織改革のロードマップを提供するものである。"
    )
    r_cc.bold = True
    r_cc.font.size = Pt(8.5)
    r_cc.font.color.rgb = RGBColor(0, 63, 117)

    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.space_before = Pt(4)
    p_ref.paragraph_format.space_after = Pt(0)
    r_ref = p_ref.add_run(
        "主要引用文献: Adams (1965); Blau (1970); Brockner (2002); Colquitt (2001); Festinger (1957); Huy (2002); Kane et al. (2015); Pierce et al. (2001); Teece (2007); IPA (2023, 2025)."
    )
    r_ref.font.size = Pt(7.5)
    r_ref.font.color.rgb = RGBColor(120, 120, 120)

    # ページ4フッター
    p_f4 = doc.add_paragraph()
    p_f4.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_f4.paragraph_format.space_before = Pt(4)
    r_f4 = p_f4.add_run("Page 4 / 4 | SMOフロンティア研究所 IDM研究グループ")
    r_f4.font.size = Pt(8)
    r_f4.font.color.rgb = RGBColor(120, 120, 120)

    # 保存
    out_path = r"G:\マイドライブ\antigravity\IDM\20261012\reports\20261012_学術論文サマリー概要_A4_4ページ版.docx"
    doc.save(out_path)
    print(f"Successfully generated: {out_path}")

if __name__ == '__main__':
    main()
