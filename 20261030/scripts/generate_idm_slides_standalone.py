#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_idm_slides_standalone.py
「20261003_IDM_SMO_DXレポートダッシュボード_完全版.html」から
「① IDM全設問スライド分析」の全機能・全データ（136問）を単独ファイルとして完全切り出し
"""

import os
import sys
import json
import re

SRC_FILE = r"G:\マイドライブ\antigravity\IDM\20261030\20261003_IDM_SMO_DXレポートダッシュボード_完全版.html"
OUT_FILE = r"G:\マイドライブ\antigravity\IDM\20261030\20261030_IDM全設問スライド分析_完全版.html"
OUT_REPORT = r"G:\マイドライブ\antigravity\IDM\20261030\reports\20261030_IDM全設問スライド分析_完全版.html"

def extract_and_build():
    if not os.path.exists(SRC_FILE):
        print(f"Error: Source file not found: {SRC_FILE}")
        sys.exit(1)

    with open(SRC_FILE, 'r', encoding='utf-8') as f:
        src_text = f.read()

    # 1. slidesData を抽出
    m = re.search(r'const slidesData\s*=\s*(\[[\s\S]*?\]);\s*let idmCurrentIndex', src_text)
    if not m:
        print("Error: Could not extract slidesData")
        sys.exit(1)
    
    slides_json = m.group(1)
    # 検証
    data = json.loads(slides_json)
    print(f"Successfully extracted slidesData: {len(data)} items.")

    # 2. 完全単独HTMLテンプレートを組み立て
    html_template = f"""<!DOCTYPE html>
