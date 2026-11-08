#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_a4_landscape_docx.py
SMOフロンティア研究所 IDM研究会 中間発表用 A4横長1枚完結Wordスライド生成スクリプト
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    """
    kwargs can be top, bottom, left, right
    values: dict(val='single', sz='12', color='005BAC', space='0')
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'<w:{edge} {nsdecls("w")} w:val="{edge_data.get("val","single")}" w:sz="{edge_data.get("sz","4")}" w:space="{edge_data.get("space","0")}" w:color="{edge_data.get("color","auto")}"/>'
        else:
            tag = f'<w:{edge} {nsdecls("w")} w:val="none"/>'
        tcBorders.append(parse_xml(tag))
    tcPr.append(tcBorders)

def create_a4_landscape_docx():
    doc = Document()
    
    # ページ設定: A4 横長 (297mm x 210mm), 余白: 上下左右 10mm
    section = doc.sections[0]
    section.orientation = docx.enum.section.WD_ORIENT.LANDSCAPE
    section.page_width = Mm(297)
    section.page_height = Mm(210)
    section.top_margin = Mm(10)
    section.bottom_margin = Mm(8)
    section.left_margin = Mm(12)
    section.right_margin = Mm(12)

    # スタイル設定
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Noto Sans JP'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(2)
    normal_style.paragraph_format.space_before = Pt(0)

    # 1. タイトルヘッダーテーブル (1行2列)
    header_table = doc.add_table(rows=1, cols=2)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False
    
    # 幅設定: 左側 195mm, 右側 78mm
    header_table.columns[0].width = Mm(195)
    header_table.columns[1].width = Mm(78)

    # 左セル: バッジ + メインタイトル + サブタイトル
    c_left = header_table.cell(0, 0)
    set_cell_margins(c_left, top=40, bottom=60, left=40, right=40)
    set_cell_border(c_left, bottom={'val': 'single', 'sz': '16', 'color': '005BAC'})

    p_badge = c_left.paragraphs[0]
    p_badge.paragraph_format.space_after = Pt(1)
    run_badge = p_badge.add_run("■ SMOフロンティア研究所 IDM研究会 中間発表")
    run_badge.font.size = Pt(8.5)
    run_badge.font.bold = True
    run_badge.font.color.rgb = RGBColor(0x00, 0x5B, 0xAC)

    p_title = c_left.add_paragraph()
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run("中堅・中小企業（SMO）のDX推進と「組織の断絶」")
    run_title.font.size = Pt(15.5)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x00, 0x3F, 0x75)

    p_sub = c_left.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(4)
    run_sub = p_sub.add_run("就業者2,035名の実証調査からみる「中間管理職の孤立」と3つの処方箋")
    run_sub.font.size = Pt(10)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # 右セル: メタ情報
    c_right = header_table.cell(0, 1)
    set_cell_margins(c_right, top=40, bottom=60, left=40, right=40)
    set_cell_border(c_right, bottom={'val': 'single', 'sz': '16', 'color': '005BAC'})
    
    p_meta = c_right.paragraphs[0]
    p_meta.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_meta.paragraph_format.space_after = Pt(1)
    r1 = p_meta.add_run("報告者: IDM研究プロジェクト\n")
    r1.font.bold = True
    r1.font.size = Pt(8.5)
    r2 = p_meta.add_run("調査対象: 全国就業者 2,035名 (全量・全産業)\n")
    r2.font.size = Pt(8)
    r2.font.color.rgb = RGBColor(0x00, 0x5B, 0xAC)
    r3 = p_meta.add_run("大企業: 1,035名 ／ SMO (1,000名未満): 1,000名")
    r3.font.size = Pt(8)
    r3.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    # スペーサー
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_after = Pt(3)
    p_space.paragraph_format.space_before = Pt(0)

    # 2. メイン 3カラム テーブル (1行3列)
    main_table = doc.add_table(rows=1, cols=3)
    main_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    main_table.autofit = False

    # カラム幅: 90mm, 88mm, 95mm (合計 273mm)
    main_table.columns[0].width = Mm(91)
    main_table.columns[1].width = Mm(88)
    main_table.columns[2].width = Mm(94)

    # =========================================================================
    # カラム 1: 何がわかったのか？（実態と真因）
    # =========================================================================
    col1 = main_table.cell(0, 0)
    set_cell_background(col1, "FFFFFF")
    set_cell_margins(col1, top=80, bottom=80, left=100, right=100)
    set_cell_border(col1, 
                    top={'val': 'single', 'sz': '16', 'color': '005BAC'},
                    left={'val': 'single', 'sz': '4', 'color': 'DDE2E5'},
                    right={'val': 'single', 'sz': '4', 'color': 'DDE2E5'},
                    bottom={'val': 'single', 'sz': '4', 'color': 'DDE2E5'})

    p_h1 = col1.paragraphs[0]
    p_h1.paragraph_format.space_after = Pt(4)
    r_h1 = p_h1.add_run("❶ 何がわかったのか？ (実態と真因)")
    r_h1.font.bold = True
    r_h1.font.size = Pt(10.5)
    r_h1.font.color.rgb = RGBColor(0x00, 0x3F, 0x75)

    # カード 1-1: 中間管理職の孤立
    p_c1_1 = col1.add_paragraph()
    p_c1_1.paragraph_format.space_after = Pt(1)
    r = p_c1_1.add_run("【発見①】 中間管理職（課長・部長）の孤立\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0xD3, 0x2F, 0x2F)
    r = p_c1_1.add_run("大企業では職階順に意識が緩やかに推移するのに対し、SMOでは中間管理職の変革当事者意識が最も大きく落ち込む現象が確認されました（一般社員は規模によらず同水準に収束）。")
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # ミニ比較
    p_cmp = col1.add_paragraph()
    p_cmp.paragraph_format.space_after = Pt(3)
    p_cmp.paragraph_format.left_indent = Inches(0.1)
    r = p_cmp.add_run("・大企業: 経営(高) ➔ 管理職(中) ➔ 一般(並)\n")
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x00, 0x5B, 0xAC)
    r = p_cmp.add_run("・SMO: 経営(高) ➔ 管理職(急落・孤立) ➔ 一般")
    r.font.bold = True
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0xD3, 0x2F, 0x2F)

    # カード 1-2: 孤立の主因
    p_c1_2 = col1.add_paragraph()
    p_c1_2.paragraph_format.space_after = Pt(3)
    r = p_c1_2.add_run("【発見②】 孤立の主因は「リーダーシップと評価」\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x00, 0x5B, 0xAC)
    r = p_c1_2.add_run("意識低下の要因は「ITツールの難しさ」ではなく、「経営陣のビジョンやリーダーシップへの疑問（方針が見えない）」と「成果が給与や人事評価に還元されない不満」であることが示唆されました。")
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # カード 1-3: 調整力
    p_c1_3 = col1.add_paragraph()
    p_c1_3.paragraph_format.space_after = Pt(2)
    r = p_c1_3.add_run("【発見③】 IT知識より「組織の調整役」が成否を分ける\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x00, 0x5B, 0xAC)
    r = p_c1_3.add_run("変革の成否を分けるのは高度な先端技術そのものではなく、現場の課題を発見し合意を形成する「調整力・PMO機能」であることが強く示唆されました。")
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # =========================================================================
    # カラム 2: では、どうすればいいのか？（処方箋の提案）
    # =========================================================================
    col2 = main_table.cell(0, 1)
    set_cell_background(col2, "FFFFFF")
    set_cell_margins(col2, top=80, bottom=80, left=100, right=100)
    set_cell_border(col2, 
                    top={'val': 'single', 'sz': '16', 'color': '228543'},
                    left={'val': 'single', 'sz': '4', 'color': 'DDE2E5'},
                    right={'val': 'single', 'sz': '4', 'color': 'DDE2E5'},
                    bottom={'val': 'single', 'sz': '4', 'color': 'DDE2E5'})

    p_h2 = col2.paragraphs[0]
    p_h2.paragraph_format.space_after = Pt(2)
    r_h2 = p_h2.add_run("❷ では、どうすればいいか？ (処方箋)")
    r_h2.font.bold = True
    r_h2.font.size = Pt(10.5)
    r_h2.font.color.rgb = RGBColor(0x22, 0x85, 0x43)

    p_sub2 = col2.add_paragraph()
    p_sub2.paragraph_format.space_after = Pt(3)
    r = p_sub2.add_run("※中間管理職を板挟み・丸投げにしない3つのアプローチ案")
    r.font.size = Pt(7.5)
    r.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    # 処方箋 A
    p_rx1 = col2.add_paragraph()
    p_rx1.paragraph_format.space_after = Pt(3)
    r = p_rx1.add_run("【処方箋A】 変革の労力を正当に評価・還元する\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x22, 0x85, 0x43)
    r = p_rx1.add_run("DX推進を既存業務の「上乗せの雑務」にせず、変革への挑戦や業務改善の取り組みそのものを人事評価や処遇に直結させます（「頑張っても報われない」不公平感の払拭）。")
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # 処方箋 B
    p_rx2 = col2.add_paragraph()
    p_rx2.paragraph_format.space_after = Pt(3)
    r = p_rx2.add_run("【処方箋B】 「ミニ推進・調整役（PMO）」の設置\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x22, 0x85, 0x43)
    r = p_rx2.add_run("現場の課長一人に背負わせず、経営の方針を現場目線に翻訳し、現場の悩みを経営へ届ける「交通整理役」を小さくても社内に公式配置します（専任でなく兼任・若手抜擢でも有効）。")
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # 処方箋 C
    p_rx3 = col2.add_paragraph()
    p_rx3.paragraph_format.space_after = Pt(2)
    r = p_rx3.add_run("【処方箋C】 決定プロセスの透明化と納得感\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x22, 0x85, 0x43)
    r = p_rx3.add_run("トップダウンの一方的な号令ではなく、「なぜ導入するのか」「現場の声がどう反映されたか」を丁寧に共有することで、現場の抵抗感が前向きな協力姿勢へ転換することが実証されています。")
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # =========================================================================
    # カラム 3: 限界と今後の課題・皆様との討議
    # =========================================================================
    col3 = main_table.cell(0, 2)
    set_cell_background(col3, "FFFFFF")
    set_cell_margins(col3, top=80, bottom=80, left=100, right=100)
    set_cell_border(col3, 
                    top={'val': 'single', 'sz': '16', 'color': '00838F'},
                    left={'val': 'single', 'sz': '4', 'color': 'DDE2E5'},
                    right={'val': 'single', 'sz': '4', 'color': 'DDE2E5'},
                    bottom={'val': 'single', 'sz': '4', 'color': 'DDE2E5'})

    p_h3 = col3.paragraphs[0]
    p_h3.paragraph_format.space_after = Pt(4)
    r_h3 = p_h3.add_run("❸ 限界と今後の課題 (意見交換の論点)")
    r_h3.font.bold = True
    r_h3.font.size = Pt(10.5)
    r_h3.font.color.rgb = RGBColor(0x00, 0x83, 0x8F)

    # 研究の限界
    p_lim = col3.add_paragraph()
    p_lim.paragraph_format.space_after = Pt(3)
    r = p_lim.add_run("【現時点の研究限界】\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x00, 0x83, 0x8F)
    r = p_lim.add_run("① 因果の前後関係: 一時点の調査データであるため、「意識が低いからDXが進まないのか」「進まないから意識が低下したのか」の時系列追跡が今後の課題です。\n② 業種特性の差: 製造・IT・伝統産業など、業種による組織構造の固有パターンのさらなる類型化が必要です。")
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # ディスカッション起爆テーマ
    p_disc_box = col3.add_paragraph()
    p_disc_box.paragraph_format.space_after = Pt(2)
    r = p_disc_box.add_run("【💬 本日の意見交換テーマ (皆様へのお伺い)】\n")
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0xB7, 0x81, 0x03)
    
    r = p_disc_box.add_run("▶ 問い1: 皆様のご専門や現場の知見から見て、SMOの中間管理職が「孤立のサンドバッグ」にならず、自発的に動き出すために最も効果的な後押しは何だとお考えでしょうか？\n")
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x3E, 0x27, 0x23)

    r = p_disc_box.add_run("▶ 問い2: リソースに余裕がない中堅・中小企業において、経営と現場のハブとなる「推進・調整役（ミニPMO）」を現実的にどう生み出すべきでしょうか？（兼任、外部伴走、若手抜擢など）")
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x3E, 0x27, 0x23)

    # 3. フッター (1行2列)
    footer_table = doc.add_table(rows=1, cols=2)
    footer_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    footer_table.autofit = False
    footer_table.columns[0].width = Mm(200)
    footer_table.columns[1].width = Mm(73)

    fc_left = footer_table.cell(0, 0)
    set_cell_margins(fc_left, top=30, bottom=10, left=20, right=20)
    set_cell_border(fc_left, top={'val': 'single', 'sz': '4', 'color': 'DDE2E5'})
    pf_l = fc_left.paragraphs[0]
    rf_l = pf_l.add_run("※ 本報告は多重統計分析に基づき、特定手法に依存しない頑健性を確認した上で要点を平易に再構成したものです。")
    rf_l.font.size = Pt(7.5)
    rf_l.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    fc_right = footer_table.cell(0, 1)
    set_cell_margins(fc_right, top=30, bottom=10, left=20, right=20)
    set_cell_border(fc_right, top={'val': 'single', 'sz': '4', 'color': 'DDE2E5'})
    pf_r = fc_right.paragraphs[0]
    pf_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    rf_r = pf_r.add_run("SMOフロンティア研究所 IDM研究会 中間発表資料")
    rf_r.font.bold = True
    rf_r.font.size = Pt(7.5)
    rf_r.font.color.rgb = RGBColor(0x00, 0x5B, 0xAC)

    # 保存
    base_dir = r"G:\マイドライブ\antigravity\IDM\20261030\reports"
    os.makedirs(base_dir, exist_ok=True)
    out_docx = os.path.join(base_dir, "20261030_SMO研究会中間発表_A4横長1枚スライド.docx")
    doc.save(out_docx)
    print(f"Generated DOCX slide: {out_docx}")

if __name__ == "__main__":
    create_a4_landscape_docx()
