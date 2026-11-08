# IDM DX Research Paper: Deterministic Microdata Analysis of 2,035 Employees

[![GitHub Repository](https://img.shields.io/badge/GitHub-netch--git%2Fidm--dx--research--paper-blue?logo=github)](https://github.com/netch-git/idm-dx-research-paper)
[![Sample Size](https://img.shields.io/badge/Sample%20Size-N%20%3D%202%2C035-brightgreen)](https://github.com/netch-git/idm-dx-research-paper)
[![Methodology](https://img.shields.io/badge/Analysis-Type%20II%20ANOVA%20%7C%20k--means%20%7C%20Logit-orange)](https://github.com/netch-git/idm-dx-research-paper)

## 📌 研究プロジェクト概要
日本国内民間企業に勤務する就業者 $N = 2,035$ 名の網羅的実査マイクロデータ（欠損値なし・完全決定論的解析）に基づき、企業規模（中小企業 vs 大企業）と組織階層（経営層・管理職・一般社員）の二元配置によるDX推進意識、当事者意識、および組織摩擦の構造的乖離を計量心理学・組織行動論の観点から解明した学術論文執筆リポジトリです。

詳細な日次活動記録は [ACTIVITY_LOG.md](ACTIVITY_LOG.md) を参照してください。

---

## 🗂 ディレクトリ構成

- `20261004/`: 初動決定論的解析パイプライン、二元配置ANOVA、IMRaD初稿、敵対的査読、確定版第1稿、Figures 1〜3
- `20261005/`: 参考文献カタログExcel自動生成、統計処理完全理解ハンドブック
- `20261006/`: CrossRef DOI自動突合監査、提出用Word（.docx）生成、インタラクティブHTML論文
- `20261007/`: リッカート尺度設問全量インベントリ、尺度理解ハンドブック
- `20261008/`: N=2,035最終Parquet、コードブック、クラスタ散布データ、EDAレポート
- `20261009/`: 実体論文PDF自動収集、モバイル対応論文ビューア
- `20261010/`: ロジスティック回帰フォレストプロット、指導教員相談レジュメ
- `20261012/`: 引用文献マスター完全統合（refs_master_complete.json）、変数対照表
- `20261013/`: 改訂論文ドラフト（本文・スライド・実行計画）
- `20261014/`: 生データ完全再計算数値突合、学術論文ドラフト確定版_2
- `20261015/` - `20261016/`: 計量経済・組織心理学 統計辞典（Markdown / HTML）
- `20261028/`: Blau & Scott (1962) 組織構造論スキャン解剖、書籍インデックス
- `20261029/`: 全引用文献分析手法カタログ、口頭試問即答マニュアル、EPUB教科書
- `20261030/`: 全設問スライド分析、SMO研究会中間発表資料（A4横・要旨）
- `.agents/`: ガバナンス規程、推測捏造絶対禁止規程、スキル定義

---

## 🔬 主要な分析結果と数理防衛

1. **二元配置分散分析（Type II ANOVA）**:
   - 組織階層の主効果: $F(2, 2029) = 138.42, p < .001, \eta_p^2 = .120$
   - 企業規模の主効果: $F(1, 2029) = 18.91, p < .001, \eta_p^2 = .009$
   - 交互作用効果: $F(2, 2029) = 4.15, p = .016, \eta_p^2 = .004$
2. **客観的k-meansクラスタリング**:
   - 牽引層（Cluster 1, 42.5%）、摩擦層（Cluster 2, 26.7%）、抵抗層（Cluster 3, 30.8%）の3分類を同定。
3. **外科的感度分析**:
   - 項目重複2問を完全除外した3項目版でも、低分配群のオッズ比は $\text{OR} = 2.409 (p < .001)$ で完全維持。
4. **共通方法バイアス（CMB）完全論破**:
   - Siemsen et al. (2010) の減衰定理を適用し、単一情報源バイアスが交互作用項を過小評価することを示し、検出された交互作用の真実性を数理的に証明。

