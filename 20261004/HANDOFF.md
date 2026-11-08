# 研究プロジェクト引き継ぎ書 (HANDOFF.md)

**プロジェクト名**: IDM DX大規模意識調査・企業規模×組織階層二元配置分散分析プロジェクト  
**作成日時**: 2026年10月4日  
**ルート作業ディレクトリ**: `G:\マイドライブ\antigravity\IDM\20261004`  
**実行Python環境**: `C:\Users\admin\AppData\Local\Python\pythoncore-3.14-64\python.exe`  

---

## 1. 概要と達成成果

本プロジェクトは、日本国内民間企業に勤務する就業者の大規模実査データ（`G:\マイドライブ\IDM\data-cross.xlsx`）のうち、本調査を完了した全有効回答者 $N = 2,035$ 名を対象に、サンプルの間引きや恣意的な足切りを一切行わない完全決定論的解析（Deterministic Complete Cohort Analysis）を実施した。

多重モデル協調・相互監査ワークフロー（Gemini 3.8 Flash & Pro）により、以下の6ステップを完全完遂した。
1. **ステップ1**: 全量EDA、尺度信頼性分析（Cronbach's $\alpha$）、二元配置分散分析（Type II ANOVA）、事後多重比較（Tukey HSD）、層別単純主効果検定（Welch $t$ + Holm調整）の自動実行（`01_analysis.py`）
2. **ステップ2**: APA第7版準拠・統一デザイン・300 DPI高解像度可視化およびベクターPDF（Figures 1〜3）の自動生成（`02_generate_figures.py`）
3. **ステップ3**: 実在する査読付オープンアクセス学術論文15本の自動収集・`pypdf`現物監査・引用根拠データベース構築（`03_harvest_literature.py`）
4. **ステップ4**: 完全数値整合性を担保したIMRaD形式学術論文ドラフトの執筆（`draft_paper.md`）
5. **ステップ5**: 上級計量心理学者視点の敵対的査読（`reviewer_critique.md`）、全43統計指標の自動文字列・数値突合監査（`04_audit_metrics.py`、不一致0件保証）、および査読対応最終原稿の確定（`final_paper.md`）
6. **ステップ6**: デスクトップ引き継ぎドキュメント（本ドキュメント `HANDOFF.md`）の策定

---

## 2. ディレクトリ構成と成果物完全インベントリ

すべての成果物は `G:\マイドライブ\antigravity\IDM\20261004` 配下に格納されており、外部ディレクトリへの依存は一切ありません。

```text
G:\マイドライブ\antigravity\IDM\20261004\
│
├── HANDOFF.md                          # [本ファイル] 全体引き継ぎ・再現手順書
├── draft_paper.md                      # ステップ4 学術論文ドラフト原稿
├── final_paper.md                      # ステップ5 査読対応完成論文原稿
│
├── scripts/                            # 実行スクリプト群（完全自動・決定論的）
│   ├── 00_inspect_columns.py           # データ構造・カラム探索用
│   ├── 01_analysis.py                  # 全量EDA・信頼性・ANOVA解析
│   ├── 02_generate_figures.py          # 300 DPI・ベクターPDF作図
│   ├── 03_harvest_literature.py        # OA論文収集・pypdfテキスト監査
│   └── 04_audit_metrics.py             # 論文内数値・JSON突合自動監査
│
├── artifacts/                          # 構造化データ成果物
│   ├── analysis_dataset_scores.csv     # N=2,035の合成スコア付き解析用データ
│   ├── results_summary.json            # 全統計検定結果マスターJSON
│   ├── literature_metadata.json        # 査読付OA論文15本の書誌・テキスト抜粋JSON
│   └── literature_grounding.md         # 論文引用根拠データベース
│
├── reports/                            # 監査レポート・査読書
│   ├── statistical_audit_log.md        # 統計監査ログ（欠損値判定、全度数表）
│   ├── reviewer_critique.md            # 上級計量心理学者による敵対的査読書
│   └── metrics_audit_report.json       # 43/43項目完全一致の自動監査ログ
│
├── figures/                            # 論文掲載用図表（300 DPI PNG & ベクター PDF）
│   ├── Figure1_Interaction.png         # 図1: 二元配置ANOVA交互作用プロット (PNG, 300 DPI)
│   ├── Figure1_Interaction.pdf         # 図1: ベクターPDF
│   ├── Figure2_Distribution.png        # 図2: バイオリンプロット・箱ひげ図分布 (PNG, 300 DPI)
│   ├── Figure2_Distribution.pdf        # 図2: ベクターPDF
│   ├── Figure3_Cluster_Analysis.png    # 図3: 2次元プロファイル・ダイナミクス (PNG, 300 DPI)
│   └── Figure3_Cluster_Analysis.pdf    # 図3: ベクターPDF
│
└── papers_pdf/                         # 査読付オープンアクセス学術論文 PDF現物（15本）
    ├── 01_2022_Drivers of Digital Transformation in SMEs.pdf
    ├── 02_2023_UNRAVELING PERCEPTIONS OF BARRIERS TO DIGITAL TRANSFORMATION...pdf
    ├── 03_2026_Digital Transformation, Dynamic Capability, and Innovation Performance...pdf
    ├── 04_2023_Digital Transformation for SMEs Development Based at Four Levels...pdf
    ├── 05_2022_Green transformational leadership and green creativity...pdf
    ├── 06_2020_The use of digital technologies by small and medium enterprises...pdf
    ├── 07_2026_Improving Leadership, Spirituality, and Organizational Performance...pdf
    ├── 08_2021_Digital Transformation Challenges in the Sales of Pharmaceutical...pdf
    ├── 09_2022_Digital Technologies and the Performance of Small and Medium...pdf
    ├── 10_2026_Digital transformation in tourism SMEs A strategic imperative...pdf
    ├── 11_2023_Digital Servitization and Business Model Innovation in SMEs...pdf
    ├── 12_2024_The role of digital transformation in boosting CSR-driven green...pdf
    ├── 13_2026_Research on the Impact of Digital Transformation on the Performance...pdf
    ├── 14_2023_Network evolution of diffusion in enterprise digitalization...pdf
    └── 15_2024_Toward the role of organizational culture in data-driven digital...pdf
```

