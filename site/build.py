import json

with open('/home/antigravity/idm-citation-cockpit/data.json', encoding='utf-8') as f:
    items = json.load(f)

json_data_str = json.dumps(items, ensure_ascii=False)

html_code = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IDM DX CITATION COCKPIT | 論文引用文献・分析手法＆結論 統合コックピット</title>
  
  <!-- Google Fonts: Noto Sans JP, JetBrains Mono, Material Symbols Outlined -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
  
  <!-- Chart.js 4.4.1 -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    /* ==========================================================
       CSS デザイントークン (Slate & Deep Navy Engineering Tone)
       ========================================================== */
    :root {
      /* 背景・方眼 */
      --bg-paper: #F8FAFC;
      --grid-line: rgba(15, 23, 42, 0.05);

      /* サーフェス */
      --surface-white: #FFFFFF;
      --surface-card: #FFFFFF;
      --surface-muted: #F1F5F9;
      --surface-slate: #E2E8F0;

      /* ディープネイビー & ダークサーフェス（AIパステルカラー回避） */
      --navy-darkest: #0B1120;
      --navy-dark: #0F172A;
      --navy-card: #1E293B;
      --navy-subtle: #334155;

      /* テキストカラー */
      --ink-darkest: #0F172A;
      --ink-slate: #334155;
      --ink-gray: #64748B;
      --text-light-primary: #F8FAFC;
      --text-light-secondary: #E2E8F0;
      --text-light-muted: #94A3B8;

      /* アクセント（彩度を落とした端正な色調） */
      --accent-navy: #1E3A8A;
      --accent-steel: #0284C7;
      --accent-amber: #D97706;
      --accent-charcoal: #374151;

      /* ボーダー & ソリッドシャドウ */
      --border-thin: 1px solid #CBD5E1;
      --border-thick: 2px solid #0F172A;
      --border-heavy: 3px solid #0F172A;
      --border-dashed: 1.5px dashed #94A3B8;
      --shadow-card: 0px 4px 0px #0F172A;
      --shadow-card-lg: 0px 6px 0px #0F172A;
      --shadow-btn: 0px 2px 0px #0F172A;
      --shadow-btn-active: 0px 0px 0px #0F172A;

      /* フォントファミリ */
      --font-sans: 'Noto Sans JP', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg-paper);
      background-image: 
        linear-gradient(var(--grid-line) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
      background-size: 20px 20px;
      color: var(--ink-darkest);
      font-family: var(--font-sans);
      line-height: 1.6;
      padding: 24px 16px 80px;
      min-height: 100vh;
    }

    .container {
      max-width: 1320px;
      margin: 0 auto;
    }

    /* Google Fonts アイコン標準クラス */
    .material-symbols-outlined {
      font-family: 'Material Symbols Outlined';
      font-weight: normal;
      font-style: normal;
      font-size: 16px;
      line-height: 1;
      display: inline-block;
      vertical-align: -2px;
      text-transform: none;
      letter-spacing: normal;
      word-wrap: normal;
      white-space: nowrap;
      direction: ltr;
    }

    /* 物理ボタン */
    .neo-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      background: var(--surface-white);
      border: var(--border-thick);
      box-shadow: var(--shadow-btn);
      padding: 8px 14px;
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      color: var(--ink-darkest);
      text-decoration: none;
      cursor: pointer;
      border-radius: 6px;
      transition: transform 0.08s ease, box-shadow 0.08s ease, background-color 0.08s ease;
      user-select: none;
    }
    .neo-btn:hover { background: #F1F5F9; }
    .neo-btn:active {
      transform: translateY(2px);
      box-shadow: var(--shadow-btn-active);
    }
    .neo-btn-primary {
      background: var(--navy-dark);
      color: #FFFFFF;
    }
    .neo-btn-primary:hover {
      background: #1E293B;
    }

    /* ヘッダーエリア */
    .header-card {
      background: var(--surface-white);
      border: var(--border-heavy);
      box-shadow: var(--shadow-card-lg);
      border-radius: 12px;
      padding: 26px 28px;
      margin-bottom: 24px;
      position: relative;
    }
    .header-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--navy-dark);
      color: var(--text-light-primary);
      border: 1px solid var(--navy-subtle);
      padding: 4px 10px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      border-radius: 4px;
      margin-bottom: 12px;
      letter-spacing: 0.5px;
    }
    .header-tag .material-symbols-outlined {
      font-size: 14px;
      color: #94A3B8;
    }
    .header-title-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 20px;
      flex-wrap: wrap;
    }
    .header-title {
      font-size: 26px;
      font-weight: 900;
      letter-spacing: -0.5px;
      line-height: 1.25;
      margin-bottom: 8px;
      color: var(--navy-dark);
    }
    .header-subtitle {
      font-size: 14px;
      color: var(--ink-gray);
      line-height: 1.5;
      font-weight: 500;
      max-width: 820px;
    }
    .header-actions {
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
    }

    .meta-badges-row {
      display: flex;
      gap: 10px;
      margin-top: 18px;
      flex-wrap: wrap;
    }
    .meta-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--surface-muted);
      border: 1px solid #CBD5E1;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 12px;
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--ink-slate);
    }
    .meta-badge.active {
      background: var(--navy-dark);
      color: var(--text-light-primary);
      border-color: var(--navy-dark);
    }
    .meta-badge .material-symbols-outlined {
      font-size: 14px;
    }

    /* KPIカードグリッド */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .kpi-card {
      background: var(--surface-white);
      border: var(--border-thick);
      box-shadow: var(--shadow-card);
      border-radius: 8px;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .kpi-label {
      font-size: 12px;
      font-weight: 700;
      color: var(--ink-gray);
      font-family: var(--font-mono);
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }
    .kpi-label .material-symbols-outlined {
      font-size: 18px;
      color: var(--ink-slate);
    }
    .kpi-value {
      font-size: 28px;
      font-weight: 900;
      font-family: var(--font-mono);
      line-height: 1.1;
      color: var(--navy-dark);
    }
    .kpi-desc {
      font-size: 12px;
      color: var(--ink-gray);
      margin-top: 6px;
      line-height: 1.4;
    }

    /* チャートセクション */
    .charts-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .chart-card {
      background: var(--surface-white);
      border: var(--border-thick);
      box-shadow: var(--shadow-card);
      border-radius: 8px;
      padding: 18px 20px;
    }
    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--surface-slate);
    }
    .chart-title {
      font-size: 14px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--navy-dark);
    }
    .chart-title .material-symbols-outlined {
      font-size: 18px;
    }

    /* 検索＆コントロールパネル */
    .control-panel {
      background: var(--surface-white);
      border: var(--border-thick);
      box-shadow: var(--shadow-card);
      border-radius: 8px;
      padding: 18px 20px;
      margin-bottom: 24px;
    }
    .search-input-wrap {
      position: relative;
      margin-bottom: 16px;
    }
    .search-input {
      width: 100%;
      background: var(--surface-muted);
      border: var(--border-thick);
      border-radius: 6px;
      padding: 12px 16px 12px 42px;
      font-size: 14px;
      font-family: var(--font-sans);
      font-weight: 500;
      outline: none;
      transition: background 0.15s, border-color 0.15s;
      color: var(--ink-darkest);
    }
    .search-input:focus {
      background: #FFFFFF;
      border-color: var(--navy-dark);
    }
    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--ink-gray);
      pointer-events: none;
    }
    .search-icon .material-symbols-outlined {
      font-size: 18px;
    }

    .tabs-wrap {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }
    .tab-btn {
      background: var(--surface-muted);
      border: 1.5px solid #CBD5E1;
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      border-radius: 4px;
      transition: all 0.08s ease;
      font-family: var(--font-mono);
      user-select: none;
      color: var(--ink-slate);
    }
    .tab-btn:hover {
      background: #E2E8F0;
    }
    .tab-btn.active {
      background: var(--navy-dark);
      color: #FFFFFF;
      border: 1.5px solid var(--navy-dark);
      box-shadow: 0px 2px 0px #000000;
      transform: translateY(-1px);
    }

    .method-filters-wrap {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      align-items: center;
      padding-top: 10px;
      border-top: 1px dashed #CBD5E1;
    }
    .method-filter-label {
      font-size: 11px;
      font-family: var(--font-mono);
      font-weight: 800;
      color: var(--ink-gray);
      margin-right: 4px;
    }
    .method-badge-btn {
      background: var(--surface-white);
      border: 1px solid #94A3B8;
      padding: 3px 8px;
      font-size: 11px;
      border-radius: 4px;
      cursor: pointer;
      font-weight: 600;
      color: var(--ink-slate);
      transition: background 0.08s;
      user-select: none;
    }
    .method-badge-btn:hover { background: #E2E8F0; }
    .method-badge-btn.active {
      background: var(--navy-card);
      color: #FFFFFF;
      border-color: var(--navy-card);
    }

    /* 文献カードリスト */
    .results-count {
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 800;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: var(--ink-slate);
    }

    .cards-list {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .ref-card {
      background: var(--surface-white);
      border: var(--border-thick);
      box-shadow: var(--shadow-card);
      border-radius: 10px;
      padding: 22px 24px;
      transition: transform 0.1s ease, box-shadow 0.1s ease;
    }
    .ref-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-card-lg);
    }

    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }
    .badges-left {
      display: flex;
      gap: 6px;
      align-items: center;
      flex-wrap: wrap;
    }
    .ref-id-badge {
      background: var(--navy-dark);
      color: #FFFFFF;
      padding: 3px 8px;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 900;
      border-radius: 4px;
      letter-spacing: 0.5px;
    }
    .year-badge {
      background: #F1F5F9;
      color: var(--ink-darkest);
      border: 1px solid #CBD5E1;
      padding: 3px 8px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      border-radius: 4px;
    }
    .category-badge {
      background: #F1F5F9;
      color: var(--ink-slate);
      border: 1px solid #CBD5E1;
      padding: 2px 8px;
      font-size: 11px;
      font-weight: 700;
      border-radius: 4px;
    }
    .method-badge-tag {
      background: #F8FAFC;
      color: var(--navy-subtle);
      border: 1px solid #94A3B8;
      padding: 2px 8px;
      font-size: 11px;
      font-weight: 700;
      border-radius: 4px;
      font-family: var(--font-mono);
    }
    .pdf-verified-badge {
      background: #F1F5F9;
      color: var(--navy-dark);
      border: 1px solid #94A3B8;
      padding: 2px 8px;
      font-size: 11px;
      font-weight: 700;
      border-radius: 4px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .pdf-verified-badge .material-symbols-outlined {
      font-size: 13px;
      color: var(--navy-dark);
    }

    .card-title-ja {
      font-size: 18px;
      font-weight: 900;
      line-height: 1.35;
      margin-bottom: 6px;
      color: var(--navy-dark);
    }
    .card-title-en {
      font-size: 13px;
      color: var(--ink-gray);
      font-style: italic;
      margin-bottom: 10px;
      line-height: 1.4;
    }
    .card-meta {
      font-size: 12px;
      color: var(--ink-gray);
      font-family: var(--font-mono);
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--surface-slate);
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
    }
    .doi-link {
      color: var(--accent-steel);
      text-decoration: none;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }
    .doi-link:hover {
      text-decoration: underline;
    }
    .doi-link .material-symbols-outlined {
      font-size: 14px;
    }

    /* 入門者向け解説ボックス（ディープネイビー背景 ＆ フォント薄いグレー） */
    .plain-boxes-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-bottom: 14px;
    }
    @media (max-width: 768px) {
      .plain-boxes-grid {
        grid-template-columns: 1fr;
      }
    }

    .plain-box {
      border-radius: 6px;
      padding: 14px 16px;
      box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.05);
    }
    /* 分析方法ボックス：ディープネイビー */
    .box-method {
      background: var(--navy-dark);
      border: 1px solid var(--navy-subtle);
      color: var(--text-light-secondary);
    }
    /* 結論ボックス：スレートネイビー */
    .box-conclusion {
      background: var(--navy-card);
      border: 1px solid var(--navy-subtle);
      color: var(--text-light-secondary);
    }

    .box-header {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 800;
      margin-bottom: 8px;
      font-family: var(--font-mono);
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: var(--text-light-muted);
    }
    .box-header .material-symbols-outlined {
      font-size: 15px;
      color: #CBD5E1;
    }
    .box-content {
      font-size: 13px;
      line-height: 1.6;
      color: var(--text-light-secondary);
      font-weight: 500;
    }

    /* 本論文での役割コールアウト（ニュートラル薄いグレー背景） */
    .role-callout {
      background: #F1F5F9;
      border: 1px solid #CBD5E1;
      border-left: 4px solid var(--navy-dark);
      border-radius: 4px;
      padding: 10px 14px;
      font-size: 12px;
      line-height: 1.5;
      margin-bottom: 14px;
      color: var(--ink-darkest);
    }
    .role-title {
      font-weight: 800;
      font-size: 11px;
      font-family: var(--font-mono);
      color: var(--ink-slate);
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .role-title .material-symbols-outlined {
      font-size: 15px;
      color: var(--navy-dark);
    }

    /* 詳細アコーディオン */
    .accordion-toggle {
      background: var(--surface-muted);
      border: 1px solid #CBD5E1;
      padding: 10px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      user-select: none;
      transition: background 0.08s ease;
      color: var(--ink-darkest);
    }
    .accordion-toggle:hover {
      background: #E2E8F0;
    }
    .accordion-toggle-left {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .accordion-toggle-left .material-symbols-outlined {
      font-size: 16px;
      color: var(--ink-gray);
    }
    .accordion-content {
      display: none;
      padding-top: 14px;
      margin-top: 10px;
      border-top: 1px dashed #CBD5E1;
      font-size: 12px;
      line-height: 1.6;
    }
    .accordion-content.open {
      display: block;
    }

    .details-subtable {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 12px;
      font-size: 12px;
    }
    .details-subtable th, .details-subtable td {
      border: 1px solid #CBD5E1;
      padding: 6px 10px;
      text-align: left;
    }
    .details-subtable th {
      background: #F1F5F9;
      font-weight: 700;
      width: 25%;
      font-family: var(--font-mono);
      color: var(--ink-slate);
    }
    .details-subtable td {
      color: var(--ink-darkest);
    }

    .qa-box {
      background: #F8FAFC;
      border: 1px solid #CBD5E1;
      border-left: 4px solid var(--navy-subtle);
      padding: 12px 14px;
      border-radius: 4px;
      margin-bottom: 12px;
    }
    .qa-q {
      font-weight: 800;
      color: var(--navy-dark);
      margin-bottom: 4px;
      font-size: 12px;
      display: flex;
      align-items: flex-start;
      gap: 6px;
    }
    .qa-q .material-symbols-outlined {
      font-size: 16px;
      color: var(--navy-subtle);
      margin-top: 1px;
    }
    .qa-a {
      color: var(--ink-slate);
      font-size: 12px;
      padding-left: 22px;
      line-height: 1.5;
    }

    /* コピーボタン */
    .copy-btn {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: #FFFFFF;
      border: 1.5px solid var(--navy-dark);
      padding: 5px 10px;
      font-size: 11px;
      font-family: var(--font-mono);
      font-weight: 700;
      border-radius: 4px;
      cursor: pointer;
      box-shadow: 0 1px 0 var(--navy-dark);
      user-select: none;
      color: var(--navy-dark);
      transition: background 0.08s, color 0.08s;
    }
    .copy-btn:hover {
      background: #F1F5F9;
    }
    .copy-btn:active {
      transform: translateY(1px);
      box-shadow: none;
    }
    .copy-btn .material-symbols-outlined {
      font-size: 14px;
    }

    /* フッター */
    .footer {
      margin-top: 50px;
      padding: 24px 0;
      border-top: var(--border-thick);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      font-size: 12px;
      font-family: var(--font-mono);
      color: var(--ink-gray);
    }
  </style>
</head>
<body>

<div class="container">
  
  <!-- ヘッダー -->
  <header class="header-card">
    <div class="header-tag">
      <span class="material-symbols-outlined">terminal</span>
      IDM ACADEMIC RESEARCH & CITATION DEFENSE COCKPIT
    </div>
    <div class="header-title-row">
      <div>
        <h1 class="header-title">IDM DX CITATION COCKPIT</h1>
        <p class="header-subtitle">
          就業者2,035名の完全決定論的マイクロデータ解析に基づくDX推進意識と組織摩擦の階層乖離研究。<br>
          論文を論理防衛する全45編の引用文献・手元保有実体PDFを完全網羅。専門用語を平易に解説し、初学者や実務家でも直感的に理解できる「分析方法」と「結論」を徹底解説。
        </p>
      </div>
      <div class="header-actions">
        <a href="https://github.com/netch-git/idm-dx-research-paper" target="_blank" class="neo-btn neo-btn-primary">
          <svg height="15" width="15" viewBox="0 0 16 16" fill="currentColor">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
          </svg>
          GitHub Repository
        </a>
      </div>
    </div>

    <!-- メタ情報 -->
    <div class="meta-badges-row">
      <div class="meta-badge active">
        <span class="material-symbols-outlined">database</span>
        ANALYTICAL SAMPLE: N = 2,035 (決定論的完全解析)
      </div>
      <div class="meta-badge">
        <span class="material-symbols-outlined">verified</span>
        CITATION CORPUS: 全45編 (一次資料現物照合済)
      </div>
      <div class="meta-badge">
        <span class="material-symbols-outlined">cloud_done</span>
        DEPLOYED ON: Cloudflare Pages
      </div>
      <div class="meta-badge">
        <span class="material-symbols-outlined">menu_book</span>
        入門者向け解説・専門用語平易化
      </div>
    </div>
  </header>

  <!-- KPIカードグリッド -->
  <section class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">
        <span>TOTAL CITATIONS</span>
        <span class="material-symbols-outlined">library_books</span>
      </div>
      <div class="kpi-value" id="kpi-total">45</div>
      <div class="kpi-desc">理論基盤26編 ＋ 中小企業実体PDF14編 ＋ 政策白書5編</div>
    </div>

    <div class="kpi-card">
      <div class="kpi-label">
        <span>PRIMARY SOURCE VERIFICATION</span>
        <span class="material-symbols-outlined">verified</span>
      </div>
      <div class="kpi-value" style="color: var(--navy-dark);">100%</div>
      <div class="kpi-desc">実体PDF・スキャン原書と頁単位照合。架空引用ゼロ保証</div>
    </div>

    <div class="kpi-card">
      <div class="kpi-label">
        <span>ANALYTICAL FRAMEWORKS</span>
        <span class="material-symbols-outlined">science</span>
      </div>
      <div class="kpi-value" style="color: var(--accent-steel);">7 系統</div>
      <div class="kpi-desc">統制実験、ANOVA、SEM、ロジット、メタ分析、質的、数理証明</div>
    </div>

    <div class="kpi-card">
      <div class="kpi-label">
        <span>SENSITIVITY & CMB DEFENSE</span>
        <span class="material-symbols-outlined">shield</span>
      </div>
      <div class="kpi-value" style="color: var(--navy-subtle);">OR 2.409</div>
      <div class="kpi-desc">重複項目外科的除外＆Siemsen減衰定理で査読疑義を完全論破</div>
    </div>
  </section>

  <!-- チャートセクション -->
  <section class="charts-row">
    <div class="chart-card">
      <div class="chart-header">
        <div class="chart-title">
          <span class="material-symbols-outlined">donut_small</span>
          分析手法カテゴリ別構成比
        </div>
        <span style="font-family: var(--font-mono); font-size: 11px; color: var(--ink-gray);">METHODOLOGY BREAKDOWN</span>
      </div>
      <div style="height: 220px; position: relative;">
        <canvas id="methodChart"></canvas>
      </div>
    </div>

    <div class="chart-card">
      <div class="chart-header">
        <div class="chart-title">
          <span class="material-symbols-outlined">bar_chart</span>
          発行年代別分布（古典理論 〜 2026年最新実証）
        </div>
        <span style="font-family: var(--font-mono); font-size: 11px; color: var(--ink-gray);">TIMELINE CHRONOLOGY</span>
      </div>
      <div style="height: 220px; position: relative;">
        <canvas id="timelineChart"></canvas>
      </div>
    </div>
  </section>

  <!-- コントロールパネル -->
  <section class="control-panel">
    <!-- 検索バー -->
    <div class="search-input-wrap">
      <span class="search-icon">
        <span class="material-symbols-outlined">search</span>
      </span>
      <input type="text" id="searchInput" class="search-input" placeholder="タイトル、著者名、発行年、キーワード（例: 不公平、レディネス、ANOVA、オッズ比、ミドル）でリアルタイム検索...">
    </div>

    <!-- カテゴリタブ -->
    <div class="tabs-wrap" id="categoryTabs">
      <button class="tab-btn active" data-category="ALL">全文献を表示 (45)</button>
      <button class="tab-btn" data-category="組織公正・心理理論">組織公正・心理理論</button>
      <button class="tab-btn" data-category="中小企業・DX実証">中小企業・DX実証</button>
      <button class="tab-btn" data-category="組織構造・規模・階層">組織構造・規模・階層</button>
      <button class="tab-btn" data-category="変革レディネス・抵抗">変革レディネス・抵抗</button>
      <button class="tab-btn" data-category="ミドルマネジメント・戦略">ミドルマネジメント・戦略</button>
      <button class="tab-btn" data-category="統計計量手法・数理防衛">統計計量手法・数理防衛</button>
      <button class="tab-btn" data-category="公的白書・政策レポート">公的白書・政策レポート</button>
    </div>

    <!-- 手法クイックフィルター -->
    <div class="method-filters-wrap" id="methodFilters">
      <span class="method-filter-label">手法絞り込み:</span>
      <button class="method-badge-btn active" data-method="ALL">すべて</button>
      <button class="method-badge-btn" data-method="実験心理学・統制実験">実験心理学・統制実験</button>
      <button class="method-badge-btn" data-method="分散分析(ANOVA)・多重比較">分散分析(ANOVA)</button>
      <button class="method-badge-btn" data-method="共分散構造分析(SEM/CFA)">共分散構造分析(SEM)</button>
      <button class="method-badge-btn" data-method="多変量回帰・ロジット分析">多変量回帰・ロジット</button>
      <button class="method-badge-btn" data-method="メタ分析(Meta-Analysis)">メタ分析</button>
      <button class="method-badge-btn" data-method="質的調査・複数事例研究">質的・事例研究</button>
      <button class="method-badge-btn" data-method="統計数理証明・計量シミュレーション">統計数理証明</button>
      <button class="method-badge-btn" data-method="大規模実態調査・公的統計">公的実態調査</button>
    </div>
  </section>

  <!-- 結果件数 -->
  <div class="results-count">
    <span>SHOWING <span id="currentCount" style="color: var(--accent-steel);">45</span> CITATION CARDS</span>
    <span style="color: var(--ink-gray); font-size: 11px;">クリックで学術詳細・査読Q&A・引用テキストを展開</span>
  </div>

  <!-- カード一覧コンテナ -->
  <main class="cards-list" id="cardsContainer">
    <!-- JSで動的にレンダリング -->
  </main>

  <!-- フッター -->
  <footer class="footer">
    <div>
      <strong>IDM DX RESEARCH CITATION COCKPIT</strong> — Deterministic Complete Cohort Analysis (N = 2,035)
    </div>
    <div>
      Powered by Cloudflare Pages & GitHub | Antigravity Engine
    </div>
  </footer>

</div>

<!-- データ埋め込み＆スクリプト -->
<script>
const rawData = """ + json_data_str + """;

let currentCategory = "ALL";
let currentMethod = "ALL";
let currentSearch = "";

// 安全なエスケープヘルパー
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// フィルタリング処理
function getFilteredData() {
  return rawData.filter(item => {
    // 検索語
    if (currentSearch) {
      const matchText = (
        (item.title_ja || "") + " " +
        (item.title_en || "") + " " +
        (item.author || "") + " " +
        (item.year || "") + " " +
        (item.doi || "") + " " +
        (item.method_plain || "") + " " +
        (item.conclusion_plain || "") + " " +
        (item.role_in_idm || "") + " " +
        (item.category || "") + " " +
        (item.method_badge || "")
      ).toLowerCase();
      if (!matchText.includes(currentSearch)) return false;
    }

    // カテゴリ
    if (currentCategory !== "ALL") {
      if (item.cat_group !== currentCategory) return false;
    }

    // 手法
    if (currentMethod !== "ALL") {
      if (item.method_badge !== currentMethod) return false;
    }

    return true;
  });
}

// カード描画関数
function renderCards() {
  const filtered = getFilteredData();
  const container = document.getElementById("cardsContainer");
  const countEl = document.getElementById("currentCount");
  if (countEl) countEl.textContent = filtered.length;

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="background: #FFFFFF; border: 2px solid #0F172A; border-radius: 8px; padding: 40px; text-align: center;">
        <div style="margin-bottom: 8px;"><span class="material-symbols-outlined" style="font-size: 28px; color: #64748B;">search_off</span></div>
        <div style="font-weight: 800; font-size: 15px; color: #0F172A;">該当する引用文献が見つかりませんでした</div>
        <div style="color: #64748B; font-size: 13px; margin-top: 4px;">検索条件やフィルターを変更してお試しください。</div>
      </div>
    `;
    return;
  }

  let html = "";
  filtered.forEach(item => {
    const doiDisplay = item.doi ? `<a href="${escapeHtml(item.doi)}" target="_blank" rel="noopener noreferrer" class="doi-link"><span class="material-symbols-outlined">open_in_new</span> ${escapeHtml(item.doi)}</a>` : `<span>No DOI (書籍/白書)</span>`;
    const pdfBadge = item.pdf_file ? `<span class="pdf-verified-badge"><span class="material-symbols-outlined">verified</span> PDF照合済 (${escapeHtml(item.pdf_file)})</span>` : `<span class="pdf-verified-badge"><span class="material-symbols-outlined">verified</span> 現物照合済</span>`;
    const apaText = `${item.author} (${item.year}). ${item.title_en}. ${item.journal || ''}. ${item.doi || ''}`.trim();

    html += `
      <article class="ref-card" id="card-${escapeHtml(item.id)}">
        <!-- 上部バッジ行 -->
        <div class="card-top">
          <div class="badges-left">
            <span class="ref-id-badge">${escapeHtml(item.id)}</span>
            <span class="year-badge">${escapeHtml(item.year)}年</span>
            <span class="category-badge">${escapeHtml(item.category)}</span>
            <span class="method-badge-tag">${escapeHtml(item.method_badge)}</span>
          </div>
          <div>
            ${pdfBadge}
          </div>
        </div>

        <!-- タイトル -->
        <h2 class="card-title-ja">${escapeHtml(item.title_ja)}</h2>
        <div class="card-title-en">${escapeHtml(item.title_en)}</div>

        <!-- 著者＆書誌 -->
        <div class="card-meta">
          <span><strong>著者:</strong> ${escapeHtml(item.author)}</span>
          <span><strong>掲載:</strong> ${escapeHtml(item.journal || '学術出版・公式報告')}</span>
          <span>${doiDisplay}</span>
        </div>

        <!-- 入門者向け解説ボックス（ディープネイビー・スレート背景 ＆ フォント薄いグレー） -->
        <div class="plain-boxes-grid">
          <!-- 分析方法（ディープネイビー背景） -->
          <div class="plain-box box-method">
            <div class="box-header">
              <span class="material-symbols-outlined">search</span>
              <span>入門者向け分析方法解説（どうやって調べたか）</span>
            </div>
            <div class="box-content">
              ${escapeHtml(item.method_plain)}
            </div>
          </div>

          <!-- コンクルージョン（スレートネイビー背景） -->
          <div class="plain-box box-conclusion">
            <div class="box-header">
              <span class="material-symbols-outlined">lightbulb</span>
              <span>入門者向け結論解説（要するに何がわかったか）</span>
            </div>
            <div class="box-content">
              ${escapeHtml(item.conclusion_plain)}
            </div>
          </div>
        </div>

        <!-- 本論文での役割（上品なニュートラルグレー背景） -->
        <div class="role-callout">
          <div class="role-title">
            <span class="material-symbols-outlined">shield</span>
            本研究（就業者2,035名解析）での防衛役割・支える仮説
          </div>
          <div>${escapeHtml(item.role_in_idm)}</div>
        </div>

        <!-- アコーディオン（学術詳細） -->
        <div class="accordion-toggle" onclick="toggleAccordion('${escapeHtml(item.id)}')">
          <div class="accordion-toggle-left">
            <span class="material-symbols-outlined">menu_book</span>
            <span>学術的標本設計・適用統計モデル・想定試問(Q&A) を見る</span>
          </div>
          <span id="arrow-${escapeHtml(item.id)}" style="font-size: 11px;">展開する</span>
        </div>

        <div class="accordion-content" id="content-${escapeHtml(item.id)}">
          <table class="details-subtable">
            <tr>
              <th>標本・対象データ</th>
              <td>${escapeHtml(item.sample || '学術調査標本')}</td>
            </tr>
            <tr>
              <th>適用統計手法</th>
              <td>${escapeHtml(item.algorithm || '多変量統計解析')}</td>
            </tr>
            <tr>
              <th>中核的実証数値</th>
              <td>${escapeHtml(item.findings || '論文内検定結果に準拠')}</td>
            </tr>
          </table>

          ${item.q_text ? `
            <div class="qa-box">
              <div class="qa-q">
                <span class="material-symbols-outlined">help</span>
                指導教官・査読者の想定試問 (Q): ${escapeHtml(item.q_text)}
              </div>
              <div class="qa-a">論理防衛回答 (A): ${escapeHtml(item.a_text)}</div>
            </div>
          ` : ''}

          <div style="display: flex; justify-content: space-between; align-items: center; background: #F8FAFC; padding: 10px 14px; border-radius: 4px; border: 1px solid #CBD5E1; gap: 8px; flex-wrap: wrap;">
            <div class="citation-text" id="cite-text-${escapeHtml(item.id)}" style="font-family: var(--font-mono); font-size: 11px; color: var(--ink-slate); word-break: break-all; flex: 1;">
              ${escapeHtml(apaText)}
            </div>
            <button class="copy-btn" onclick="copyCitationFromElement('cite-text-${escapeHtml(item.id)}', this)">
              <span class="material-symbols-outlined">content_copy</span>
              APA引用をコピー
            </button>
          </div>
        </div>
      </article>
    `;
  });

  container.innerHTML = html;
}

// アコーディオン開閉（グローバル定義）
window.toggleAccordion = function(id) {
  const content = document.getElementById("content-" + id);
  const arrow = document.getElementById("arrow-" + id);
  if (!content || !arrow) return;
  if (content.classList.contains("open")) {
    content.classList.remove("open");
    arrow.textContent = "展開する";
  } else {
    content.classList.add("open");
    arrow.textContent = "閉じる";
  }
};

// 引用コピー（DOM要素から直接取得）
window.copyCitationFromElement = function(elementId, btn) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const text = el.textContent.trim();
  
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => {
      showCopiedSuccess(btn);
    }).catch(() => {
      fallbackCopy(text, btn);
    });
  } else {
    fallbackCopy(text, btn);
  }
};

function showCopiedSuccess(btn) {
  const originalHtml = btn.innerHTML;
  btn.innerHTML = `<span class="material-symbols-outlined" style="color: #0F172A;">check</span> コピー完了`;
  btn.style.background = "#E2E8F0";
  setTimeout(() => {
    btn.innerHTML = originalHtml;
    btn.style.background = "#FFFFFF";
  }, 2000);
}

function fallbackCopy(text, btn) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.select();
  try {
    document.execCommand('copy');
    showCopiedSuccess(btn);
  } catch (err) {
    alert("コピーに失敗しました。手動で選択してコピーしてください。");
  }
  document.body.removeChild(textArea);
}

// Chart.js初期化（モノトーン・スレート・エンジニアリング配色）
function initCharts() {
  if (typeof Chart === 'undefined') {
    console.warn("Chart.js not loaded yet");
    return;
  }
  try {
    // 1. 手法別集計
    const methodCounts = {};
    rawData.forEach(d => {
      const m = d.method_badge || 'その他';
      methodCounts[m] = (methodCounts[m] || 0) + 1;
    });

    const canvasMethod = document.getElementById("methodChart");
    if (canvasMethod) {
      new Chart(canvasMethod.getContext("2d"), {
        type: 'doughnut',
        data: {
          labels: Object.keys(methodCounts),
          datasets: [{
            data: Object.values(methodCounts),
            backgroundColor: [
              '#0F172A', '#1E293B', '#334155', '#475569', '#64748B', '#94A3B8', '#CBD5E1', '#E2E8F0'
            ],
            borderWidth: 1.5,
            borderColor: '#FFFFFF'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                font: { family: "'Noto Sans JP', sans-serif", size: 10 },
                color: '#334155',
                boxWidth: 12
              }
            }
          }
        }
      });
    }

    // 2. 年代別集計
    const eraCounts = {
      "〜1970年代 (古典理論)": 0,
      "1980〜1990年代 (確立期)": 0,
      "2000〜2010年代 (発展期)": 0,
      "2020〜2026年 (最新実証)": 0
    };

    rawData.forEach(d => {
      const y = Number(d.year) || 2020;
      if (y < 1980) eraCounts["〜1970年代 (古典理論)"]++;
      else if (y < 2000) eraCounts["1980〜1990年代 (確立期)"]++;
      else if (y < 2020) eraCounts["2000〜2010年代 (発展期)"]++;
      else eraCounts["2020〜2026年 (最新実証)"]++;
    });

    const canvasTimeline = document.getElementById("timelineChart");
    if (canvasTimeline) {
      new Chart(canvasTimeline.getContext("2d"), {
        type: 'bar',
        data: {
          labels: Object.keys(eraCounts),
          datasets: [{
            label: '文献数',
            data: Object.values(eraCounts),
            backgroundColor: '#0F172A',
            borderColor: '#0F172A',
            borderWidth: 1,
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 5, font: { family: "'JetBrains Mono', monospace" }, color: '#64748B' },
              grid: { color: '#E2E8F0' }
            },
            x: {
              ticks: { font: { family: "'Noto Sans JP', sans-serif", size: 10 }, color: '#334155' },
              grid: { display: false }
            }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    }
  } catch (err) {
    console.error("Chart init error:", err);
  }
}

// イベントリスナーのセットアップ
function setupEventListeners() {
  // 検索入力
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      currentSearch = e.target.value.toLowerCase().trim();
      renderCards();
    });
  }

  // カテゴリタブ
  const catButtons = document.querySelectorAll("#categoryTabs .tab-btn");
  catButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      catButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentCategory = btn.getAttribute("data-category") || "ALL";
      renderCards();
    });
  });

  // 手法フィルター
  const methodButtons = document.querySelectorAll("#methodFilters .method-badge-btn");
  methodButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      methodButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentMethod = btn.getAttribute("data-method") || "ALL";
      renderCards();
    });
  });
}

// 起動
if (document.readyState === 'loading') {
  document.addEventListener("DOMContentLoaded", () => {
    setupEventListeners();
    renderCards();
    initCharts();
  });
} else {
  setupEventListeners();
  renderCards();
  initCharts();
}
</script>

</body>
</html>
"""

with open('/home/antigravity/idm-citation-cockpit/index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Generated clean robust index.html without emojis or pastels! Size:", len(html_code))
