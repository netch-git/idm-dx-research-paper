# -*- coding: utf-8 -*-
"""
build_web_textbook.py
Builds the complete interactive Web textbook for IDM statistical methods.
Uses textbook_master_data.py as single source of truth.
Features:
- Dynamic Navigation with live active scroll spy
- 5 Interactive Canvas Simulators
- Deep Roots & Foundations Drill-down tree for all 16 chapters
- 15 Scholarly Dialogue Q&A Accordions
- Robust KaTeX Rendering with Offline Unicode Fallback
"""

import os
import sys

# Ensure scripts dir is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from textbook_master_data import BOOK_METADATA, CHAPTERS_DATA, QA_TOPICS

SIMULATORS_HTML = {
    "sim-anova": r"""
        <div class="simulator-box">
          <div class="sim-header">
            <span class="sim-title">📊 動的シミュレーター 1: ANOVA シグナル vs ノイズ比率シミュレーター</span>
            <span style="font-size: 0.8rem; color: var(--ink-muted);">N = 2,035 仮想分布モデル</span>
          </div>
          <div class="sim-controls">
            <div class="control-group">
              <label class="control-label">群間の離れ具合（シグナル）: <span id="anova-diff-val" class="control-val">1.2</span></label>
              <input type="range" id="anova-diff" min="0.1" max="2.5" step="0.1" value="1.2" />
            </div>
            <div class="control-group">
              <label class="control-label">グループ内のバラツキ SD（ノイズ）: <span id="anova-noise-val" class="control-val">1.1</span></label>
              <input type="range" id="anova-noise" min="0.5" max="2.5" step="0.1" value="1.1" />
            </div>
          </div>
          <div class="sim-canvas-wrapper">
            <canvas id="canvas-anova" class="interactive-canvas" width="860" height="280"></canvas>
          </div>
          <div class="sim-stats-bar">
            <div class="stat-chip">
              <span class="stat-chip-label">F 統計量</span>
              <span id="anova-f" class="stat-chip-value success">18.42</span>
            </div>
            <div class="stat-chip">
              <span class="stat-chip-label">有意確率 (p 値)</span>
              <span id="anova-p" class="stat-chip-value success">&lt; 0.001</span>
            </div>
            <div class="stat-chip">
              <span class="stat-chip-label">効果量 &eta;&sup2; (イータ自乗)</span>
              <span id="anova-eta" class="stat-chip-value">0.018</span>
            </div>
          </div>
        </div>
""",
    "sim-kmeans": r"""
        <div class="simulator-box">
          <div class="sim-header">
            <span class="sim-title">🧭 動的シミュレーター 2: k-means クラスタ重心収束シミュレーター</span>
            <span style="font-size: 0.8rem; color: var(--ink-muted);">N = 2,035 仮想回答者マッピング</span>
          </div>
          <div class="sim-controls">
            <div class="control-group">
              <label class="control-label">クラスタ数 (k): <span id="kmeans-k-val" class="control-val">3</span></label>
              <input type="range" id="kmeans-k" min="2" max="5" step="1" value="3" />
            </div>
            <div class="control-group" style="display: flex; align-items: flex-end;">
              <button id="kmeans-step-btn" class="sim-btn">▶ 次の反復ステップ（重心再計算）</button>
              <button id="kmeans-reset-btn" class="sim-btn secondary" style="margin-left: 8px;">初期化</button>
            </div>
          </div>
          <div class="sim-canvas-wrapper">
            <canvas id="canvas-kmeans" class="interactive-canvas" width="860" height="320"></canvas>
          </div>
          <div class="sim-stats-bar">
            <div class="stat-chip">
              <span class="stat-chip-label">反復回数</span>
              <span id="kmeans-iter" class="stat-chip-value">0</span>
            </div>
            <div class="stat-chip">
              <span class="stat-chip-label">クラスタ内誤差平方和 (WSS)</span>
              <span id="kmeans-wss" class="stat-chip-value">1248.5</span>
            </div>
            <div class="stat-chip">
              <span class="stat-chip-label">収束状態</span>
              <span id="kmeans-status" class="stat-chip-value">待機中</span>
            </div>
          </div>
        </div>
""",
    "sim-logistic": r"""
        <div class="simulator-box">
          <div class="sim-header">
            <span class="sim-title">📈 動的シミュレーター 3: ロジスティック回帰 シグモイド曲線シミュレーター</span>
            <span style="font-size: 0.8rem; color: var(--ink-muted);">確率 0%〜100% の境界制約モデル</span>
          </div>
          <div class="sim-controls">
            <div class="control-group">
              <label class="control-label">傾き係数 &beta;₁ (オッズ比への影響度): <span id="log-b1-val" class="control-val">1.2</span></label>
              <input type="range" id="log-b1" min="0.2" max="3.0" step="0.1" value="1.2" />
            </div>
            <div class="control-group">
              <label class="control-label">切片 &beta;₀ (基準確率のシフト): <span id="log-b0-val" class="control-val">0.0</span></label>
              <input type="range" id="log-b0" min="-3.0" max="3.0" step="0.2" value="0.0" />
            </div>
          </div>
          <div class="sim-canvas-wrapper">
            <canvas id="canvas-logistic" class="interactive-canvas" width="860" height="280"></canvas>
          </div>
          <div class="sim-stats-bar">
            <div class="stat-chip">
              <span class="stat-chip-label">算出オッズ比 Exp(&beta;₁)</span>
              <span id="log-or" class="stat-chip-value success">3.32</span>
            </div>
            <div class="stat-chip">
              <span class="stat-chip-label">X=0 での予測確率</span>
              <span id="log-p0" class="stat-chip-value">50.0%</span>
            </div>
            <div class="stat-chip">
              <span class="stat-chip-label">X=1 での予測確率</span>
              <span id="log-p1" class="stat-chip-value">76.9%</span>
            </div>
          </div>
        </div>
""",
    "sim-moderation": r"""
        <div class="simulator-box">
          <div class="sim-header">
            <span class="sim-title">⚡ 動的シミュレーター 4: 調整効果（交互作用）クロスプロット</span>
            <span style="font-size: 0.8rem; color: var(--ink-muted);">条件によって変化する傾きのダイナミクス</span>
          </div>
          <div class="sim-controls">
            <div class="control-group">
              <label class="control-label">主効果 &beta;₁ (DX教育の効果): <span id="mod-b1-val" class="control-val">0.45</span></label>
              <input type="range" id="mod-b1" min="0.0" max="1.0" step="0.05" value="0.45" />
            </div>
            <div class="control-group">
              <label class="control-label">交互作用 &beta;₃ (上司支援による加速効果): <span id="mod-b3-val" class="control-val">0.35</span></label>
              <input type="range" id="mod-b3" min="-0.6" max="0.8" step="0.05" value="0.35" />
            </div>
          </div>
          <div class="sim-canvas-wrapper">
            <canvas id="canvas-moderation" class="interactive-canvas" width="860" height="280"></canvas>
          </div>
          <div class="sim-stats-bar">
            <div class="stat-chip">
              <span class="stat-chip-label">上司支援 +1SD での傾き</span>
              <span id="mod-slope-high" class="stat-chip-value success">+0.80</span>
            </div>
            <div class="stat-chip">
              <span class="stat-chip-label">上司支援 平均 での傾き</span>
              <span id="mod-slope-mean" class="stat-chip-value">+0.45</span>
            </div>
            <div class="stat-chip">
              <span class="stat-chip-label">上司支援 -1SD での傾き</span>
              <span id="mod-slope-low" class="stat-chip-value">+0.10</span>
            </div>
          </div>
        </div>
""",
    "sim-siemsen": r"""
        <div class="simulator-box">
          <div class="sim-header">
            <span class="sim-title">🛡️ 動的シミュレーター 5: Siemsen 減衰効果シミュレーター</span>
            <span style="font-size: 0.8rem; color: var(--ink-muted);">共通方法バイアス（CMB）下での主効果 vs 交互作用項</span>
          </div>
          <div class="sim-controls">
            <div class="control-group">
              <label class="control-label">共通方法バイアス強度 (CMB &gamma;): <span id="siem-gamma-val" class="control-val">0.30</span></label>
              <input type="range" id="siem-gamma" min="0.0" max="0.6" step="0.05" value="0.30" />
            </div>
            <div class="control-group">
              <label class="control-label">真の交互作用効果 (&beta;*₃): <span id="siem-beta3-val" class="control-val">0.40</span></label>
              <input type="range" id="siem-beta3" min="0.1" max="0.8" step="0.05" value="0.40" />
            </div>
          </div>
          <div class="sim-canvas-wrapper">
            <canvas id="canvas-siemsen" class="interactive-canvas" width="860" height="280"></canvas>
          </div>
          <div class="sim-stats-bar">
            <div class="stat-chip">
              <span class="stat-chip-label">主効果の見かけの膨張</span>
              <span id="siem-main-infl" class="stat-chip-value warning">+28.5% (水増し)</span>
            </div>
            <div class="stat-chip">
              <span class="stat-chip-label">交互作用項の見かけの推定値</span>
              <span id="siem-mod-est" class="stat-chip-value success">0.31 (過小・縮小)</span>
            </div>
            <div class="stat-chip">
              <span class="stat-chip-label">頑健性評価</span>
              <span class="stat-chip-value success">有意なら真実</span>
            </div>
          </div>
        </div>
"""
}

