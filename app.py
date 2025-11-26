import pandas as pd

# 讀取 CSV
base_df = pd.read_csv("mount_2024.csv")
add_df = pd.read_csv("Price_ATC_S.csv")

# 清理欄位名稱，避免 BOM 或空格
def clean_columns(df):
    df.columns = [col.strip().replace("\ufeff", "") for col in df.columns]
    return df

base_df = clean_columns(base_df)
add_df = clean_columns(add_df)

# 確認欄位
print("mount_2024.csv 欄位：", base_df.columns.tolist())
print("Price_ATC_S.csv 欄位：", add_df.columns.tolist())

# 合併
merged_df = pd.merge(
    base_df,
    add_df.drop(columns=["drugid"], errors="ignore"),  # 避免重複欄位
    on="drugid",
    how="left"
)

# 輸出
merged_df.to_csv("merged_output.csv", index=False, encoding="utf-8")
print("✅ 合併完成，共", len(merged_df), "筆資料")
