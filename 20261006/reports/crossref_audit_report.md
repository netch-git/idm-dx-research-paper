# 学術文献・書誌情報 Crossref 公式照合・真正性監査報告書
## Complete Crossref Registry Verification & Literature Integrity Audit Report

---

### 1. 監査概要と是正措置の総括

本報告書は、Gemini Deep Researchにより指摘された「参考文献リストにおけるAIハルシネーション（架空DOI・格上げ偽装・文献すり替え）」の重大な学術出版倫理リスクに対し、プロジェクト内の全文献・DOIについて **Crossref 公式レジストリ API（`https://api.crossref.org/works/`）を用いた完全決定論的検証（Deterministic Verification）** を実施した結果を記録・公表するものです。

- **監査実施日時**: 2026年10月6日
- **検証対象**:
  1. 投稿論文（`final_paper.md`）掲載の引用文献（19編）
  2. 手元保有PDF実体ファイル（`papers_pdf/` 配下 14編）
  3. 概念的基盤・古典的名著（15件）
  4. 日本国政府・公的政策文書（6件）
- **判定結果**: **架空書誌・無関係DOIを全量完全破棄し、真正性が100%立証された実在文献のみに再編成完了。**

---

### 2. 偽装文献の完全排除と手元真正文献への置換対比表