def render_foundations_box(f_data):
    if not f_data:
        return ""
    steps_html = []
    for idx, step in enumerate(f_data.get("steps", []), 1):
        steps_html.append(f"""
          <div class="drilldown-step">
            <div class="step-badge">{idx}</div>
            <div class="step-title">{step['title']}</div>
            <div class="step-desc">{step['desc']}</div>
          </div>
""")
    return f"""
        <div class="foundations-box">
          <div class="foundations-header">
            <span class="foundations-tag">Roots &amp; Foundations</span>
            <h4 class="foundations-title">{f_data['title']}</h4>
          </div>
          {''.join(steps_html)}
        </div>
"""

def build_web_html():
    out_dir = r"G:\マイドライブ\antigravity\IDM\20261029\textbook_web"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "index.html")

    # Build Navigation
    nav_part1 = []
    nav_part2 = []

    for ch in CHAPTERS_DATA:
        ch_id = ch["id"]
        ch_num = ch["num"]
        short_title = ch["title"].split("—")[0].strip() if "—" in ch["title"] else ch["title"]
        nav_item = f'<li class="nav-item"><a href="#{ch_id}"><span class="nav-num">{ch_num}</span>{short_title}</a></li>'
        if int(ch_num) <= 8:
            nav_part1.append(nav_item)
        else:
            nav_part2.append(nav_item)

    # Build Chapters Content
    chapters_html = []
    for idx, ch in enumerate(CHAPTERS_DATA):
        ch_num_int = int(ch["num"])
        
        # Insert Part Dividers
        if ch_num_int == 0:
            chapters_html.append("""
      <div style="margin: 40px 0 20px; padding-bottom: 8px; border-bottom: 2px solid var(--primary-blue);">
        <span style="font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; color: var(--primary-blue); letter-spacing: 0.1em;">PART I</span>
        <h2 style="font-family: var(--font-serif); font-size: 1.8rem; color: var(--ink-primary); margin: 4px 0 0;">本研究の基盤分析パイプライン ＆ 基礎へのドリルダウン</h2>
      </div>
""")
        elif ch_num_int == 9:
            chapters_html.append("""
      <div style="margin: 50px 0 20px; padding-bottom: 8px; border-bottom: 2px solid var(--secondary-teal);">
        <span style="font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; color: var(--secondary-teal); letter-spacing: 0.1em;">PART II</span>
        <h2 style="font-family: var(--font-serif); font-size: 1.8rem; color: var(--ink-primary); margin: 4px 0 0;">引用文献の高度実証手法 ＆ 基礎へのドリルダウン（全40編）</h2>
      </div>
""")

        sections_body = []
        for sec in ch.get("sections", []):
            sections_body.append(f"""
        <h3 class="subhead">{sec['subhead']}</h3>
        {sec['content']}
""")

        sim_key = ch.get("simulator_id")
        sim_html = SIMULATORS_HTML.get(sim_key, "") if sim_key else ""
        foundations_html = render_foundations_box(ch.get("foundations"))

        chapters_html.append(f"""
      <!-- CHAPTER {ch['num']} -->
      <section id="{ch['id']}" class="chapter-section">
        <div class="chapter-header">
          <div class="chapter-number">CHAPTER {ch['num']}</div>
          <h2 class="chapter-title">{ch['title']}</h2>
          <p class="chapter-lead">{ch['lead']}</p>
        </div>

        {''.join(sections_body)}
        {sim_html}
        {foundations_html}
      </section>
""")

    # Build Epilogue & QA
    qa_items = []
    for idx, item in enumerate(QA_TOPICS, 1):
        qa_items.append(f"""
        <div class="qa-item">
          <button class="qa-trigger">
            <span class="qa-num">Q{idx:02d}</span>
            <span class="qa-question">{item['q']}</span>
            <span class="qa-icon">▼</span>
          </button>
          <div class="qa-content">
            <div class="qa-answer">{item['a']}</div>
          </div>
        </div>
""")

    epilogue_html = f"""
      <!-- ====================================================================
           PART III: DIALOGUE & Q&A
           ==================================================================== -->
      <div style="margin: 50px 0 20px; padding-bottom: 8px; border-bottom: 2px solid var(--accent-gold);">
        <span style="font-family: var(--font-mono); font-size: 0.85rem; font-weight: 700; color: var(--accent-gold); letter-spacing: 0.1em;">PART III</span>
        <h2 style="font-family: var(--font-serif); font-size: 1.8rem; color: var(--ink-primary); margin: 4px 0 0;">学術的対話と共有知のための討議手引（15選）</h2>
      </div>

      <section id="epilogue" class="chapter-section">
        <div class="chapter-header">
          <div class="chapter-number">CHAPTER 16</div>
          <h2 class="chapter-title">エピローグ: チームと育む学術的討議の作法（Q&amp;A 15選）</h2>
          <p class="chapter-lead">試問を「防衛」の場から「探究の深化」の場へ。審査員やチームメンバーと建設的な対話を紡ぐための15の視点。</p>
        </div>

        <p>
          分析手法についての質問を受けるとき、それを「追及」や「試練」と捉えて防衛的になると、視野が狭まってしまいます。指導教官や査読者は、研究の妥当性を共に高め、より確かな知見へと磨き上げるためのパートナーです。
        </p>
        <p>
          以下に、本研究および先行研究の分析手法に関して交わされる代表的な15の学術的問いと、それに対する論理的・誠実な対話の指針をまとめました。
        </p>

        <div class="qa-container">
          {''.join(qa_items)}
        </div>
      </section>
"""

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{BOOK_METADATA['title']} — {BOOK_METADATA['subtitle']}</title>

  <!-- Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&family=Noto+Sans+JP:wght@400;500;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Shippori+Mincho:wght@500;700;800&display=swap" rel="stylesheet" />

  <!-- KaTeX for High-Precision Mathematical Typesetting -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css" crossorigin="anonymous" />
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js" crossorigin="anonymous"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>

  <!-- Stylesheet -->
  <link rel="stylesheet" href="css/style.css" />
