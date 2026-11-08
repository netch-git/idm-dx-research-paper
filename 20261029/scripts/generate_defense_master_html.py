#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDM Project - 学術論文 引用文献・理論基盤・分析妥当性 完全防衛マスター台帳 HTML版生成スクリプト
DADS（デジタル庁デザインシステム）準拠、完全オフライン対応、インタラクティブ検索＆タブUI
"""

import os
import sys
import json
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

OUTPUT_HTML = Path(r"G:\マイドライブ\antigravity\IDM\20261029\reports\20261029_学術論文_引用文献・理論基盤・分析妥当性_完全防衛マスター台帳.html")

from generate_defense_master_report import ALL_REFS

def build_html():
    refs_json = json.dumps(ALL_REFS, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>学術論文 引用文献・理論基盤・分析妥当性 完全防衛マスター台帳</title>
  <!-- KaTeX CSS/JS (CDN + Fallback) -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
  <style>
    :root {{
      --primary: #005BAC;
      --primary-dark: #004080;
      --primary-light: #E8F1FA;
      --secondary: #00838F;
      --success: #228543;
      --danger: #D32F2F;
      --warning: #F57C00;
      --bg: #F8F9FA;
      --surface: #FFFFFF;
      --text: #1A1A1A;
      --text-muted: #555555;
      --border: #DDE2E5;
      --shadow: 0 4px 12px rgba(0, 91, 172, 0.08);
      --font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: var(--font-family);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.7;
      padding-bottom: 80px;
    }}

    /* Header */
    header {{
      background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
      color: white;
      padding: 30px 20px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }}
    .header-container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    .badge-pill {{
      display: inline-block;
      padding: 4px 12px;
      font-size: 12px;
      font-weight: bold;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.2);
      margin-bottom: 10px;
    }}
    h1 {{ font-size: 26px; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.5px; }}
    .subtitle {{ font-size: 14px; opacity: 0.9; }}

    /* Layout */
    .container {{
      max-width: 1200px;
      margin: 20px auto;
      padding: 0 15px;
    }}

    /* Navigation Tabs */
    .nav-tabs {{
      display: flex;
      gap: 8px;
      background: white;
      padding: 8px;
      border-radius: 12px;
      border: 1px solid var(--border);
      margin-bottom: 25px;
      box-shadow: var(--shadow);
      overflow-x: auto;
    }}
    .nav-btn {{
      padding: 10px 18px;
      border: none;
      background: none;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }}
    .nav-btn.active {{
      background: var(--primary);
      color: white;
      box-shadow: 0 2px 8px rgba(0, 91, 172, 0.3);
    }}

    /* Search & Filter Bar */
    .search-box {{
      background: white;
      padding: 16px;
      border-radius: 12px;
      border: 1px solid var(--border);
      margin-bottom: 25px;
      box-shadow: var(--shadow);
      display: flex;
      gap: 15px;
      flex-wrap: wrap;
    }}
    .search-input {{
      flex: 1;
      min-width: 260px;
      padding: 10px 15px;
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 14px;
      outline: none;
    }}
    .search-input:focus {{ border-color: var(--primary); }}

    /* Cards Grid */
    .cards-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
    }}

    .ref-card {{
      background: white;
      border-radius: 12px;
      border: 1px solid var(--border);
      padding: 24px;
      box-shadow: var(--shadow);
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .ref-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(0, 91, 172, 0.12);
    }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid var(--border);
      padding-bottom: 12px;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .card-id {{
      font-size: 13px;
      font-weight: 800;
      color: var(--primary);
      background: var(--primary-light);
      padding: 3px 8px;
      border-radius: 4px;
    }}
    .card-title {{
      font-size: 18px;
      font-weight: 800;
      color: var(--primary-dark);
      flex: 1;
      margin-left: 10px;
    }}
    .card-category {{
      font-size: 12px;
      background: #EFEFEF;
      padding: 4px 10px;
      border-radius: 6px;
      color: #333;
    }}

    .section-title {{
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--secondary);
      margin-top: 14px;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .summary-box {{
      background: #F4F8FC;
      border-left: 4px solid var(--primary);
      padding: 12px 16px;
      border-radius: 0 8px 8px 0;
      font-size: 14.5px;
      margin-bottom: 12px;
    }}

    .reason-box {{
      font-size: 14px;
      margin-bottom: 12px;
      color: #222;
    }}

    .qa-box {{
      background: #FFF9F2;
      border: 1px solid #FFE0B2;
      border-radius: 8px;
      padding: 14px;
      margin-top: 14px;
    }}
    .q-text {{
      font-weight: 800;
      color: var(--danger);
      font-size: 14px;
      margin-bottom: 8px;
    }}
    .a-text {{
      font-size: 14px;
      color: #1A1A1A;
      line-height: 1.65;
    }}

    .meta-tags {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 14px;
      padding-top: 10px;
      border-top: 1px dashed var(--border);
    }}
    .meta-tag {{ background: #F0F2F5; padding: 2px 8px; border-radius: 4px; }}

    /* Tab Contents */
    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}

    /* FAQ Styles */
    .faq-item {{
      background: white;
      border-radius: 12px;
      border: 1px solid var(--border);
      padding: 20px;
      margin-bottom: 16px;
      box-shadow: var(--shadow);
    }}
    .faq-q {{
      font-size: 16px;
      font-weight: 800;
      color: var(--primary-dark);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .faq-q::before {{
      content: "Q";
      background: var(--danger);
      color: white;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: bold;
      flex-shrink: 0;
    }}
    .faq-a {{
      font-size: 14.5px;
      line-height: 1.7;
      color: #222;
      background: var(--primary-light);
      padding: 14px 18px;
      border-radius: 8px;
      border-left: 4px solid var(--primary);
    }}

    /* Table Styles */
    .custom-table {{
      width: 100%;
      border-collapse: collapse;
      background: white;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: var(--shadow);
      font-size: 13.5px;
    }}
    .custom-table th, .custom-table td {{
      padding: 12px 14px;
      border: 1px solid var(--border);
      text-align: left;
    }}
    .custom-table th {{
      background: var(--primary);
      color: white;
      font-weight: 700;
    }}
    .custom-table tr:nth-child(even) {{ background: #FAFAFA; }}

    /* Footer */
    footer {{
      text-align: center;
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 40px;
    }}
  </style>
</head>
<body>

<header>
  <div class="header-container">
    <div class="badge-pill">🛡️ 学術的誠実性・査読最強防衛マスター</div>
    <h1>学術論文 引用文献・理論基盤・分析妥当性 完全防衛台帳</h1>
    <div class="subtitle">就業者 N = 2,035 名 完全決定論的マイクロデータ解析 ｜ 指導教官試問・査読想定問答集</div>
  </div>
</header>

<div class="container">
  <!-- Navigation Tabs -->
  <div class="nav-tabs">
    <button class="nav-btn active" onclick="switchTab('tab-cards')">📚 全25文献カード目録</button>
    <button class="nav-btn" onclick="switchTab('tab-faq')">🎯 指導教官想定問答（FAQ 10選）</button>
    <button class="nav-btn" onclick="switchTab('tab-blau')">🏛️ 【特論】Blau & Scott (1962)</button>
    <button class="nav-btn" onclick="switchTab('tab-methods')">🔬 分析手法の採用妥当性（数理防衛）</button>
  </div>

  <!-- TAB 1: CARDS -->
  <div id="tab-cards" class="tab-content active">
    <div class="search-box">
      <input type="text" id="searchInput" class="search-input" placeholder="🔍 著者名、キーワード、仮説（例: Colquitt, 分配的公正, 仮説2, CMB）で瞬時に絞り込み..." oninput="filterCards()">
      <div style="font-size: 13px; color: var(--text-muted); display: flex; align-items: center;">
        該当文献数: <span id="cardCount" style="font-weight: bold; margin-left: 5px; color: var(--primary);">25</span> 件
      </div>
    </div>
    <div id="cardsContainer" class="cards-grid"></div>
  </div>

  <!-- TAB 2: FAQ -->
  <div id="tab-faq" class="tab-content">
    <div id="faqContainer"></div>
  </div>

  <!-- TAB 3: BLAU & SCOTT -->
  <div id="tab-blau" class="tab-content">
    <div class="ref-card" style="margin-bottom: 20px;">
      <h2 style="color: var(--primary-dark); margin-bottom: 12px;">🏛️ Peter M. Blau & W. Richard Scott (1962) 批判的検証と肯定的防衛</h2>
      <p style="font-size: 14.5px; margin-bottom: 15px;">
        一次資料: 2026年10月28日受領 スキャン全14分冊（<code>G:\\マイドライブ\\antigravity\\IDM\\20261028\\papers_pdf</code>）
      </p>
      <div class="summary-box">
        <strong>原著の確定事実（該当ページより文字通り抽出）:</strong><br>
        ・<strong>pp. 223–227</strong>: 組織規模（Size）の拡大は構造的複雑性（Complexity）をもたらし、専門分化と水平的・垂直的分化を進展させる。<br>
        ・<strong>pp. 162–164, 234</strong>: 階層段数（Hierarchical levels）の多段化は、大規模組織における調整機能の不可欠な帰結である。<br>
        ・<strong>p. 159, 232</strong>: 階層間の社会的距離（Social distance）および非人格性（Impersonality）が拡大し、トップと現場の心理的断絶を深める。<br>
        ・<strong>pp. 172–173, 242–244</strong>: 階層的権威構造は上方コミュニケーションを著しく歪曲（Distortion of upward communication）させ、上位層には都合よく選別・濾過された情報しか届かない。
      </div>

      <table class="custom-table" style="margin-top: 20px;">
        <tr>
          <th style="width: 40%;">査読者・教官からの批判的ツッコミ（批判的視点）</th>
          <th style="width: 60%;">本研究の肯定的防衛ロジック（反論・回答シナリオ）</th>
        </tr>
        <tr>
          <td><strong>「1962年の半世紀前の製造業・官公庁の古典理論は、アジャイルでフラットな現代DX組織には時代錯誤ではないか？」</strong></td>
          <td><strong>【深層構造の普遍性】</strong>: クラウドやTeams等で見かけ上のフラット化が進んでも、Blau & Scottが示した『分業による責任の細分化と社会的距離』は消滅しない。むしろ現場の暗黙知が定量的ダッシュボードから脱落し、経営層と現場の認識乖離は水面下でより不可視化・深刻化している。</td>
        </tr>
        <tr>
          <td><strong>「大企業の方がDX投資余力があり、社内教育も充実しているのだから、現場の当事者意識も高いはずではないか？」</strong></td>
          <td><strong>【実証データによる証明】</strong>: 本研究の実証結果（N=2,035）では、仮説1bの通り<strong>規模が大きい組織ほど経営層と現場の当事者意識の乖離が有意に拡大する（交互作用 β = -0.114, p < 0.001）</strong> ことが明確に示された。大企業ほど分化が進み情報が歪曲されるというBlau & Scottの理論的予測が、現代のDXにおいても強固に機能している揺るぎない証拠である。</td>
        </tr>
      </table>
    </div>
  </div>

  <!-- TAB 4: METHODS -->
  <div id="tab-methods" class="tab-content">
    <div class="ref-card">
      <h2 style="color: var(--primary-dark); margin-bottom: 12px;">🔬 分析手法の採用妥当性と頑健性検証（数理防衛）</h2>
      <div class="qa-box" style="margin-bottom: 15px;">
        <div class="q-text">1. なぜ k-means クラスタリング（3分類）を採用したのか？</div>
        <div class="a-text">
          変革推進意識（SC18）と組織摩擦（SC21）という直交する2軸から、恣意的な基準を排したデータ駆動型の類型化を行うためです。エルボー法によるクラスタ内二乗和（SSE）の変化点、およびシルエット係数の最大化を検証した結果、統計的にk=3が最適解として導出されました。これにより「変革牽引層」「摩擦直面層（当事者意識はあるが摩擦に苦しむ層）」「低当事者意識・高摩擦層（抵抗層）」という極めて解釈性の高い3類型が客観的に同定されました。
        </div>
      </div>

      <div class="qa-box" style="margin-bottom: 15px;">
        <div class="q-text">2. 分配的公正（SC18-1, 4）と当事者意識（SC18-1〜5）の項目重複（自己相関）に対する防御は？</div>
        <div class="a-text">
          <strong>【査読最強防御】</strong> 重複する2項目を完全に除外した「3項目版（SC18-2, 3, 5：業務効率化・負担軽減・スキル向上期待）」による再クラスタリング感度分析を実施しました。その結果、重複を完全排除しても低分配群のオッズ比は <strong>OR = 2.409 (p < 0.001)</strong> と高度に有意であり、多項ロジットでも <strong>OR = 3.842 (p < 0.001)</strong> と強固な正の関連が維持されることを確認しております。
        </div>
      </div>

      <div class="qa-box" style="margin-bottom: 15px;">
        <div class="q-text">3. 共通方法バイアス（CMB）への数理的防護（Siemsen et al., 2010）</div>
        <div class="a-text">
          同一回答者データにおいて、共通方法バイアスは主効果を水増しすることはあっても、<strong>交互作用項（掛け算・調整効果）を人為的に作り出すことは絶対に不可能であり、むしろ真の効果を保守的に減衰（過小推定）させる</strong> ことが数理的に証明されています（Siemsen et al., 2010, ORM誌）。本研究において仮説1b、仮説3、仮説5の交互作用効果が極めて高度（p < 0.001）に有意であった事実そのものが、本結果がCMBによる偽相関ではない数学的証明です。
        </div>
      </div>
    </div>
  </div>

</div>

<footer>
  IDM Project Literature Defense Master Dashboard &copy; 2026 | Full Sample Deterministic N = 2,035 Validated
</footer>

<script>
const REFS_DATA = {refs_json};

const FAQ_DATA = [
  {{
    q: "Q1: なぜこのテーマ（DX推進意識と組織摩擦の階層乖離）を選んだのか？",
    a: "従来のDX研究は、最新ツールの導入（技術決定論）やトップの強力なリーダーシップというマクロ視点、あるいは現場のIT受容というミクロ視点に偏っていました。しかし現実の日本企業では、経営層が旗を振っても現場が冷淡に反発し、中間管理職が板挟みで悲鳴を上げています。この『階層間のパーセプション・ギャップ（認識のズレ）』と『分配的不公正』こそが変革停滞の真のボトルネックであると着眼し、組織行動論と情報システム論を統合して2,035名のマイクロデータで解明した点に本研究の独自性と社会的意義があります。"
  }},
  {{
    q: "Q2: なぜk-meansクラスタリングでクラスタ数を『3』にしたのか？",
    a: "変革当事者意識（SC18）と組織摩擦（SC21）という2つの直交する軸から、恣意性を排したデータ駆動型の類型化を行うためです。エルボー法によるクラスタ内二乗和（SSE）の減少率の変化点、およびシルエット係数の最大化を検証した結果、統計的にk=3が最適解として導出されました。これにより、『変革牽引層』『摩擦直面層』『低当事者意識・高摩擦層』という、組織行動論的に極めて解釈性の高い3類型が客観的に同定されました。"
  }},
  {{
    q: "Q3: 仮説2で、分配的公正（SC18-1, 4）と当事者意識（SC18-1〜5）の項目重複（自己相関）があるのでは？",
    a: "本研究では、個人の金銭・処遇還元への期待そのものが変革当事者意識の中核要素であると理論的に位置づけて主分析を行いましたが、自己相関の懸念を100%払拭するため、重複する2項目を完全に除外した『3項目版（SC18-2, 3, 5）』による再クラスタリング感度分析を実施しました。その結果、重複を完全排除しても低分配群のオッズ比は OR = 2.409 (p < 0.001)、多項ロジットでも OR = 3.842 (p < 0.001) と強固な正の関連が維持されることを確認しております。"
  }},
  {{
    q: "Q4: 横断的アンケート調査における共通方法バイアス（CMB）への反論は？",
    a: "手続的対策およびHarmanの単因子検定（第1因子の説明率が50%未満）に加え、決定的な証拠としてSiemsen et al. (2010, ORM誌) が数理統計学的に証明した通り、共通方法分散は交互作用項を人為的に有意にすることはできず、むしろ真の効果を保守的に減衰させます。本研究において仮説1b、仮説3、仮説5の交互作用効果が高度（p < 0.001）に有意であった事実そのものが、CMBによる偽相関ではない数学的証明です。"
  }},
  {{
    q: "Q5: なぜ1962年のBlau & Scottのような古典を現代のDXに引っ張ってきたのか？",
    a: "組織規模の拡大がもたらす『専門分化 → 階層多段化 → 社会的距離の拡大 → 情報の歪曲』という官僚制の深層病理は、テクノロジーが変わっても人間組織の普遍的構造として変わらないからです。むしろデジタル化で見かけのフラット化が進んだ現代においてこそ、現場の生々しい抵抗が定量的ダッシュボードから脱落し、経営層と現場の認識乖離が不可視化されるという『デジタル・パラドックス』を説明する上で、Blau & Scottの理論が最強の分析枠組みを提供してくれるためです。"
  }},
  {{
    q: "Q6: 中小企業と大企業で、なぜ当事者意識や摩擦の傾向が異なるのか？",
    a: "中小企業（SMO）は階層段数が少なく、経営者と現場の距離が近いため意図が伝播しやすい一方、外部IT資源への依存度（Pfeffer & Salancik, 1978）が高くリソース制約に直面します。対して大企業は、資金・IT人材は豊富であるものの、Blau & Scottが示したように階層が多段化してトップと現場の社会的距離が極大化し情報が歪曲されるため、経営層の意図が現場に浸透せず乖離が最も拡大するという構造的トレードオフが存在するためです。"
  }},
  {{
    q: "Q7: 現場の抵抗は単なる『ITスキル不足』や『新しいことへの不安』ではないのか？",
    a: "従来の技術受容モデル（TAM等）ではそう片付けられがちでした。しかし本研究の実証結果では、分配的公正（給与や評価への還元）を認知している現場層は、ITリテラシーに関わらず変革に極めて前向きです。いくら研修を行っても、追加の負担に対して評価や処遇の還元が約束されない組織では、Adams (1965) の衡平理論の通り、現場は自己防衛として合理的に抵抗を選択します。すなわち現場抵抗の本質は『スキルの問題』ではなく『組織の分配公正性の欠落』です。"
  }},
  {{
    q: "Q8: 手続的公正（対話や参加）があれば、給与を上げなくても現場は納得するのか？",
    a: "Folger (1977) の発言権効果（Voice Effect）が示す通り、手続的公正は分配の低さを完全に帳消しにする魔法ではありません。しかし、短期的には全員の昇給が難しい経営環境において、意思決定プロセスの透明性を高め、現場の意見を吸い上げる手続的公正を担保することで、『不満が致命的な組織摩擦や破壊的サボタージュへ転化することを劇的に食い止める緩衝装置（バッファー）』として機能することを本研究の調整効果（仮説3）が実証しています。"
  }},
  {{
    q: "Q9: なぜ中間管理職（課長・部長）が最も高い摩擦を抱えるのか？",
    a: "Huy (2002) が示した『感情的バランシング』およびBalogun & Johnson (2004) の『センスメイキング論』がその理由を解明しています。中間管理職は、経営層からの抽象的な変革プレッシャーを受け止めつつ、現場の日常業務の崩壊を防ぐために防波堤となって葛藤を調停しています。本研究のデータでも、彼らは当事者意識を持ちながらも摩擦に苦しむ『摩擦直面層（クラスタ2）』に最も多く分布しており、変革の重圧を一身に背負う『最も過酷な結節点』であることが立証されました。"
  }},
  {{
    q: "Q10: 本研究が経営情報学および組織行動学にもたらす最大の学術的貢献（新規性）は何か？",
    a: "一言で言えば、『情報システム（IS）研究におけるDXの議論を、組織行動論（OB）における組織公正・階層乖離論と融合させ、就業者2,035名の完全決定論的マイクロデータによって実証的にモデル化した点』にあります。これまで精神論や技術論で語られていた現場の変革抵抗を、社会交換理論と組織構造論のレンズを通じて『分配的公正の欠落と階層間情報歪曲が生み出す合理的帰結』として科学的に解明した点に最大の新規性があります。"
  }}
];

function switchTab(tabId) {{
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
  
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}}

function renderCards(refs) {{
  const container = document.getElementById('cardsContainer');
  container.innerHTML = '';
  document.getElementById('cardCount').textContent = refs.length;

  refs.forEach(r => {{
    const card = document.createElement('div');
    card.className = 'ref-card';
    card.innerHTML = `
      <div class="card-header">
        <span class="card-id">${{r.id}}</span>
        <span class="card-title">${{r.key}}：${{r.author}} (${{r.year}})</span>
        <span class="card-category">${{r.category}}</span>
      </div>

      <div style="font-size: 13px; color: #666; margin-bottom: 10px;">
        <strong>原題:</strong> <em>${{r.title}}</em><br>
        <strong>掲載:</strong> ${{r.source}} ${{r.doi ? '｜ DOI: ' + r.doi : ''}}
      </div>

      <div class="section-title">📖 誰でも理解できる平易な要約（論文の中核内容）</div>
      <div class="summary-box">${{r.plain_summary}}</div>

      <div class="section-title">🎯 本論文での採用根拠（なぜこの論文でなければならないのか？）</div>
      <div class="reason-box">${{r.adoption_reason}}</div>

      <div class="section-title">🔬 分析手法・統計的妥当性の根拠としての役割</div>
      <div class="reason-box">${{r.methodological_role}}</div>

      <div class="qa-box">
        <div class="q-text">⚔️ 指導教官・査読者からの批判的ツッコミ:</div>
        <div style="font-style: italic; margin-bottom: 8px;">${{r.critical_review_question}}</div>
        <div class="q-text" style="color: var(--success);">🛡️ 完璧な学術的・実証的防衛ロジック（肯定的回答シナリオ）:</div>
        <div class="a-text">${{r.defensive_answer}}</div>
      </div>

      <div class="meta-tags">
        <span class="meta-tag">📍 引用箇所: ${{r.in_text_location}}</span>
        <span class="meta-tag">🎯 対応仮説: ${{r.hypothesis}}</span>
        <span class="meta-tag">📄 実体PDF: <code>${{r.pdf}}</code></span>
      </div>
    `;
    container.appendChild(card);
  }});
}}

function renderFAQ() {{
  const container = document.getElementById('faqContainer');
  container.innerHTML = '';
  FAQ_DATA.forEach(f => {{
    const div = document.createElement('div');
    div.className = 'faq-item';
    div.innerHTML = `
      <div class="faq-q">${{f.q}}</div>
      <div class="faq-a">${{f.a}}</div>
    `;
    container.appendChild(div);
  }});
}}

function filterCards() {{
  const query = document.getElementById('searchInput').value.toLowerCase().trim();
  if (!query) {{
    renderCards(REFS_DATA);
    return;
  }}
  const filtered = REFS_DATA.filter(r => {{
    return (
      r.key.toLowerCase().includes(query) ||
      r.author.toLowerCase().includes(query) ||
      r.title.toLowerCase().includes(query) ||
      r.plain_summary.toLowerCase().includes(query) ||
      r.adoption_reason.toLowerCase().includes(query) ||
      r.hypothesis.toLowerCase().includes(query) ||
      r.defensive_answer.toLowerCase().includes(query)
    );
  }});
  renderCards(filtered);
}}

window.addEventListener('DOMContentLoaded', () => {{
  renderCards(REFS_DATA);
  renderFAQ();
  if (window.renderMathInElement) {{
    renderMathInElement(document.body, {{
      delimiters: [
        {{left: '$$', right: '$$', display: true}},
        {{left: '$', right: '$', display: false}}
      ],
      throwOnError: false
    }});
  }}
}});
</script>

</body>
</html>
"""
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML レポート生成完了: {OUTPUT_HTML}")

if __name__ == "__main__":
    build_html()