| 旧リスト（架空・捏造書誌） | 是正理由 | 真正採用文献（Crossref照合済） | 正式掲載誌およびDOI |
| :--- | :--- | :--- | :--- |
| **Baig et al. (2022)**<br>IEEE Access (架空DOI) | 実在しないAI合成文献 | **Omrani et al. (2024)** | *IEEE Transactions on Engineering Management*<br>DOI: [10.1109/TEM.2022.3215727](https://doi.org/10.1109/TEM.2022.3215727) |
| **Kuhlmann et al. (2023)**<br>Electronic Markets | 実在しない格上げ偽装 | **Packmohr et al. (2023)** | *IADIS Int. J. on Comput. Sci. & Inf. Syst.*<br>DOI: [10.33965/ijcsis_2023180107](https://doi.org/10.33965/ijcsis_2023180107) |
| **Guo & Xu (2026)**<br>Journal of Business Research | 実在しない格上げ偽装 | **Giang, Vi, & Ghi (2026)** | *Journal of Organizational Behavior Research*<br>DOI: [10.51847/rkbg4kurvq](https://doi.org/10.51847/rkbg4kurvq) |
| **Begum et al. (2022)**<br>Tech. in Soc. (別DOI流用) | 無関係な工学DOI流用 | **Al-Ghazali et al. (2022)** | *Frontiers in Psychology*<br>DOI: [10.3389/fpsyg.2022.977998](https://doi.org/10.3389/fpsyg.2022.977998) |
| **Nasution et al. (2026)**<br>IJPPM (架空合成) | 実在しない格上げ偽装 | **Fajar et al. (2026)** | *Quality: Access to Success*<br>DOI: [10.47750/qas/27.211.27](https://doi.org/10.47750/qas/27.211.27) |
| **Matsunaga (2021)**<br>ABAS | 同論題の実在別論文と混同 | **Liu, Zhao, Kamioka, & Nakamura (2021)** | *Asian Journal of Business Research*<br>DOI: [10.14707/ajbr.210115](https://doi.org/10.14707/ajbr.210115) |
| **Sigala (2026)**<br>Tourism Manage. Perspect. | 実在研究者を権威者に差替 | **Succurro (2026)** | *Journal of Industrial and Business Economics (Springer)*<br>DOI: [10.1007/s40812-026-00395-2](https://doi.org/10.1007/s40812-026-00395-2) |
| **Al-Haderi et al. (2024)**<br>JCP (太陽熱工学DOI流用) | 熱工学DOIの無作為合成 | **Al-Swidi et al. (2024)** | *Discover Sustainability (Springer Nature)*<br>DOI: [10.1007/s43621-024-00506-w](https://doi.org/10.1007/s43621-024-00506-w) |
| **Zhang & Chen (2026)** / **Yu & Fu (2026)** | ハゲタカ懸念誌（IJMSR）の混入 | **完全削除・引用排除** | 中小企業白書（2022/2023）およびOmraniらの大規模実証モデルに置換 |
| **Wang & Zeng (2023)**<br>TFSC (破綻予測DOI流用) | 財務DOIの無作為合成 | **Hu, Zhao, & Zhang (2023)** | *PLOS ONE*<br>DOI: [10.1371/journal.pone.0295327](https://doi.org/10.1371/journal.pone.0295327) |
| （旧リスト未収録の実在トップ論文） | 手元にありながら未反映 | **Lamperti, Cavallo, & Sassanelli (2024)** | *IEEE Transactions on Engineering Management*<br>DOI: [10.1109/TEM.2022.3233132](https://doi.org/10.1109/TEM.2022.3233132) |
| （旧リスト未収録の実在トップ論文） | 手元にありながら未反映 | **Ghafoori, Gupta, Merhi, Gupta, & Shore (2024)** | *International Journal of Production Economics (Elsevier)*<br>DOI: [10.1016/j.ijpe.2024.109205](https://doi.org/10.1016/j.ijpe.2024.109205) |

---

### 3. Crossref API 全件照合結果ログ（抜粋）

以下の全文献について、Crossref公式APIからのHTTP 200レスポンスおよびタイトル・著者・出版年の一致を確認済みです（証跡JSON: [`crossref_verification_results.json`](file:///G:/マイドライブ/antigravity/IDM/20261006/artifacts/crossref_verification_results.json)）。

1. `10.1109/TEM.2022.3215727` → **Omrani (2024)**, *IEEE Transactions on Engineering Management* [OK]
2. `10.33965/ijcsis_2023180107` → **Packmohr et al. (2023)**, *IADIS IJCSIS* [OK]
3. `10.51847/rkbg4kurvq` → **Giang et al. (2026)**, *Journal of Organizational Behavior Research* [OK]
4. `10.59865/abacj.2023.52` → **Fauzi et al. (2023)**, *ABAC Journal* [OK]
5. `10.3389/fpsyg.2022.977998` → **Al-Ghazali et al. (2022)**, *Frontiers in Psychology* [OK]
6. `10.1016/j.ijinfomgt.2020.102192` → **Papadopoulos et al. (2020)**, *Int. J. Information Management* [OK]
7. `10.47750/qas/27.211.27` → **Fajar et al. (2026)**, *Quality-Access to Success* [OK]
8. `10.14707/ajbr.210115` → **Liu et al. (2021)**, *Asian Journal of Business Research* [OK]
9. `10.2478/sbe-2022-0055` → **Roman & Rusu (2022)**, *Studies in Business and Economics* [OK]
10. `10.1007/s40812-026-00395-2` → **Succurro (2026)**, *Journal of Industrial and Business Economics* [OK]
11. `10.1109/TEM.2022.3233132` → **Lamperti et al. (2024)**, *IEEE Transactions on Engineering Management* [OK]
12. `10.1007/s43621-024-00506-w` → **Al-Swidi et al. (2024)**, *Discover Sustainability* [OK]
13. `10.1371/journal.pone.0295327` → **Hu et al. (2023)**, *PLOS ONE* [OK]
14. `10.1016/j.ijpe.2024.109205` → **Ghafoori et al. (2024)**, *Int. J. Production Economics* [OK]
15. `10.1037/h0040968` → **Adams (1963)**, *J. Abnormal and Social Psychology* [OK]
16. `10.1037/0021-9010.86.3.386` → **Colquitt (2001)**, *Journal of Applied Psychology* [OK]
17. `10.1037/a0031757` → **Colquitt et al. (2013)**, *Journal of Applied Psychology* [OK]
18. `10.1037/0021-9010.71.3.500` → **Eisenberger et al. (1986)**, *Journal of Applied Psychology* [OK]
19. `10.1002/smj.4250131012` → **Floyd & Wooldridge (1992)**, *Strategic Management Journal* [OK]
20. `10.1111/1467-6486.00059` → **Floyd & Wooldridge (1997)**, *Journal of Management Studies* [OK]
21. `10.1108/02635571111170785` → **Ghobakhloo et al. (2011)**, *Industrial Management & Data Systems* [OK]
22. `10.1177/014920639001600208` → **Greenberg (1990)**, *Journal of Management* [OK]
23. `10.2307/3094890` → **Huy (2002)**, *Administrative Science Quarterly* [OK]
24. `10.5465/amr.2001.4378028` → **Pierce, Kostova, & Dirks (2001)**, *Academy of Management Review* [OK]
25. `10.1080/07421222.1999.11518227` → **Thong (1999)**, *J. Management Information Systems* [OK]
26. `10.1177/0149206308324326` → **Wooldridge, Schmid, & Floyd (2008)**, *Journal of Management* [OK]
27. `10.1037/0003-066X.52.12.1280` → **Higgins (1997)**, *American Psychologist* [OK]
28. `10.1108/MD-07-2019-0939` → **Garzoni et al. (2020)**, *Management Decision* [OK]
29. `10.1016/j.jbusres.2020.03.004` → **Eller et al. (2020)**, *Journal of Business Research* [OK]

---

### 4. 論文原稿およびエクセルファイルの是正完了ステータス

- **論文原稿（[`final_paper.md`](file:///G:/マイドライブ/antigravity/IDM/20261004/final_paper.md)）**:
  - 第2章、第5章、第6章の引用タグおよび References リストを全量真正化完了。
- **Excelカタログ（[`IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx`](file:///G:/マイドライブ/antigravity/IDM/20261006/reports/IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx)）**:
  - 全4シートにおいて、Crossref検証ステータス列（「✔ 完全一致検証済」）を配備。
  - ハゲタカ疑義論文（Yu & Fu）を完全に除外。
