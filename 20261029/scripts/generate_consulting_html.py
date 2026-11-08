#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDM Project - DX推進企業への実践的改善提案フレームワーク HTML版 生成スクリプト
"""

import sys
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

OUTPUT_HTML = Path(r"G:\マイドライブ\antigravity\IDM\20261029\reports\20261029_DX推進企業への実践的改善提案フレームワーク.html")

def generate_consulting_html():
    html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DXに苦しむ企業への実践的改善提案フレームワーク</title>
  <!-- Mermaid JS for Diagrams -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({startOnLoad: true, theme: 'neutral'});</script>
  <style>
    :root {
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
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: var(--font-family);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.75;
      padding-bottom: 80px;
    }

    header {
      background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
      color: white;
      padding: 35px 20px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }
    .header-container {
      max-width: 1100px;
      margin: 0 auto;
    }
    .badge {
      display: inline-block;
      padding: 4px 12px;
      font-size: 12px;
      font-weight: 700;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.2);
      margin-bottom: 12px;
    }
    h1 { font-size: 26px; font-weight: 800; margin-bottom: 8px; }
    .subtitle { font-size: 14.5px; opacity: 0.9; }

    .container {
      max-width: 1100px;
      margin: 30px auto;
      padding: 0 20px;
    }

    .card {
      background: white;
      border-radius: 12px;
      border: 1px solid var(--border);
      padding: 28px;
      box-shadow: var(--shadow);
      margin-bottom: 25px;
    }

    h2 {
      font-size: 20px;
      font-weight: 800;
      color: var(--primary-dark);
      border-bottom: 2px solid var(--primary-light);
      padding-bottom: 10px;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .prescription-card {
      border-left: 5px solid var(--primary);
      background: #FFFFFF;
      border-radius: 0 10px 10px 0;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
      border-top: 1px solid var(--border);
      border-right: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
    }
    .prescription-num {
      display: inline-block;
      font-size: 12px;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 4px;
      color: white;
      background: var(--primary);
      margin-bottom: 8px;
    }
    .prescription-title {
      font-size: 18px;
      font-weight: 800;
      color: var(--primary-dark);
      margin-bottom: 10px;
    }

    .quote-box {
      background: #F4F8FC;
      border-left: 4px solid var(--secondary);
      padding: 14px 18px;
      border-radius: 0 8px 8px 0;
      font-size: 14.5px;
      margin-top: 12px;
      color: #2D3748;
    }

    /* Comparison Table */
    .custom-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
      margin-top: 15px;
    }
    .custom-table th, .custom-table td {
      padding: 12px 14px;
      border: 1px solid var(--border);
      vertical-align: top;
      text-align: left;
    }
    .custom-table th {
      background: var(--primary);
      color: white;
      font-weight: 700;
    }
    .custom-table tr:nth-child(even) { background: #FAFAFA; }

    .highlight-pill {
      display: inline-block;
      font-size: 11.5px;
      font-weight: bold;
      padding: 2px 8px;
      border-radius: 12px;
      margin-right: 5px;
    }
    .pill-red { background: #FFEBEE; color: var(--danger); }
    .pill-green { background: #E8F5E9; color: var(--success); }
    .pill-blue { background: #E3F2FD; color: var(--primary); }

    footer {
      text-align: center;
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 50px;
    }
  </style>
</head>
<body>

<header>
  <div class="header-container">
    <div class="badge">🚀 実践的介入コンサルティング・フレームワーク</div>
    <h1>DXに苦しむ企業への実践的改善提案</h1>
    <div class="subtitle">「ツールの導入」から「組織公正と階層対話の設計」へ ｜ 就業者 N = 2,035 名 完全決定論的エビデンスに基づく処方箋</div>
  </div>
</header>

<div class="container">

  <!-- CARD 1: ROADMAP -->
  <div class="card">
    <h2>🧭 3段階の介入ロードマップ（Intervention Roadmap）</h2>
    <div class="mermaid">
    flowchart TD
      Phase1["【Phase 1: 診断と覚醒（可視化）】<br/>『ツールの問題ではなく、公正性と階層断絶の問題である』ことをデータで直視させる<br/>・社内パーセプション・ギャップ診断<br/>・当事者意識 vs 組織摩擦の3類型クラスタリング"]
      --> Phase2["【Phase 2: 制度の再設計（土台構築）】<br/>『ツールを入れる前に、還元と対話のルールを明文化する』<br/>・分配的公正の設計（DX還元型評価制度）<br/>・手続的公正の担保（現場参画型Voiceメカニズム）"]
      --> Phase3["【Phase 3: 現場の運用（環境防護）】<br/>『中間管理職の板挟みを解き、現場の自律走行を促す』<br/>・ミドルの引き算マネジメント（既存業務の強制廃止）<br/>・階層をバイパスするアジャイル小チームの設置"]

      style Phase1 fill:#FFF3E0,stroke:#E65100,stroke-width:2px
      style Phase2 fill:#E3F2FD,stroke:#1565C0,stroke-width:2px
      style Phase3 fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px
    </div>
  </div>

  <!-- CARD 2: 5 PRESCRIPTIONS -->
  <div class="card">
    <h2>🛠️ 5つの具体的改善処方箋（Actionable Prescriptions）</h2>

    <div class="prescription-card">
      <span class="prescription-num">処方箋 1</span>
      <div class="prescription-title">【分配的公正の再設計】「DX還元型評価制度」の導入</div>
      <p style="font-size: 14.5px;">
        現場社員は「DXに協力して効率化しても、空いた時間で別のノルマを振られるだけで給与も上がらない」という不衡平（Adams 1965）を感じています。
      </p>
      <ul style="margin-left: 20px; font-size: 14px; margin-top: 8px;">
        <li><strong>効率化果実の還元ルール明文化:</strong> 削減できた業務時間やコストの一定割合を決算賞与や特別インセンティブとして現場に還元するルールを公約する。</li>
        <li><strong>評価シートの刷新:</strong> 売上ノルマ偏重を改め、「業務プロセスの改善」「デジタルツールによる組織貢献」をMBO/OKRに最低20〜30%の比重で組み込む。</li>
      </ul>
      <div class="quote-box">
        🗣️ <strong>企業への働きかけ文句:</strong><br>
        「社長、DXの投資回収率（ROI）を最大化したいなら、まず『頑張った現場がどう得をするか』の還元ルールを先に決めてください。還元が約束されない変革は、現場にとって単なる『サービス残業の押しつけ』であり、サボタージュされるのは社会科学の必然です。」
      </div>
    </div>

    <div class="prescription-card">
      <span class="prescription-num">処方箋 2</span>
      <div class="prescription-title">【手続的公正の担保】「現場参画型・双方向Voiceメカニズム」</div>
      <p style="font-size: 14.5px;">
        情シスやコンサルだけで仕様を決め、現場には「来月からこれを使って」と頭ごなしに下達するため、手続的不公正とシニシズムが蔓延します。
      </p>
      <ul style="margin-left: 20px; font-size: 14px; margin-top: 8px;">
        <li><strong>現場エースの巻き込み:</strong> 初期段階から現場の実務担当者を「変革アンバサダー」としてコミッティに参画させ、発言権（Folger 1977）を与える。</li>
        <li><strong>不満・不具合の改善ダッシュボード:</strong> 現場からの「使いにくい」「二重入力」という声を吸い上げ、2週間以内に改善状況を全社にオープンにする。</li>
      </ul>
      <div class="quote-box">
        🗣️ <strong>企業への働きかけ文句:</strong><br>
        「全員の給料をすぐに上げることは難しくても、現場の意見を聞いて仕様に反映する『手続的公正』があれば、組織摩擦は劇的に抑えられます（本研究の仮説3実証知見）。現場を決定の『受け身』から『共創者』に変えてください。」
      </div>
    </div>

    <div class="prescription-card">
      <span class="prescription-num">処方箋 3</span>
      <div class="prescription-title">【中間管理職の防護】「引き算のマネジメント（既存業務の強制棚卸し）」</div>
      <p style="font-size: 14.5px;">
        実証データ上、最も深刻なのは<strong>中間管理職（課長・部長）が当事者意識を持ちながらも『摩擦直面層（約4割）』に集中している事実</strong>です。ミドルの感情的バランシング（Huy 2002）は限界です。
      </p>
      <ul style="margin-left: 20px; font-size: 14px; margin-top: 8px;">
        <li><strong>「足し算」の前に「引き算」を義務化:</strong> 新ツールを入れる際、経営陣は廃止する既存業務・紙の帳票・定例会議をセットで指定する（1つ足すなら2つ引く）。</li>
        <li><strong>業務廃棄権限の付与:</strong> 管理職に対し、「自部門の無駄な定例業務を即座に廃止・簡略化できる権限」を正式に認める。</li>
      </ul>
      <div class="quote-box">
        🗣️ <strong>企業への働きかけ文句:</strong><br>
        「中間管理職をDXの『抵抗勢力』と呼ぶのは不当です。彼らは変革意欲を持ちながら、現場の日常業務を破綻させないために防波堤となって倒れかけています。彼らに必要なのは研修ではなく、『既存業務を捨てる権限（引き算）』です。」
      </div>
    </div>

    <div class="prescription-card">
      <span class="prescription-num">処方箋 4</span>
      <div class="prescription-title">【組織規模別の介入差別化】大企業と中小企業の処方箋を分ける</div>
      <p style="font-size: 14.5px;">
        大企業と中小企業では、DXが停滞する構造的病理が全く異なります（Blau & Scott 1962 / Pfeffer & Salancik 1978）。
      </p>
      <ul style="margin-left: 20px; font-size: 14px; margin-top: 8px;">
        <li><strong>大企業（官僚制の壁をバイパス）:</strong> ピラミッド組織の上意下達を廃し、経営直轄の「自律型クロスファンクショナル小チーム（5〜8名）」に変革権限を委譲する。</li>
        <li><strong>中小企業（外部資源の補完）:</strong> 壮大な独自開発を真似させず、既成SaaSと公的伴走支援（商工会議所、IT導入補助金）をフル活用する。</li>
      </ul>
    </div>

    <div class="prescription-card">
      <span class="prescription-num">処方箋 5</span>
      <div class="prescription-title">【社内パーセプション・ギャップ診断】の提供</div>
      <p style="font-size: 14.5px;">
        企業に改善策を提案する際、いきなり正論を言っても経営者は動きません。本研究のフレームワーク（SC18当事者意識 × SC21組織摩擦）を簡易診断ツールとして提供し、自社の階層乖離を「客観的数値」として突きつけます。
      </p>
      <div class="quote-box">
        📊 <strong>診断アウトプット例:</strong><br>
        「御社の役員のDX当事者意識は 4.2点 ですが、現場社員は 2.1点 であり、乖離幅は全国平均の大企業よりも深刻です。社内の 38% が『低当事者意識・高摩擦層（諦め・抵抗層）』に属しており、その最大の原因は『努力が評価されない（分配的不公正）』にあります。」
      </div>
    </div>

  </div>

  <!-- CARD 3: STAKEHOLDER SCRIPTS -->
  <div class="card">
    <h2>👥 ステークホルダー別「刺さる対話スクリプト」</h2>
    <table class="custom-table">
      <thead>
        <tr>
          <th style="width: 20%;">相手</th>
          <th style="width: 35%;">相手の思い込み・言い分</th>
          <th style="width: 45%;">こちらの切り返し・働きかけスクリプト</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>経営トップ<br>（社長・役員）</strong></td>
          <td>「最新のAIやクラウドを導入したのに、現場が使わない。社員のIT教育に金を使うべきだ。」</td>
          <td><strong>「社長、現場が動かないのはスキルの問題ではなく、『使っても自分に何の得もない（むしろ仕事が増える）』からです。2,035名のデータ分析では、処遇への還元期待がない社員は抵抗層へ転落するリスクが約4倍になります。ツール予算の2割を、現場の改善成果に対するインセンティブと評価制度の改定に回してください。」</strong></td>
        </tr>
        <tr>
          <td><strong>人事部長</strong></td>
          <td>「DXは情シスやDX推進室の仕事であって、人事部の管轄ではない。」</td>
          <td><strong>「部長、DXの最大のボトルネックは『評価と処遇』です。情シスがどんなに良いシステムを入れても、人事部が『DX推進をどう評価し、浮いた時間をどう処遇するか』を設計しない限り、現場はサボタージュを続けます。DXの成否を握っているのは情シスではなく、人事部です。」</strong></td>
        </tr>
        <tr>
          <td><strong>DX推進室長<br>情シス部長</strong></td>
          <td>「現場から文句ばかり出てプロジェクトが進まない。現場は変化を嫌う保守的な連中だ。」</td>
          <td><strong>「推進室長、現場の抵抗は悪意ではなく、手続的不公正（頭ごなしの押しつけ）に対する合理的防衛です。仕様決めの段階から現場の実務者を巻き込み、意見を吸い上げる『手続的公正』を担保すれば、摩擦は有意に抑制できます。現場を共創パートナーとして巻き込みましょう。」</strong></td>
        </tr>
        <tr>
          <td><strong>現場リーダー<br>（課長・係長）</strong></td>
          <td>「上からは『DXをやれ』と言われ、現場からは『通常業務で手一杯だ』と責められ、もう限界だ。」</td>
          <td><strong>「その通りです。データ上も中間管理職の皆様が最も過酷な摩擦に直面しています。皆様がこれ以上疲弊しないよう、経営陣に対して『新しいDX業務を始める代わりに、既存の報告業務や紙の帳票を2つ廃止する権限（引き算のマネジメント）』を正式に認めさせる交渉を支援します。」</strong></td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- CARD 4: CONCLUSION -->
  <div class="card" style="background: linear-gradient(135deg, #F4F8FC 0%, #E8F1FA 100%); border-left: 6px solid var(--primary);">
    <h2 style="border-bottom: none; padding-bottom: 0;">🏁 改善提案の結論（3大原則）</h2>
    <div style="font-size: 16px; font-weight: 800; color: var(--primary-dark); margin: 15px 0;">
      1. 「ツールを買うな、評価を変えろ」（分配的公正の確立）<br>
      2. 「押しつけるな、意見を聞け」（手続的公正の担保）<br>
      3. 「足すな、引け」（ミドルの負荷軽減と既存業務廃止）
    </div>
    <p style="font-size: 14.5px; color: #333;">
      この学術的・実証的エビデンスに基づく3大原則を提示することで、精神論やITベンダーの言いなりで疲弊している日本企業を、本質的な組織変革へと導くことができます。
    </p>
  </div>

</div>

<footer>
  IDM Project Consulting Framework &copy; 2026 | Full Sample Deterministic N = 2,035 Validated
</footer>

</body>
</html>
"""
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML 生成完了: {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_consulting_html()
