import pandas as pd

def merge_csv(base_file, add_file, output_file, key_col=None):
    """
    以 base_file 為基礎，將 add_file 中相同 key_col 的欄位整合進來
    並輸出成 UTF-8 格式的 CSV

    Parameters:
    base_file (str): 主檔案路徑 (例如 mount_2024.csv)
    add_file (str): 要合併的檔案路徑 (例如 Price_ATC_S.csv)
    output_file (str): 輸出檔案路徑 (例如 merged_output.csv)
    key_col (str): 合併的共同欄位名稱。如果為 None，會自動偵測交集欄位
    """

    # 讀取 CSV
    base_df = pd.read_csv(base_file)
    add_df = pd.read_csv(add_file)

    # 如果沒有指定 key_col，則自動偵測共同欄位
    if key_col is None:
        common_cols = list(set(base_df.columns) & set(add_df.columns))
        if not common_cols:
            raise ValueError("兩個檔案沒有共同欄位，請手動指定 key_col")
        key_col = common_cols[0]  # 預設取第一個共同欄位
        print(f"自動偵測共同欄位：{key_col}")

    # 合併
    merged_df = pd.merge(
        base_df,
        add_df.drop(columns=[key_col]),  # 避免重複 key_col
        left_on=key_col,
        right_on=key_col,
        how="left"   # 以 base_file 為主
    )

    # 輸出 UTF-8 格式
    merged_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"已生成 {output_file}，共 {len(merged_df)} 筆資料")

# 使用範例
merge_csv(
    base_file="mount_2024.csv",
    add_file="Price_ATC_S.csv",
    output_file="merged_output.csv",
    key_col="drug_code"   # 如果欄位名稱不同，改成實際的藥品代碼欄位
)