---

## 3. 分析対象データと主要統計パラメータ

- **解析対象母集団**: 本調査完了者 $N = 2,035$ 名（欠損値 0 件）
- **独立変数 1（企業規模: 2水準）**:
  - 大企業（Large: 従業員1,000人以上）: $n = 745$ 名 (36.6%)
  - 中小企業（SMO: 従業員1,000人未満）: $n = 1,290$ 名 (63.4%)
- **独立変数 2（職制グループ: 3水準）**:
  - 1. 経営層（Executives）: $n = 329$ 名 (16.2%)
  - 2. 部課長クラス（Managers）: $n = 806$ 名 (39.6%)
  - 3. 一般社員（Staff）: $n = 900$ 名 (44.2%)
- **主従属変数（SC18: DX推進意識・心理的所有感, 9項目）**:
  - クロンバック $\alpha = 0.8592$
  - 全体平均: $M = 3.2709, SD = 0.6279$
  - 規模主効果: $F(1, 2029) = 8.04, p = 0.0046, \eta_p^2 = 0.0039$
  - 職制主効果: $F(2, 2029) = 38.58, p = 3.60 \times 10^{-17}, \eta_p^2 = 0.0366$
  - 交互作用効果: $F(2, 2029) = 4.32, p = 0.0134, \eta_p^2 = 0.0042$
- **補完的従属変数（SC15: DXリスク懸念・組織摩擦, 9項目）**:
  - クロンバック $\alpha = 0.8183$
  - 全体平均: $M = 3.0802, SD = 0.6327$
  - 規模主効果: $F(1, 2029) = 1.97, p = 0.1601, \eta_p^2 = 0.0010$ (有意差なし)
  - 職制主効果: $F(2, 2029) = 61.98, p = 7.44 \times 10^{-27}, \eta_p^2 = 0.0576$
  - 交互作用効果: $F(2, 2029) = 5.79, p = 0.0031, \eta_p^2 = 0.0057$
- **尺度間直交性**:
  - ピアソン相関係数 $r = -0.0901, p = 4.66 \times 10^{-5}$（共有分散 $r^2 < 1\%$）

---

## 4. 完全再現（Replication）コマンド手順

本研究成果は以下のコマンドを順次実行することで、ゼロから100%同一の結果を再生成可能です。

```powershell
# 作業環境のディレクトリへ移動
cd "G:\マイドライブ\antigravity\IDM\20261004"

# 1. 統計解析およびJSON成果物の生成
C:\Users\admin\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/01_analysis.py

# 2. 論文用300 DPI高解像度図表・ベクターPDFの生成
C:\Users\admin\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/02_generate_figures.py

# 3. 査読付オープンアクセス論文の監査と引用根拠DB生成
C:\Users\admin\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/03_harvest_literature.py

# 4. 論文内数値とJSONデータの完全突合監査（43項目チェック）
C:\Users\admin\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/04_audit_metrics.py
```

---

## 5. 今後の拡張性および引き継ぎ注意事項

1. **業種別統制の拡張**:  
   `analysis_dataset_scores.csv` には業種区分（SC1）の追加結合が容易な形式で保存されています。業種ダミーを共変量とした共分散分析（ANCOVA）や多変量分散分析（MANOVA）への拡張が可能です。
2. **図表の統一性維持**:  
   追加で図表を作成する際は、`scripts/02_generate_figures.py` で定義されているカラーパレット（大企業: `#1B365D`, 中小企業: `#C0392B`）、マーカー（`o` vs `s`）、およびフォント設定（Meiryo, Yu Gothic）を必ず継承してください。
3. **論文の投稿先想定**:  
   本稿（`final_paper.md`）は、情報システム系・経営管理系の査読付学会誌（情報経営学会誌、経営情報学会誌、日本経営学会誌、または *Electronic Markets* などの国際OA誌）の投稿規程に準拠したフォーマットで構成されています。
