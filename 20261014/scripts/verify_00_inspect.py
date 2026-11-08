import sys, pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
RAW = r"G:\マイドライブ\antigravity\IDM\data\data[企業規模-職制カラム追加].xlsx"
REF = r"G:\マイドライブ\antigravity\IDM\data\IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx"
df = pd.read_excel(RAW, sheet_name=0)
print("shape", df.shape)
for i, c in enumerate(df.columns):
    s = df[c]
    print(i, repr(c), s.dtype, "nuniq=", s.nunique(), "na=", s.isna().sum(), "ex=", list(s.dropna().unique()[:6]))
x = pd.ExcelFile(REF)
for s in x.sheet_names:
    d = pd.read_excel(x, s)
    print("== sheet", s, d.shape)
    print(list(d.columns))
