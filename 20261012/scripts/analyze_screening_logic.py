import pandas as pd
import numpy as np

path = r'G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx'
df = pd.read_excel(path, sheet_name='data', header=0)
q_labels = df.iloc[0]
df_data = df.iloc[1:].copy()

flag_col = 'SC_MAIN'
val_main = 2 # 本調査終了
val_sc = 1   # SC終了

print("==================================================")
print("STAGE 1: SC1 (業種) Dropout Analysis")
print("==================================================")
# SC2 is null for people who dropped at SC1
sc1_drop = df_data[df_data['SC2'].isna()]
print(f"Total dropped at SC1: {len(sc1_drop)}")
print("SC1 value distribution for those who dropped at SC1 vs those who proceeded:")
print("Dropped at SC1:")
print(sc1_drop['SC1'].value_counts())
print("Proceeded to SC2:")
print(df_data[df_data['SC2'].notna()]['SC1'].value_counts().sort_index())

print("\n==================================================")
print("STAGE 2: SC7 (役職) Dropout Analysis")
print("==================================================")
# SC8 is null but SC2 is not null
sc7_drop = df_data[df_data['SC2'].notna() & df_data['SC8'].isna()]
print(f"Total dropped at SC7: {len(sc7_drop)}")
print("SC7 value distribution for those dropped at SC7:")
print(sc7_drop['SC7'].value_counts())
print("SC7 distribution for those who proceeded to SC8:")
print(df_data[df_data['SC8'].notna()]['SC7'].value_counts().sort_index())

print("\n==================================================")
print("STAGE 3: SC17 (DX認知度) Dropout Analysis")
print("==================================================")
# SC18.1 is null but SC8 is not null
sc17_drop = df_data[df_data['SC8'].notna() & df_data['SC18.1'].isna()]
print(f"Total dropped at SC17: {len(sc17_drop)}")
print("SC17 value distribution for those dropped at SC17:")
print(sc17_drop['SC17'].value_counts())
print("SC17 distribution for those who proceeded to SC18:")
print(df_data[df_data['SC18.1'].notna()]['SC17'].value_counts().sort_index())

print("\n==================================================")
print("STAGE 4: SC18-SC20 Final Selection Analysis (N=4,222)")
print("==================================================")
df_stage4 = df_data[df_data['SC18.1'].notna()].copy()
print(f"Total reached SC18-SC20: {len(df_stage4)}")
print("Breakdown by SC_MAIN:")
print(df_stage4[flag_col].value_counts())

# Check SC19 (DX取組状況)
print("\nSC19 (DX取組状況) vs SC_MAIN:")
ct_sc19 = pd.crosstab(df_stage4['SC19'], df_stage4[flag_col], margins=True)
print(ct_sc19)

