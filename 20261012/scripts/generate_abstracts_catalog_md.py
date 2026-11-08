# -*- coding: utf-8 -*-
"""
Markdownカタログレポート生成スクリプト
"""
import json

with open(r'G:\マイドライブ\antigravity\IDM\20261012\artifacts\refs_master_complete.json', 'r', encoding='utf-8') as f:
    refs_db = json.load(f)

md_lines = [
    "# IDM-DX 投稿論文 全引用文献アブストラクト（要約和訳）データベースカタログ",
    "",
    "- **更新日**: 2026年10月12日",
    "- **対象Excel正本**: [`IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx`](file:///G:/マイドライブ/antigravity/IDM/data/IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx)",
    f"- **総登録文献数**: 全{len(refs_db)}編（完全決定論的マスター）",
    "- **格納先シート**: `【全引用文献】要約和訳DB`（タイトルのすぐ右隣に和訳を完備）",
    "",
    "---",
    "",
    "## 📂 Excel格納仕様と列構成",
    "",
    "| 列記号 | 列名 | 内容 | 備考 |",
    "| :---: | :--- | :--- | :--- |",
    "| **A** | 文献ID | `REF-01` 〜 `REF-48` | 一意キー |",
    "| **B** | 学術区分・カテゴリ | DX実証研究 / 組織公正 / 組織構造 / 公的白書 等 | 絞り込み用 |",
    "| **C** | 著者名 (Authors) | 正式著者名リスト | APA準拠 |",
    "| **D** | 発行年 | 出版・公表年 (1947〜2026) | |",
    "| **E** | **文献タイトル (Title)** | 正式論文・書籍・レポート題目 | 太字表示 |",
    "| **F** | **要約の和訳（日本語アブストラクト）** | 学術用語に忠実な高品質日本語要約 | **★タイトルのすぐ右隣** |",
    "| **G** | 要約原文（英語・原著アブストラクト） | 公式Abstract原文 | 比較参照用 |",
    "| **H** | 掲載ジャーナル名 / 出版元 | ジャーナル名、出版社、政府機関 | |",
    "| **I** | 巻号・ページ | Vol, Issue, pp. | |",
    "| **J** | DOI / 公式アクセスリンク | クリック可能なハイパーリンク | 一次情報直結 |",
    "| **K** | 本研究での引用箇所・理論的役割 | H1〜H5、序論、考察等の対応関係 | 研究連動 |",
    "| **L** | 手元保有状況・取得判定 | ローカルPDF、オープンアクセス、学認等 | 入手性 |",
    "",
    "---",
    "",
    "## 📚 全引用文献 アブストラクト和訳一覧（全48編）",
    ""
]

# カテゴリ別に出力
categories = {}
for r in refs_db:
    cat = r["category"]
    categories.setdefault(cat, []).append(r)

for cat, items in categories.items():
    md_lines.append(f"### ■ {cat}（{len(items)}編）\n")
    for item in items:
        md_lines.append(f"#### [{item['id']}] {item['title']}")
        md_lines.append(f"- **著者・年**: {item['author']} ({item['year']})")
        md_lines.append(f"- **掲載誌 / 出版元**: *{item['journal']}*, {item['vol_page']}")
        if item['doi']:
            md_lines.append(f"- **DOI / リンク**: [{item['doi']}]({item['doi']})")
        md_lines.append(f"- **本論文での役割**: {item['role']}")
        md_lines.append(f"- **手元保有状況**: {item['status']}")
        md_lines.append("")
        md_lines.append("> **【要約の和訳（日本語アブストラクト）】**  ")
        md_lines.append(f"> {item['abstract_ja']}")
        md_lines.append("")
        if item['abstract_en']:
            md_lines.append("<details><summary>英語原文アブストラクト (Abstract)</summary>")
            md_lines.append("")
            md_lines.append(f"{item['abstract_en']}")
            md_lines.append("</details>")
            md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

out_md_path = r'G:\マイドライブ\antigravity\IDM\20261012\reports\20261012_引用文献アブストラクト和訳データベースカタログ.md'
with open(out_md_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(md_lines))

print(f"Generated Markdown catalog: {out_md_path}")
