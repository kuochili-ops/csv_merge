import pandas as pd

base_df = pd.read_csv("mount_2024.csv")
add_df = pd.read_csv("Price_ATC_S.csv")

print("mount_2024.csv 欄位：", base_df.columns.tolist())
print("Price_ATC_S.csv 欄位：", add_df.columns.tolist())
print("共同欄位：", set(base_df.columns) & set(add_df.columns))
