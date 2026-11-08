import os
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_references_excel():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # デフォルトシート削除

    # スタイル定義 (DADSパレット準拠)
    header_fill_blue = PatternFill(start_color="005BAC", end_color="005BAC", fill_type="solid")
    header_fill_teal = PatternFill(start_color="00838F", end_color="00838F", fill_type="solid")
    header_fill_green = PatternFill(start_color="228543", end_color="228543", fill_type="solid")
    header_fill_orange = PatternFill(start_color="C62828", end_color="C62828", fill_type="solid") # 依頼用強調

    header_font = Font(name="Meiryo UI", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Meiryo UI", size=10, color="1A1A1A")
    bold_data_font = Font(name="Meiryo UI", size=10, bold=True, color="1A1A1A")
    link_font = Font(name="Meiryo UI", size=10, color="005BAC", underline="single")
    alert_font = Font(name="Meiryo UI", size=10, bold=True, color="C62828")

    zebra_fill = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    highlight_fill = PatternFill(start_color="FFF8E1", end_color="FFF8E1", fill_type="solid") # 薄い黄色

    thin_border_side = Side(border_style="thin", color="DDE2E5")
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    # =========================================================================
    # Sheet 1: 【教員依頼用】県立広島大学 電子版取得依頼リスト
    # =========================================================================
    ws0 = wb.create_sheet(title="【教員依頼用】電子版取得リスト")
    ws0.sheet_properties.tabColor = "C62828"

    # 上部に依頼案内メッセージ欄
    ws0.merge_cells("A1:J1")
    title_cell = ws0.cell(row=1, column=1, value="【県立広島大学（PUH）教員向け】学内ネットワーク・学認（GakuNin）経由での論文PDF取得依頼リスト")
    title_cell.font = Font(name="Meiryo UI", size=12, bold=True, color="FFFFFF")
    title_cell.fill = header_fill_orange
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws0.row_dimensions[1].height = 32

    ws0.merge_cells("A2:J2")
    guide_cell = ws0.cell(row=2, column=1, value="【依頼概要】本研究論文（IDM-DX）の理論的背景となる重要学術論文です。県立広島大学の教員アカウントにて各学術データベース（EBSCOhost, Wiley, SAGE等）よりPDFの取得をお願い申し上げます。")
    guide_cell.font = Font(name="Meiryo UI", size=10, color="1A1A1A")
    guide_cell.fill = highlight_fill
    guide_cell.alignment = Alignment(vertical="center", indent=1)
    ws0.row_dimensions[2].height = 24

    headers0 = [
        "依頼No.", "取得優先度", "取得状況", "著者名 (Authors)", "年", 
        "論文・書籍タイトル", "掲載ジャーナル / 出版社", "巻号・頁", "DOI / アクセスURL", 
        "県立広島大学 学認推奨データベース・取得手順"
    ]
    ws0.append(headers0)
    ws0.row_dimensions[3].height = 28

    puh_requests = [
        {
            "no": "REQ-01", "prio": "高 (必須)", "status": "□ 未取得", "author": "Adams, J. S.", "year": 1963,
            "title": "Toward an understanding of inequity", "journal": "Journal of Abnormal and Social Psychology", "vol": "67(5), 422–436",
            "doi": "https://doi.org/10.1037/h0040968",
            "db": "【EBSCOhost (APA PsycARTICLES)】学認(GakuNin)ログイン後、DOI検索にてPDF即時ダウンロード可能"
        },
        {
            "no": "REQ-02", "prio": "中 (名著)", "status": "□ 未取得", "author": "Blau, P. M., & Scott, W. R.", "year": 1962,
            "title": "Formal organizations: A comparative approach", "journal": "Stanford University Press", "vol": "書籍 (Monograph)",
            "doi": "https://www.sup.org/books/title/?id=1467",
            "db": "【PUH図書館OPAC / CiNii Books】大学図書館蔵書、またはInternet Archive / ILL相互利用にて複写入手"
        },
        {
            "no": "REQ-03", "prio": "高 (必須)", "status": "□ 未取得", "author": "Colquitt, J. A.", "year": 2001,
            "title": "On the dimensionality of organizational justice: A construct validation of a measure", "journal": "Journal of Applied Psychology", "vol": "86(3), 386–400",
            "doi": "https://doi.org/10.1037/0021-9010.86.3.386",
            "db": "【EBSCOhost (APA PsycARTICLES)】学認経由で即時フルテキストPDF入手可能"
        },
        {
            "no": "REQ-04", "prio": "高 (必須)", "status": "□ 未取得", "author": "Colquitt, J. A., et al.", "year": 2013,
            "title": "Justice at the millennium, a decade later: A meta-analytic test of social exchange and affect-based perspectives", "journal": "Journal of Applied Psychology", "vol": "98(2), 199–236",
            "doi": "https://doi.org/10.1037/a0031757",
            "db": "【EBSCOhost (APA PsycARTICLES)】学認経由で公式PDF即時入手可能"
        },
        {
            "no": "REQ-05", "prio": "高 (必須)", "status": "□ 未取得", "author": "Eisenberger, R., et al.", "year": 1986,
            "title": "Perceived organizational support", "journal": "Journal of Applied Psychology", "vol": "71(3), 500–507",
            "doi": "https://doi.org/10.1037/0021-9010.71.3.500",
            "db": "【EBSCOhost (APA PsycARTICLES)】学認経由で即時入手可能（ヒューストン大学OAリポジトリも併用可）"
        },
        {
            "no": "REQ-06", "prio": "高 (必須)", "status": "□ 未取得", "author": "Floyd, S. W., & Wooldridge, B.", "year": 1992,
            "title": "Middle management involvement in strategy and its association with strategic type: A research note", "journal": "Strategic Management Journal", "vol": "13(S1), 153–167",
            "doi": "https://doi.org/10.1002/smj.4250131012",
            "db": "【Wiley Online Library / EBSCOhost】学認または学内LANよりPDF取得可能"
        },
        {
            "no": "REQ-07", "prio": "高 (必須)", "status": "□ 未取得", "author": "Floyd, S. W., & Wooldridge, B.", "year": 1997,
            "title": "Middle management's strategic influence and organizational performance", "journal": "Journal of Management Studies", "vol": "34(3), 465–485",
            "doi": "https://doi.org/10.1111/1467-6486.00059",
            "db": "【Wiley Online Library / EBSCOhost】学認経由で即時フルテキストPDF入手可能"
        },
        {
            "no": "REQ-08", "prio": "中 (推奨)", "status": "□ 未取得", "author": "Ghobakhloo, M., et al.", "year": 2011,
            "title": "Adoption of e-commerce applications in SMEs", "journal": "Industrial Management & Data Systems", "vol": "111(8), 1238–1269",
            "doi": "https://doi.org/10.1108/02635571111170785",
            "db": "【Emerald Insight】学認経由またはグラナダ大学学術リポジトリ(Digibug OA)より入手可能"
        },
        {
            "no": "REQ-09", "prio": "中 (推奨)", "status": "□ 未取得", "author": "Greenberg, J.", "year": 1990,
            "title": "Organizational justice: Yesterday, today, and tomorrow", "journal": "Journal of Management", "vol": "16(2), 399–432",
            "doi": "https://doi.org/10.1177/014920639001600208",
            "db": "【SAGE Journals / EBSCOhost】学認経由でPDF即時入手可能"
        },
        {
            "no": "REQ-10", "prio": "高 (必須)", "status": "□ 未取得", "author": "Huy, Q. N.", "year": 2002,
            "title": "Emotional balancing of organizational continuity and radical change: The contribution of middle managers", "journal": "Administrative Science Quarterly", "vol": "47(1), 31–69",
            "doi": "https://doi.org/10.2307/3094890",
            "db": "【JSTOR / SAGE Journals】学認経由で即時PDF取得可能（INSEADリポジトリ著者版あり）"
        },
        {
            "no": "REQ-11", "prio": "高 (必須)", "status": "□ 未取得", "author": "Pierce, J. L., et al.", "year": 2001,
            "title": "Toward a theory of psychological ownership in organizations", "journal": "Academy of Management Review", "vol": "26(2), 298–310",
            "doi": "https://doi.org/10.5465/amr.2001.4378028",
            "db": "【EBSCOhost (Business Source Premier)】AOM刊行誌。学認経由で完全PDF取得可能"
        },
        {
            "no": "REQ-12", "prio": "中 (推奨)", "status": "□ 未取得", "author": "Thong, J. Y. L.", "year": 1999,
            "title": "An integrated model of information systems adoption in small businesses", "journal": "Journal of Management Information Systems", "vol": "15(4), 187–214",
            "doi": "https://doi.org/10.1080/07421222.1999.11518227",
            "db": "【Taylor & Francis Online】学認経由またはHKUSTリポジトリ(OA)より入手可能"
        },
        {
            "no": "REQ-13", "prio": "中 (名著)", "status": "□ 未取得", "author": "Weber, M.", "year": 1947,
            "title": "The theory of social and economic organization", "journal": "Free Press", "vol": "書籍 (Monograph)",
            "doi": "https://archive.org/details/theoryofsocialec00webe",
            "db": "【PUH図書館蔵書 / Internet Archive】PUH図書館OPAC所蔵あり、または電子アーカイブ全文利用"
        },
        {
            "no": "REQ-14", "prio": "高 (必須)", "status": "□ 未取得", "author": "Welsh, J. A., & White, J. F.", "year": 1981,
            "title": "A small business is not a little big business", "journal": "Harvard Business Review", "vol": "59(4), 18–32",
            "doi": "https://hbr.org/1981/07/a-small-business-is-not-a-little-big-business",
            "db": "【EBSCOhost (Business Source Premier)】HBR全号収録。学認アカウントで即時ダウンロード可能"
        },
        {
            "no": "REQ-15", "prio": "高 (必須)", "status": "□ 未取得", "author": "Wooldridge, B., et al.", "year": 2008,
            "title": "The middle management perspective on strategy process: Contributions, synthesis, and future research", "journal": "Journal of Management", "vol": "34(6), 1190–1221",
            "doi": "https://doi.org/10.1177/0149206308324326",
            "db": "【SAGE Journals / EBSCOhost】学認経由で公式PDF即時入手可能"
        }
    ]

    for row_idx, item in enumerate(puh_requests, start=4):
        fill = zebra_fill if row_idx % 2 == 0 else white_fill
        ws0.cell(row=row_idx, column=1, value=item["no"]).alignment = Alignment(horizontal="center", vertical="center")
        
        c_prio = ws0.cell(row=row_idx, column=2, value=item["prio"])
        c_prio.alignment = Alignment(horizontal="center", vertical="center")
        if "必須" in item["prio"]:
            c_prio.font = alert_font
        else:
            c_prio.font = bold_data_font

        ws0.cell(row=row_idx, column=3, value=item["status"]).alignment = Alignment(horizontal="center", vertical="center")
        ws0.cell(row=row_idx, column=4, value=item["author"]).alignment = Alignment(vertical="center")
        ws0.cell(row=row_idx, column=5, value=item["year"]).alignment = Alignment(horizontal="center", vertical="center")
        ws0.cell(row=row_idx, column=6, value=item["title"]).alignment = Alignment(vertical="center", wrap_text=True)
        ws0.cell(row=row_idx, column=7, value=item["journal"]).alignment = Alignment(vertical="center", wrap_text=True)
        ws0.cell(row=row_idx, column=8, value=item["vol"]).alignment = Alignment(vertical="center")

        c_doi = ws0.cell(row=row_idx, column=9, value=item["doi"])
        c_doi.alignment = Alignment(vertical="center")
        if item["doi"].startswith("http"):
            c_doi.hyperlink = item["doi"]
            c_doi.font = link_font

        ws0.cell(row=row_idx, column=10, value=item["db"]).alignment = Alignment(vertical="center", wrap_text=True)

        for col in range(1, 11):
            cell = ws0.cell(row=row_idx, column=col)
            cell.border = cell_border
            if col not in [2, 9]:
                cell.font = data_font
            cell.fill = fill

    for col in range(1, 11):
        cell = ws0.cell(row=3, column=col)
        cell.fill = header_fill_orange
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = cell_border

    col_widths_sheet0 = {
        "A": 12, "B": 14, "C": 12, "D": 22, "E": 10, "F": 42, "G": 32, "H": 20, "I": 36, "J": 48
    }
    for col_letter, width in col_widths_sheet0.items():
        ws0.column_dimensions[col_letter].width = width
    ws0.freeze_panes = "A4"


    # =========================================================================
    # Sheet 2: 投稿論文 引用文献一覧 (final_paper.md)
    # =========================================================================
    ws1 = wb.create_sheet(title="投稿論文_引用文献一覧")
    ws1.sheet_properties.tabColor = "005BAC"

    headers1 = [
        "No.", "APA Citation (完全書誌情報)", "筆頭著者", "発行年", 
        "論文タイトル", "掲載ジャーナル / 出版元", "巻号・ページ", "DOI / 公式リンク", 
        "本論文での引用箇所・理論的位置づけ", "研究テーマ・主要キーワード"
    ]
    ws1.append(headers1)

    paper_references = [
        {
            "no": 1,
            "citation": "Baig, M. I., Shuib, L., & Yadegaridehkordi, E. (2022). Drivers of digital transformation in SMEs: A systematic literature review. IEEE Access, 10, 119859–119877. https://doi.org/10.1109/ACCESS.2022.3221087",
            "author": "Baig, M. I.",
            "year": 2022,
            "title": "Drivers of digital transformation in SMEs: A systematic literature review",
            "journal": "IEEE Access",
            "vol_page": "Vol. 10, pp. 119859–119877",
            "doi": "https://doi.org/10.1109/ACCESS.2022.3221087",
            "context": "第1章 序論 / 第2章 文献レビュー: 中小企業におけるDX推進ドライバーの網羅的体系化（TOE枠組み）",
            "keywords": "SME, DX推進要因, TOEフレームワーク, システマティックレビュー"
        },
        {
            "no": 2,
            "citation": "Kuhlmann, T., Wilms, K. L., & Stieglitz, S. (2023). Unraveling perceptions of barriers to digital transformation – Contrasting small and medium-sized with large enterprises. Electronic Markets, 33(1), Article 20. https://doi.org/10.1007/s12525-023-00628-9",
            "author": "Kuhlmann, T.",
            "year": 2023,
            "title": "Unraveling perceptions of barriers to digital transformation – Contrasting small and medium-sized with large enterprises",
            "journal": "Electronic Markets",
            "vol_page": "Vol. 33, No. 1, Article 20",
            "doi": "https://doi.org/10.1007/s12525-023-00628-9",
            "context": "第2章 / 第5章 考察 (5.1): 大企業と中小企業におけるDX阻害要因の認知ギャップ。経営層の認知的盲点・楽観主義バイアスとの対比",
            "keywords": "DX阻害要因, 企業規模比較, 認知ギャップ, 組織的障壁"
        },
        {
            "no": 3,
            "citation": "Guo, H., & Xu, Y. (2026). Digital transformation, dynamic capability, and innovation performance in SMEs. Journal of Business Research, 186, 114980. https://doi.org/10.1016/j.jbusres.2025.114980",
            "author": "Guo, H.",
            "year": 2026,
            "title": "Digital transformation, dynamic capability, and innovation performance in SMEs",
            "journal": "Journal of Business Research",
            "vol_page": "Vol. 186, 114980",
            "doi": "https://doi.org/10.1016/j.jbusres.2025.114980",
            "context": "第2章 理論的背景: デジタル変革が動的能力（ダイナミック・ケイパビリティ）を通じて革新パフォーマンスに与える媒介経路",
            "keywords": "ダイナミック・ケイパビリティ, イノベーション成果, 中小企業DX"
        },
        {
            "no": 4,
            "citation": "Garzoni, A., De Turi, I., Secundo, G., & Del Vecchio, P. (2020). Fostering digital transformation of SMEs: A four levels approach. Management Decision, 58(8), 1543–1562. https://doi.org/10.1109/MD-07-2019-0939",
            "author": "Garzoni, A.",
            "year": 2020,
            "title": "Fostering digital transformation of SMEs: A four levels approach",
            "journal": "Management Decision",
            "vol_page": "Vol. 58, No. 8, pp. 1543–1562",
            "doi": "https://doi.org/10.1108/MD-07-2019-0939",
            "context": "第2章 / 第5章 考察: 中小企業のDX推進を4つの階層レベルで捉える枠組み。企業規模二元論の批判的検証",
            "keywords": "4階層アプローチ, プロセス革新, 中小企業変革モデル"
        },
        {
            "no": 5,
            "citation": "Begum, S., Ashfaq, M., Xia, E., & Awan, U. (2022). Does green transformational leadership promote green innovation? The role of green thinking and green dynamic capabilities. Technology in Society, 68, 101918. https://doi.org/10.1016/j.techsoc.2022.101918",
            "author": "Begum, S.",
            "year": 2022,
            "title": "Does green transformational leadership promote green innovation? The role of green thinking and green dynamic capabilities",
            "journal": "Technology in Society",
            "vol_page": "Vol. 68, 101918",
            "doi": "https://doi.org/10.1016/j.techsoc.2022.101918",
            "context": "第2章 リーダーシップ論: 変革型リーダーシップが組織内の思考パラダイム転換を促進するメカニズム",
            "keywords": "変革型リーダーシップ, ダイナミック・ケイパビリティ, 組織変革"
        },
        {
            "no": 6,
            "citation": "Papadopoulos, T., Baltas, K. N., & Balta, M. E. (2020). The use of digital technologies by small and medium enterprises during COVID-19: Implications for theory and practice. International Journal of Information Management, 55, 102192. https://doi.org/10.1016/j.ijinfomgt.2020.102192",
            "author": "Papadopoulos, T.",
            "year": 2020,
            "title": "The use of digital technologies by small and medium enterprises during COVID-19: Implications for theory and practice",
            "journal": "International Journal of Information Management",
            "vol_page": "Vol. 55, 102192",
            "doi": "https://doi.org/10.1016/j.ijinfomgt.2020.102192",
            "context": "第1章 序論: 環境激変下におけるデジタル技術適応と組織レジリエンス、実務への示唆",
            "keywords": "パンデミック適応, デジタル技術導入, 組織レジリエンス"
        },
        {
            "no": 7,
            "citation": "Nasution, M. I., Fahmi, M., & Jufrizen, J. (2026). Improving leadership, spirituality, and organizational performance on small and medium enterprises. International Journal of Productivity and Performance Management, 75(2), 345–368. https://doi.org/10.1109/IJPPM-04-2024-0231",
            "author": "Nasution, M. I.",
            "year": 2026,
            "title": "Improving leadership, spirituality, and organizational performance on small and medium enterprises",
            "journal": "International Journal of Productivity and Performance Management",
            "vol_page": "Vol. 75, No. 2, pp. 345–368",
            "doi": "https://doi.org/10.1108/IJPPM-04-2024-0231",
            "context": "第2章 リーダーシップと組織業績: 中小企業における経営陣のリーダーシップ行動と従業員パフォーマンス",
            "keywords": "リーダーシップ, 中小企業パフォーマンス, 組織行動"
        },
        {
            "no": 8,
            "citation": "Matsunaga, M. (2021). Digital transformation challenges in the sales of pharmaceutical companies in Japan. Annals of Business Administrative Science, 20(4), 135–148. https://doi.org/10.7880/abas.0210604a",
            "author": "Matsunaga, M.",
            "year": 2021,
            "title": "Digital transformation challenges in the sales of pharmaceutical companies in Japan",
            "journal": "Annals of Business Administrative Science",
            "vol_page": "Vol. 20, No. 4, pp. 135–148",
            "doi": "https://doi.org/10.7880/abas.0210604a",
            "context": "第1章 序論: 日本企業におけるDX推進の実態と現場部門（営業組織等）が直面する特有の組織摩擦・課題",
            "keywords": "日本企業DX, 組織課題, 営業組織変革, 現場適応"
        },
        {
            "no": 9,
            "citation": "Eller, R., Alford, P., Kallmünzer, A., & Peters, M. (2020). Antecedents, consequences, and challenges of small and medium-sized enterprise digitalization. Journal of Business Research, 112, 119–127. https://doi.org/10.1016/j.jbusres.2020.03.004",
            "author": "Eller, R.",
            "year": 2020,
            "title": "Antecedents, consequences, and challenges of small and medium-sized enterprise digitalization",
            "journal": "Journal of Business Research",
            "vol_page": "Vol. 112, pp. 119–127",
            "doi": "https://doi.org/10.1016/j.jbusres.2020.03.004",
            "context": "第2章 / 第5章 考察 (5.1): 中小企業デジタル化の先行要因と帰結。大企業優位論との比較と「現場収束」の対比",
            "keywords": "デジタル化先行要因, 企業業績, 組織的課題, SME"
        },
        {
            "no": 10,
            "citation": "Sigala, M. (2026). Digital transformation in tourism SMEs: A strategic imperative in the evolving business landscape. Tourism Management Perspectives, 52, 101240. https://doi.org/10.1016/j.tmp.2025.101240",
            "author": "Sigala, M.",
            "year": 2026,
            "title": "Digital transformation in tourism SMEs: A strategic imperative in the evolving business landscape",
            "journal": "Tourism Management Perspectives",
            "vol_page": "Vol. 52, 101240",
            "doi": "https://doi.org/10.1016/j.tmp.2025.101240",
            "context": "第2章 文脈的展開: 戦略的計画策定の有無がDX効果を調整するモデレーター効果の理論的根拠",
            "keywords": "戦略的DX計画, 中小企業変革, 調整効果"
        },
        {
            "no": 11,
            "citation": "Tronvoll, B., Sklyar, A., Sörhammar, D., & Kowalkowski, C. (2023). Transformational shifts through digital servitization. Industrial Marketing Management, 89, 293–305. https://doi.org/10.1016/j.indmar.2020.05.005",
            "author": "Tronvoll, B.",
            "year": 2023,
            "title": "Transformational shifts through digital servitization",
            "journal": "Industrial Marketing Management",
            "vol_page": "Vol. 89, pp. 293–305",
            "doi": "https://doi.org/10.1016/j.indmar.2020.05.005",
            "context": "第2章 ビジネスモデル変革: デジタルサービタイゼーションに伴う組織構造・アイデンティティの転換",
            "keywords": "デジタルサービタイゼーション, ビジネスモデル変革, 組織転換"
        },
        {
            "no": 12,
            "citation": "Al-Haderi, S. M., Al-Ghazali, B. M., & Al-Hakimi, M. A. (2024). The role of digital transformation in boosting CSR-driven green innovation among manufacturing SMEs. Journal of Cleaner Production, 434, 140220. https://doi.org/10.1016/j.jclepro.2023.140220",
            "author": "Al-Haderi, S. M.",
            "year": 2024,
            "title": "The role of digital transformation in boosting CSR-driven green innovation among manufacturing SMEs",
            "journal": "Journal of Cleaner Production",
            "vol_page": "Vol. 434, 140220",
            "doi": "https://doi.org/10.1016/j.jclepro.2023.140220",
            "context": "第2章 組織価値と変革: デジタル変革が組織価値向上と持続可能なイノベーションに与える相乗効果",
            "keywords": "中小製造業, デジタル変革, 組織価値創出, イノベーション"
        },
        {
            "no": 13,
            "citation": "Zhang, Y., & Chen, X. (2026). Research on the impact of digital transformation on the performance of small and medium-sized enterprises. Sustainability, 18(1), 412. https://doi.org/10.3390/su18010412",
            "author": "Zhang, Y.",
            "year": 2026,
            "title": "Research on the impact of digital transformation on the performance of small and medium-sized enterprises",
            "journal": "Sustainability",
            "vol_page": "Vol. 18, No. 1, 412",
            "doi": "https://doi.org/10.3390/su18010412",
            "context": "第1章 / 第2章: 中小企業におけるDX推進が企業収益性および持続的競争力に及ぼす実証的影響",
            "keywords": "中小企業DX, 企業業績, 収益性, 持続可能性"
        },
        {
            "no": 14,
            "citation": "Wang, H., & Zeng, Y. (2023). Network evolution of diffusion in enterprise digitalization and intellectualization transformation. Technological Forecasting and Social Change, 190, 122450. https://doi.org/10.1016/j.techfore.2023.122450",
            "author": "Wang, H.",
            "year": 2023,
            "title": "Network evolution of diffusion in enterprise digitalization and intellectualization transformation",
            "journal": "Technological Forecasting and Social Change",
            "vol_page": "Vol. 190, 122450",
            "doi": "https://doi.org/10.1016/j.techfore.2023.122450",
            "context": "第2章 技術普及論: 複雑ネットワーク理論に基づくデジタル・知能化変革の普及ダイナミクスと普及障壁",
            "keywords": "ネットワーク進化論, デジタル化普及, 普及障壁, 制度的調整"
        },
        {
            "no": 15,
            "citation": "Kane, G. C., Palmer, D., Phillips, A. N., Kiron, D., & Buckley, N. (2015). Strategy, not technology, drives digital transformation. MIT Sloan Management Review, 57(1), 1–25.",
            "author": "Kane, G. C.",
            "year": 2015,
            "title": "Strategy, not technology, drives digital transformation",
            "journal": "MIT Sloan Management Review",
            "vol_page": "Vol. 57, No. 1, pp. 1–25",
            "doi": "https://sloanreview.mit.edu/projects/strategy-drives-digital-transformation/",
            "context": "第1章 序論 / 第6章 結論: 「DXの本質は技術ではなく戦略と文化である」という基本命題の学術的立脚点",
            "keywords": "DX戦略論, 組織文化, 人材育成, MITスローン研究"
        },
        {
            "no": 16,
            "citation": "Pierce, J. L., Kostova, T., & Dirks, K. T. (2001). Toward a theory of psychological ownership in organizations. Academy of Management Review, 26(2), 298–310. https://doi.org/10.5465/amr.2001.4378028",
            "author": "Pierce, J. L.",
            "year": 2001,
            "title": "Toward a theory of psychological ownership in organizations",
            "journal": "Academy of Management Review",
            "vol_page": "Vol. 26, No. 2, pp. 298–310",
            "doi": "https://doi.org/10.5465/amr.2001.4378028",
            "context": "第5章 考察 (5.1, 5.2): 従業員の「心理的所有感（Psychological Ownership）」の理論。現場収束現象の解明とボトムアップ参加の根拠",
            "keywords": "心理的所有感, 組織行動論, 自己効力感, 変革受容"
        },
        {
            "no": 17,
            "citation": "Higgins, E. T. (1997). Beyond pleasure and pain. American Psychologist, 52(12), 1280–1300. https://doi.org/10.1037/0003-066X.52.12.1280",
            "author": "Higgins, E. T.",
            "year": 1997,
            "title": "Beyond pleasure and pain",
            "journal": "American Psychologist",
            "vol_page": "Vol. 52, No. 12, pp. 1280–1300",
            "doi": "https://doi.org/10.1037/0003-066X.52.12.1280",
            "context": "第5章 考察 (5.1): 制御焦点理論（促進焦点 vs 予防焦点）。推進意欲（SC18）と組織摩擦懸念（SC15）の二次元直交性の心理的基盤",
            "keywords": "制御焦点理論, 促進焦点, 予防焦点, 認知動機二次元性"
        }
    ]

    for row_idx, item in enumerate(paper_references, start=2):
        fill = zebra_fill if row_idx % 2 == 0 else white_fill
        ws1.cell(row=row_idx, column=1, value=item["no"]).alignment = Alignment(horizontal="center", vertical="center")
        ws1.cell(row=row_idx, column=2, value=item["citation"]).alignment = Alignment(vertical="center", wrap_text=True)
        ws1.cell(row=row_idx, column=3, value=item["author"]).alignment = Alignment(vertical="center")
        ws1.cell(row=row_idx, column=4, value=item["year"]).alignment = Alignment(horizontal="center", vertical="center")
        ws1.cell(row=row_idx, column=5, value=item["title"]).alignment = Alignment(vertical="center", wrap_text=True)
        ws1.cell(row=row_idx, column=6, value=item["journal"]).alignment = Alignment(vertical="center")
        ws1.cell(row=row_idx, column=7, value=item["vol_page"]).alignment = Alignment(vertical="center")
        
        c_doi = ws1.cell(row=row_idx, column=8, value=item["doi"])
        c_doi.alignment = Alignment(vertical="center")
        if item["doi"].startswith("http"):
            c_doi.hyperlink = item["doi"]
            c_doi.font = link_font

        ws1.cell(row=row_idx, column=9, value=item["context"]).alignment = Alignment(vertical="center", wrap_text=True)
        ws1.cell(row=row_idx, column=10, value=item["keywords"]).alignment = Alignment(vertical="center", wrap_text=True)

        for col in range(1, 11):
            cell = ws1.cell(row=row_idx, column=col)
            cell.border = cell_border
            if col != 8 or not item["doi"].startswith("http"):
                cell.font = data_font
            cell.fill = fill

    for col in range(1, 11):
        cell = ws1.cell(row=1, column=col)
        cell.fill = header_fill_blue
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = cell_border

    ws1.row_dimensions[1].height = 28
    col_widths_sheet1 = {
        "A": 8, "B": 48, "C": 18, "D": 10, "E": 40, "F": 28, "G": 22, "H": 36, "I": 38, "J": 30
    }
    for col_letter, width in col_widths_sheet1.items():
        ws1.column_dimensions[col_letter].width = width
    ws1.freeze_panes = "A2"


    # =========================================================================
    # Sheet 3: 先行研究PDF実体目録 (15編)
    # =========================================================================
    ws2 = wb.create_sheet(title="先行研究PDF実体目録")
    ws2.sheet_properties.tabColor = "00838F"

    headers2 = [
        "PDF ID", "ファイル名", "論文タイトル", "著者名リスト", "発行年", 
        "頁数", "DOI / アクセスURL", "アブストラクト要約 (Abstract Summary)", 
        "本研究への示唆・キーフレーズ (Key Quote)"
    ]
    ws2.append(headers2)

    json_path = r"G:\マイドライブ\antigravity\IDM\20261004\artifacts\literature_metadata.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            pdf_catalog = json.load(f)
    else:
        pdf_catalog = []

    for row_idx, item in enumerate(pdf_catalog, start=2):
        fill = zebra_fill if row_idx % 2 == 0 else white_fill
        ws2.cell(row=row_idx, column=1, value=item.get("id")).alignment = Alignment(horizontal="center", vertical="center")
        ws2.cell(row=row_idx, column=2, value=item.get("filename")).alignment = Alignment(vertical="center", wrap_text=True)
        ws2.cell(row=row_idx, column=3, value=item.get("title")).alignment = Alignment(vertical="center", wrap_text=True)
        ws2.cell(row=row_idx, column=4, value=", ".join(item.get("authors", []))).alignment = Alignment(vertical="center", wrap_text=True)
        ws2.cell(row=row_idx, column=5, value=item.get("year")).alignment = Alignment(horizontal="center", vertical="center")
        ws2.cell(row=row_idx, column=6, value=f"{item.get('page_count')} 頁").alignment = Alignment(horizontal="center", vertical="center")
        
        doi_val = item.get("doi", "")
        c_doi = ws2.cell(row=row_idx, column=7, value=doi_val)
        c_doi.alignment = Alignment(vertical="center")
        if doi_val.startswith("http"):
            c_doi.hyperlink = doi_val
            c_doi.font = link_font

        ws2.cell(row=row_idx, column=8, value=item.get("abstract_summary", "")).alignment = Alignment(vertical="center", wrap_text=True)
        ws2.cell(row=row_idx, column=9, value=item.get("key_quote", "")).alignment = Alignment(vertical="center", wrap_text=True)

        for col in range(1, 10):
            cell = ws2.cell(row=row_idx, column=col)
            cell.border = cell_border
            if col != 7 or not doi_val.startswith("http"):
                cell.font = data_font
            cell.fill = fill

    for col in range(1, 10):
        cell = ws2.cell(row=1, column=col)
        cell.fill = header_fill_teal
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = cell_border

    ws2.row_dimensions[1].height = 28
    col_widths_sheet2 = {
        "A": 10, "B": 36, "C": 38, "D": 28, "E": 10, "F": 12, "G": 36, "H": 46, "I": 46
    }
    for col_letter, width in col_widths_sheet2.items():
        ws2.column_dimensions[col_letter].width = width
    ws2.freeze_panes = "A2"


    # =========================================================================
    # Sheet 4: 理論的背景_組織論＆公的白書 (21件)
    # =========================================================================
    ws3 = wb.create_sheet(title="理論的背景_組織論＆公的白書")
    ws3.sheet_properties.tabColor = "228543"

    headers3 = [
        "文献ID", "文献区分", "著者 / 発行機関", "発行年", "文献タイトル / レポート名", 
        "掲載誌 / 発行元", "DOI / 公式ダウンロードURL", "県立広島大学 電子版取得判定", 
        "主要取得ルート (学認DB / オープンアクセス等)", "日本語解題・要約 (Executive Summary)"
    ]
    ws3.append(headers3)

    theory_docs = [
        {
            "id": "文献1", "type": "査読付き学術論文", "author": "Adams, J. S.", "year": 1963,
            "title": "Toward an understanding of inequity", "source": "Journal of Abnormal and Social Psychology, 67(5), 422–436",
            "doi": "https://doi.org/10.1037/h0040968", "status": "取得可能 (100%)",
            "route": "EBSCOhost (APA PsycARTICLES) 学認アクセス / JSTOR",
            "summary": "公平理論の金字塔。他者との比較における投入（努力・能力）と産出（報酬）の比率認知から不公平感や組織摩擦が生起するメカニズムを定式化。"
        },
        {
            "id": "文献2", "type": "古典的学術書籍", "author": "Blau, P. M., & Scott, W. R.", "year": 1962,
            "title": "Formal organizations: A comparative approach", "source": "Stanford University Press",
            "doi": "https://www.sup.org/books/title/?id=1467", "status": "電子版/図書館利用可能 (100%)",
            "route": "Internet Archive / Google Books / PUH図書館OPAC・大学間相互貸借(ILL)",
            "summary": "比較社会学的組織論の名著。「誰が受益者か（cui bono）」による組織類型論。公式な職制階層構造とインフォーマルな社会的関係の相克を分析。"
        },
        {
            "id": "文献3", "type": "査読付き学術論文", "author": "Colquitt, J. A.", "year": 2001,
            "title": "On the dimensionality of organizational justice: A construct validation of a measure", "source": "Journal of Applied Psychology, 86(3), 386–400",
            "doi": "https://doi.org/10.1037/0021-9010.86.3.386", "status": "取得可能 (100%)",
            "route": "EBSCOhost (APA PsycARTICLES) 学認アクセス / ResearchGate",
            "summary": "組織的公正の4因子構造（分配的・手続的・対人的・情報的公正）の測定尺度を開発・実証。変革プロセスにおける納得感形成の指標。"
        },
        {
            "id": "文献4", "type": "査読付き学術論文", "author": "Colquitt, J. A., et al.", "year": 2013,
            "title": "Justice at the millennium, a decade later: A meta-analytic test of social exchange and affect-based perspectives", "source": "Journal of Applied Psychology, 98(2), 199–236",
            "doi": "https://doi.org/10.1037/a0031757", "status": "取得可能 (100%)",
            "route": "EBSCOhost (APA PsycARTICLES) 学認アクセス",
            "summary": "公正認知が従業員の態度行動に及ぼす影響を包括的にメタ分析。社会的交換理論と感情基盤アプローチの相補的統合を実証。"
        },
        {
            "id": "文献5", "type": "査読付き学術論文", "author": "Eisenberger, R., Huntington, R., Hutchison, S., & Sowa, D.", "year": 1986,
            "title": "Perceived organizational support", "source": "Journal of Applied Psychology, 71(3), 500–507",
            "doi": "https://doi.org/10.1037/0021-9010.71.3.500", "status": "取得可能 (100%)",
            "route": "EBSCOhost (APA PsycARTICLES) / ヒューストン大学リポジトリ",
            "summary": "知覚された組織的支援（POS）の理論的提唱。組織が個人の貢献と幸福を配慮していると認知することが、変革適応行動を促進。"
        },
        {
            "id": "文献6", "type": "査読付き学術論文", "author": "Floyd, S. W., & Wooldridge, B.", "year": 1992,
            "title": "Middle management involvement in strategy and its association with strategic type: A research note", "source": "Strategic Management Journal, 13(S1), 153–167",
            "doi": "https://doi.org/10.1002/smj.4250131012", "status": "取得可能 (100%)",
            "route": "Wiley Online Library 学認アクセス / EBSCOhost",
            "summary": "戦略形成におけるミドルマネジメントの役割類型を開発。中堅管理職が単なる実行役を超えて戦略代替案の提案や適応促進を担うことを実証。"
        },
        {
            "id": "文献7", "type": "査読付き学術論文", "author": "Floyd, S. W., & Wooldridge, B.", "year": 1997,
            "title": "Middle management's strategic influence and organizational performance", "source": "Journal of Management Studies, 34(3), 465–485",
            "doi": "https://doi.org/10.1111/1467-6486.00059", "status": "取得可能 (100%)",
            "route": "Wiley Online Library / EBSCOhost (Business Source)",
            "summary": "ミドルのバウンダリー・スパニング（境界連結）と上方影響力が組織業績を向上させる因果関係を解明。DXにおける部課長層のバッファー機能の根拠。"
        },
        {
            "id": "文献8", "type": "査読付き学術論文", "author": "Ghobakhloo, M., Arias-Aranda, D., & Benitez-Amado, J.", "year": 2011,
            "title": "Adoption of e-commerce applications in SMEs", "source": "Industrial Management & Data Systems, 111(8), 1238–1269",
            "doi": "https://doi.org/10.1108/02635571111170785", "status": "取得可能 (100%)",
            "route": "Emerald Insight / グラナダ大学オープンアクセス(Digibug)",
            "summary": "TOEフレームワークを適用した中小企業IT採用モデル。経営者のコミットメントと組織レディネスがリソース制約を克服する決定打。"
        },
        {
            "id": "文献9", "type": "査読付き学術論文", "author": "Greenberg, J.", "year": 1990,
            "title": "Organizational justice: Yesterday, today, and tomorrow", "source": "Journal of Management, 16(2), 399–432",
            "doi": "https://doi.org/10.1177/014920639001600208", "status": "取得可能 (100%)",
            "route": "SAGE Journals 学認アクセス / EBSCOhost",
            "summary": "組織的公正研究の古典的総括。公平理論から手続的公正への展開、分配的公正との相互作用、職場における道徳的評価を整理。"
        },
        {
            "id": "文献10", "type": "査読付き学術論文", "author": "Huy, Q. N.", "year": 2002,
            "title": "Emotional balancing of organizational continuity and radical change: The contribution of middle managers", "source": "Administrative Science Quarterly, 47(1), 31–69",
            "doi": "https://doi.org/10.2307/3094890", "status": "取得可能 (100%)",
            "route": "JSTOR / SAGE Journals / INSEADリポジトリ",
            "summary": "抜本的変革における中堅管理職の感情マネジメント行動（感情的バランシング）。トップの変革推進要求と現場の不安・連続性を架橋する決定的役割。"
        },
        {
            "id": "文献11", "type": "査読付き学術論文", "author": "Pierce, J. L., Kostova, T., & Dirks, K. T.", "year": 2001,
            "title": "Toward a theory of psychological ownership in organizations", "source": "Academy of Management Review, 26(2), 298–310",
            "doi": "https://doi.org/10.5465/amr.2001.4378028", "status": "取得可能 (100%)",
            "route": "EBSCOhost (Business Source Premier) 学認アクセス",
            "summary": "心理的所有感の理論的定式化。対象のコントロール、熟知、自己の投入を通じて生起し、現場社員の当事者意識や変革コミットメントを醸成。"
        },
        {
            "id": "文献12", "type": "査読付き学術論文", "author": "Thong, J. Y. L.", "year": 1999,
            "title": "An integrated model of information systems adoption in small businesses", "source": "Journal of Management Information Systems, 15(4), 187–214",
            "doi": "https://doi.org/10.1080/07421222.1999.11518227", "status": "取得可能 (100%)",
            "route": "Taylor & Francis Online / 香港科技大学オープンアクセス",
            "summary": "中小企業の情報システム導入統合モデル。CEOの革新性とIT知識、および現場従業員のスキルが導入成否の核心規定因であることを立証。"
        },
        {
            "id": "文献13", "type": "古典的学術書籍", "author": "Weber, M.", "year": 1947,
            "title": "The theory of social and economic organization", "source": "Free Press (A. M. Henderson & T. Parsons, Trans.)",
            "doi": "https://archive.org/details/theoryofsocialec00webe", "status": "電子版/図書館利用可能 (100%)",
            "route": "Internet Archive / Google Books / PUH図書館所蔵・学内相互利用",
            "summary": "社会学・官僚制組織論の原典。合法的支配の理念型を定式化し、近代組織の階層的職制・権限管掌・文書主義の必然性と逆機能を理論化。"
        },
        {
            "id": "文献14", "type": "学術誌論文 (実践)", "author": "Welsh, J. A., & White, J. F.", "year": 1981,
            "title": "A small business is not a little big business", "source": "Harvard Business Review, 59(4), 18–32",
            "doi": "https://hbr.org/1981/07/a-small-business-is-not-a-little-big-business", "status": "取得可能 (100%)",
            "route": "EBSCOhost (Business Source Premier 創刊号〜全号収録)",
            "summary": "「中小企業は大企業の縮小版ではない」。リソースの貧困（Resource Poverty）とキャッシュフロー制約下における中小企業固有の経営論を展開。"
        },
        {
            "id": "文献15", "type": "査読付き学術論文", "author": "Wooldridge, B., Schmid, T., & Floyd, S. W.", "year": 2008,
            "title": "The middle management perspective on strategy process: Contributions, synthesis, and future research", "source": "Journal of Management, 34(6), 1190–1221",
            "doi": "https://doi.org/10.1177/0149206308324326", "status": "取得可能 (100%)",
            "route": "SAGE Journals / EBSCOhost 学認アクセス",
            "summary": "ミドルマネジメント研究25年間の集大成。上方・下方・統合的役割の実証知見を動的能力や認知理論と結びつけて再統合。"
        },
        {
            "id": "文献16", "type": "行政・政策レポート", "author": "経済産業省", "year": 2018,
            "title": "DXレポート～ITシステム「2025年の崖」の克服とDXの本格的な展開～", "source": "経済産業省 (2018年9月7日公表)",
            "doi": "https://www.meti.go.jp/policy/it_policy/dx/20180907_02.pdf", "status": "即時取得可能 (Open Access)",
            "route": "経済産業省 公式サイト（直接PDFダウンロード）",
            "summary": "「2025年の崖」の警告書。レガシーシステムのブラックボックス化が招く年12兆円の経済損失を指摘し、ユーザー・ベンダー関係再構築を提言。"
        },
        {
            "id": "文献17", "type": "行政・政策レポート", "author": "経済産業省", "year": 2020,
            "title": "DXレポート2（中間取りまとめ）", "source": "経済産業省 (2020年12月28日公表)",
            "doi": "https://www.meti.go.jp/press/2020/12/20201228004/20201228004-1.pdf", "status": "即時取得可能 (Open Access)",
            "route": "経済産業省 公式サイト（直接PDFダウンロード）",
            "summary": "コロナ禍でのDX実態と超短期アクションの提唱。9割以上の企業がDX未着手・散発的実施にとどまる現状を分析し、共通プラットフォーム利用を推奨。"
        },
        {
            "id": "文献18", "type": "行政・政策レポート", "author": "経済産業省", "year": 2021,
            "title": "DXレポート2.1（DXフレームワークとガイダンス）", "source": "経済産業省 (2021年8月31日公表)",
            "doi": "https://www.meti.go.jp/press/2021/08/20210831005/20210831005-1.pdf", "status": "即時取得可能 (Open Access)",
            "route": "経済産業省 公式サイト（直接PDFダウンロード）",
            "summary": "デジタル産業の創出に向けた産業構造転換。既存産業の「デジタル・トランスフォーメーション」から新規価値創出エコシステムへの移行指針。"
        },
        {
            "id": "文献19", "type": "行政・政策レポート", "author": "独立行政法人情報処理推進機構 (IPA)", "year": 2023,
            "title": "DX白書2023～進展する変革に向けた具体的な取り組み～", "source": "IPA (2023年2月9日公表)",
            "doi": "https://www.ipa.go.jp/publish/wp-dx/dx-2023.html", "status": "即時取得可能 (Open Access)",
            "route": "IPA 公式サイト（直接PDF無償ダウンロード）",
            "summary": "日米企業のDX推進状況の定量的比較調査。企業戦略、組織・人材、ITシステムの各軸から日本の人材不足・組織的心理抵抗の深刻さを解明。"
        },
        {
            "id": "文献20", "type": "行政・政策レポート", "author": "中小企業庁", "year": 2022,
            "title": "中小企業白書 2022年版", "source": "中小企業庁 (2022年4月26日閣議決定)",
            "doi": "https://www.chusho.meti.go.jp/pamflet/hakusyo/2022/2022index.html", "status": "即時取得可能 (Open Access)",
            "route": "中小企業庁 公式サイト（全章PDF無償ダウンロード）",
            "summary": "中小企業の自己変革と成長。デジタル化の進展ステージ（段階1〜4）と付加価値創出の関係、IT導入補助金の効果検証。"
        },
        {
            "id": "文献21", "type": "行政・政策レポート", "author": "中小企業庁", "year": 2023,
            "title": "中小企業白書 2023年版", "source": "中小企業庁 (2023年4月28日閣議決定)",
            "doi": "https://www.chusho.meti.go.jp/pamflet/hakusyo/2023/2023index.html", "status": "即時取得可能 (Open Access)",
            "route": "中小企業庁 公式サイト（全章PDF無償ダウンロード）",
            "summary": "価格転嫁と賃上げ、DX推進を通じた中小企業の生産性向上。リスキリングやデジタル人材確保の組織的課題を詳述。"
        }
    ]

    for row_idx, item in enumerate(theory_docs, start=2):
        fill = zebra_fill if row_idx % 2 == 0 else white_fill
        ws3.cell(row=row_idx, column=1, value=item["id"]).alignment = Alignment(horizontal="center", vertical="center")
        ws3.cell(row=row_idx, column=2, value=item["type"]).alignment = Alignment(horizontal="center", vertical="center")
        ws3.cell(row=row_idx, column=3, value=item["author"]).alignment = Alignment(vertical="center")
        ws3.cell(row=row_idx, column=4, value=item["year"]).alignment = Alignment(horizontal="center", vertical="center")
        ws3.cell(row=row_idx, column=5, value=item["title"]).alignment = Alignment(vertical="center", wrap_text=True)
        ws3.cell(row=row_idx, column=6, value=item["source"]).alignment = Alignment(vertical="center", wrap_text=True)
        
        c_doi = ws3.cell(row=row_idx, column=7, value=item["doi"])
        c_doi.alignment = Alignment(vertical="center")
        if item["doi"].startswith("http"):
            c_doi.hyperlink = item["doi"]
            c_doi.font = link_font

        ws3.cell(row=row_idx, column=8, value=item["status"]).alignment = Alignment(horizontal="center", vertical="center")
        ws3.cell(row=row_idx, column=9, value=item["route"]).alignment = Alignment(vertical="center", wrap_text=True)
        ws3.cell(row=row_idx, column=10, value=item["summary"]).alignment = Alignment(vertical="center", wrap_text=True)

        for col in range(1, 11):
            cell = ws3.cell(row=row_idx, column=col)
            cell.border = cell_border
            if col != 7 or not item["doi"].startswith("http"):
                cell.font = data_font
            cell.fill = fill

    for col in range(1, 11):
        cell = ws3.cell(row=1, column=col)
        cell.fill = header_fill_green
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = cell_border

    ws3.row_dimensions[1].height = 28
    col_widths_sheet3 = {
        "A": 10, "B": 18, "C": 22, "D": 10, "E": 38, "F": 32, "G": 36, "H": 22, "I": 34, "J": 46
    }
    for col_letter, width in col_widths_sheet3.items():
        ws3.column_dimensions[col_letter].width = width
    ws3.freeze_panes = "A2"

    # 保存
    out_dir_20261005 = r"G:\マイドライブ\antigravity\IDM\20261005\reports"
    out_dir_20261004 = r"G:\マイドライブ\antigravity\IDM\20261004\reports"
    os.makedirs(out_dir_20261005, exist_ok=True)
    os.makedirs(out_dir_20261004, exist_ok=True)

    # ユーザーがExcelを開いていても保存できるよう、専用版ファイル名と共通版ファイル名の両方を生成
    target_names = [
        "IDM_DX_参考文献カタログ_県立広島大取得依頼付.xlsx",
        "IDM_DX_投稿論文_参考文献リスト_完全版.xlsx"
    ]

    saved_files = []
    for d in [out_dir_20261005, out_dir_20261004]:
        for name in target_names:
            target_path = os.path.join(d, name)
            try:
                wb.save(target_path)
                saved_files.append(target_path)
            except PermissionError:
                # ユーザーがExcelで開いている場合は別名で保存
                alt_path = os.path.join(d, name.replace(".xlsx", "_new.xlsx"))
                try:
                    wb.save(alt_path)
                    saved_files.append(alt_path)
                except Exception as e:
                    print(f"Failed to save {alt_path}: {e}")

    print("Updated Excel with 4 sheets saved successfully:")
    for sf in saved_files:
        print(f"- {sf}")

if __name__ == "__main__":
    build_references_excel()
