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

# 確認欄位
print("主檔案欄位：", base_df.columns.tolist())
print("合併檔案欄位：", add_df.columns.tolist())

# 合併，指定 key 為 drugid
if "drugid" in base_df.columns and "drugid" in add_df.columns:
    merged_df = pd.merge(
        base_df,
        add_df.drop(columns=["drugid"], errors="ignore"),
        on="drugid",
        how="left"
    )
    merged_df.to_csv("merged_output.csv", index=False, encoding="utf-8")
    print("✅ 合併完成，共", len(merged_df), "筆資料")
else:
    print("❌ 找不到欄位 'drugid'，請確認兩個檔案都有這個欄位")
