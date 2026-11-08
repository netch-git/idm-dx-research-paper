---
name: html-math-rendering
description: >-
  Enforces flawless rendering of mathematical formulas, Greek characters, and statistical notations in HTML files.
  Prevents raw LaTeX ($...$) code leakage in browsers, enforces clean Unicode/HTML entities for inline statistics,
  and provides automated verification scripts and KaTeX integration guidelines.
---

# HTML Math & Statistical Notation Rendering Skill

## 1. 目的と適用場面
本スキルは、HTMLドキュメント（Webレポート、研究論文HTML、教材、スライド等）を生成・編集する際に、**LaTeX記法の生コード（例: `$\alpha \ge 0.70$`, `$\chi^2$`, `$N = 2,035$`）がブラウザ上にそのまま文字列として露出する表示バグを恒久的に防止・根絶**するための運用基準と自動検証手順です。

---

## 2. 表示崩れの根本原因
1. **Markdown/LaTeX思考の無意識な流出**:
   AIモデルが推論やドキュメント生成を行う際、数式表記として標準的な LaTeX 構文（`$...$`, `\(...\)`, `\alpha`, `\ge`）をそのまま HTML のテキストノード内に出力してしまう。
2. **ブラウザにおける未展開レンダリング**:
   HTMLファイル自体に KaTeX や MathJax などの JavaScript レンダリングエンジンが読み込まれていない場合、ブラウザはドルマーク `$` やバックスラッシュ `\` を通常の文字としてそのまま描画するため、ユーザーには「`Cronbach's $\alpha \ge 0.70$`」と見えてしまう。

---

## 3. レンダリング二重運用プロトコル

### プロトコル A: インライン統計量・記号（最も推奨・完全オフライン対応）
通常の本文中、見出し、表（テーブル）内の統計量・記号は、**LaTeX記法（`$...$`）を一切使わず、直接Unicode文字またはHTMLタグ**で記述する。

#### 完全対応テーブル（LaTeX → Unicode / HTML）
| 対象記号 / 概念 | ❌ 誤り（生LaTeX混入） | ⭕ 正しい表記（Unicode/HTML） | 備考 |
| :--- | :--- | :--- | :--- |
| **信頼性係数 α** | `$\alpha$` / `\alpha` | **`α`** | ギリシャ文字小文字 |
| **回帰係数 β** | `$\beta$` / `\beta` | **`β`** | ギリシャ文字小文字 |
| **効果量 η²** | `$\eta^2$` / `\eta^2` | **`η²`** または `η<sup>2</sup>` | 上付き数字 |
| **カイ二乗 χ²** | `$\chi^2$` / `\chi^2` | **`χ²`** または `χ<sup>2</sup>` | ギリシャ文字＋上付き |
| **母平均 μ / 標準偏差 σ** | `$\mu$`, `$\sigma$` | **`μ`**, **`σ`** | Unicode直接 |
| **以上（不等号）** | `$\ge$` / `\ge` / `>=` | **`≥`** または `&ge;` | 数学記号 |
| **以下（不等号）** | `$\le$` / `\le` / `<=` | **`≤`** または `&le;` | 数学記号 |
| **不一致（ノットイコール）** | `$\ne$` / `\ne` / `!=` | **`≠`** または `&ne;` | 数学記号 |
| **プラスマイナス** | `$\pm$` / `\pm` | **`±`** または `&plusmn;` | 数学記号 |
| **サンプルサイズ** | `$N = 2,035$` | **`N = 2,035`** | ドルマーク不要 |
| **有意確率** | `$p < 0.05$` | **`p < 0.05`** | ドルマーク不要 |
| **相関係数** | `$r = 0.45$` | **`r = 0.45`** | ドルマーク不要 |
| **決定係数** | `$R^2$`, `$\Delta R^2$` | **`R²`**, **`ΔR²`** | ギリシャ大文字＋上付き |
| **効果量** | `Cohen's $d$`, `Cramer's $V$` | **`Cohen's d`**, **`Cramer's V`** | 英字斜体または立体 |

---

### プロトコル B: 複数行の複雑な数式ブロック（Display Math）
分散分析モデル式、回帰方程式、構造方程式モデルなど、分数（`\frac`）や総和記号（`\sum`）を含む本格的な数式を表示する場合は、以下のいずれかを採用する。

#### 方法 1: KaTeX 自動レンダラーの組み込み（Web配信・リッチ表示）
HTMLの `<head>` に KaTeX を読み込み、`renderMathInElement` を実行する。
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {
    delimiters: [
      {left: '$$', right: '$$', display: true},
      {left: '\\(', right: '\\)', display: false}
    ],
    throwOnError: false
  });"></script>
```

#### 方法 2: セマンティックな HTML / CSS スタイリング（完全オフライン・最軽量）
```html
<div class="formula-box">
  <em>Y</em><sub>ijk</sub> = <em>μ</em> + <em>α</em><sub>i</sub>(Hierarchy) + <em>β</em><sub>j</sub>(Scale) + (<em>αβ</em>)<sub>ij</sub> + <em>ε</em><sub>ijk</sub>
</div>
```

---

## 4. 自動検証スクリプト（検証の決定論的自動化）

HTMLファイルを新規作成または編集した後は、必ず付属の自動検証スクリプトを実行し、未置換のLaTeX生コード（`$...$`）が残存していないかを機械的に検証する。

### 実行コマンド例
```powershell
python .agents/skills/html-math-rendering/scripts/verify_html_rendering.py <対象HTMLファイルパス>
```

- **正常判定**: 検出件数 0 件（SUCCESS）
- **エラー判定**: `$\alpha$` 等の該当行番号・マッチ文字列・修正推奨候補を出力（FAIL）