</head>
<body>

  <!-- Mobile Toggle Button -->
  <button id="mobile-toggle" class="mobile-toggle" aria-label="目次を開く">☰ 目次</button>

  <div class="app-container">
    <!-- Sidebar Navigation -->
    <aside id="sidebar" class="sidebar">
      <div class="sidebar-header">
        <span class="badge-tag">IDM RESEARCH ACADEMY</span>
        <h2 class="sidebar-title">組織調査と計量分析の<br />実践知</h2>
        <p class="sidebar-subtitle">チームで共有するアンケート・統計手法の直感と数理（完全体系化版）</p>
      </div>
      <ul class="nav-menu">
        <li style="padding: 10px 20px 4px; font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">第I部：基盤分析パイプライン</li>
        {''.join(nav_part1)}

        <li style="padding: 16px 20px 4px; font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">第II部：引用文献の高度実証手法</li>
        {''.join(nav_part2)}

        <li style="padding: 16px 20px 4px; font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">第III部：対話と共有知</li>
        <li class="nav-item"><a href="#epilogue"><span class="nav-num">16</span>学術的対話の討議手引(15選)</a></li>
      </ul>
    </aside>

    <!-- Main Content Area -->
    <main class="main-wrapper">
      
      <!-- Hero Banner -->
      <section class="hero-banner">
        <div class="hero-eyebrow">IDM EMPIRICAL METHODOLOGY STUDY GUIDE</div>
        <h1 class="hero-title">{BOOK_METADATA['title']}<br />— {BOOK_METADATA['subtitle']}</h1>
        <p class="hero-desc">
          本教材は、統計学や社会調査の専門知識をこれからの学びとする方々に向けて編纂された学習手引書です。本研究で直接実行した分析パイプライン（ANOVA、k-means、ロジスティック回帰、調整効果、SEM等）に加え、引用文献40編が駆使する高度な計量・実証手法（プロビット回帰、パネルデータ、PLS-SEM、媒介ブートストラップ、メタアナリシス、Gioiaメソッド、ABM等）を網羅しました。各手法には「難易度の階層を下げて根本原理へ遡る基礎学習ドリルダウン」を併載し、チームの共有知を確実に高めます。
        </p>
        <div class="hero-meta">
          <span class="hero-tag">全40編の引用・実体文献完全網羅</span>
          <span class="hero-tag">全16章に基礎ドリルダウン併載</span>
          <span class="hero-tag">動的シミュレーター 5基搭載</span>
          <span class="hero-tag">学術的対話・討議手引 15選完備</span>
        </div>
      </section>

      {''.join(chapters_html)}
      {epilogue_html}

      <!-- Page Footer -->
      <footer style="margin-top: 60px; padding: 40px 0; border-top: 1px solid var(--border-color); text-align: center; color: var(--ink-muted); font-size: 0.85rem;">
        <p style="margin-bottom: 8px;"><strong>{BOOK_METADATA['title']} — {BOOK_METADATA['subtitle']}</strong></p>
        <p style="margin-bottom: 4px;">{BOOK_METADATA['authors']} ｜ {BOOK_METADATA['affiliation']}</p>
        <p>{BOOK_METADATA['rights']}</p>
      </footer>
    </main>
  </div>

  <!-- Simulators & Logic Scripts -->
  <script src="js/simulators.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
"""

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Web Textbook successfully built: {out_file} (Size: {len(html)} bytes)")

if __name__ == "__main__":
    build_web_html()
