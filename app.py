import pandas as pd

# 讀取 CSV
base_df = pd.read_csv("mount_2024.csv")
add_df = pd.read_csv("Price_ATC_S.csv")

# 清理欄位名稱：去除空格、BOM、換行符號
def clean_columns(df):
    df.columns = [col.strip().replace("\ufeff", "").replace("\r", "").replace("\n", "") for col in df.columns]
    return df

base_df = clean_columns(base_df)
add_df = clean_columns(add_df)

# 顯示欄位名稱
print("主檔案欄位：", base_df.columns.tolist())
print("合併檔案欄位：", add_df.columns.tolist())

# 自動偵測共同欄位
common_cols = list(set(base_df.columns) & set(add_df.columns))
print("共同欄位：", common_cols)

if not common_cols:
    raise ValueError("❌ 沒有共同欄位，請確認欄位名稱一致")

# 使用第一個交集欄位來合併
key_col = common_cols[0]

# 合併
merged_df = pd.merge(
    base_df,
    add_df.drop(columns=[key_col], errors="ignore"),
    on=key_col,
    how="left"
)

# 輸出
merged_df.to_csv("merged_output.csv", index=False, encoding="utf-8")
print("✅ 合併完成，共", len(merged_df), "筆資料")
