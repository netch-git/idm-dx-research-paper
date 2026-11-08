# -*- coding: utf-8 -*-
"""
generate_standalone_likert_web_text.py
Chart.js（約205KB）の全ソースコードをHTML内部に直接ハードコード（インライン埋め込み）し、
外部ファイル・外部アセット・インターネット通信が一切不要で単独完結（Self-Contained）動作する
完全版Webテキストを生成するスクリプト。
"""
import os
import sys

CHART_JS_PATH = r"G:\マイドライブ\antigravity\IDM\20261007\reports\assets\chart.umd.min.js"
TARGET_FILES = [
    r"G:\マイドライブ\antigravity\IDM\20261007\reports\リッカート尺度_完全理解ハンドブック_Chartjs搭載Webテキスト.html",
    r"G:\マイドライブ\antigravity\IDM\20261007\reports\リッカート尺度_完全理解ハンドブック_単独完結版.html",
    r"G:\マイドライブ\IDM\リッカート尺度_完全理解ハンドブック_Chartjs搭載Webテキスト.html",
    r"G:\マイドライブ\IDM\リッカート尺度_完全理解ハンドブック_単独完結版.html"
]

def main():
    if not os.path.exists(CHART_JS_PATH):
        print(f"Error: {CHART_JS_PATH} not found.")
        return

    with open(CHART_JS_PATH, "r", encoding="utf-8") as f:
        chart_js_code = f.read()

    print(f"Read Chart.js code: {len(chart_js_code)} chars ({len(chart_js_code.encode('utf-8'))} bytes)")

    # HTMLテンプレート作成
    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>リッカート尺度 完全理解ハンドブック（単独完結・完全ハードコード版）</title>
  
  <style>
    :root {{
      --dads-primary-dark: #002B66;
      --dads-primary: #004EA2;
      --dads-primary-tint: #E8F1FA;
      --dads-secondary: #00838F;
      --dads-text-main: #111827;
      --dads-text-sub: #374151;
      --dads-text-muted: #64748B;
      --dads-bg-body: #F8FAFC;
      --dads-bg-card: #FFFFFF;
      --dads-border-light: #E2E8F0;
      --dads-border-main: #CBD5E1;
      --dads-success: #065F46;
      --dads-success-bg: #ECFDF5;
      --dads-warning: #9A3412;
      --dads-warning-bg: #FFF7ED;
      --dads-danger: #B91C1C;
      --dads-danger-bg: #FEF2F2;
      --font-base: "Noto Sans JP", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --font-mono: "Consolas", "Courier New", monospace;
      --font-scale: 1.0;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: var(--font-base);
      color: var(--dads-text-main);
      background-color: var(--dads-bg-body);
      line-height: 1.85;
      font-size: calc(16.5px * var(--font-scale));
      transition: font-size 0.2s ease;
    }}

    /* 固定上部ツールバー */
    .top-toolbar {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: #FFFFFF;
      border-bottom: 1.5px solid var(--dads-border-light);
      padding: 10px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }}

    .toolbar-title {{
      font-size: 15px;
      font-weight: 800;
      color: var(--dads-primary-dark);
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .badge-dads {{
      background: var(--dads-primary);
      color: #FFFFFF;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      letter-spacing: 0.5px;
    }}

    .badge-offline {{
      background: #065F46;
      color: #FFFFFF;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      letter-spacing: 0.5px;
    }}

    .controls-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .font-ctrl-group {{
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .btn-action {{
      padding: 5px 12px;
      font-size: 13px;
      font-weight: 700;
      font-family: var(--font-base);
      border: 1px solid var(--dads-border-main);
      background: #F8FAFC;
      color: var(--dads-text-sub);
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .btn-action:hover {{
      background: var(--dads-primary-tint);
      color: var(--dads-primary);
      border-color: var(--dads-primary);
    }}

    .btn-action.active {{
      background: var(--dads-primary);
      color: #FFFFFF;
      border-color: var(--dads-primary-dark);
    }}

    /* レイアウト */
    .app-layout {{
      display: flex;
      min-height: calc(100vh - 54px);
    }}

    .sidebar {{
      width: 320px;
      background: #FFFFFF;
      border-right: 1.5px solid var(--dads-border-light);
      position: sticky;
      top: 54px;
      height: calc(100vh - 54px);
      overflow-y: auto;
      padding: 24px 18px 40px 18px;
      flex-shrink: 0;
    }}

    .sidebar-header {{
      padding-bottom: 12px;
      border-bottom: 2px solid var(--dads-primary);
      margin-bottom: 16px;
    }}

    .sidebar-title {{
      font-size: 15px;
      font-weight: 800;
      color: var(--dads-primary-dark);
    }}

    .sidebar-menu {{
      list-style: none;
    }}

    .sidebar-menu li {{
      margin-bottom: 6px;
    }}

    .sidebar-menu a {{
      display: block;
      padding: 8px 12px;
      font-size: 13.5px;
      font-weight: 600;
      color: var(--dads-text-sub);
      text-decoration: none;
      border-radius: 6px;
      transition: all 0.15s ease;
      line-height: 1.4;
    }}

    .sidebar-menu a:hover {{
      background: var(--dads-primary-tint);
      color: var(--dads-primary);
    }}

    .content-area {{
      flex: 1;
      max-width: 1040px;
      margin: 0 auto;
      padding: 40px 48px 80px 48px;
    }}

    /* ヒーローヘッダー */
    .hero-header {{
      background: linear-gradient(135deg, var(--dads-primary-dark) 0%, #004EA2 100%);
      color: #FFFFFF;
      padding: 36px 40px;
      border-radius: 12px;
      margin-bottom: 36px;
      box-shadow: 0 4px 14px rgba(0, 43, 102, 0.12);
    }}

    .hero-tags {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
    }}

    .hero-tag {{
      display: inline-block;
      background: rgba(255, 255, 255, 0.2);
      color: #FFFFFF;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 20px;
      letter-spacing: 0.8px;
    }}

    .hero-title {{
      font-size: 26px;
      font-weight: 900;
      line-height: 1.35;
      margin-bottom: 12px;
    }}

    .hero-sub {{
      font-size: 15px;
      opacity: 0.92;
      line-height: 1.6;
    }}

    /* セクション・カード */
    .section-block {{
      margin-bottom: 48px;
      scroll-margin-top: 70px;
    }}

    .section-title {{
      font-size: 22px;
      font-weight: 800;
      color: var(--dads-primary-dark);
      border-left: 6px solid var(--dads-primary);
      padding-left: 14px;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .card {{
      background: var(--dads-bg-card);
      border: 1px solid var(--dads-border-light);
      border-radius: 10px;
      padding: 28px;
      margin-bottom: 24px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }}

    .card-title {{
      font-size: 18px;
      font-weight: 800;
      color: var(--dads-primary-dark);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    /* アラート・吹き出し */
    .alert-box {{
      border-radius: 8px;
      padding: 18px 22px;
      margin: 20px 0;
      font-size: 15px;
      line-height: 1.7;
    }}

    .alert-danger {{
      background: var(--dads-danger-bg);
      border-left: 5px solid var(--dads-danger);
      color: #7F1D1D;
    }}

    .alert-success {{
      background: var(--dads-success-bg);
      border-left: 5px solid var(--dads-success);
      color: #064E3B;
    }}

    .alert-warning {{
      background: var(--dads-warning-bg);
      border-left: 5px solid var(--dads-warning);
      color: #7C2D12;
    }}

    .alert-info {{
      background: var(--dads-primary-tint);
      border-left: 5px solid var(--dads-primary);
      color: #002B66;
    }}

    .alert-title {{
      font-weight: 800;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* チャートコンテナ */
    .chart-container {{
      background: #FFFFFF;
      border: 1.5px solid var(--dads-border-light);
      border-radius: 10px;
      padding: 24px;
      margin: 24px 0;
      box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }}

    .chart-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--dads-border-light);
    }}

    .chart-title {{
      font-size: 16px;
      font-weight: 800;
      color: var(--dads-primary-dark);
    }}

    .chart-caption {{
      font-size: 13px;
      color: var(--dads-text-muted);
      margin-top: 12px;
      line-height: 1.6;
    }}

    .canvas-wrapper {{
      position: relative;
      height: 340px;
      width: 100%;
    }}

    /* 対話的コントロール */
    .interactive-panel {{
      background: #F1F5F9;
      border-radius: 8px;
      padding: 14px 18px;
      margin-bottom: 16px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 16px;
    }}

    .ctrl-label {{
      font-size: 13.5px;
      font-weight: 700;
      color: var(--dads-text-sub);
    }}

    .ctrl-buttons {{
      display: flex;
      gap: 6px;
    }}

    .btn-toggle {{
      padding: 5px 14px;
      font-size: 13px;
      font-weight: 700;
      font-family: var(--font-base);
      border: 1px solid var(--dads-border-main);
      background: #FFFFFF;
      color: var(--dads-text-sub);
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .btn-toggle:hover {{
      background: var(--dads-primary-tint);
      color: var(--dads-primary);
    }}

    .btn-toggle.active {{
      background: var(--dads-primary);
      color: #FFFFFF;
      border-color: var(--dads-primary);
    }}

    .slider-group {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex: 1;
    }}

    .slider-input {{
      flex: 1;
      height: 6px;
      accent-color: var(--dads-primary);
      cursor: pointer;
    }}

    .slider-val {{
      font-size: 14px;
      font-weight: 800;
      color: var(--dads-primary);
      min-width: 40px;
    }}

    /* テーブル */
    .table-container {{
      overflow-x: auto;
      margin: 20px 0;
      border-radius: 8px;
      border: 1px solid var(--dads-border-light);
    }}

    .dads-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14.5px;
      text-align: left;
      background: #FFFFFF;
    }}

    .dads-table th {{
      background: var(--dads-primary);
      color: #FFFFFF;
      padding: 12px 16px;
      font-weight: 700;
      white-space: nowrap;
    }}

    .dads-table td {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--dads-border-light);
      color: var(--dads-text-sub);
      line-height: 1.5;
    }}

    .dads-table tr:nth-child(even) td {{
      background: #F8FAFC;
    }}

    .dads-table tr:hover td {{
      background: var(--dads-primary-tint);
    }}

    /* 数式表現（完全オフライン対応） */
    .math-block {{
      background: #F8FAFC;
      border: 1px solid var(--dads-border-light);
      border-radius: 8px;
      padding: 14px 20px;
      margin: 16px 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: "Cambria Math", "Times New Roman", serif;
      font-size: 18px;
      color: var(--dads-primary-dark);
      overflow-x: auto;
    }}

    .math-inline {{
      font-family: "Cambria Math", "Times New Roman", serif;
      font-style: italic;
      color: var(--dads-primary-dark);
      padding: 0 2px;
    }}

    .fraction {{
      display: inline-flex;
      flex-direction: column;
      vertical-align: middle;
      text-align: center;
      padding: 0 4px;
    }}

    .fraction .numerator {{
      border-bottom: 1.5px solid var(--dads-primary-dark);
      padding-bottom: 2px;
    }}

    .fraction .denominator {{
      padding-top: 2px;
    }}

    /* コードブロック */
    pre code {{
      display: block;
      background: #1E293B;
      color: #F8FAFC;
      padding: 20px 24px;
      border-radius: 8px;
      font-family: var(--font-mono);
      font-size: 13.5px;
      line-height: 1.6;
      overflow-x: auto;
      margin: 16px 0;
    }}

    .badge-status {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 700;
    }}
    .badge-danger {{ background: #FEE2E2; color: #991B1B; }}
    .badge-success {{ background: #D1FAE5; color: #065F46; }}

    @media (max-width: 900px) {{
      .app-layout {{ flex-direction: column; }}
      .sidebar {{ width: 100%; height: auto; position: static; border-right: none; border-bottom: 1px solid var(--dads-border-light); }}
      .content-area {{ padding: 24px 16px; }}
      .canvas-wrapper {{ height: 280px; }}
    }}
  </style>

  <!-- ============================================================== -->
  <!-- Chart.js 完全インラインハードコード（外部通信・ファイル不要） -->
  <!-- ============================================================== -->
  <script>
{chart_js_code}
  </script>
</head>
<body>

  <!-- 固定トップツールバー -->
  <header class="top-toolbar">
    <div class="toolbar-title">
      <span>📊 統計自習ハンドブック</span>
      <span class="badge-dads">リッカート尺度編</span>
      <span class="badge-offline">単独完結・完全ハードコード版</span>
    </div>
    <div class="controls-group">
      <div class="font-ctrl-group">
        <span style="font-size: 12px; font-weight: 700; color: #64748B;">文字サイズ:</span>
        <button class="btn-action" onclick="setFontScale(0.95)">小</button>
        <button class="btn-action active" id="btn-scale-mid" onclick="setFontScale(1.0)">標準</button>
        <button class="btn-action" onclick="setFontScale(1.15)">大</button>
      </div>
      <button class="btn-action" onclick="toggleFullScreen()" title="全画面表示 (Fキー)">⛶ 全画面</button>
    </div>
  </header>

  <div class="app-layout">
    <!-- サイドバー目次 -->
    <nav class="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-title">目次ナビゲーション</div>
      </div>
      <ul class="sidebar-menu">
        <li><a href="#sec1">第1章: リッカート尺度とは何か？</a></li>
        <li><a href="#sec2">第2章: 尺度水準とリッカートの立場</a></li>
        <li><a href="#sec3">第3章: 初心者が陥る7大落とし穴</a></li>
        <li style="padding-left: 12px;"><a href="#pit1">落とし穴1: 順序尺度と平均値</a></li>
        <li style="padding-left: 12px;"><a href="#pit2">落とし穴2: 「わからない(3点)」</a></li>
        <li style="padding-left: 12px;"><a href="#pit3">落とし穴3: 逆転項目の反転漏れ</a></li>
        <li style="padding-left: 12px;"><a href="#pit4">落とし穴4: クロンバックαの盲信</a></li>
        <li style="padding-left: 12px;"><a href="#pit5">落とし穴5: 大規模サンプル病</a></li>
        <li style="padding-left: 12px;"><a href="#pit6">落とし穴6: 天井・床効果の罠</a></li>
        <li style="padding-left: 12px;"><a href="#pit7">落とし穴7: 共通方法バイアス</a></li>
        <li><a href="#sec4">第4章: 本プロジェクト模範設計</a></li>
        <li><a href="#sec5">第5章: 実践チェックリスト</a></li>
        <li><a href="#sec6">第6章: コピペ用Pythonコード</a></li>
      </ul>
    </nav>

    <!-- メインコンテンツエリア -->
    <main class="content-area">

      <!-- カバーヒーロー -->
      <section class="hero-header">
        <div class="hero-tags">
          <span class="hero-tag">IDM-DX 統計教育リソース</span>
          <span class="hero-tag">Self-Contained Standalone HTML</span>
        </div>
        <h1 class="hero-title">リッカート尺度（Likert Scale）完全理解ハンドブック<br>初心者向け落とし穴とプロの統計実践術</h1>
        <p class="hero-sub">
          「1:まったく思わない〜5:非常に思う」を安易に平均してはいけない理由とは？<br>
          就業者2,035名のビッグデータを題材に、動的なChart.js図表（完全内蔵）で直感的にマスターする決定版教材。
        </p>
      </section>

      <!-- 第1章 -->
      <section id="sec1" class="section-block">
        <h2 class="section-title">第1章: リッカート尺度とは何か？</h2>
        <div class="card">
          <p>
            アンケート調査で最も頻繁に使われるのが、**「1: まったくそう思わない」から「5: 非常にそう思う」**までの多段階選択肢です。この測定方式は、アメリカの心理学者・社会学者である**レンシス・リッカート（Rensis Likert, 1903–1981）**が1932年に提唱したため、**リッカート尺度（Likert Scale）**と呼ばれます。
          </p>
          <div class="alert-box alert-info">
            <div class="alert-title">💡 学術的に超重要な区別：アイテム（Item）とスケール（Scale）</div>
            多くの初心者が混同しますが、学術界では厳格に区別されます：
            <ul style="margin-left: 20px; margin-top: 6px;">
              <li><strong>リッカート項目（Likert Item）</strong>: 1問単独の質問。「DXが必要だと思うか？」の1問だけ。</li>
              <li><strong>リッカート尺度（Likert Scale）</strong>: 同じ概念（例: DX推進意識）を測定するために設計された**複数の項目（5〜10問など）を合計・平均した合成得点**。</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- 第2章 -->
      <section id="sec2" class="section-block">
        <h2 class="section-title">第2章: 尺度水準とリッカート尺度の微妙な立ち位置</h2>
        <div class="card">
          <p>
            心理学者スティーブンス（S. S. Stevens, 1946）は、測定データを以下の4段階に分類しました。
          </p>
          <div class="table-container">
            <table class="dads-table">
              <thead>
                <tr>
                  <th>尺度水準</th>
                  <th>データの性質</th>
                  <th>日常の例</th>
                  <th>可能な演算・代表値</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>名義尺度 (Nominal)</strong></td>
                  <td>単なる分類・ラベル（順序なし）</td>
                  <td>性別、血液型、背番号</td>
                  <td>最頻値 (Mode)</td>
                </tr>
                <tr>
                  <td><strong>順序尺度 (Ordinal)</strong></td>
                  <td>順序・優劣はあるが「間隔」が不等</td>
                  <td>順位、辛さの段階、<strong>1問の回答</strong></td>
                  <td>中央値 (Median), 比率 (%)</td>
                </tr>
                <tr>
                  <td><strong>間隔尺度 (Interval)</strong></td>
                  <td>目盛りの間隔が等しい（差に意味あり）</td>
                  <td>温度(℃)、西暦、知能指数(IQ)</td>
                  <td><strong>平均値 (Mean), 標準偏差</strong></td>
                </tr>
                <tr>
                  <td><strong>比率尺度 (Ratio)</strong></td>
                  <td>絶対的なゼロ点があり「何倍」と言える</td>
                  <td>身長、体重、売上、給料、時間</td>
                  <td>すべての統計演算（比率・比）</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="alert-box alert-warning">
            <div class="alert-title">⚠️ ここが最大の論争点！</div>
            1問ごとの質問（リッカート項目）は**「順序尺度」**です。「1点」と「2点」の心の距離と、「4点」と「5点」の心の距離が等しい保証はありません。したがって、<strong>「1問だけの平均値」を算出して比較することは、厳密な統計学では禁止手（御法度）</strong>とされます。
          </div>
        </div>
      </section>

      <!-- 第3章 -->
      <section id="sec3" class="section-block">
        <h2 class="section-title">第3章: 統計初心者が陥る「7大落とし穴」と具体的対応策</h2>

        <!-- 落とし穴 1 -->
        <div id="pit1" class="card">
          <div class="card-title">
            <span class="badge-status badge-danger">落とし穴 1</span>
            単一項目の「順序尺度」を安易に平均化して盲信する
          </div>
          <p>
            「DX意識の質問で、営業部の平均は 3.42、開発部は 3.71 でした！」と報告していませんか？<br>
            前述の通り、1問ごとのデータは「順序尺度」です。激辛カレーの例と同じで、1段階ごとの「心理的段差」は均一ではありません。
          </p>

          <!-- Chart 1: 順序尺度 vs 間隔尺度 & 中央極限定理 -->
          <div class="chart-container">
            <div class="chart-header">
              <div class="chart-title">【動的図表 1】項目合成による「中央極限定理（釣鐘型への収束）」シミュレーター</div>
            </div>
            <div class="interactive-panel">
              <span class="ctrl-label">合算する質問項目数 (k):</span>
              <div class="slider-group">
                <input type="range" class="slider-input" id="slider-items" min="1" max="9" value="1" oninput="updateCltChart(this.value)">
                <span class="slider-val" id="val-items">1 問</span>
              </div>
            </div>
            <div class="canvas-wrapper">
              <canvas id="cltChart"></canvas>
            </div>
            <p class="chart-caption">
              ▲ <strong>操作方法</strong>: スライダーを「1問」から「9問」へ動かしてみてください。1問単体ではガタガタした順序尺度の度数分布が、質問項目を束ねて合成得点（平均）にするにつれて、<strong>中央極限定理によって驚くほど綺麗な釣鐘型の「正規分布（間隔尺度）」へと収束</strong>していく様子が分かります。
            </p>
          </div>

          <div class="alert-box alert-success">
            <div class="alert-title"> プロの対応策：項目合成で「間隔尺度」へと昇格させる</div>
            先行研究（Carifio & Perla, 2008）が立証している通り、**同じ概念を測る複数のリッカート項目（例: 9問）を束ねて合計・平均した「合成得点」は、間隔尺度としてパラメトリック検定（ANOVAやt検定）に投入することが数学的に正当化されます**。1問だけを比較したいときは「度数分布（%）や中央値」を用いましょう。
          </div>
        </div>

        <!-- 落とし穴 2 -->
        <div id="pit2" class="card">
          <div class="card-title">
            <span class="badge-status badge-danger">落とし穴 2</span>
            「わからない・どちらともいえない」を無批判に「3点」にする
          </div>
          <p>
            5件法の真ん中「3」には、日本人の心理として**全く異なる2つの集団**が混入しています。
          </p>
          <div class="table-container">
            <table class="dads-table">
              <thead>
                <tr>
                  <th>3を選んだ人の内訳</th>
                  <th>心理状態</th>
                  <th>3点（普通）として扱うリスク</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>真の中立派 (Neutral)</strong></td>
                  <td>メリットもデメリットも半々で悩んだ</td>
                  <td>問題なし（真ん中として妥当）</td>
                </tr>
                <tr>
                  <td><strong>知識欠如・無関心 (Don't Know)</strong></td>
                  <td>そもそもDXが何か知らず判断不能</td>
                  <td><strong>「無知」が「普通の賛成度」に誤認される！</strong></td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Chart 2: 感度分析 -->
          <div class="chart-container">
            <div class="chart-header">
              <div class="chart-title">【動的図表 2】「3点」の扱いによる感度分析（平均値シフトの検証）</div>
              <div class="ctrl-buttons">
                <button class="btn-toggle active" id="btn-sens-all" onclick="toggleSensitivity(true)">3点を含める (N=2,035)</button>
                <button class="btn-toggle" id="btn-sens-ex" onclick="toggleSensitivity(false)">3点を除外・欠損扱い</button>
              </div>
            </div>
            <div class="canvas-wrapper">
              <canvas id="sensitivityChart"></canvas>
            </div>
            <p class="chart-caption">
              ▲ <strong>解説</strong>: ボタンを切り替えると、「3点（わからない）」を計算に含めた場合と、除外した場合の職制別平均値が比較できます。「わからない」を除外すると全般的に平均値が上昇しますが、<strong>「経営層 ＞ 部課長 ＞ 一般社員」という階層格差のトレンド自体は一切崩れていない</strong>ことが確認できます。
            </p>
          </div>

          <div class="alert-box alert-success">
            <div class="alert-title"> プロの対応策：感度分析（Sensitivity Analysis）で頑健性を立証する</div>
            「3点を含めた結果」と「3点を除外した結果」の両方を算出し、<strong>「どちらの処理を採用しても論文の主結論（有意差や傾向）が変わらない」ことを論文内で明記する</strong>のが世界一流の査読対応作法です（本プロジェクト `01_analysis.py` 準拠）。
          </div>
        </div>

        <!-- 落とし穴 3 -->
        <div id="pit3" class="card">
          <div class="card-title">
            <span class="badge-status badge-danger">落とし穴 3</span>
            逆転項目（Reverse-coded items）の反転処理を忘れる
          </div>
          <p>
            アンケートには、回答者の適当なマークを防ぐため、わざとネガティブな質問を混ぜることがあります（逆転項目）。これをそのまま足し算すると、**ポジティブな人とネガティブな人が相殺し合い、指標が完全に崩壊**します。
          </p>

          <!-- Chart 3: 逆転項目の反転ビフォー・アフター -->
          <div class="chart-container">
            <div class="chart-header">
              <div class="chart-title">【動的図表 3】逆転項目 反転処理ビフォー・アフター（相関と信頼性の変化）</div>
              <div class="ctrl-buttons">
                <button class="btn-toggle active" id="btn-rev-before" onclick="toggleReverseMode('before')">反転忘れ（大失敗）</button>
                <button class="btn-toggle" id="btn-rev-after" onclick="toggleReverseMode('after')">正しく反転 (6 - X)</button>
              </div>
            </div>
            <div class="canvas-wrapper">
              <canvas id="reverseChart"></canvas>
            </div>
            <p class="chart-caption">
              ▲ <strong>解説</strong>: 「反転忘れ」では、ポジティブ項目とネガティブ項目が真逆のベクトルを向くため、クロンバックのαは α = -0.15 と壊滅します。「正しく反転」を押すと、全項目が同一方向（エンゲージメント）に揃い、α = 0.82 の高信頼性尺度へと生まれ変わります。
            </p>
          </div>

          <div class="alert-box alert-success">
            <div class="alert-title"> プロの対応策：反転公式 6 - X の自動適用</div>
            5件法の場合、反転公式はシンプルです：
            <div class="math-block">
              <span>反転後の値 ＝ 6 － X</span>
            </div>
            （1 → 5, 2 → 4, 3 → 3, 4 → 2, 5 → 1）。合成前には必ず相関行列を出力し、マイナスの相関を持つ項目がないか目視点検しましょう。
          </div>
        </div>

        <!-- 落とし穴 4 -->
        <div id="pit4" class="card">
          <div class="card-title">
            <span class="badge-status badge-danger">落とし穴 4</span>
            信頼性分析（Cronbach's α）の未検証、および「α の盲信」
          </div>
          <p>
            「適当に作った10問を足して合計点にしました」は学術論文では即リジェクトされます。必ず**内的整合性（信頼性係数 α）**を検証しなければなりません。しかし、α にも落とし穴があります。
          </p>
          <div class="alert-box alert-warning">
            <div class="alert-title">⚠️ クロンバックの α は「問題数が増えるだけで自動的に高くなる」！</div>
            <div class="math-block">
              <span class="math-inline">α</span> ＝ 
              <span class="fraction"><span class="numerator"><span class="math-inline">k</span></span><span class="denominator"><span class="math-inline">k</span> － 1</span></span>
              <span>×</span>
              <span>(</span>
              <span>1 － </span>
              <span class="fraction"><span class="numerator">∑ <span class="math-inline">s</span><sub>i</sub><sup>2</sup></span><span class="denominator"><span class="math-inline">s</span><sub>T</sub><sup>2</sup></span></span>
              <span>)</span>
            </div>
            式の中の <span class="math-inline">k</span>（項目数）が増えると、質問同士の相関が弱くても α の値は上がってしまいます。
          </div>
          <div class="alert-box alert-success">
            <div class="alert-title"> プロの対応策：CITC と 主成分分析の二重チェック</div>
            1. **修正項目-全体相関（CITC）**: その項目を除いた合計点との相関が 0.30 以上あるか確認し、足を引っ張っている問題を取り除く。<br>
            2. **主成分分析（PCA）**: スクリープロットで第1主成分の寄与率を確認し、本当に「1つの潜在変数」を測っているか（一次元性）を担保する。
          </div>
        </div>

        <!-- 落とし穴 5 -->
        <div id="pit5" class="card">
          <div class="card-title">
            <span class="badge-status badge-danger">落とし穴 5</span>
            大規模サンプル病（N=2,035）による「何でも p &lt; .05 で有意」の錯覚
          </div>
          <p>
            本調査のように N = 2,035 名もあると、統計的検定力が強大になりすぎ、**平均値の差がわずか 0.05（1%の差）であっても p &lt; 0.001 で有意**になってしまいます。
          </p>

          <!-- Chart 4: 有意性と効果量の対比 -->
          <div class="chart-container">
            <div class="chart-header">
              <div class="chart-title">【動的図表 4】統計的有意（p値） vs 実質的差（効果量 ηp²）の完全比較</div>
            </div>
            <div class="canvas-wrapper">
              <canvas id="effectSizeChart"></canvas>
            </div>
            <p class="chart-caption">
              ▲ <strong>本調査の実測値</strong>: 左の「企業規模」は p = 0.0046 で有意ですが、効果量は ηp² = 0.0039（わずか0.4%の説明力＝実質差なし）。右の「職制（役職）」は p = 10⁻¹⁷ で有意かつ ηp² = 0.0366（実質的な大差）。<strong>p 値だけ見ていては、何が本当に意味のある要因かを見誤ります</strong>。
            </p>
          </div>

          <div class="alert-box alert-success">
            <div class="alert-title"> プロの対応策：効果量（Effect Size）の義務付け</div>
            分散分析なら **偏イータ二乗 ηp²**、t検定なら **Cohen's d** を必ず併記します（本プロジェクトのガバナンス規則第2条でも厳格に義務付けられています）。
          </div>
        </div>

        <!-- 落とし穴 6 -->
        <div id="pit6" class="card">
          <div class="card-title">
            <span class="badge-status badge-danger">落とし穴 6</span>
            天井効果（Ceiling Effect）と床効果（Floor Effect）の無視
          </div>
          <p>
            全員が「そう思う（5）」と答えるような質問（例: SC14「無駄な仕事は減らしたいか？」→ 肯定78%）は、ばらつき（分散）が存在しないため、他の変数との相関分析や回帰分析にかけても有意な予測力を持ちません。
          </p>

          <!-- Chart 5: 天井効果 vs 正規分布 -->
          <div class="chart-container">
            <div class="chart-header">
              <div class="chart-title">【動的図表 5】天井効果（極端な偏り）と理想的な正規分布の比較</div>
            </div>
            <div class="canvas-wrapper">
              <canvas id="ceilingChart"></canvas>
            </div>
            <p class="chart-caption">
              ▲ <strong>解説</strong>: 赤色の SC14 は回答が右端（4〜5）に極端に集中しており「天井効果」を起こしています。青色の SC18（合成得点）は美しい中央の山（正規分布）を描いており、多変量解析に理想的な性質を持っています。
            </p>
          </div>
        </div>

        <!-- 落とし穴 7 -->
        <div id="pit7" class="card">
          <div class="card-title">
            <span class="badge-status badge-danger">落とし穴 7</span>
            共通方法バイアス（Common Method Bias: CMB）
          </div>
          <p>
            同じ回答者が同じWeb画面で一度に回答すると、「気分が明るい人は全体的に高め、暗い人は全体的に低め」とマークし、無関係な質問同士に見かけ上の相関が生じます。
          </p>
          <div class="alert-box alert-success">
            <div class="alert-title"> 本研究の神対応：アクセルとブレーキの「直交性（r = -0.09）」立証</div>
            本論文では、DX推進意識（SC18）とデジタル化懸念（SC15）の相関係数が r = -0.0901（無相関）であることを示し、共通方法バイアスによってデータが汚染されていないことを数学的に論破しました。
          </div>
        </div>

      </section>

      <!-- 第4章 -->
      <section id="sec4" class="section-block">
        <h2 class="section-title">第4章: 本プロジェクト（N=2,035）における模範設計</h2>
        <div class="card">
          <p>本プロジェクト（IDM-DX）では、以上の落とし穴をすべてクリアした以下の2大合成尺度を開発・実証しました。</p>
          <div class="table-container">
            <table class="dads-table">
              <thead>
                <tr>
                  <th>尺度コード</th>
                  <th>尺度名称</th>
                  <th>項目数</th>
                  <th>クロンバックの α</th>
                  <th>全体平均 (SD)</th>
                  <th>理論的位置づけ</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>SC18</strong></td>
                  <td>DX推進意識・心理的所有感</td>
                  <td>9 項目</td>
                  <td><strong>0.8592</strong> (高信頼性)</td>
                  <td>3.2709 (0.6279)</td>
                  <td>変革の推進力（アクセル）</td>
                </tr>
                <tr>
                  <td><strong>SC15</strong></td>
                  <td>デジタル化懸念・組織摩擦</td>
                  <td>9 項目</td>
                  <td><strong>0.8183</strong> (高信頼性)</td>
                  <td>3.0802 (0.6327)</td>
                  <td>心理的抵抗感（ブレーキ）</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- 第5章 -->
      <section id="sec5" class="section-block">
        <h2 class="section-title">第5章: 実践チェックリスト（これさえ守れば完璧）</h2>
        <div class="card">
          <div class="table-container">
            <table class="dads-table">
              <thead>
                <tr>
                  <th>フェーズ</th>
                  <th>確認項目</th>
                  <th>合否判定基準</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>データ準備</strong></td>
                  <td>ネガティブ項目の反転処理</td>
                  <td>6 - X を適用し、相関が正になっているか？</td>
                </tr>
                <tr>
                  <td><strong>データ準備</strong></td>
                  <td>「わからない(3点)」の扱い</td>
                  <td>含める場合と除外する場合の感度分析を用意したか？</td>
                </tr>
                <tr>
                  <td><strong>尺度構成</strong></td>
                  <td>内的整合性の検証</td>
                  <td>クロンバックの α ≥ 0.70、CITC ≥ 0.30 を確認したか？</td>
                </tr>
                <tr>
                  <td><strong>集計・検定</strong></td>
                  <td>単一項目 vs 合成得点</td>
                  <td>1問だけの質問を無理にANOVAにかけていないか？</td>
                </tr>
                <tr>
                  <td><strong>結果報告</strong></td>
                  <td>効果量の明記</td>
                  <td>p 値だけでなく、ηp² や Cohen's d を記載したか？</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- 第6章 -->
      <section id="sec6" class="section-block">
        <h2 class="section-title">第6章: コピペで使えるPython黄金コード</h2>
        <div class="card">
          <p>以下のスクリプトをコピーするだけで、落とし穴を完全回避したリッカート尺度分析が実行できます。</p>
          <pre><code>import pandas as pd
import numpy as np

# 1. 安全な数値変換辞書の適用
MAP_LIKERT = {{
    "まったくそう思わない": 1,
    "あまりそう思わない": 2,
    "わからない・どちらともいえない": 3,
    "ややそう思う": 4,
    "非常にそう思う": 5
}}
df_num = df[items].replace(MAP_LIKERT)

# 2. 逆転項目の反転処理 (5件法: 6 - X)
for rev_col in reverse_items:
    df_num[rev_col] = 6 - df_num[rev_col]

# 3. クロンバックのα（内的整合性）を計算
def calc_cronbach(data):
    k = data.shape[1]
    item_vars = data.var(axis=0, ddof=1).sum()
    total_var = data.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_vars / total_var)

alpha = calc_cronbach(df_num)
print(f"Cronbach's alpha: {{alpha:.4f}}")

# 4. α >= 0.70 を満たした場合のみ、合成得点を算出
if alpha >= 0.70:
    df["composite_score"] = df_num.mean(axis=1)
    print("合成得点を正常に生成しました。ANOVA等の検定へ進んでください。")
</code></pre>
        </div>
      </section>

    </main>
  </div>

  <!-- Chart.js 動的スクリプト実装（完全オフライン・単独動作） -->
  <script>
    // フォントスケール設定
    function setFontScale(scale) {{
      document.documentElement.style.setProperty('--font-scale', scale);
      document.querySelectorAll('.font-ctrl-group .btn-action').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');
    }}

    // 全画面表示切替
    function toggleFullScreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(err => console.log(err));
      }} else {{
        if (document.exitFullscreen) document.exitFullscreen();
      }}
    }}
    document.addEventListener('keydown', e => {{
      if (e.key === 'f' || e.key === 'F') {{
        if (!['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) toggleFullScreen();
      }}
    }});

    // 共通チャートフォント
    Chart.defaults.font.family = "'Noto Sans JP', sans-serif";
    Chart.defaults.font.size = 13;
    Chart.defaults.color = '#374151';

    // -------------------------------------------------------------
    // Chart 1: 中央極限定理シミュレーター
    // -------------------------------------------------------------
    let cltChartInstance = null;
    function getNormalDist(items) {{
      const bins = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0];
      if (items === 1) {{
        return [8.3, 0, 21.3, 0, 44.0, 0, 22.6, 0, 3.8];
      }}
      const variance = 0.8 / items;
      return bins.map(x => {{
        const diff = x - 3.27;
        const p = Math.exp(-(diff * diff) / (2 * variance));
        return parseFloat((p * (25 + items * 5)).toFixed(1));
      }});
    }}

    function initCltChart() {{
      const ctx = document.getElementById('cltChart').getContext('2d');
      cltChartInstance = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: ['1.0点', '1.5点', '2.0点', '2.5点', '3.0点', '3.5点', '4.0点', '4.5点', '5.0点'],
          datasets: [{{
            label: '回答度数 (%)',
            data: getNormalDist(1),
            backgroundColor: 'rgba(0, 78, 162, 0.75)',
            borderColor: '#002B66',
            borderWidth: 1.5,
            borderRadius: 4
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{ callbacks: {{ label: ctx => `比率: ${{ctx.raw}}%` }} }}
          }},
          scales: {{
            y: {{ beginAtZero: true, max: 70, title: {{ display: true, text: '回答構成比 (%)' }} }},
            x: {{ title: {{ display: true, text: '得点（1問単体 vs 合成平均得点）' }} }}
          }}
        }}
      }});
    }}

    function updateCltChart(val) {{
      document.getElementById('val-items').innerText = `${{val}} 問`;
      const num = parseInt(val);
      cltChartInstance.data.datasets[0].data = getNormalDist(num);
      cltChartInstance.data.datasets[0].backgroundColor = num === 1 ? 'rgba(185, 28, 28, 0.75)' : 'rgba(0, 78, 162, 0.75)';
      cltChartInstance.update();
    }}

    // -------------------------------------------------------------
    // Chart 2: 感度分析比較
    // -------------------------------------------------------------
    let sensChartInstance = null;
    function initSensChart() {{
      const ctx = document.getElementById('sensitivityChart').getContext('2d');
      sensChartInstance = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: ['1. 経営層', '2. 部課長クラス', '3. 一般社員'],
          datasets: [
            {{
              label: '3点（わからない）を含める (N=2,035)',
              data: [3.58, 3.32, 3.11],
              backgroundColor: '#004EA2',
              borderRadius: 4
            }},
            {{
              label: '3点を除外・欠損扱い (N=1,139)',
              data: [3.82, 3.56, 3.35],
              backgroundColor: '#00838F',
              borderRadius: 4
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ min: 2.5, max: 4.5, title: {{ display: true, text: 'DX推進意識 平均得点 (M)' }} }}
          }},
          plugins: {{
            legend: {{ position: 'top' }}
          }}
        }}
      }});
    }}

    function toggleSensitivity(showAll) {{
      document.getElementById('btn-sens-all').classList.toggle('active', showAll);
      document.getElementById('btn-sens-ex').classList.toggle('active', !showAll);
      sensChartInstance.data.datasets[0].hidden = !showAll;
      sensChartInstance.data.datasets[1].hidden = showAll;
      sensChartInstance.update();
    }}

    // -------------------------------------------------------------
    // Chart 3: 逆転項目シミュレーター
    // -------------------------------------------------------------
    let revChartInstance = null;
    function initRevChart() {{
      const ctx = document.getElementById('reverseChart').getContext('2d');
      revChartInstance = new Chart(ctx, {{
        type: 'line',
        data: {{
          labels: ['Q1(売上貢献)', 'Q2(業績無関心)', 'Q3(給料不満)', 'Q4(周囲認知)', 'Q5(公正評価)'],
          datasets: [
            {{
              label: '項目スコア（反転忘れ・大失敗: α = -0.15）',
              data: [3.8, 1.9, 1.8, 3.6, 3.5],
              borderColor: '#B91C1C',
              backgroundColor: 'rgba(185, 28, 28, 0.1)',
              fill: true,
              tension: 0.3,
              pointRadius: 6
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ min: 1.0, max: 5.0, title: {{ display: true, text: '平均得点' }} }}
          }}
        }}
      }});
    }}

    function toggleReverseMode(mode) {{
      document.getElementById('btn-rev-before').classList.toggle('active', mode === 'before');
      document.getElementById('btn-rev-after').classList.toggle('active', mode === 'after');
      if (mode === 'before') {{
        revChartInstance.data.datasets[0].label = '項目スコア（反転忘れ・大失敗: α = -0.15）';
        revChartInstance.data.datasets[0].data = [3.8, 1.9, 1.8, 3.6, 3.5];
        revChartInstance.data.datasets[0].borderColor = '#B91C1C';
        revChartInstance.data.datasets[0].backgroundColor = 'rgba(185, 28, 28, 0.1)';
      }} else {{
        revChartInstance.data.datasets[0].label = '項目スコア（正しく 6 - X 反転後: α = 0.82）';
        revChartInstance.data.datasets[0].data = [3.8, 4.1, 4.2, 3.6, 3.5];
        revChartInstance.data.datasets[0].borderColor = '#065F46';
        revChartInstance.data.datasets[0].backgroundColor = 'rgba(6, 95, 70, 0.1)';
      }}
      revChartInstance.update();
    }}

    // -------------------------------------------------------------
    // Chart 4: 有意性 vs 効果量
    // -------------------------------------------------------------
    function initEffectChart() {{
      const ctx = document.getElementById('effectSizeChart').getContext('2d');
      new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: ['企業規模 (大企業 vs 中小)', '職制グループ (経営層 vs 一般社員)'],
          datasets: [
            {{
              type: 'bar',
              label: '平均値の差（点）',
              data: [0.08, 0.47],
              backgroundColor: '#004EA2',
              yAxisID: 'y'
            }},
            {{
              type: 'line',
              label: '効果量 ηp² (説明力 %)',
              data: [0.0039 * 100, 0.0366 * 100],
              borderColor: '#B91C1C',
              backgroundColor: '#B91C1C',
              pointRadius: 8,
              borderWidth: 2,
              yAxisID: 'y1'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ position: 'left', min: 0, max: 0.6, title: {{ display: true, text: '平均値の差（5点満点中）' }} }},
            y1: {{ position: 'right', min: 0, max: 5.0, grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: '効果量 ηp² (%)' }} }}
          }}
        }}
      }});
    }}

    // -------------------------------------------------------------
    // Chart 5: 天井効果
    // -------------------------------------------------------------
    function initCeilingChart() {{
      const ctx = document.getElementById('ceilingChart').getContext('2d');
      new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: ['1: 全く思わない', '2: あまり思わない', '3: わからない', '4: そう思う', '5: 非常にそう思う'],
          datasets: [
            {{
              label: 'SC14（天井効果の例: 業務改善意欲）',
              data: [1.7, 12.6, 7.8, 49.0, 28.9],
              backgroundColor: 'rgba(185, 28, 28, 0.8)',
              borderRadius: 4
            }},
            {{
              label: 'SC18（理想的な正規分布: DX推進意識）',
              data: [3.8, 21.3, 44.0, 22.6, 8.3],
              backgroundColor: 'rgba(0, 78, 162, 0.8)',
              borderRadius: 4
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ beginAtZero: true, max: 60, title: {{ display: true, text: '回答割合 (%)' }} }}
          }}
        }}
      }});
    }}

    // ページロード時初期化
    window.addEventListener('DOMContentLoaded', () => {{
      initCltChart();
      initSensChart();
      initRevChart();
      initEffectChart();
      initCeilingChart();
    }});
  </script>
</body>
</html>
"""

    for target in TARGET_FILES:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(html_template)
        print(f"Generated standalone file: {target} ({len(html_template.encode('utf-8'))} bytes)")

if __name__ == "__main__":
    main()
