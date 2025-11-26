import pandas as pd

base_df = pd.read_csv("mount_2024.csv")
add_df = pd.read_csv("Price_ATC_S.csv")

# 去除欄位名稱前後空格，處理 BOM
base_df.rename(columns=lambda x: x.strip().replace("\ufeff", ""), inplace=True)
add_df.rename(columns=lambda x: x.strip().replace("\ufeff", ""), inplace=True)

# 找出共同欄位
common_cols = set(base_df.columns) & set(add_df.columns)
print("共同欄位：", common_cols)

if not common_cols:
    raise ValueError("兩個檔案沒有共同欄位，請確認欄位名稱一致")

# 取第一個共同欄位來合併（通常就是藥品代碼）
key_col = list(common_cols)[0]

merged_df = pd.merge(
    base_df,
    add_df.drop(columns=[key_col], errors="ignore"),
    on=key_col,
    how="left"
)

merged_df.to_csv("merged_output.csv", index=False, encoding="utf-8")
print("✅ 合併完成，共", len(merged_df), "筆資料")
