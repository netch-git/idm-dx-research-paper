# -*- coding: utf-8 -*-
"""
Colabノートブックの全コードセルをローカル環境でシミュレーション実行し、
文法エラーや実行時エラーが存在しないかを完全検証するテストスクリプト
"""
import sys, os, json

sys.stdout.reconfigure(encoding="utf-8")
nb_path = r"G:\マイドライブ\antigravity\IDM\20261014\reports\IDM_DX_Academic_Analysis_Replication.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.show = lambda: None

global_env = {'display': print, 'plt': plt}

for idx, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        code_lines = cell["source"]
        # Colab用マジックコマンド（!pip 等）を除外
        executable_lines = [l for l in code_lines if not l.strip().startswith("!") and not "google.colab" in l and not "files.upload" in l]
        code_str = "".join(executable_lines)
        
        first_line = code_lines[0].strip() if code_lines else ""
        print(f"\n--- Running Cell {idx}: {first_line[:50]} ---")
        try:
            exec(code_str, global_env)
            print(f"Cell {idx} passed successfully.")
        except Exception as e:
            print(f"❌ Error in Cell {idx}: {e}")
            sys.exit(1)

print("\n🎉 ALL CODE CELLS IN THE NOTEBOOK EXECUTED WITHOUT ANY ERROR!")
