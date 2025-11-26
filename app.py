import pandas as pd

# 讀取 CSV
base_df = pd.read_csv("mount_2024.csv")
add_df = pd.read_csv("Price_ATC_S.csv")

# 去除欄位名稱前後空格，避免 KeyError
base_df.rename(columns=lambda x: x.strip(), inplace=True)
add_df.rename(columns=lambda x: x.strip(), inplace=True)

# 合併，以 mount_2024.csv 為基準
merged_df = pd.merge(
    base_df,
    add_df.drop(columns=["藥品代碼"], errors="ignore"),  # 避免重複欄位
    on="藥品代碼",
    how="left"
)

# 輸出 UTF-8 格式
merged_df.to_csv("merged_output.csv", index=False, encoding="utf-8")
print("✅ 合併完成，共", len(merged_df), "筆資料")
