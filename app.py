import pandas as pd

base_df = pd.read_csv("mount_2024.csv")
add_df = pd.read_csv("Price_ATC_S.csv")

# 去除欄位名稱前後空格，避免 KeyError
base_df.rename(columns=lambda x: x.strip(), inplace=True)
add_df.rename(columns=lambda x: x.strip(), inplace=True)

# 如果主檔案用的是「商品代碼」，合併檔案用的是「藥品代碼」，先統一名稱
base_df.rename(columns={"商品代碼": "藥品代碼"}, inplace=True)
add_df.rename(columns={"商品代碼": "藥品代碼"}, inplace=True)

# 合併
merged_df = pd.merge(
    base_df,
    add_df.drop(columns=["藥品代碼"], errors="ignore"),
    on="藥品代碼",
    how="left"
)

merged_df.to_csv("merged_output.csv", index=False, encoding="utf-8")
print("✅ 合併完成，共", len(merged_df), "筆資料")
