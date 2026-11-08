#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_a4_landscape_slide.py
SMOフロンティア研究所 IDM研究会 中間発表用 A4横長1枚完結スライド生成スクリプト
"""

import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SMOフロンティア研究所 IDM研究会 中間発表 | SMOのDX推進と組織の断絶</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
  <style>
    /* ==========================================================================
       DADS準拠 カラーパレット & 基本設計
       ========================================================================== */
    :root {
      --dads-primary: #005BAC;
      --dads-primary-dark: #003F75;
      --dads-primary-light: #EBF3FA;
      --dads-secondary: #00838F;
      --dads-secondary-light: #E0F7FA;
      --dads-success: #228543;
      --dads-success-light: #E8F5E9;
      --dads-alert: #D32F2F;
      --dads-alert-light: #FFEBEE;
      --dads-warning: #B78103;
      --dads-warning-light: #FFF8E1;
      --dads-bg: #F8F9FA;
      --dads-card-bg: #FFFFFF;
      --dads-border: #DDE2E5;
      --dads-border-light: #ECEFF1;
      --dads-text: #1A1A1A;
      --dads-text-sub: #4A5568;
      --dads-text-muted: #718096;
      --font-base: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: var(--font-base);
      background-color: #525659;
      color: var(--dads-text);
      line-height: 1.45;
      -webkit-font-smoothing: antialiased;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 20px 10px;
      min-height: 100vh;
    }

    /* ツールバー（画面表示時のみ） */
    .toolbar {
      width: 100%;
      max-width: 1120px;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #FFFFFF;
      padding: 8px 16px;
      border-radius: 6px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    .toolbar-info {
      font-size: 13px;
      font-weight: 700;
      color: var(--dads-primary-dark);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .toolbar-badge {
      background: var(--dads-primary-light);
      color: var(--dads-primary);
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
    }

    .toolbar-actions {
      display: flex;
      gap: 10px;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 700;
      border-radius: 4px;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s;
      font-family: var(--font-base);
      text-decoration: none;
    }

    .btn-primary {
      background: var(--dads-primary);
      color: #FFFFFF;
    }

    .btn-primary:hover {
      background: var(--dads-primary-dark);
    }

    .btn-outline {
      background: #FFFFFF;
      color: var(--dads-primary);
      border-color: var(--dads-primary);
    }

    .btn-outline:hover {
      background: var(--dads-primary-light);
    }

    /* ==========================================================================
       A4 横長スライド コンテナ（297mm × 210mm 相当、比率 1.414:1）
       ========================================================================== */
    .slide-page {
      width: 1120px;
      height: 792px; /* 1120 / 1.414 ≒ 792px (A4横長比率完全固定) */
      background: #FFFFFF;
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
      border-radius: 4px;
      overflow: hidden;
      padding: 24px 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }

    /* スライドヘッダー */
    .slide-header {
      border-bottom: 2px solid var(--dads-primary);
      padding-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }

    .header-left {
      flex: 1;
    }

    .conf-badge {
      display: inline-block;
      font-size: 11px;
      font-weight: 700;
      color: var(--dads-primary);
      background: var(--dads-primary-light);
      padding: 2px 8px;
      border-radius: 3px;
      margin-bottom: 4px;
      letter-spacing: 0.05em;
    }

    .main-title {
      font-size: 23px;
      font-weight: 900;
      color: var(--dads-primary-dark);
      letter-spacing: -0.02em;
      line-height: 1.25;
      margin-bottom: 3px;
    }

    .sub-title {
      font-size: 13.5px;
      font-weight: 700;
      color: var(--dads-text-sub);
    }

    .header-right {
      text-align: right;
      font-size: 11.5px;
      color: var(--dads-text-muted);
      line-height: 1.4;
      padding-left: 16px;
    }

    .data-source-tag {
      font-weight: 700;
      color: var(--dads-primary);
    }

    /* ==========================================================================
       スライドメイン領域：3カラム グリッド
       ========================================================================== */
    .slide-content {
      display: grid;
      grid-template-columns: 1.08fr 1fr 1.02fr;
      gap: 16px;
      margin-top: 14px;
      flex: 1;
      min-height: 0;
    }

    /* 各カラム共通パネル */
    .col-panel {
      background: #FFFFFF;
      border: 1px solid var(--dads-border);
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .panel-header {
      padding: 8px 12px;
      font-size: 14px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
      border-bottom: 1px solid var(--dads-border);
    }

    .panel-header.primary {
      background: var(--dads-primary-light);
      color: var(--dads-primary-dark);
      border-top: 3px solid var(--dads-primary);
    }

    .panel-header.success {
      background: var(--dads-success-light);
      color: var(--dads-success);
      border-top: 3px solid var(--dads-success);
    }

    .panel-header.secondary {
      background: var(--dads-secondary-light);
      color: var(--dads-secondary);
      border-top: 3px solid var(--dads-secondary);
    }

    .panel-number {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: currentColor;
      color: #FFFFFF !important;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 900;
    }

    .panel-body {
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      flex: 1;
      font-size: 12px;
      color: var(--dads-text);
      justify-content: space-between;
    }

    /* 各ブロック内のカード装飾 */
    .sub-card {
      background: var(--dads-bg);
      border-left: 3.5px solid var(--dads-primary);
      padding: 8px 10px;
      border-radius: 0 4px 4px 0;
    }

    .sub-card.alert {
      border-left-color: var(--dads-alert);
      background: #FFF5F5;
    }

    .sub-card.success {
      border-left-color: var(--dads-success);
      background: #F4FBF7;
    }

    .sub-card.secondary {
      border-left-color: var(--dads-secondary);
      background: #F0FAFA;
    }

    .card-headline {
      font-size: 12.5px;
      font-weight: 800;
      margin-bottom: 3px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .card-headline.alert { color: var(--dads-alert); }
    .card-headline.success { color: var(--dads-success); }
    .card-headline.secondary { color: var(--dads-secondary); }
    .card-headline.primary { color: var(--dads-primary); }

    .tag-stat {
      font-size: 10px;
      padding: 1px 5px;
      border-radius: 3px;
      font-weight: 700;
      background: #E2E8F0;
      color: #2D3748;
    }

    .tag-stat.sig {
      background: #EBF8FF;
      color: #2B6CB0;
    }

    .sub-card p {
      font-size: 11.5px;
      line-height: 1.45;
      color: var(--dads-text-sub);
    }

    .sub-card strong {
      color: var(--dads-text);
      font-weight: 700;
    }

    /* コントラスト図解ミニボックス（第1カラム用） */
    .mini-compare-box {
      background: #FFFFFF;
      border: 1px dashed var(--dads-border);
      border-radius: 4px;
      padding: 6px 8px;
      font-size: 11px;
      line-height: 1.4;
    }

    .compare-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 2px;
      padding-bottom: 2px;
      border-bottom: 1px dotted var(--dads-border-light);
    }

    .compare-row:last-child {
      margin-bottom: 0;
      padding-bottom: 0;
      border-bottom: none;
    }

    /* 討論を促すクエスチョンBOX（第3カラム用） */
    .discussion-trigger-box {
      background: linear-gradient(135deg, #FFFDF0 0%, #FFF8E1 100%);
      border: 1.5px solid #FBC02D;
      border-radius: 5px;
      padding: 9px 10px;
    }

    .discussion-title {
      font-size: 12px;
      font-weight: 800;
      color: #795548;
      display: flex;
      align-items: center;
      gap: 5px;
      margin-bottom: 5px;
    }

    .discussion-item {
      font-size: 11.2px;
      color: #3E2723;
      line-height: 1.4;
      margin-bottom: 4px;
      padding-left: 14px;
      position: relative;
    }

    .discussion-item::before {
      content: "▶";
      position: absolute;
      left: 0;
      color: #E65100;
      font-size: 8px;
      top: 3px;
    }

    /* ==========================================================================
       スライドフッター
       ========================================================================== */
    .slide-footer {
      border-top: 1px solid var(--dads-border);
      padding-top: 8px;
      margin-top: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: var(--dads-text-muted);
    }

    .footer-left {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .footer-note {
      font-size: 10.5px;
      color: var(--dads-text-sub);
    }

    .footer-right {
      font-weight: 700;
      color: var(--dads-primary);
    }

    /* ==========================================================================
       印刷用スタイル（A4 横長 1枚に完全固定）
       ========================================================================== */
    @media print {
      body {
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
      }

      .toolbar {
        display: none !important;
      }

      .slide-page {
        width: 100% !important;
        height: 100vh !important;
        max-height: 100vh !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        padding: 14mm 16mm 10mm 16mm !important;
        page-break-after: avoid !important;
        page-break-inside: avoid !important;
      }

      @page {
        size: A4 landscape;
        margin: 0;
      }
    }
  </style>
</head>
<body>

  <!-- 画面上部操作ツールバー -->
  <div class="toolbar">
    <div class="toolbar-info">
      <span class="toolbar-badge">中間発表用 1枚スライド</span>
      <span>SMOフロンティア研究所 IDM研究会（2026年10月）</span>
    </div>
    <div class="toolbar-actions">
      <button class="btn btn-outline" onclick="toggleFullscreen()">全画面表示 (F)</button>
      <button class="btn btn-primary" onclick="window.print()">A4横で印刷 / PDF保存</button>
    </div>
  </div>

  <!-- A4 横長 1枚スライド 本体 -->
  <div class="slide-page" id="slide-container">

    <!-- ヘッダー -->
    <header class="slide-header">
      <div class="header-left">
        <span class="conf-badge">SMOフロンティア研究所 IDM研究会 中間発表</span>
        <h1 class="main-title">中堅・中小企業（SMO）のDX推進と「組織の断絶」</h1>
        <p class="sub-title">就業者2,035名の実証調査からみる「中間管理職の孤立」と3つの処方箋</p>
      </div>
      <div class="header-right">
        <div>報告者: <strong>IDM研究プロジェクト</strong></div>
        <div>調査対象: <span class="data-source-tag">全国正規就業者 2,035名</span>（全産業）</div>
        <div>大企業: 1,035名 ／ SMO（1,000名未満）: 1,000名</div>
      </div>
    </header>

    <!-- 3カラム メインコンテンツ -->
    <main class="slide-content">

      <!-- カラム1: 何がわかったのか？（事実とメカニズム） -->
      <section class="col-panel">
        <div class="panel-header primary">
          <span class="panel-number">1</span>
          <span>何がわかったのか？（実態と真因）</span>
        </div>
        <div class="panel-body">
          <!-- 発見1 -->
          <div class="sub-card alert">
            <div class="card-headline alert">
              <span>① 中間管理職（課長・部長）の孤立</span>
              <span class="tag-stat sig">有意差を確認</span>
            </div>
            <p>大企業では職階順に意識が緩やかに推移するのに対し、<strong>SMOでは中間管理職の変革当事者意識が最も大きく落ち込む</strong>現象が確認されました（一般社員は規模によらず同水準に収束）。</p>
          </div>

          <!-- ミニ比較図解 -->
          <div class="mini-compare-box">
            <div class="compare-row">
              <span style="font-weight:700; color:var(--dads-primary);">大企業（1,000名以上）</span>
              <span>経営層(高) ➔ 管理職(中) ➔ 一般社員(並)</span>
            </div>
            <div class="compare-row">
              <span style="font-weight:700; color:var(--dads-alert);">SMO（1,000名未満）</span>
              <span>経営層(高) ➔ <strong>管理職(急落・孤立)</strong> ➔ 一般社員</span>
            </div>
          </div>

          <!-- 発見2 -->
          <div class="sub-card">
            <div class="card-headline primary">
              <span>② 孤立の主因は「リーダーシップと評価」</span>
              <span class="tag-stat sig">統計的に示唆</span>
            </div>
            <p>意識低下の要因は「ITツールの難しさ」ではなく、<strong>「経営陣のビジョンやリーダーシップへの疑問（方針が見えない）」</strong>と<strong>「成果が給与や人事評価に還元されない不満」</strong>であることが示唆されました。</p>
          </div>

          <!-- 発見3 -->
          <div class="sub-card">
            <div class="card-headline primary">
              <span>③ ITスキルより「組織の調整役」が成否を分ける</span>
              <span class="tag-stat sig">強い影響を示唆</span>
            </div>
            <p>変革の成否を分けるのは高度な先端IT知識そのものではなく、<strong>現場の課題を発見し合意を形成する「調整力・PMO機能」</strong>であることが強く示唆されました。</p>
          </div>
        </div>
      </section>

      <!-- カラム2: では、どうすればいいのか？（処方箋の提案） -->
      <section class="col-panel">
        <div class="panel-header success">
          <span class="panel-number">2</span>
          <span>では、どうすればいいのか？（処方箋）</span>
        </div>
        <div class="panel-body">
          <p style="font-size:11px; color:var(--dads-text-sub); margin-bottom:-4px;">
            ※「中間管理職を板挟み・丸投げにしない」ための3つのアプローチ案
          </p>

          <!-- 処方箋1 -->
          <div class="sub-card success">
            <div class="card-headline success">
              <span>処方箋 A: 変革の労力を正当に評価する</span>
            </div>
            <p>
              DX推進を既存業務の「上乗せの雑務」にせず、<strong>変革への挑戦や業務改善の取り組みそのものを人事評価や処遇に直結</strong>させます（「頑張っても報われない」不公平感の払拭）。
            </p>
          </div>

          <!-- 処方箋2 -->
          <div class="sub-card success">
            <div class="card-headline success">
              <span>処方箋 B: 「ミニ推進・調整役（PMO）」の設置</span>
            </div>
            <p>
              現場の課長一人に背負わせず、<strong>経営の方針を現場目線に翻訳し、現場の悩みを経営へ届ける「交通整理役」</strong>を小さくても社内に公式配置します（専任でなく兼任・若手抜擢でも有効）。
            </p>
          </div>

          <!-- 処方箋3 -->
          <div class="sub-card success">
            <div class="card-headline success">
              <span>処方箋 C: 決定プロセスの透明化と納得感</span>
            </div>
            <p>
              トップダウンの号令だけでなく、「なぜ導入するのか」「現場の声がどう反映されたか」を丁寧に共有することで、<strong>現場の抵抗感が前向きな協力意向へ転換</strong>することが実証されています。
            </p>
          </div>
        </div>
      </section>

      <!-- カラム3: 限界と今後の課題・皆様との討議 -->
      <section class="col-panel">
        <div class="panel-header secondary">
          <span class="panel-number">3</span>
          <span>現在の限界と今後の課題（意見交換の論点）</span>
        </div>
        <div class="panel-body">
          <!-- 限界と課題 -->
          <div class="sub-card secondary">
            <div class="card-headline secondary">
              <span>現時点における研究の限界</span>
            </div>
            <p style="margin-bottom: 4px;">
              <strong>① 因果の前後関係:</strong> 一時点の調査データであるため、「意識が低いからDXが進まないのか」「進まないから意識が低下したのか」の時系列追跡が今後の課題です。
            </p>
            <p>
              <strong>② 業種・業態の差:</strong> SMOの中でも製造・IT・サービス・伝統産業など業種による固有パターンの詳細な類型化が求められます。
            </p>
          </div>

          <!-- ディスカッション起爆ボックス -->
          <div class="discussion-trigger-box">
            <div class="discussion-title">
              <span>💬 本日の意見交換テーマ（皆様へのお伺い）</span>
            </div>
            <div class="discussion-item">
              <strong>問い 1:</strong> 「皆様のご専門や現場の知見から見て、SMOの中間管理職が『孤立のサンドバッグ』にならず、自発的に動き出すために最も効果的な後押しは何だとお考えでしょうか？」
            </div>
            <div class="discussion-item">
              <strong>問い 2:</strong> 「リソースに余裕がない中堅・中小企業において、経営と現場のハブとなる『推進・調整役（ミニPMO）』を現実的にどう生み出すべきでしょうか？（兼任、外部伴走、若手抜擢など）」
            </div>
          </div>
        </div>
      </section>

    </main>

    <!-- フッター -->
    <footer class="slide-footer">
      <div class="footer-left">
        <span>※ 本報告は学術的な多重統計分析に基づき、結論の頑健性を確認した上で要点を平易に再構成したものです。</span>
        <span class="footer-note">（統計的詳細：規模×階層の交互作用効果、統制変数投入後も有意性を維持）</span>
      </div>
      <div class="footer-right">
        <span>IDM研究会 中間発表資料 (1枚完結版)</span>
      </div>
    </footer>

  </div>

  <script>
    // 全画面表示トグル (Fキー対応)
    function toggleFullscreen() {
      const container = document.getElementById('slide-container');
      if (!document.fullscreenElement) {
        if (container.requestFullscreen) {
          container.requestFullscreen();
        } else if (container.webkitRequestFullscreen) {
          container.webkitRequestFullscreen();
        }
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    }

    document.addEventListener('keydown', function(e) {
      if (e.key === 'f' || e.key === 'F') {
        toggleFullscreen();
      }
    });
  </script>
</body>
</html>
"""

def main():
    base_dir = r"G:\マイドライブ\antigravity\IDM\20261030\reports"
    os.makedirs(base_dir, exist_ok=True)
    out_html = os.path.join(base_dir, "20261030_SMO研究会中間発表_A4横長1枚スライド.html")

    with open(out_html, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    print(f"Generated HTML slide: {out_html}")

if __name__ == "__main__":
    main()