<html class="h-full" lang="ja">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>IDM調査研究 意識構造分析 全136設問スライド分析システム | HBMS-SMOフロンティア研</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            da: {{
              primary: '#004098',         /* デジタル庁ブルー DADS Blue 900 */
              'primary-hover': '#002f70', /* DADS Blue 1000 */
              'primary-light': '#e6f0fa', /* DADS Blue 50 */
              text: '#1a1a1a',            /* DADS Gray 900 */
              'text-muted': '#4d4d4d',    /* DADS Gray 700 */
              border: '#d9d9d9',          /* DADS Gray 300 */
              'border-dark': '#707070',   /* DADS Gray 600 */
              bg: '#ffffff',
              'bg-subtle': '#f5f7fa',     /* DADS Gray 50 */
              focus: '#ffd700',           /* DADS Focus Yellow */
              success: '#00703c',         /* DADS Green */
              warning: '#d4351c',         /* DADS Red */
              tag: '#eef2f6'
            }}
          }},
          fontFamily: {{
            sans: ['"Noto Sans JP"', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
            mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Consolas', 'monospace']
          }}
        }}
      }}
    }}
  </script>

  <!-- Google Fonts & FontAwesome -->
  <link href="https://fonts.googleapis.com" rel="preconnect"/>
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+JP:wght@400;500;600;700;900&display=swap" rel="stylesheet"/>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet"/>

  <style>
    html {{
      font-feature-settings: "palt";
    }}
    body {{
      font-family: 'Noto Sans JP', sans-serif;
      color: #1a1a1a;
      background-color: #f5f7fa;
    }}
    /* デジタル庁DADS準拠 フォーカスリング */
    a:focus-visible, button:focus-visible, select:focus-visible, input:focus-visible {{
      outline: 3px solid #004098 !important;
      outline-offset: 2px !important;
      box-shadow: 0 0 0 4px #ffd700 !important;
    }}
    .dads-tab-active {{
      background-color: #004098 !important;
      color: #ffffff !important;
      font-weight: 700 !important;
    }}
    .dads-toggle-active {{
      background-color: #004098 !important;
      color: #ffffff !important;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
    }}
    body.font-size-normal {{ --font-scale: 1; }}
    body.font-size-large {{ --font-scale: 1.15; }}
    body.font-size-xlarge {{ --font-scale: 1.3; }}
    #single-stat {{
      font-size: calc(1.18rem * var(--font-scale, 1)) !important;
      font-weight: 800 !important;
      color: #1a1a1a !important;
      line-height: 1.45 !important;
      word-break: break-all !important;
      white-space: pre-wrap !important;
    }}
    #single-title {{
      font-size: calc(0.92rem * var(--font-scale, 1)) !important;
      font-weight: 700 !important;
      color: #004098 !important;
      white-space: pre-wrap !important;
    }}
    #single-text {{
      font-size: calc(0.98rem * var(--font-scale, 1)) !important;
      line-height: 1.8 !important;
    }}
    .card-stat-text {{
      font-size: calc(0.92rem * var(--font-scale, 1)) !important;
    }}
    .card-body-text {{
      font-size: calc(0.85rem * var(--font-scale, 1)) !important;
      line-height: 1.65 !important;
    }}
    #all-cards-grid h3,
    #group-cards-container h3,
    article h3 {{
      white-space: pre-wrap !important;
      word-break: break-all !important;
      line-height: 1.45 !important;
    }}

    .slide-svg-chart {{
      width: 100%;
      height: auto;
      max-height: 380px;
      display: block;
      margin: 0 auto;
    }}
    .chart-label {{ font-size: 11px; fill: #1a1a1a; font-family: 'Noto Sans JP', sans-serif; font-weight: 500; }}
    .chart-label-muted {{ font-size: 10px; fill: #4d4d4d; font-family: 'Noto Sans JP', sans-serif; }}
    .chart-val-label {{ font-size: 10px; fill: #ffffff; font-weight: 700; text-anchor: middle; }}

    /* =========================================================================
       印刷用スタイル (A4 横長 1問1ページ完全収容)
       ========================================================================= */
    @page {{
      size: A4 landscape;
      margin: 6mm 8mm;
    }}
    @media screen {{
      #idm-print-all-pages {{
        display: none !important;
      }}
    }}
    @media print {{
      .no-print,
      header,
      nav,
      footer,
      #idm-view-single,
      #idm-view-all,
      #idm-view-group,
      #idm-single-controls,
      #slide-progress {{
        display: none !important;
      }}

      html, body {{
        width: 100% !important;
        height: auto !important;
        margin: 0 !important;
        padding: 0 !important;
        background: #ffffff !important;
        color: #1a1a1a !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }}

      main {{
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
      }}

      #idm-print-all-pages {{
        display: block !important;
        width: 100% !important;
      }}

      .idm-print-page {{
        page-break-after: always !important;
        break-after: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        width: 100% !important;
        height: 194mm !important;
        max-height: 194mm !important;
        box-sizing: border-box !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        padding: 5mm 7mm !important;
        border: 1px solid #d9d9d9 !important;
        border-radius: 4px !important;
        background: #ffffff !important;
        margin: 0 !important;
        overflow: hidden !important;
      }}

      .idm-print-page:last-child {{
        page-break-after: auto !important;
        break-after: auto !important;
      }}

      .idm-print-header {{
        margin-bottom: 2mm !important;
        flex-shrink: 0 !important;
      }}

      .idm-print-question-title {{
        font-size: 10.5pt !important;
        font-weight: 800 !important;
        color: #1a1a1a !important;
        line-height: 1.35 !important;
        margin: 0 0 1.5mm 0 !important;
        word-break: break-all !important;
        white-space: pre-wrap !important;
      }}

      .idm-print-stat-sub {{
        font-size: 9.5pt !important;
        font-weight: 700 !important;
        color: #004098 !important;
        border-bottom: 1.5pt solid #004098 !important;
        padding-bottom: 1.5mm !important;
        margin-top: 1mm !important;
        margin-bottom: 1.5mm !important;
      }}

      .idm-print-chart-box {{
        flex: 1 1 auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 1.5mm !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 4px !important;
        background: #ffffff !important;
        margin-bottom: 2mm !important;
        overflow: hidden !important;
        min-height: 0 !important;
      }}

      .idm-print-chart-box svg {{
        width: 100% !important;
        max-height: 88mm !important;
        height: auto !important;
        display: block !important;
      }}

      .idm-print-comment-box {{
        flex-shrink: 0 !important;
        background-color: #f5f7fa !important;
        border-left: 3pt solid #004098 !important;
        padding: 2.5mm 3.5mm !important;
        border-radius: 0 4px 4px 0 !important;
        margin-bottom: 1.5mm !important;
      }}

      .idm-print-comment-text {{
        font-size: 9pt !important;
        line-height: 1.5 !important;
        color: #1a1a1a !important;
        margin: 0 !important;
      }}

      .idm-print-footer {{
        flex-shrink: 0 !important;
        border-top: 1px solid #d9d9d9 !important;
        padding-top: 1mm !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        font-size: 7.5pt !important;
        color: #4d4d4d !important;
      }}
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col selection:bg-indigo-200 selection:text-indigo-900">

  <!-- ========================================================= -->
  <!-- デジタル庁DADS準拠 最上位ヘッダー・操作ツールバー          -->
  <!-- ========================================================= -->
  <header class="no-print bg-white border-b border-da-border sticky top-0 z-50 shadow-xs">
    <div class="max-w-7xl mx-auto px-4 py-2.5 flex flex-col lg:flex-row lg:items-center justify-between gap-3">
      <!-- サイトタイトル -->
      <div class="flex items-center gap-3">
        <span class="bg-da-primary text-white text-xs px-2.5 py-1 rounded font-bold tracking-wider">HBMS-SMOフロンティア研</span>
        <div>
          <h1 class="text-sm sm:text-base font-bold text-da-text leading-tight">IDM調査研究 意識構造分析 全136設問スライド分析システム</h1>
          <p class="text-[11px] text-da-text-muted hidden sm:block">全国就業者実証調査（N=2,035）に基づく全設問の集計・意識構造分析スライド（完全ベクター描画）</p>
        </div>
      </div>

      <!-- 操作系・コントロール群 -->
      <div class="flex flex-wrap items-center gap-2">
        <!-- 表示モード切替 -->
        <div class="flex items-center gap-1 bg-da-bg-subtle p-1 rounded border border-da-border text-xs">
          <button class="px-3 py-1 text-xs rounded transition-colors dads-tab-active font-bold cursor-pointer" id="idm-mode-single" onclick="idmSwitchMode('single')" type="button">単一スライド</button>
          <button class="px-3 py-1 text-xs rounded transition-colors text-da-text hover:bg-white font-medium cursor-pointer" id="idm-mode-all" onclick="idmSwitchMode('all')" type="button">一括表示</button>
          <button class="px-3 py-1 text-xs rounded transition-colors text-da-text hover:bg-white font-medium cursor-pointer" id="idm-mode-group" onclick="idmSwitchMode('group')" type="button">設問グループ別</button>
        </div>

        <!-- 文字サイズ切替 -->
        <div class="flex items-center gap-1 bg-da-bg-subtle p-1 rounded border border-da-border text-xs">
          <span class="text-da-text-muted px-1.5 font-bold text-[11px] hidden sm:inline">文字:</span>
          <button class="px-2.5 py-0.5 text-xs rounded transition-colors font-bold dads-tab-active cursor-pointer" id="font-size-normal" onclick="setFontSize('normal')" type="button">標準</button>
          <button class="px-2.5 py-0.5 text-xs rounded transition-colors text-da-text hover:bg-white font-medium cursor-pointer" id="font-size-large" onclick="setFontSize('large')" type="button">大</button>
          <button class="px-2.5 py-0.5 text-xs rounded transition-colors text-da-text hover:bg-white font-medium cursor-pointer" id="font-size-xlarge" onclick="setFontSize('xlarge')" type="button">特大</button>
        </div>

        <!-- スライドナビゲーション操作系（単一表示時） -->
        <div class="flex items-center gap-1.5" id="idm-single-controls">
          <select aria-label="スライド選択" class="text-xs border border-da-border rounded px-2.5 py-1.5 bg-white text-da-text max-w-xs truncate cursor-pointer" id="slide-select" onchange="idmRenderSlide(parseInt(this.value, 10))">
          </select>
          <button class="px-3 py-1.5 text-xs font-bold border border-da-border rounded bg-white hover:bg-da-bg-subtle text-da-primary transition-colors disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer" id="idm-prev-btn" onclick="idmPrevSlide()" type="button">前へ</button>
          <span class="text-xs font-bold text-da-text px-1 min-w-[70px] text-center" id="slide-counter">1 / 136</span>
          <button class="px-3 py-1.5 text-xs font-bold border border-da-border rounded bg-white hover:bg-da-bg-subtle text-da-primary transition-colors disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer" id="idm-next-btn" onclick="idmNextSlide()" type="button">次へ</button>
        </div>

        <!-- 印刷 / PDF ボタン -->
        <button class="px-3 py-1.5 text-xs font-bold bg-da-primary text-white rounded hover:bg-da-primary-hover shadow-xs transition-colors cursor-pointer" onclick="window.print()" type="button">
          <i class="fa-solid fa-print mr-1"></i>印刷 / PDF
        </button>
      </div>
    </div>
  </header>

  <!-- ========================================================= -->
  <!-- メインコンテンツ領域                                      -->
  <!-- ========================================================= -->
  <main class="max-w-7xl mx-auto w-full px-4 pt-4 pb-10 flex-1">

    <!-- 1. 単一スライド表示 -->
    <section class="flex flex-col items-center justify-start" id="idm-view-single">
      <div class="w-full max-w-5xl bg-white border border-da-border rounded-lg shadow-sm p-6 sm:p-8 flex flex-col justify-between transition-all" id="touch-card-container">
        <div>
          <!-- 上部バッジ群 -->
          <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold bg-da-tag text-da-primary px-2.5 py-1 rounded border border-da-border" id="single-group-badge"></span>
              <span class="text-sm font-bold text-da-primary" id="single-title"></span>
            </div>
            <span class="text-[11px] text-da-success font-medium bg-green-50 border border-green-200 px-2 py-0.5 rounded">完全ベクター描画</span>
          </div>

          <!-- 設問見出し -->
          <h2 class="font-bold text-da-text pb-3 mb-4 border-b-2 border-da-border leading-snug" id="single-stat"></h2>

          <!-- SVGチャート枠 -->
          <div class="my-4 p-4 border border-da-border rounded bg-white overflow-hidden shadow-2xs">
            <div class="w-full flex items-center justify-center" id="single-chart-slot"></div>
          </div>

          <!-- 分析解説ボックス -->
          <div class="bg-da-bg-subtle border-l-4 border-da-primary p-5 rounded-r shadow-xs">
            <p class="text-da-text leading-relaxed font-normal" id="single-text"></p>
          </div>
        </div>

        <!-- カード下部フッター -->
        <div class="mt-6 pt-3 border-t border-da-border flex flex-wrap justify-between items-center gap-2 text-xs text-da-text-muted">
          <span>HBMS-SMOフロンティア研究所 IDM調査研究報告（N=2,035）</span>
          <span class="font-bold" id="single-footer-counter"></span>
        </div>
      </div>

      <!-- プログレスバー -->
      <div class="w-full max-w-5xl mt-3 bg-gray-200 h-1.5 rounded-full overflow-hidden">
        <div class="bg-da-primary h-full transition-all duration-300 w-0" id="slide-progress"></div>
      </div>
    </section>

    <!-- 2. 全スライド一括表示 -->
    <section class="hidden" id="idm-view-all">
      <div class="mb-4 flex justify-between items-center">
        <p class="text-sm font-bold text-da-text-muted" id="all-summary-text">全スライド一覧（全136設問）</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6" id="all-cards-grid"></div>
    </section>

    <!-- 3. 設問グループ別 -->
    <section class="hidden" id="idm-view-group">
      <nav aria-label="グループ目次" class="no-print bg-white p-4 rounded-lg border border-da-border mb-8 shadow-sm">
        <p class="text-xs font-bold text-da-text-muted mb-2.5">グループ一覧（クリックで移動）</p>
        <div class="flex flex-wrap gap-2" id="group-nav-links"></div>
      </nav>
      <div class="space-y-12" id="group-cards-container"></div>
    </section>

    <!-- 4. 印刷用コンテナ (A4横・全問展開) -->
    <div aria-hidden="true" id="idm-print-all-pages"></div>

  </main>

  <!-- 画面下部フッター -->
  <footer class="no-print bg-white border-t border-da-border py-4 text-center text-xs text-da-text-muted">
    キーボードの [←] [→] キーまたは画面スワイプでスライド送り（単一表示モード時）
  </footer>

  <!-- ========================================================= -->
  <!-- 完全決定論的スクリプト（全136設問データ & SVG描画エンジン）   -->
  <!-- ========================================================= -->
  <script>
    // -------------------------------------------------------------
    // 1. 全136設問マスターデータ (N = 2,035)
    // -------------------------------------------------------------
    const slidesData = {slides_json};
    let idmCurrentIndex = 0;
    const idmTotalSlides = slidesData.length;

    // -------------------------------------------------------------
    // 2. ベクターSVGチャート描画エンジン
    // -------------------------------------------------------------
    function idmGenerateSVG(slide, width = 740) {{
      const data = slide.data || [];
      const series = slide.series || [
        {{ name: "該当・肯定", color: "#004098" }},
        {{ name: "その他", color: "#e2e8f0" }}
      ];

      const rowHeight = 22;
      const labelWidth = 110;
      const chartAreaWidth = width - labelWidth - 30;
      const height = 40 + (data.length * rowHeight) + 30;

      let svg = `<svg viewBox="0 0 ${{width}} ${{height}}" class="slide-svg-chart" xmlns="http://www.w3.org/2000/svg">`;
      svg += `<g transform="translate(${{labelWidth}}, 15)">`;
      let legendX = 0;
      series.forEach(s => {{
        svg += `
          <rect x="${{legendX}}" y="0" width="12" height="10" rx="2" fill="${{s.color}}" />
          <text x="${{legendX + 16}}" y="9" class="chart-label-muted">${{s.name}}</text>
        `;
        legendX += s.name.length * 11 + 32;
      }});
      svg += `</g>`;

      const ticks = [0, 25, 50, 75, 100];
      svg += `<g transform="translate(${{labelWidth}}, 32)">`;
      ticks.forEach(t => {{
        const x = (t / 100) * chartAreaWidth;
        svg += `
          <line x1="${{x}}" y1="0" x2="${{x}}" y2="${{data.length * rowHeight}}" stroke="#eaeaea" stroke-width="1" />
          <text x="${{x}}" y="${{data.length * rowHeight + 15}}" text-anchor="middle" class="chart-label-muted">${{t}}%</text>
        `;
      }});
      svg += `</g>`;

      data.forEach((row, i) => {{
        const y = 35 + (i * rowHeight);
        svg += `<text x="${{labelWidth - 10}}" y="${{y + 13}}" text-anchor="end" class="chart-label">${{row.label}}</text>`;
        let currentX = 0;
        const total = row.values.reduce((a, b) => a + b, 0) || 100;
        row.values.forEach((val, vIdx) => {{
          const barW = (val / total) * chartAreaWidth;
          const color = (series[vIdx] && series[vIdx].color) ? series[vIdx].color : "#718096";
          if (barW > 0.5) {{
            svg += `
              <rect x="${{labelWidth + currentX}}" y="${{y + 2}}" width="${{barW}}" height="${{rowHeight - 6}}" fill="${{color}}">
                <title>${{row.label}} - ${{series[vIdx] ? series[vIdx].name : ''}}: ${{val.toFixed(1)}}%</title>
              </rect>
            `;
            if (barW > 28) {{
              svg += `<text x="${{labelWidth + currentX + (barW / 2)}}" y="${{y + 12}}" class="chart-val-label">${{val.toFixed(1)}}%</text>`;
            }}
          }}
          currentX += barW;
        }});
      }});
      svg += `</svg>`;
      return svg;
    }}

    // -------------------------------------------------------------
    // 3. 単一スライドレンダリング (DADSパッチ適用完全版)
    // -------------------------------------------------------------
    function idmRenderSlide(index) {{
      if (index < 0 || index >= idmTotalSlides) return;
      idmCurrentIndex = index;
      const data = slidesData[idmCurrentIndex];

      const groupEl = document.getElementById('single-group-badge');
      const titleEl = document.getElementById('single-title');
      const statEl = document.getElementById('single-stat');
      const textEl = document.getElementById('single-text');
      const chartSlot = document.getElementById('single-chart-slot');

      if (groupEl) groupEl.textContent = data.group || '';
      if (statEl) statEl.textContent = data.title || '';
      if (titleEl) titleEl.textContent = data.stat || '';
      if (textEl) textEl.textContent = data.text || '';
      if (chartSlot && typeof idmGenerateSVG === 'function') {{
        chartSlot.innerHTML = idmGenerateSVG(data, 760);
      }}

      const countStr = `${{idmCurrentIndex + 1}} / ${{idmTotalSlides}}`;
      const counterEl = document.getElementById('slide-counter');
      const footerCounterEl = document.getElementById('single-footer-counter');
      const selectEl = document.getElementById('slide-select');
      const progressBar = document.getElementById('slide-progress');

      if (counterEl) counterEl.textContent = countStr;
      if (footerCounterEl) footerCounterEl.textContent = `スライド ${{countStr}}`;
      if (selectEl) selectEl.value = idmCurrentIndex;
      if (progressBar) progressBar.style.width = `${{((idmCurrentIndex + 1) / idmTotalSlides) * 100}}%`;

      const prevBtn = document.getElementById('idm-prev-btn');
      const nextBtn = document.getElementById('idm-next-btn');
      if (prevBtn) prevBtn.disabled = (idmCurrentIndex === 0);
      if (nextBtn) nextBtn.disabled = (idmCurrentIndex === idmTotalSlides - 1);
    }}

    window.idmPrevSlide = function() {{ if (idmCurrentIndex > 0) idmRenderSlide(idmCurrentIndex - 1); }};
    window.idmNextSlide = function() {{ if (idmCurrentIndex < idmTotalSlides - 1) idmRenderSlide(idmCurrentIndex + 1); }};

    // -------------------------------------------------------------
    // 4. 表示モード切替 (単一 / 一括 / グループ別)
    // -------------------------------------------------------------
    window.idmSwitchMode = function(mode) {{
      const bSingle = document.getElementById('idm-mode-single');
      const bAll = document.getElementById('idm-mode-all');
      const bGroup = document.getElementById('idm-mode-group');
      const vSingle = document.getElementById('idm-view-single');
      const vAll = document.getElementById('idm-view-all');
      const vGroup = document.getElementById('idm-view-group');
      const ctrl = document.getElementById('idm-single-controls');

      bSingle.classList.remove('dads-tab-active');
      bAll.classList.remove('dads-tab-active');
      bGroup.classList.remove('dads-tab-active');
      vSingle.classList.add('hidden');
      vAll.classList.add('hidden');
      vGroup.classList.add('hidden');

      if (mode === 'single') {{
        bSingle.classList.add('dads-tab-active');
        vSingle.classList.remove('hidden');
        ctrl.style.display = 'flex';
      }} else if (mode === 'all') {{
        bAll.classList.add('dads-tab-active');
        vAll.classList.remove('hidden');
        ctrl.style.display = 'none';
      }} else if (mode === 'group') {{
        bGroup.classList.add('dads-tab-active');
        vGroup.classList.remove('hidden');
        ctrl.style.display = 'none';
      }}
    }};

    window.jumpToSlide = function(idx) {{
      idmSwitchMode('single');
      idmRenderSlide(idx);
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }};

    // -------------------------------------------------------------
    // 5. 文字サイズ切替 (標準 / 大 / 特大)
    // -------------------------------------------------------------
    window.setFontSize = function(size) {{
      document.body.classList.remove('font-size-normal', 'font-size-large', 'font-size-xlarge');
      document.getElementById('font-size-normal').classList.remove('dads-tab-active');
      document.getElementById('font-size-large').classList.remove('dads-tab-active');
      document.getElementById('font-size-xlarge').classList.remove('dads-tab-active');

      if (size === 'large') {{
        document.body.classList.add('font-size-large');
        document.getElementById('font-size-large').classList.add('dads-tab-active');
      }} else if (size === 'xlarge') {{
        document.body.classList.add('font-size-xlarge');
        document.getElementById('font-size-xlarge').classList.add('dads-tab-active');
      }} else {{
        document.body.classList.add('font-size-normal');
        document.getElementById('font-size-normal').classList.add('dads-tab-active');
      }}
    }};

    // -------------------------------------------------------------
    // 6. グリッド・グループ別ビュー構築
    // -------------------------------------------------------------
    function idmBuildGrids() {{
      const sel = document.getElementById('slide-select');
      const allGrid = document.getElementById('all-cards-grid');
      const grpNav = document.getElementById('group-nav-links');
      const grpCont = document.getElementById('group-cards-container');
      const groupsMap = new Map();

      sel.innerHTML = '';
      allGrid.innerHTML = '';
      grpNav.innerHTML = '';
      grpCont.innerHTML = '';

      slidesData.forEach((s, idx) => {{
        const opt = document.createElement('option');
        opt.value = idx;
        opt.textContent = `${{idx + 1}}. [${{s.group}}] ${{s.title}}`;
        sel.appendChild(opt);

        if (!groupsMap.has(s.group)) groupsMap.set(s.group, []);
        groupsMap.get(s.group).push({{ ...s, originalIndex: idx }});
      }});

      function cardHTML(s, idx) {{
        return `
          <article class="bg-white border border-da-border rounded-lg shadow-sm p-5 flex flex-col justify-between hover:border-da-primary hover:shadow transition-all">
            <div>
              <div class="flex items-center justify-between gap-2 mb-2">
                <span class="text-xs font-bold text-da-primary bg-da-tag px-2.5 py-0.5 rounded border border-da-border">${{s.group}}</span>
                <span class="text-xs text-da-text-muted font-bold">No. ${{idx + 1}}</span>
              </div>
              <h3 class="text-sm font-bold text-da-primary mb-1">${{s.title}}</h3>
              <h4 class="card-stat-text font-bold text-da-text pb-2 mb-3 border-b border-da-border leading-snug">${{s.stat}}</h4>
              <div class="my-3 p-2 bg-white border border-da-border rounded flex items-center justify-center overflow-hidden">
                ${{idmGenerateSVG(s, 520)}}
              </div>
              <div class="card-body-text bg-da-bg-subtle border-l-4 border-da-primary p-3 rounded-r leading-relaxed text-da-text">
                ${{s.text}}
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-da-border flex justify-between items-center text-xs text-da-text-muted">
              <span>N=2,035</span>
              <button type="button" onclick="jumpToSlide(${{idx}})" class="text-da-primary hover:underline font-bold py-1 px-2 rounded hover:bg-da-primary-light transition-colors cursor-pointer">単一スライドで見る →</button>
            </div>
          </article>
        `;
      }}

      allGrid.innerHTML = slidesData.map((s, idx) => cardHTML(s, idx)).join('');

      let gIdx = 0;
      groupsMap.forEach((items, groupName) => {{
        const gId = `grp-sec-${{gIdx}}`;
        const nBtn = document.createElement('a');
        nBtn.href = `#${{gId}}`;
        nBtn.className = "text-xs bg-white hover:bg-da-primary-light text-da-primary border border-da-border px-3 py-1.5 rounded font-medium transition-colors shadow-2xs";
        nBtn.textContent = `${{groupName}} (${{items.length}})`;
        grpNav.appendChild(nBtn);

        const sec = document.createElement('section');
        sec.id = gId;
        sec.className = "scroll-mt-24";
        sec.innerHTML = `
          <div class="border-b-2 border-da-primary pb-2 mb-4 flex items-center justify-between">
            <h2 class="text-base sm:text-lg font-bold text-da-text flex items-center gap-2">
              <span class="w-2.5 h-5 bg-da-primary rounded-xs inline-block"></span>
              ${{groupName}}
            </h2>
            <span class="text-xs text-da-text-muted font-bold">${{items.length}} 設問</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            ${{items.map(s => cardHTML(s, s.originalIndex)).join('')}}
          </div>
        `;
        grpCont.appendChild(sec);
        gIdx++;
      }});
    }}

    // -------------------------------------------------------------
    // 7. 印刷用レイアウト生成 (A4横・全問展開)
    // -------------------------------------------------------------
    function buildAllPrintPages() {{
      const container = document.getElementById('idm-print-all-pages');
      if (!container || container.children.length > 0) return;
      if (typeof slidesData === 'undefined' || !Array.isArray(slidesData)) return;

      const total = slidesData.length;
      let html = '';
      slidesData.forEach((s, idx) => {{
        const svgCode = (typeof idmGenerateSVG === 'function') 
          ? idmGenerateSVG(s, 760) 
          : '';
        
        html += `
          <article class="idm-print-page">
            <div class="idm-print-header">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5mm;">
                <span style="font-size: 8pt; font-weight: 700; color: #004098; background: #eef2f6; border: 1px solid #d9d9d9; padding: 1px 6px; border-radius: 3px;">${{s.group || ''}}</span>
                <span style="font-size: 8pt; font-weight: 700; color: #4d4d4d;">No. ${{idx + 1}} / ${{total}}</span>
              </div>
              <h2 class="idm-print-question-title">${{s.title || ''}}</h2>
              <div class="idm-print-stat-sub">${{s.stat || ''}}</div>
            </div>
            <div class="idm-print-chart-box">${{svgCode}}</div>
            <div class="idm-print-comment-box"><p class="idm-print-comment-text">${{s.text || ''}}</p></div>
            <div class="idm-print-footer">
              <span>HBMS-SMOフロンティア研究所 IDM調査研究報告（N=2,035）</span>
              <span style="font-weight: 700;">スライド ${{idx + 1}} / ${{total}}</span>
            </div>
          </article>
        `;
      }});
      container.innerHTML = html;
    }}

    // -------------------------------------------------------------
    // 8. キーボード ＆ スワイプ操作イベント
    // -------------------------------------------------------------
    window.addEventListener('keydown', (e) => {{
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {{
        e.preventDefault();
        idmNextSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        e.preventDefault();
        idmPrevSlide();
      }}
    }});

    // スワイプ操作
    let touchStartX = 0;
    let touchEndX = 0;
    const touchArea = document.getElementById('touch-card-container');
    if (touchArea) {{
      touchArea.addEventListener('touchstart', e => {{
        touchStartX = e.changedTouches[0].screenX;
      }}, {{ passive: true }});
      touchArea.addEventListener('touchend', e => {{
        touchEndX = e.changedTouches[0].screenX;
        if (touchEndX < touchStartX - 50) {{
          idmNextSlide();
        }}
        if (touchEndX > touchStartX + 50) {{
          idmPrevSlide();
        }}
      }}, {{ passive: true }});
    }}

    // -------------------------------------------------------------
    // 9. イベントバインド
    // -------------------------------------------------------------
    window.addEventListener('beforeprint', buildAllPrintPages);

    window.addEventListener('DOMContentLoaded', () => {{
      idmBuildGrids();
      idmRenderSlide(0);
    }});
  </script>
</body>
</html>
"""

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Generated standalone file: {OUT_FILE} ({os.path.getsize(OUT_FILE):,} bytes)")

    # reports ディレクトリにも配置
    os.makedirs(os.path.dirname(OUT_REPORT), exist_ok=True)
    with open(OUT_REPORT, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Copied to reports: {OUT_REPORT} ({os.path.getsize(OUT_REPORT):,} bytes)")

if __name__ == "__main__":
    extract_and_build()
