import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_border(cell, **kwargs):
    """
    APA 形式の罫線（上部・下部のみ、縦罫線なし）を設定
    kwargs: top, bottom, left, right (e.g. sz=12, val='single', color='000000')
    """
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(r'<w:tcBorders {}/>'.format(nsdecls('w')))
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = parse_xml(r'<{} {} w:val="{}" w:sz="{}" w:space="0" w:color="{}"/>'.format(
                tag, nsdecls('w'),
                edge_data.get('val', 'single'),
                edge_data.get('sz', '4'),
                edge_data.get('color', 'auto')
            ))
            tcBorders.append(element)
    tcPr.append(tcBorders)

def create_submission_docx():
    doc = docx.Document()
    
    # ページ余白 (標準 1インチ = 25.4mm)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    # 基本フォント設定 (明朝体 + Times New Roman)
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(11)
    normal_style.paragraph_format.line_spacing = 1.35
    normal_style.paragraph_format.space_after = Pt(6)

    # 1. 表紙 (Title Page)
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("企業規模と組織階層がDX推進意識および組織摩擦認知に及ぼす影響：\n2,035名の就業者データに基づく二元配置分散分析と階層乖離ダイナミクス")
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(11, 37, 69)

    p_title_en = doc.add_paragraph()
    p_title_en.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title_en = p_title_en.add_run("Effects of Firm Size and Hierarchical Level on DX Promotion Consciousness and Organizational Friction: A Two-Way ANOVA Study of 2,035 Japanese Employees")
    run_title_en.font.size = Pt(12)
    run_title_en.font.italic = True
    run_title_en.font.color.rgb = RGBColor(80, 80, 80)

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_author = p_author.add_run("IDM デジタル変革調査研究グループ\n(IDM Digital Transformation Research Consortium)")
    run_author.font.size = Pt(11)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_meta = p_meta.add_run("投稿用正式原稿 (Formal Peer-Review Submission Manuscript)\n作成日: 2026年10月6日")
    run_meta.font.size = Pt(9.5)
    run_meta.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 要約 (Abstract)
    h_abs = doc.add_heading("要約 (Abstract)", level=2)
    h_abs.paragraph_format.space_before = Pt(12)
    
    p_abs = doc.add_paragraph()
    p_abs.paragraph_format.line_spacing = 1.25
    p_abs.add_run(
        "本研究は、日本国内の就業者2,035名を対象とした全量データに基づき、企業規模（大企業 n = 745 名 vs 中小企業 n = 1,290 名）および組織階層（経営層 n = 329 名、部課長クラス n = 806 名、一般社員 n = 900 名）が、DXに対する推進意識・心理的所有感（SC18合成スコア、9項目、α = 0.859）およびDXに伴うリスク懸念・組織摩擦認知（SC15合成スコア、9項目、α = 0.818）に及ぼす影響を二元配置分散分析（Type II ANOVA）および層別単純主効果検定により厳密に検証した。\n"
        "分析の結果、DX推進意識（SC18）においては、企業規模主効果（F(1, 2029) = 8.04, p = 0.0046, η²p = 0.0039）、職制主効果（F(2, 2029) = 38.58, p = 3.60 × 10⁻¹⁷, η²p = 0.0366）、および交互作用効果（F(2, 2029) = 4.32, p = 0.0134, η²p = 0.0042）のすべてが統計的に有意であった。単純主効果分析により、経営層（大企業 M = 3.77 vs 中小 M = 3.48, p = 0.0200, g = 0.44）および部課長クラス（大企業 M = 3.37 vs 中小 M = 3.22, p = 0.0010, g = 0.24）では大企業が有意に高い推進意識を示す一方、一般社員層では企業規模による有意差が完全に消失し（大企業 M = 3.18 vs 中小 M = 3.18, p = 0.9032, g = 0.01）、現場の意識が低位収束している実態（現場収束現象）が明らかとなった。\n"
        "さらに補完的従属変数である組織摩擦認知（SC15）においては、規模主効果は有意でなかったが（F(1, 2029) = 1.97, p = 0.1601, η²p = 0.0010）、職制主効果（F(2, 2029) = 61.98, p = 7.44 × 10⁻²⁷, η²p = 0.0576）と交互作用効果（F(2, 2029) = 5.79, p = 0.0031, η²p = 0.0057）が極めて顕著に有意であった。特筆すべきは中小企業における階層乖離であり、中小企業の経営層はリスク・摩擦認知が極端に低い（M = 2.69）のに対し、部課長クラス（M = 3.10）および一般社員（M = 3.18）は高い摩擦を認知しており（経営層との乖離 p < 0.001, g = 0.79）、経営層の過度な楽観主義バイアスと現場の負担感との間に深刻な構造的断絶が存在することが実証された。また、推進意識と摩擦認知の相関は r = -0.0901（p < 0.001）と微弱であり、両者が心理的に独立した直交次元を形成していることが示された。"
    )

    p_kw = doc.add_paragraph()
    run_kw_label = p_kw.add_run("キーワード: ")
    run_kw_label.bold = True
    p_kw.add_run("デジタルトランスフォーメーション (DX), 企業規模, 職制グループ, 二元配置分散分析, 心理的所有感, 組織摩擦, 現場収束現象, 直交ダイナミクス")

    doc.add_page_break()

    # 2. 本文 (Main Text)
    # 1. 序論
    h1 = doc.add_heading("1. 序論 (Introduction)", level=1)
    h1.paragraph_format.space_before = Pt(12)
    
    doc.add_paragraph(
        "デジタル技術を活用した業務プロセスの変革やビジネスモデルの再構築を目指すデジタルトランスフォーメーション（Digital Transformation: DX）は、企業の持続的競争優位性を左右する最重要経営課題となっている（Kane et al., 2015）。しかし、多くの組織においてDX推進は順調に進展しておらず、経済産業省が警鐘を鳴らす「2025年の崖」問題や組織内の抵抗に直面している。先行研究は、DXの成否を決定づける要因として、単なる技術導入の多寡にとどまらず、組織構成員の変革受容性、推進意識、および組織内摩擦のマネジメントが不可欠であることを示唆している（Papadopoulos et al., 2020）。"
    )
    doc.add_paragraph(
        "特に、企業規模（大企業 vs 中小企業）と組織階層（経営層、管理職層、一般社員層）がDX認識に及ぼす影響については、理論的に強い関心が寄せられている。大企業は豊富な資金・人材リソースを背景にDXを戦略的に推進する体制を整えやすい一方で、組織の階層性や官僚主義が現場への浸透を阻害する可能性がある。対照的に、中小企業（SMEs）は機動性や経営者のリーダーシップが直接的に組織を動かす力を持つ反面、デジタル投資余力や専門人材の不足という構造的制約を抱えている（Eller et al., 2020; Garzoni et al., 2020）。"
    )
    doc.add_paragraph(
        "さらに、組織内の「階層（職制）」による視点の相違は、DX推進における致命的な摩擦を生み出す要因となる。経営層がデジタル変革を自社の将来戦略として捉える一方で、実務の変革を直接担う部課長クラスはリソース配分や業務負荷の増大に直面し、一般社員は雇用の安定性や既存スキルの陳腐化に対する懸念を抱きやすい。"
    )
    doc.add_paragraph(
        "先行研究の多くは、定性的な事例分析や特定の階層（主に経営者やIT担当役員）のみを対象としたアンケート調査に依存しており、同一組織コンテキストにおける企業規模と複数階層の「交差（交互作用）」を全量統計的に検証した実証知見は極めて乏しい。本研究では、国内2,035名の就業者から得られたマイクロデータを対象とし、企業規模（2水準）と職制（3水準）の要因配置に基づく二元配置分散分析（Two-Way ANOVA）を実行することで、以下のリサーチ・クエスチョン（RQ）を解明することを目的とする。\n"
        "• RQ1: DX推進意識・心理的所有感（SC18）において、企業規模および組織階層による主効果、ならびに両者の交互作用効果が存在するか。\n"
        "• RQ2: DXに伴うリスク懸念・組織摩擦認知（SC15）において、企業規模および組織階層による差異はどのように発現し、推進意識とどのように連動しているか。\n"
        "• RQ3: 大企業と中小企業において、階層間の認識乖離パターンにはどのような構造的特異性が見られるか。"
    )

    # 2. 文献レビューと仮説構築
    h2 = doc.add_heading("2. 文献レビューと仮説構築 (Literature Review & Hypotheses)", level=1)
    h2.paragraph_format.space_before = Pt(12)

    doc.add_heading("2.1 企業規模とDX推進（大企業 vs 中小企業）", level=2)
    doc.add_paragraph(
        "組織能力論および資源依拠観点（RBV）において、デジタル技術の導入と活用は組織の吸収能力（Absorptive Capacity）および動的能力（Dynamic Capabilities）に依存する。大企業は、デジタル専門部署の設置、外部コンサルタントの活用、および体系的なリスキリングプログラムを展開する資源余力を有するため、全体的なDX推進意識が高まりやすい。"
    )
    doc.add_paragraph(
        "一方で、中小企業に関する近年の実証研究は、中小企業におけるDX推進が経営者の個人的ビジョンと直接的な推進力に強く依存していることを指摘している。Omrani et al. (2024) は、EU域内15,346社の中小企業データを分析し、TOE枠組みに基づきITインフラや既存の革新水準がDX推進の決定的要因であることを立証している。また、AlNuaimi et al. (2022) は組織の敏捷性（アジリティ）とデジタル戦略の整合における変革型リーダーシップの決定的役割を論じ、経営層の戦略的コミットメントの重要性を強調している。さらに、日本企業における実態調査として Liu et al. (2021) は、製薬企業営業部門におけるDX推進課題を分析し、現場部門が直面する特有の組織摩擦を報告している。しかし、現場レベルにおいてはデジタルツール導入に伴う初期負担や業務プロセスの混乱に対する耐性が大企業よりも低いため、組織全体としての一体感を維持することは容易ではない（Roman & Rusu, 2022）。"
    )

    doc.add_heading("2.2 組織階層と心理的所有感・組織摩擦", level=2)
    doc.add_paragraph(
        "心理的所有感理論（Psychological Ownership Theory; Pierce et al., 2001）によれば、個人が変革対象に対して「自己の目標」「我々の組織の将来」としての所有感を抱くとき、変革への積極的参画が促進される。DXにおいて、経営層は変革の決定権と全体像を把握しているため、最も高い心理的所有感を持つ。他方、中堅管理職（部課長クラス）は経営方針と現場実務の板挟みとなり、現場社員は受動的な業務変更を強いられるため、所有感は階層が下降するにつれて低下することが予測される。"
    )
    doc.add_paragraph(
        "同時に、組織変革に伴うリスクや摩擦（SC15）の認知に関しても、階層差が顕著に生じる。Packmohr et al. (2023) は、大企業と中小企業におけるDX推進障壁の認知差を分析し、階層や企業規模によって直面する障壁の種類（技術的、組織的、心理的）が明確に分化することを示した。また、データ駆動型DXにおいては単なる技術導入を超えた組織文化の変革が不可欠であり、文化的な受容基盤が欠如している場合、現場の心理的抵抗が激化することが指摘されている（Ghafoori et al., 2024）。経営層が戦略的機会に焦点を当てる「プロモーション・フォーカス」を持つ傾向があるのに対し、管理職や現場社員は日常業務の破綻やエラーの増大を防ぐ「プリベンション・フォーカス」を持ちやすく（Higgins, 1997）、これが組織摩擦認知の階層間ギャップを生み出す。"
    )

    doc.add_heading("2.3 仮説の設定", level=2)
    doc.add_paragraph(
        "• 仮説1（推進意識の規模主効果）: DX推進意識・心理的所有感（SC18）は、大企業が中小企業よりも有意に高い。\n"
        "• 仮説2（推進意識の職制主効果）: DX推進意識・心理的所有感（SC18）は、経営層、部課長クラス、一般社員の順に有意に低下する。\n"
        "• 仮説3（推進意識の交互作用効果）: 企業規模と職制グループの間に交互作用が存在し、大企業と中小企業の差は上位階層ほど大きく、一般社員層では収束する。\n"
        "• 仮説4（摩擦認知の職制主効果と交互作用）: DXリスク懸念・組織摩擦認知（SC15）は階層間で有意に異なり、特に中小企業において経営層と現場管理職・一般社員との間の認識乖離が大企業よりも顕著に拡大する。"
    )

    # 3. 研究方法
    h3 = doc.add_heading("3. 研究方法 (Methodology)", level=1)
    h3.paragraph_format.space_before = Pt(12)

    doc.add_heading("3.1 調査設計と対象地域の選定", level=2)
    doc.add_paragraph(
        "本研究の実証データは、提携モニターを対象としたクローズド方式のインターネット調査（実査：株式会社サーベイリサーチセンター）により収集された。\n"
        "調査対象は、日本国内の特定地域（北海道、宮城、東京、愛知、大阪、広島、福岡、熊本の8地域）に所在する民間企業に勤務する「経営者」「管理職」「一般職」である。対象地域の選定にあたっては、IT人材の流動性や都市規模を考慮し、各地方の主要中枢都市（札幌、仙台、東京、名古屋、大阪、広島、福岡）に加えて、半導体産業の急速な集積により産業構造および就業環境の変革が著しい熊本県を抽出対象として加えた。"
    )

    doc.add_heading("3.2 サンプリング手続きと回収割付", level=2)
    doc.add_paragraph(
        "1. 調査期間: 令和7年（2025年）11月20日 〜 11月25日\n"
        "2. 有効回答数: スクリーニング調査有効回答 8,274サンプル → 本調査有効回答 2,035サンプル\n"
        "3. 抽出条件: スクリーニング調査において、勤務先が「DXに取り組んでいる」と回答した就業者層を厳格に抽出した。\n"
        "4. 回収割付: 組織内の職階間における認識乖離を解明するため、「経営者（役員・取締役・社長、n = 329 名、16.2%）」「管理職（部課長クラス、n = 806 名、39.6%）」「一般職（一般社員、n = 900 名、44.2%）」の3区分で均等割付を志向した層化抽出を実施した。さらに、厚生労働省「賃金構造基本統計調査」の基準に準拠し、常用労働者1,000人以上を「大企業（Large, n = 745 名、36.6%）」、1,000人未満を「SMO（Small and Medium Organization：中小組織, n = 1,290 名、63.4%）」と定義した。"
    )

    doc.add_heading("3.3 データ品質管理と研究上の配慮", level=2)
    doc.add_paragraph(
        "Web調査システムの論理チェックおよび必須回答制御により、本調査完了データセット（N = 2,035）内には項目無回答や欠損値（Missing Values）は一切存在しない（完全決定論的データセット）。調査会社のデータクレンジング段階において、全設問同一選択肢回答（Straight-lining）や異常な短時間回答者（Speeders）は事前に検知・排除された。\n"
        "本調査は人を対象とする非侵襲的な意識調査であり、調査会社（サーベイリサーチセンター）のモニター規約に基づき個人を特定可能な情報は収集されず、完全匿名化された統計データとして集計・解析された。また、回答者は調査会社の事前登録規約および調査画面における趣旨明示に基づき、自発的な意志によって回答を行った。"
    )

    doc.add_heading("3.4 変数定義と測定尺度", level=2)
    doc.add_paragraph(
        "1. DX推進意識・心理的所有感（SC18, 9項目）: 自社のDXに対する当事者意識、競争力強化への期待、推進コミットメント等を測定する9項目（1: 全くそう思わない 〜 5: 非常にそう思うの5点リッカート尺度）の算術平均値。\n"
        "2. DXリスク懸念・組織摩擦認知（SC15, 9項目）: 新技術導入に伴う業務負荷増加、既存業務との軋轢、現場の孤立感、成果還元の不透明感等を測定する9項目（同5点リッカート尺度）の算術平均値。\n"
        "3. 理論的背景：組織的公正（分配的公正）: Colquitt (2001) の組織的公正理論に基づき、DXに伴う学習負荷や業務変革に対して昇給や賞与といった適切な成果還元が期待できない状況（分配的公正の欠如）が一般職の心理的離反を招く背景要因として位置付けられる。"
    )

    doc.add_heading("3.5 尺度信頼性と概念の直交性検証", level=2)
    doc.add_paragraph(
        "クロンバックの α 係数による内的整合性の検証において、SC18（DX推進意識）は α = 0.8592（k = 9, N = 2,035, CITC: 0.392 〜 0.651）、SC15（DX摩擦認知）は α = 0.8183（k = 9, N = 2,035, CITC: 0.419 〜 0.595）といずれも高い信頼基準を満たした。SC18とSC15の相関係数は r = -0.0901（p = 4.66 × 10⁻⁵, r² = 0.0081）と微弱であり、両尺度が直交する独立した心理動機構成概念であることが実証的に確認された。"
    )

    doc.add_heading("3.6 統計分析モデル", level=2)
    doc.add_paragraph(
        "不均等セル頻度に対応するため、Type II 平方和（Type II Sum of Squares）による二元配置分散分析（Two-Way ANOVA）を実行した。効果量として偏イータ二乗（η²p）を算出した。HC3異分散頑健標準誤差による感度分析およびBrown-Forsythe検定を実施し、事後検定としてテューキーのHSD検定、ならびにウェルチの t 検定（Holm法多重性調整）による層別単純主効果検定を実施した。"
    )

    # 4. 分析結果
    h4 = doc.add_heading("4. 分析結果 (Results)", level=1)
    h4.paragraph_format.space_before = Pt(12)

    doc.add_heading("4.1 記述統計量", level=2)
    p_t1_cap = doc.add_paragraph()
    run_t1_cap = p_t1_cap.add_run("表1. 企業規模別・職制別の記述統計量一覧 (N = 2,035)")
    run_t1_cap.bold = True

    # 表1 作成 (APAスタイル)
    t1 = doc.add_table(rows=8, cols=7)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["企業規模", "職制グループ", "n", "SC18 平均 ± SD", "SC18 95% CI", "SC15 平均 ± SD", "SC15 95% CI"]
    for i, h in enumerate(headers):
        cell = t1.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_border(cell, top={'sz': 12, 'val': 'single'}, bottom={'sz': 6, 'val': 'single'})

    t1_data = [
        ["大企業", "1. 経営層", "31", "3.77 ± 0.62", "[3.54, 3.99]", "3.10 ± 0.72", "[2.83, 3.36]"],
        ["大企業", "2. 部課長クラス", "295", "3.37 ± 0.61", "[3.30, 3.44]", "3.08 ± 0.58", "[3.01, 3.15]"],
        ["大企業", "3. 一般社員", "419", "3.18 ± 0.64", "[3.12, 3.24]", "3.22 ± 0.60", "[3.16, 3.28]"],
        ["中小企業", "1. 経営層", "298", "3.48 ± 0.65", "[3.41, 3.55]", "2.69 ± 0.67", "[2.62, 2.77]"],
        ["中小企業", "2. 部課長クラス", "511", "3.22 ± 0.60", "[3.17, 3.28]", "3.10 ± 0.63", "[3.04, 3.15]"],
        ["中小企業", "3. 一般社員", "481", "3.18 ± 0.59", "[3.12, 3.23]", "3.18 ± 0.58", "[3.13, 3.23]"],
        ["全体", "-", "2,035", "3.27 ± 0.63", "[3.24, 3.30]", "3.08 ± 0.63", "[3.05, 3.11]"]
    ]
    for row_idx, row_data in enumerate(t1_data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = t1.cell(row_idx, col_idx)
            cell.text = text
            if row_idx == 7:
                set_cell_border(cell, bottom={'sz': 12, 'val': 'single'})
            else:
                set_cell_border(cell)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    doc.add_heading("4.2 DX推進意識（SC18）の二元配置分散分析", level=2)
    doc.add_paragraph(
        "SC18に対する二元配置分散分析（Type II ANOVA）の結果、企業規模主効果（F(1, 2029) = 8.04, p = 0.0046, η²p = 0.0039）、職制主効果（F(2, 2029) = 38.58, p = 3.60 × 10⁻¹⁷, η²p = 0.0366）、および交互作用効果（F(2, 2029) = 4.32, p = 0.0134, η²p = 0.0042）のすべてが有意であった。職制主効果の説明力は規模効果の約9.3倍に達した。"
    )
    doc.add_paragraph(
        "層別単純主効果検定（ウェルチの t 検定, Holm調整）の結果、経営層（大企業 3.77 vs 中小 3.48, p = 0.0200, g = 0.44）および部課長クラス（大企業 3.37 vs 中小 3.22, p = 0.0010, g = 0.24）では大企業が有意に高い推進意識を示した一方、一般社員層では企業規模による有意差が完全に消失した（大企業 3.18 vs 中小 3.18, p = 0.9032, g = 0.01）。これにより、現場の意識が低位収束する実態（現場収束現象）が確認され、仮説1、仮説2、仮説3はすべて支持された。"
    )

    doc.add_heading("4.3 組織摩擦認知（SC15）の二元配置分散分析", level=2)
    doc.add_paragraph(
        "SC15に対する二元配置分散分析の結果、規模主効果は有意でなかったが（F(1, 2029) = 1.97, p = 0.1601, η²p = 0.0010）、職制主効果（F(2, 2029) = 61.98, p = 7.44 × 10⁻²⁷, η²p = 0.0576）および交互作用効果（F(2, 2029) = 5.79, p = 0.0031, η²p = 0.0057）が極めて顕著に有意であった。"
    )
    doc.add_paragraph(
        "特に中小企業において、経営層の摩擦認知（M = 2.69）は部課長クラス（M = 3.10）および一般社員（M = 3.18）と比較して著しく低く、経営層と一般社員との間に g = 0.79（p < 0.001）という巨大な認知乖離が存在していた。大企業では経営層（3.10）、部課長（3.08）、一般社員（3.22）と比較的フラットであるのに対し、中小企業ではトップの過度な楽観バイアスと現場の負担感との間に深刻な構造的断絶が存在することが実証された（仮説4支持）。"
    )

    # 5. 考察
    h5 = doc.add_heading("5. 考察 (Discussion)", level=1)
    h5.paragraph_format.space_before = Pt(12)

    doc.add_heading("5.1 理論的示唆 (Theoretical Implications)", level=2)
    doc.add_paragraph(
        "第1に、「属性規定性よりも階層規定性の優位」と「現場収束現象」の実証である。効果量の比較から、企業規模単独の効果量（η²p = 0.0039）よりも職制グループの効果量（η²p = 0.0366 〜 0.0576）が約9〜15倍大きく、DX意識を決定づける主因は「企業規模」ではなく「組織内の階層位置」であることが実証された。さらに、大企業の優位性が経営層（g = 0.44）および部課長層（g = 0.24）にとどまり、現場の一般社員層においては完全に同一水準（大企業 3.18 vs 中小 3.18, g = 0.01）に収束した。これは、先行研究が前提としてきた「大企業先進・中小企業遅延」というマクロな二元論（Eller et al., 2020; Garzoni et al., 2020）を精緻化するものである。どれほど大企業が資金やインフラを投入しても、末端の従業員に対する心理的所有感の移転（Ownership Transfer; Pierce et al., 2001）に失敗している現実を露呈している。"
    )
    doc.add_paragraph(
        "第2に、中小企業における「経営層の楽観主義バイアスと現場孤立」の解明である。中小企業において、経営層の組織摩擦認知は 2.69 と異常に低く、現場社員（3.18）との間に g = 0.79 もの巨大な認知断絶が存在した。Packmohr et al. (2023) が指摘するように、企業変革における阻害要因の認知差において、経営層はデジタル導入の戦略的果実を強調するあまり、現場が抱える既存業務の負荷や操作習熟の苦痛（Learning Curve Friction）を過小評価する「認知的盲点（Cognitive Blindspot）」に陥りやすい。中小企業の現場管理職や一般社員は、経営者直下のトップダウン圧力に晒されながらも代替リソースを与えられないため、大企業現場と同等以上の疲弊感と摩擦を抱え込んでいる。"
    )
    doc.add_paragraph(
        "第3に、DX意識の「二次元直交性（Orthogonal Dynamic）」の解明である。SC18とSC15の相関が r = -0.0901（p < 0.001）と微弱であった事実は、Higgins (1997) の制御焦点理論が示すように、独立した二つの認知動機システムとして併存していることを強く示唆している。すなわち、「DXに強い意欲を持ちながらも、現場の摩擦を同時に強く懸念する」という心理状態が一般的であり、摩擦を無視した推進論は組織崩壊を招く危険性がある。"
    )

    doc.add_heading("5.2 実務的示唆 (Practical Implications)", level=2)
    doc.add_paragraph(
        "1. 中小企業経営者への警鐘：現場の「見えない摩擦」の可視化と組織文化の醸成\n"
        "中小企業の経営者は、自らが主導するDXに対して現場が強い摩擦（3.18）を感じている事実を直視しなければならない。Ghafoori et al. (2024) や Succurro (2026) が実証するように、DXの定着には単なるツールの導入ではなく、戦略的計画の明文化とデータ駆動型組織文化の醸成が不可欠である。定期的なパルスサーベイや現場同席による業務モニタリングを導入し、業務プロセスの簡素化を先行させることが求められる。"
    )
    doc.add_paragraph(
        "2. 大企業における現場社員の「心理的所有感」の再設計とビジネスモデル変革\n"
        "大企業においては、部課長から一般社員への「意識の目詰まり」が最大のボトルネックとなっている。経営企画やDX推進室主導の全社プロジェクトから、各事業部の現場社員が小さな改善アイデアを自ら提案・実装する「ボトムアップ型ローコード開発」を奨励し、Pierce et al. (2001) の「対象への自己投資」の機会を提供する必要がある。さらに、Lamperti et al. (2024) が提示するように、現場が主体となって既存の製品・業務をサービス化するサービタイゼーションへの移行を促すことが有効である。"
    )
    doc.add_paragraph(
        "3. 中間管理職（部課長クラス）のバッファー機能の強化\n"
        "両規模ともに部課長クラスは、上層部からの推進圧力と現場からの抵抗・不満の板挟みとなっている。管理職層に対してDX評価指標（KPI）を成果直結型だけでなく「現場の変革適応度」にも配分し、心理的安全性を担保したチェンジマネジメント研修を実施すべきである。"
    )

    # 6. 結論と研究の限界
    h6 = doc.add_heading("6. 結論と研究の限界 (Conclusion & Limitations)", level=1)
    h6.paragraph_format.space_before = Pt(12)

    doc.add_heading("6.1 結論", level=2)
    doc.add_paragraph(
        "本研究は、2,035名の就業者全量データを用い、企業規模と組織階層がDX推進意識（SC18）および組織摩擦認知（SC15）に及ぼす影響を実証的に検証した。主要な知見として、(1) DX推進意識において企業規模と職制の有意な交互作用が確認され、大企業優位は上位層に限られ一般社員層では完全に低位収束すること、(2) 組織摩擦認知において中小企業の経営層（2.69）と現場層（3.10〜3.18）との間に g = 0.79 に達する深刻な認知乖離が存在すること、を統計的に立証した。これらの知見は、DXを単なる技術導入ではなく、組織階層間の認識統合と心理的所有感の再構築プロセスとして捉え直す重要性を強く要請している。"
    )

    doc.add_heading("6.2 研究の限界と今後の課題 (Limitations & Future Research)", level=2)
    doc.add_paragraph(
        "本研究には、結果の解釈において留意すべき以下の学術的限界が存在する。\n"
        "第1に、横断的調査デザイン（Cross-Sectional Survey Design）に伴う因果推論の限界である。本研究は同一時点での観測データに基づくため、変数間の共変関係および交互作用の存在は厳密に実証されたものの、厳密な時間的先行性や直接的な因果関係（Causality）を断定することはできない。例えば、中小企業経営層の低摩擦認知が現場の孤立を招いているのか、あるいは現場の摩擦激化から経営層が無意識に目を背けているのかといった双方向的・動態的な影響関係を確定するためには、複数時点にわたる縦断的パネル調査（Longitudinal Panel Design）や介入実験による検証が不可欠である。\n"
        "第2に、自己申告式データに伴う共通方法バイアス（Common Method Bias: CMB）の検証である。本調査では設問群の物理的分離（SC15とSC18の別ブロック提示）およびアンカーの多角化により手続的統制を図っており、実証的にもSC18とSC15の相関が極めて低い（r = -0.0901, r² < 1%）ことから、単一の回答傾向による系統的歪み（ハロー効果や社会的望ましさバイアス）は極めて軽微であると判断される。\n"
        "第3に、大企業経営層の標本サイズ（n = 31）は統計的検定力を維持しているものの、中小企業経営層（n = 298）と比較して相対的に小さいため、大規模企業特有のトップマネジメント層の細分化（CIO, CDO, 現場役員）を考慮したさらなる標本拡充が望まれる。今後は、業種別（製造、サービス、IT等）の統制変数を含めた多層モデル（Hierarchical Linear Modeling）による精緻な検証が期待される。"
    )

    doc.add_page_break()

    # 参考文献 (References: 全20編 APA第7版ぶら下げインデント)
    h_ref = doc.add_heading("参考文献 (References)", level=1)
    h_ref.paragraph_format.space_before = Pt(12)

    references = [
        "Al-Ghazali, B. M., Gelaidan, H. M., Shah, S. H. A., & Amjad, R. (2022). Green transformational leadership and green creativity? The mediating role of green thinking and green organizational identity in SMEs. Frontiers in Psychology, 13, 977998. https://doi.org/10.3389/fpsyg.2022.977998",
        "AlNuaimi, B. K., Kumar Singh, S., Ren, S., Budhwar, P., & Vorobyev, D. (2022). Mastering digital transformation: The nexus between leadership, agility, and digital strategy. Journal of Business Research, 145, 636–648. https://doi.org/10.1016/j.jbusres.2022.03.038",
        "Al-Swidi, A. K., Al-Hakimi, M. A., Al Koliby, I. S., Hasan, M. B., & Abdul-Talib, A.-N. (2024). The role of digital transformation in boosting CSR-driven green innovation among Yemeni manufacturing SMEs. Discover Sustainability, 5, 299. https://doi.org/10.1007/s43621-024-00506-w",
        "Colquitt, J. A. (2001). On the dimensionality of organizational justice: A construct validation of a measure. Journal of Applied Psychology, 86(3), 386–400. https://doi.org/10.1037/0021-9010.86.3.386",
        "Eller, R., Alford, P., Kallmünzer, A., & Peters, M. (2020). Antecedents, consequences, and challenges of small and medium-sized enterprise digitalization. Journal of Business Research, 112, 119–127. https://doi.org/10.1016/j.jbusres.2020.03.004",
        "Fauzi, F., Siregar, H., Barus, B., & Indraprahasta, G. S. (2023). Digital transformation for SME development at four levels of unit analysis – A literature review. ABAC Journal, 43(4), 276–302. https://doi.org/10.59865/abacj.2023.52",
        "Garzoni, A., De Turi, I., Secundo, G., & Del Vecchio, P. (2020). Fostering digital transformation of SMEs: A four levels approach. Management Decision, 58(8), 1543–1562. https://doi.org/10.1108/MD-07-2019-0939",
        "Ghafoori, A., Gupta, M., Merhi, M. I., Gupta, S., & Shore, A. P. (2024). Toward the role of organizational culture in data-driven digital transformation. International Journal of Production Economics, 271, 109205. https://doi.org/10.1016/j.ijpe.2024.109205",
        "Giang, P. X., Vi, T. T. T., & Ghi, T. N. (2026). Digital transformation, dynamic capability, and innovation performance in SMEs. Journal of Organizational Behavior Research, 11(1), 198–206. https://doi.org/10.51847/rkbg4kurvq",
        "Higgins, E. T. (1997). Beyond pleasure and pain. American Psychologist, 52(12), 1280–1300. https://doi.org/10.1037/0003-066X.52.12.1280",
        "Hu, H., Zhao, M., & Zhang, X. (2023). Network evolution of diffusion in enterprise digitalization and intellectualization transformation: A technology—organization—environment framework perspective. PLOS ONE, 18(12), e0295327. https://doi.org/10.1371/journal.pone.0295327",
        "Kane, G. C., Palmer, D., Phillips, A. N., Kiron, D., & Buckley, N. (2015). Strategy, not technology, drives digital transformation. MIT Sloan Management Review, 57(1), 1–25.",
        "Lamperti, S., Cavallo, A., & Sassanelli, C. (2024). Digital servitization and business model innovation in SMEs: A model to escape from market disruption. IEEE Transactions on Engineering Management, 71, 7159–7173. https://doi.org/10.1109/TEM.2022.3233132",
        "Liu, Q., Zhao, Y., Kamioka, T., & Nakamura, M. (2021). Digital transformation challenges in the sales of pharmaceutical companies in Japan. Asian Journal of Business Research, 11(3), 72–91. https://doi.org/10.14707/ajbr.210115",
        "Omrani, N., Rejeb, N., Maâlaoui, A., Dabić, M., & Kraus, S. (2024). Drivers of digital transformation in SMEs. IEEE Transactions on Engineering Management, 71, 5032–5045. https://doi.org/10.1109/TEM.2022.3215727",
        "Packmohr, S., Brink, H., & Paul, F.-H. (2023). Unraveling perceptions of barriers to digital transformation – Contrasting small and medium-sized with large enterprises. IADIS International Journal on Computer Science and Information Systems, 18(1), 102–119. https://doi.org/10.33965/ijcsis_2023180107",
        "Papadopoulos, T., Baltas, K. N., & Balta, M. E. (2020). The use of digital technologies by small and medium enterprises during COVID-19: Implications for theory and practice. International Journal of Information Management, 55, 102192. https://doi.org/10.1016/j.ijinfomgt.2020.102192",
        "Pierce, J. L., Kostova, T., & Dirks, K. T. (2001). Toward a theory of psychological ownership in organizations. Academy of Management Review, 26(2), 298–310. https://doi.org/10.5465/amr.2001.4378028",
        "Roman, A., & Rusu, V. D. (2022). Digital technologies and the performance of small and medium enterprises. Studies in Business and Economics, 17(3), 190–203. https://doi.org/10.2478/sbe-2022-0055",
        "Succurro, M. (2026). Digital transformation in tourism SMEs: A strategic imperative in the evolving business landscape. Journal of Industrial and Business Economics, 53, 941–985. https://doi.org/10.1007/s40812-026-00395-2"
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.add_run(ref)

    out_paths = [
        r"G:\マイドライブ\IDM\final_paper_submission.docx",
        r"G:\マイドライブ\antigravity\IDM\20261006\reports\final_paper_submission.docx"
    ]

    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        try:
            doc.save(p)
            print(f"Submission Word document saved: {p}")
        except PermissionError:
            alt_path = p.replace(".docx", "_revised.docx")
            doc.save(alt_path)
            print(f"Warning: {p} is locked (possibly open in Microsoft Word). Saved as: {alt_path}")

if __name__ == "__main__":
    create_submission_docx()

