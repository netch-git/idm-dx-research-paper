#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pptx_slide.py
SMOフロンティア研究所 IDM研究会 中間発表用 1枚完結PowerPointスライド生成スクリプト
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_slide():
    prs = Presentation()
    # 16:9 ワイドスクリーン設定 (13.333 x 7.5 インチ)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # 空白レイアウトの取得
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # 背景色の設定 (Light Gray: #F8F9FA)
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0xF8, 0xF9, 0xFA)

    # DADS カラー定数
    C_PRIMARY_DARK = RGBColor(0x00, 0x3F, 0x75)
    C_PRIMARY = RGBColor(0x00, 0x5B, 0xAC)
    C_PRIMARY_LIGHT = RGBColor(0xEB, 0xF3, 0xFA)
    C_SECONDARY = RGBColor(0x00, 0x83, 0x8F)
    C_SECONDARY_LIGHT = RGBColor(0xE0, 0xF7, 0xFA)
    C_SUCCESS = RGBColor(0x22, 0x85, 0x43)
    C_SUCCESS_LIGHT = RGBColor(0xE8, 0xF5, 0xE9)
    C_ALERT = RGBColor(0xD3, 0x2F, 0x2F)
    C_ALERT_LIGHT = RGBColor(0xFF, 0xEB, 0xEE)
    C_WARNING_BG = RGBColor(0xFF, 0xF8, 0xE1)
    C_WARNING_BORDER = RGBColor(0xFB, 0xC0, 0x2D)
    C_WARNING_TEXT = RGBColor(0x79, 0x55, 0x48)
    C_TEXT = RGBColor(0x1A, 0x1A, 0x1A)
    C_TEXT_SUB = RGBColor(0x4A, 0x55, 0x68)
    C_TEXT_MUTED = RGBColor(0x71, 0x80, 0x96)
    C_BORDER = RGBColor(0xDD, 0xE2, 0xE5)
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

    FONT_FAMILY = "Noto Sans JP"

    # =========================================================================
    # 1. ヘッダー領域
    # =========================================================================
    # ヘッダー背景バー
    header_box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.35), Inches(12.333), Inches(0.95)
    )
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = C_WHITE
    header_box.line.color.rgb = C_BORDER
    header_box.line.width = Pt(1)

    # 左側：バッジ + タイトル + サブタイトル
    tf_hl = header_box.text_frame
    tf_hl.word_wrap = True
    tf_hl.margin_left = Inches(0.2)
    tf_hl.margin_top = Inches(0.08)
    tf_hl.margin_right = Inches(3.2)
    tf_hl.margin_bottom = Inches(0.05)

    p_badge = tf_hl.paragraphs[0]
    p_badge.space_after = Pt(1)
    r_badge = p_badge.add_run()
    r_badge.text = "SMOフロンティア研究所 IDM研究会 中間発表"
    r_badge.font.name = FONT_FAMILY
    r_badge.font.size = Pt(8.5)
    r_badge.font.bold = True
    r_badge.font.color.rgb = C_PRIMARY

    p_title = tf_hl.add_paragraph()
    p_title.space_after = Pt(1)
    r_title = p_title.add_run()
    r_title.text = "中堅・中小企業（SMO）のDX推進と「組織の断絶」"
    r_title.font.name = FONT_FAMILY
    r_title.font.size = Pt(15.5)
    r_title.font.bold = True
    r_title.font.color.rgb = C_PRIMARY_DARK

    p_sub = tf_hl.add_paragraph()
    r_sub = p_sub.add_run()
    r_sub.text = "就業者2,035名の実証調査からみる「中間管理職の孤立」と3つの処方箋"
    r_sub.font.name = FONT_FAMILY
    r_sub.font.size = Pt(9.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = C_TEXT_SUB

    # 右側：メタ情報テキストボックス
    meta_box = slide.shapes.add_textbox(
        Inches(9.2), Inches(0.38), Inches(3.5), Inches(0.88)
    )
    tf_meta = meta_box.text_frame
    tf_meta.word_wrap = True
    tf_meta.margin_left = Inches(0.1)
    tf_meta.margin_top = Inches(0.05)
    tf_meta.margin_right = Inches(0.15)

    p_m1 = tf_meta.paragraphs[0]
    p_m1.alignment = PP_ALIGN.RIGHT
    r_m1 = p_m1.add_run()
    r_m1.text = "報告者: IDM研究プロジェクト\n"
    r_m1.font.name = FONT_FAMILY
    r_m1.font.size = Pt(8.5)
    r_m1.font.bold = True
    r_m1.font.color.rgb = C_TEXT

    r_m2 = p_m1.add_run()
    r_m2.text = "調査対象: 全国正規就業者 2,035名 (全産業)\n"
    r_m2.font.name = FONT_FAMILY
    r_m2.font.size = Pt(8)
    r_m2.font.bold = True
    r_m2.font.color.rgb = C_PRIMARY

    r_m3 = p_m1.add_run()
    r_m3.text = "大企業: 1,035名 ／ SMO (1,000名未満): 1,000名"
    r_m3.font.name = FONT_FAMILY
    r_m3.font.size = Pt(8)
    r_m3.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # 2. メイン 3カラム設定
    # =========================================================================
    col_width = Inches(3.91)
    col_height = Inches(5.42)
    gap = Inches(0.30)
    col_top = Inches(1.42)

    col1_left = Inches(0.5)
    col2_left = col1_left + col_width + gap
    col3_left = col2_left + col_width + gap

    # -------------------------------------------------------------------------
    # カラム 1: ❶ 何がわかったのか？（実態と真因）
    # -------------------------------------------------------------------------
    # カラムコンテナ外枠
    c1_panel = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, col1_left, col_top, col_width, col_height
    )
    c1_panel.fill.solid()
    c1_panel.fill.fore_color.rgb = C_WHITE
    c1_panel.line.color.rgb = C_BORDER
    c1_panel.line.width = Pt(1)

    # カラムヘッダー帯
    c1_hdr = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, col1_left, col_top, col_width, Inches(0.40)
    )
    c1_hdr.fill.solid()
    c1_hdr.fill.fore_color.rgb = C_PRIMARY_LIGHT
    c1_hdr.line.color.rgb = C_PRIMARY
    c1_hdr.line.width = Pt(1.5)
    tf1_h = c1_hdr.text_frame
    tf1_h.margin_left = Inches(0.15)
    p = tf1_h.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = "❶ 何がわかったのか？ (実態と真因)"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = C_PRIMARY_DARK

    # カラム1 コンテンツ (カード1-1, ミニ比較, カード1-2, カード1-3)
    c1_tb = slide.shapes.add_textbox(
        col1_left + Inches(0.12), col_top + Inches(0.45), col_width - Inches(0.24), col_height - Inches(0.50)
    )
    tf1 = c1_tb.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.05)
    tf1.margin_right = Inches(0.05)
    tf1.margin_top = Inches(0.05)
    tf1.margin_bottom = Inches(0.05)

    # 発見①
    p = tf1.paragraphs[0]
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "① 中間管理職（課長・部長）の孤立 "
    r.font.name = FONT_FAMILY
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_ALERT
    r_tag = p.add_run()
    r_tag.text = "【有意差を確認】\n"
    r_tag.font.name = FONT_FAMILY
    r_tag.font.size = Pt(8)
    r_tag.font.bold = True
    r_tag.font.color.rgb = C_PRIMARY

    r = p.add_run()
    r.text = "大企業では職階順に意識が推移するのに対し、SMOでは中間管理職の変革当事者意識が最も大きく落ち込む現象が確認されました（一般社員は企業規模によらず同水準に収束）。"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(8.5)
    r.font.color.rgb = C_TEXT_SUB

    # ミニ比較ボックス
    p = tf1.add_paragraph()
    p.space_before = Pt(3)
    p.space_after = Pt(4)
    r = p.add_run()
    r.text = "┌────────────────────────────┐\n"
    r.font.size = Pt(7)
    r.font.color.rgb = C_BORDER
    r1 = p.add_run()
    r1.text = "  ・大企業: 経営(高) ➔ 管理職(中) ➔ 一般社員(並)\n"
    r1.font.name = FONT_FAMILY
    r1.font.size = Pt(7.8)
    r1.font.color.rgb = C_PRIMARY
    r2 = p.add_run()
    r2.text = "  ・SMO   : 経営(高) ➔ 管理職(急落・孤立) ➔ 一般\n"
    r2.font.name = FONT_FAMILY
    r2.font.size = Pt(7.8)
    r2.font.bold = True
    r2.font.color.rgb = C_ALERT
    r = p.add_run()
    r.text = "└────────────────────────────┘"
    r.font.size = Pt(7)
    r.font.color.rgb = C_BORDER

    # 発見②
    p = tf1.add_paragraph()
    p.space_before = Pt(3)
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "② 孤立の主因は「リーダーシップと評価」 "
    r.font.name = FONT_FAMILY
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_PRIMARY
    r_tag = p.add_run()
    r_tag.text = "【統計的に示唆】\n"
    r_tag.font.name = FONT_FAMILY
    r_tag.font.size = Pt(8)
    r_tag.font.bold = True
    r_tag.font.color.rgb = C_PRIMARY

    r = p.add_run()
    r.text = "意識低下の要因は「ITツールの難しさ」ではなく、「経営陣のビジョンやリーダーシップへの疑問（方針が見えない）」と「成果が給与や人事評価に還元されない不満」であることが示唆されました。"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(8.5)
    r.font.color.rgb = C_TEXT_SUB

    # 発見③
    p = tf1.add_paragraph()
    p.space_before = Pt(5)
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "③ IT知識より「組織の調整役」が成否を分ける "
    r.font.name = FONT_FAMILY
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_PRIMARY
    r_tag = p.add_run()
    r_tag.text = "【強い影響を示唆】\n"
    r_tag.font.name = FONT_FAMILY
    r_tag.font.size = Pt(8)
    r_tag.font.bold = True
    r_tag.font.color.rgb = C_PRIMARY

    r = p.add_run()
    r.text = "変革の成否を分けるのは高度な先端IT知識そのものではなく、現場の課題を発見し合意を形成する「調整力・PMO機能」であることが強く示唆されました。"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(8.5)
    r.font.color.rgb = C_TEXT_SUB

    # -------------------------------------------------------------------------
    # カラム 2: ❷ では、どうすればいいのか？（処方箋）
    # -------------------------------------------------------------------------
    c2_panel = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, col2_left, col_top, col_width, col_height
    )
    c2_panel.fill.solid()
    c2_panel.fill.fore_color.rgb = C_WHITE
    c2_panel.line.color.rgb = C_BORDER
    c2_panel.line.width = Pt(1)

    c2_hdr = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, col2_left, col_top, col_width, Inches(0.40)
    )
    c2_hdr.fill.solid()
    c2_hdr.fill.fore_color.rgb = C_SUCCESS_LIGHT
    c2_hdr.line.color.rgb = C_SUCCESS
    c2_hdr.line.width = Pt(1.5)
    tf2_h = c2_hdr.text_frame
    tf2_h.margin_left = Inches(0.15)
    p = tf2_h.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = "❷ では、どうすればいいのか？ (処方箋)"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = C_SUCCESS

    c2_tb = slide.shapes.add_textbox(
        col2_left + Inches(0.12), col_top + Inches(0.45), col_width - Inches(0.24), col_height - Inches(0.50)
    )
    tf2 = c2_tb.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.05)
    tf2.margin_right = Inches(0.05)
    tf2.margin_top = Inches(0.05)
    tf2.margin_bottom = Inches(0.05)

    p = tf2.paragraphs[0]
    p.space_after = Pt(6)
    r = p.add_run()
    r.text = "※中間管理職を板挟み・丸投げにしない3つのアプローチ案"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(8)
    r.font.color.rgb = C_TEXT_MUTED

    # 処方箋 A
    p = tf2.add_paragraph()
    p.space_before = Pt(4)
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "処方箋 A: 変革の労力を正当に評価・還元する\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_SUCCESS
    r = p.add_run()
    r.text = "DX推進を既存業務の「上乗せの雑務」にせず、変革への挑戦や業務改善の取り組みそのものを人事評価や処遇に直結させます（「頑張っても報われない」不公平感の払拭）。"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(8.5)
    r.font.color.rgb = C_TEXT_SUB

    # 処方箋 B
    p = tf2.add_paragraph()
    p.space_before = Pt(8)
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "処方箋 B: 「ミニ推進・調整役（PMO）」の設置\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_SUCCESS
    r = p.add_run()
    r.text = "現場の課長一人に背負わせず、経営の方針を現場目線に翻訳し、現場の悩みを経営へ届ける「交通整理役」を小さくても社内に公式配置します（専任でなく兼任・若手抜擢でも有効）。"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(8.5)
    r.font.color.rgb = C_TEXT_SUB

    # 処方箋 C
    p = tf2.add_paragraph()
    p.space_before = Pt(8)
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "処方箋 C: 決定プロセスの透明化と納得感\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_SUCCESS
    r = p.add_run()
    r.text = "トップダウンの一方的な号令だけでなく、「なぜ導入するのか」「現場の声がどう反映されたか」を丁寧に共有することで、現場の抵抗感が前向きな協力姿勢へ転換することが実証されています。"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(8.5)
    r.font.color.rgb = C_TEXT_SUB

    # -------------------------------------------------------------------------
    # カラム 3: ❸ 限界と今後の課題（意見交換の論点）
    # -------------------------------------------------------------------------
    c3_panel = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, col3_left, col_top, col_width, col_height
    )
    c3_panel.fill.solid()
    c3_panel.fill.fore_color.rgb = C_WHITE
    c3_panel.line.color.rgb = C_BORDER
    c3_panel.line.width = Pt(1)

    c3_hdr = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, col3_left, col_top, col_width, Inches(0.40)
    )
    c3_hdr.fill.solid()
    c3_hdr.fill.fore_color.rgb = C_SECONDARY_LIGHT
    c3_hdr.line.color.rgb = C_SECONDARY
    c3_hdr.line.width = Pt(1.5)
    tf3_h = c3_hdr.text_frame
    tf3_h.margin_left = Inches(0.15)
    p = tf3_h.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = "❸ 限界と今後の課題 (意見交換の論点)"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = C_SECONDARY

    c3_tb = slide.shapes.add_textbox(
        col3_left + Inches(0.12), col_top + Inches(0.45), col_width - Inches(0.24), col_height - Inches(0.50)
    )
    tf3 = c3_tb.text_frame
    tf3.word_wrap = True
    tf3.margin_left = Inches(0.05)
    tf3.margin_right = Inches(0.05)
    tf3.margin_top = Inches(0.05)
    tf3.margin_bottom = Inches(0.05)

    # 現時点の研究限界
    p = tf3.paragraphs[0]
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "【現時点における研究の限界】\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_SECONDARY

    r = p.add_run()
    r.text = "① 因果の前後関係:\n一時点の調査データであるため、「意識が低いからDXが進まないのか」「進まないから意識が低下したのか」の時系列追跡が今後の課題です。\n\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(8.2)
    r.font.color.rgb = C_TEXT_SUB

    r = p.add_run()
    r.text = "② 業種・業態の差:\nSMOの中でも製造・IT・サービス・伝統産業など業種による固有パターンの詳細な類型化が求められます。"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(8.2)
    r.font.color.rgb = C_TEXT_SUB

    # 討論起爆ボックス
    p = tf3.add_paragraph()
    p.space_before = Pt(8)
    p.space_after = Pt(2)
    r = p.add_run()
    r.text = "【💬 本日の意見交換テーマ (皆様へのお伺い)】\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xB7, 0x81, 0x03)

    r = p.add_run()
    r.text = "▶ 問い 1:\n「皆様のご専門や現場の知見から見て、SMOの中間管理職が『孤立のサンドバッグ』にならず、自発的に動き出すために最も効果的な後押しは何だとお考えでしょうか？」\n\n"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(8.2)
    r.font.color.rgb = C_WARNING_TEXT

    r = p.add_run()
    r.text = "▶ 問い 2:\n「リソースに余裕がない中堅・中小企業において、経営と現場のハブとなる『推進・調整役（ミニPMO）』を現実的にどう生み出すべきでしょうか？（兼任、外部伴走、若手抜擢など）」"
    r.font.name = FONT_FAMILY
    r.font.size = Pt(8.2)
    r.font.color.rgb = C_WARNING_TEXT

    # =========================================================================
    # 3. フッター領域
    # =========================================================================
    footer_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(6.92), Inches(12.333), Inches(0.40)
    )
    tf_f = footer_box.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = Inches(0.1)
    tf_f.margin_top = Inches(0.05)
    tf_f.margin_right = Inches(0.1)

    p_f = tf_f.paragraphs[0]
    r_fl = p_f.add_run()
    r_fl.text = "※ 本報告は多重統計分析に基づき、特定手法に依存しない頑健性を確認した上で要点を平易に再構成したものです。（統制変数投入後も有意性を維持）"
    r_fl.font.name = FONT_FAMILY
    r_fl.font.size = Pt(7.8)
    r_fl.font.color.rgb = C_TEXT_MUTED

    r_fr = p_f.add_run()
    r_fr.text = "       SMOフロンティア研究所 IDM研究会 中間発表資料 (1枚完結版)"
    r_fr.font.name = FONT_FAMILY
    r_fr.font.size = Pt(7.8)
    r_fr.font.bold = True
    r_fr.font.color.rgb = C_PRIMARY

    # 保存
    base_dir = r"G:\マイドライブ\antigravity\IDM\20261030\reports"
    os.makedirs(base_dir, exist_ok=True)
    out_pptx = os.path.join(base_dir, "20261030_SMO研究会中間発表_A4横長1枚スライド.pptx")
    prs.save(out_pptx)
    print(f"Generated PPTX slide: {out_pptx}")

if __name__ == "__main__":
    create_slide()
