import pandas as pd

# 先讀取 CSV
base_df = pd.read_csv("mount_2024.csv")
add_df = pd.read_csv("Price_ATC_S.csv")

# 再檢查欄位
print("mount_2024.csv 欄位：", base_df.columns.tolist())
print("Price_ATC_S.csv 欄位：", add_df.columns.tolist())

# 如果要改欄位名稱
base_df.rename(columns={"藥品代碼": "drugid"}, inplace=True)
add_df.rename(columns={"藥品代碼": "drugid"}, inplace=True)

# 合併
merged_df = pd.merge(
    base_df,
    add_df.drop(columns=["drugid"], errors="ignore"),
    on="drugid",
    how="left"
)

print("✅ 合併完成，共", len(merged_df), "筆資料")
