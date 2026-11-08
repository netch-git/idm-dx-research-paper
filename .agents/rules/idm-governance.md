---
trigger: always_on
description: "IDM-DX Research Project governance rules for data analysis, presentation decks, and pedagogical artifacts"
---

# IDM-DX Project Governance Rules

## 1. Scope & Root Directory
- Root Path: `G:\マイドライブ\antigravity\IDM`
- Master Dataset: `G:\マイドライブ\IDM\data-cross.xlsx` ($N = 2,035$)

## 2. Statistical Analysis & Code Integrity
- Always maintain full-sample ($N = 2,035$) deterministic parsing.
- Fix all random seeds (`random_state=42`) for clustering and decomposition algorithms.
- Always report effect sizes ($\eta^2$, Cohen's $d$, Cramer's $V$) alongside $p$-values.

## 3. UI/UX, Design, & Slide Presentations
- Strictly adhere to Digital Agency Design System (DADS) color palettes:
  - Primary `#005BAC`, Accent Green `#228543`, Accent Red `#D32F2F`, Background `#FFFFFF`/`#F8F9FA`.
- Presentation slides must have high projector visibility:
  - Main text $\ge 22\text{px}$, headings $\ge 32\text{px}$.
  - Support keyboard shortcuts: Arrow keys, Space, and `F` for fullscreen toggle.
  - Native Chart.js charts with unified font `'Noto Sans JP', sans-serif`.
  - Self-contained offline assets (`assets/chart.umd.min.js`).
  - Prohibit pie/doughnut charts; prioritize horizontal bar charts for comparison and proportions to ensure cognitive clarity.


## 4. Documentation & Links
- Provide clickable Markdown links using `file:///G:/マイドライブ/...` with forward slashes.

## 5. HTML Document Math & Notation Rendering Governance
- Strictly prohibit raw LaTeX code (`$...$`, `\(...\)`) in generated HTML files when no renderer is active.
- Always use native Unicode characters or HTML tags for statistical notations in HTML:
  - Greek letters: `α`, `β`, `η`, `χ`, `μ`, `σ`
  - Operators: `≥`, `≤`, `≠`, `±`, `×`, `÷` (never `\ge`, `\le`)
  - Superscripts/Subscripts: `²`, `³`, `<sup>2</sup>`, `<sub>k</sub>`
  - Specific examples: `Cronbach's α ≥ 0.70`, `χ²`, `η²`, `N = 2,035`, `p < 0.05`, `Cohen's d`.
- For complex mathematical formula blocks, integrate KaTeX/MathJax properly or format with clean semantic HTML/CSS (`<div class="formula-box">`).

## 6. Critical Auditing of Hardcoded Values
- Prohibit blind reliance on hardcoded numbers, past scripts, or draft outputs.
- Maintain a critical stance ("existing numbers might be flawed") and strictly bind report texts to calculated runtime objects.
- Ensure 100% numerical consistency across tables, body texts, and summary callouts.

## 7. Interaction & Approvals in Japanese
- Always communicate with the user, report statuses, and seek approval/confirmation in clear, professional Japanese.

## 8. Academic Integrity & Zero-Fabrication Governance (学術的誠実性と捏造絶対禁止規程)
- **Zero-Assumption Protocol on Survey Methodology (調査手法の推測・無断補完の絶対禁止)**:
  - Strictly limit methodology, sampling, and data quality descriptions to what is explicitly stated in primary source documents (PDF text, verified dataset, official codebook).
  - Absolutely forbid fabricating or guessing procedures (e.g., Helsinki declaration, speeder response removal, straight-lining checks) without primary source evidence.
  - If standard peer-review items are missing from primary sources, do not make assumptions; explicitly notify the user: `※元資料に記載がありません。実態のご確認をお願いします`.
- **Zero-Fabrication on Citations & References (引用文献の捏造・架空生成の絶対禁止)**:
  - Never fabricate authors, journal titles, volume/issue numbers, or DOIs.
  - Only cite literature verified in the primary PDF, verified project master lists (20 confirmed papers), or verified via web search (Google Scholar / Crossref).
- **Prohibition of Literary / Colloquial Metaphors and Unnecessary Katakana Loanwords (文学的修辞・不要なカタカナ語の排除)**:
  - Exclude emotional or poetic expressions ("警鐘を鳴らす", "冷え込み", "沈殿").
  - Replace unnecessary loanwords with formal academic Japanese ("示唆", "根拠", "阻害要因", "処遇への還元").


