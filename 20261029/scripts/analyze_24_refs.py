#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDM Project - 確定引用文献（24編）とExcel・PDF詳細突合スクリプト
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CITATION_DIR = Path(r"G:\マイドライブ\antigravity\IDM\citation")
EXCEL_PATH = CITATION_DIR / "IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx"

# 確定論文で引用されている全24編のリスト
DRAFT_24_REFS = [
    {
        "key": "Adams (1965)",
        "author": "Adams, J. S.",
        "year": "1965",
        "title": "Inequity in social exchange",
        "source": "Advances in Experimental Social Psychology, Vol. 2, pp. 267–299",
        "doi": "https://doi.org/10.1016/S0065-2601(08)60108-2",
        "category": "組織公正理論（古典・名著）"
    },
    {
        "key": "Aiken & West (1991)",
        "author": "Aiken, L. S., & West, S. G.",
        "year": "1991",
        "title": "Multiple regression: Testing and interpreting interactions",
        "source": "Sage Publications",
        "doi": "",
        "category": "統計解析・調整効果（方法論標準）"
    },
    {
        "key": "Armenakis et al. (1993)",
        "author": "Armenakis, A. A., Harris, S. G., & Mossholder, K. W.",
        "year": "1993",
        "title": "Creating readiness for organizational change",
        "source": "Human Relations, 46(6), 681–703",
        "doi": "https://doi.org/10.1177/001872679304600601",
        "category": "組織変革レディネス論"
    },
    {
        "key": "Balogun & Johnson (2004)",
        "author": "Balogun, J., & Johnson, G.",
        "year": "2004",
        "title": "Organizational restructuring and middle manager sensemaking",
        "source": "Academy of Management Journal, 47(4), 523–549",
        "doi": "https://doi.org/10.2307/20159599",
        "category": "ミドルマネジメント・センスメイキング論"
    },
    {
        "key": "Besson & Rowe (2012)",
        "author": "Besson, P., & Rowe, F.",
        "year": "2012",
        "title": "Strategizing information systems-enabled organizational transformation: A transdisciplinary review and new agenda",
        "source": "The Journal of Strategic Information Systems, 21(2), 103–124",
        "doi": "https://doi.org/10.1016/j.jsis.2012.05.001",
        "category": "IS組織変革論（JSIS）"
    },
    {
        "key": "Colquitt (2001)",
        "author": "Colquitt, J. A.",
        "year": "2001",
        "title": "On the dimensionality of organizational justice: A construct validation of a measure",
        "source": "Journal of Applied Psychology, 86(3), 386–400",
        "doi": "https://doi.org/10.1037/0021-9010.86.3.386",
        "category": "組織公正4次元モデル（JAP・金字塔）"
    },
    {
        "key": "Dean et al. (1998)",
        "author": "Dean, J. W., Brandes, P., & Dharwadkar, R.",
        "year": "1998",
        "title": "Organizational cynicism",
        "source": "Academy of Management Review, 23(2), 341–352",
        "doi": "https://doi.org/10.5465/amr.1998.533230",
        "category": "組織的シニシズム論（AMR）"
    },
    {
        "key": "Festinger (1957)",
        "author": "Festinger, L.",
        "year": "1957",
        "title": "A theory of cognitive dissonance",
        "source": "Stanford University Press",
        "doi": "",
        "category": "認知心理学・認知的不協和理論（古典）"
    },
    {
        "key": "Folger (1977)",
        "author": "Folger, R.",
        "year": "1977",
        "title": "Distributive and procedural justice: Combined impact of voice and process outcome on satisfaction",
        "source": "Journal of Personality and Social Psychology, 35(2), 108–119",
        "doi": "https://doi.org/10.1037/0022-3514.35.2.108",
        "category": "手続的公正・発言権（Voice）理論（JPSP）"
    },
    {
        "key": "Greenberg (1990)",
        "author": "Greenberg, J.",
        "year": "1990",
        "title": "Organizational justice: Yesterday, today, and tomorrow",
        "source": "Journal of Management, 16(2), 399–432",
        "doi": "https://doi.org/10.1177/014920639001600208",
        "category": "組織公正理論レビュー（JOM）"
    },
    {
        "key": "Herscovitch & Meyer (2002)",
        "author": "Herscovitch, L., & Meyer, J. P.",
        "year": "2002",
        "title": "Commitment to organizational change: Extension of a three-component model",
        "source": "Journal of Applied Psychology, 87(3), 474–487",
        "doi": "https://doi.org/10.1037/0021-9010.87.3.474",
        "category": "組織変革コミットメント論（JAP）"
    },
    {
        "key": "Huy (2002)",
        "author": "Huy, Q. N.",
        "year": "2002",
        "title": "Emotional balancing of organizational continuity and radical change: The contribution of middle managers",
        "source": "Administrative Science Quarterly, 47(1), 31–69",
        "doi": "https://doi.org/10.2307/3094890",
        "category": "ミドルマネジメント感情バランシング論（ASQ）"
    },
    {
        "key": "IPA (2023)",
        "author": "情報処理推進機構 (IPA)",
        "year": "2023",
        "title": "DX白書2023：進む変革、進まぬ変革",
        "source": "独立行政法人情報処理推進機構",
        "doi": "",
        "category": "公的白書・日本企業DX実態調査"
    },
    {
        "key": "Kane et al. (2015)",
        "author": "Kane, G. C., Palmer, D., Phillips, A. N., Kiron, D., & Buckley, N.",
        "year": "2015",
        "title": "Strategy, not technology, drives digital transformation: Becoming a digitally mature enterprise",
        "source": "MIT Sloan Management Review and Deloitte University Press",
        "doi": "",
        "category": "DX戦略・組織文化論（MIT Sloan）"
    },
    {
        "key": "経済産業省 (2018)",
        "author": "経済産業省",
        "year": "2018",
        "title": "DXレポート：ITシステム「2025年の崖」克服とDXの本格的な展開",
        "source": "経済産業省",
        "doi": "",
        "category": "公的報告書・DX定義とレガシー課題"
    },
    {
        "key": "Kerzner (2018)",
        "author": "Kerzner, H.",
        "year": "2018",
        "title": "Project management best practices: Achieving global excellence (4th ed.)",
        "source": "John Wiley & Sons",
        "doi": "",
        "category": "プロジェクトマネジメント論"
    },
    {
        "key": "Leventhal (1980)",
        "author": "Leventhal, G. S.",
        "year": "1980",
        "title": "What should be done with equity theory? New approaches to the study of fairness in social relationships",
        "source": "Social exchange: Advances in theory and research (pp. 27–55). Plenum Press",
        "doi": "https://doi.org/10.1007/978-1-4613-3087-5_2",
        "category": "手続的公正の6基準理論"
    },
    {
        "key": "Nonaka & Takeuchi (1995)",
        "author": "Nonaka, I., & Takeuchi, H.",
        "year": "1995",
        "title": "The knowledge-creating company: How Japanese companies create the dynamics of innovation",
        "source": "Oxford University Press",
        "doi": "",
        "category": "知識創造企業・ミドルアップダウン論（古典）"
    },
    {
        "key": "Pfeffer & Salancik (1978)",
        "author": "Pfeffer, J., & Salancik, G. R.",
        "year": "1978",
        "title": "The external control of organizations: A resource dependence perspective",
        "source": "Harper & Row",
        "doi": "",
        "category": "資源依存理論（古典）"
    },
    {
        "key": "Rizzo et al. (1970)",
        "author": "Rizzo, J. R., House, R. J., & Lirtzman, S. I.",
        "year": "1970",
        "title": "Role conflict and ambiguity in complex organizations",
        "source": "Administrative Science Quarterly, 15(2), 150–163",
        "doi": "https://doi.org/10.2307/2391486",
        "category": "役割葛藤・役割曖昧性尺度（ASQ・古典）"
    },
    {
        "key": "Siemsen et al. (2010)",
        "author": "Siemsen, E., Roth, A., & Oliveira, P.",
        "year": "2010",
        "title": "Common method bias in regression models with linear, quadratic, and interaction effects",
        "source": "Organizational Research Methods, 13(3), 456–476",
        "doi": "https://doi.org/10.1177/1094428109351241",
        "category": "共通方法バイアス（CMB）と交互作用項の頑健性（ORM）"
    },
    {
        "key": "中小企業庁 (2022)",
        "author": "中小企業庁",
        "year": "2022",
        "title": "中小企業白書2022年版：新たな時代を切り拓く中小企業",
        "source": "中小企業庁",
        "doi": "",
        "category": "公的白書・日本の中小企業DX"
    },
    {
        "key": "Thibaut & Walker (1975)",
        "author": "Thibaut, J. W., & Walker, L.",
        "year": "1975",
        "title": "Procedural justice: A psychological analysis",
        "source": "L. Erlbaum Associates",
        "doi": "",
        "category": "手続的公正理論の創始（古典）"
    },
    {
        "key": "Vial (2019)",
        "author": "Vial, G.",
        "year": "2019",
        "title": "Understanding digital transformation: A review and a research agenda",
        "source": "The Journal of Strategic Information Systems, 28(2), 118–144",
        "doi": "https://doi.org/10.1016/j.jsis.2019.01.003",
        "category": "DX包括的枠組み・構造的抵抗論（JSIS・最高峰）"
    }
]

print(f"確定引用文献: {len(DRAFT_24_REFS)} 編の定義完了")
