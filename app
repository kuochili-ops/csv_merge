import pandas as pd

# 讀取兩個 CSV 檔案 (UTF-8 編碼)
mount_df = pd.read_csv("mount_2024.csv", encoding="utf-8")
price_df = pd.read_csv("Price_ATC_S.csv", encoding="utf-8")

# 只保留 mount_2024.csv 中需要的欄位
mount_selected = mount_df[["藥品代碼", "含包裹支付的醫令量_合計"]]

# 依照「藥品代碼」合併
merged_df = pd.merge(price_df, mount_selected, on="藥品代碼", how="left")

# 輸出成新的 UTF-8 CSV 檔案
merged_df.to_csv("merged_output.csv", encoding="utf-8", index=False)

print("合併完成！檔案已輸出為 merged_output.csv")
