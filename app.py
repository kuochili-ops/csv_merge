import pandas as pd

def merge_csv(base_file, add_file, output_file):
    """
    以 base_file 為基礎，將 add_file 中相同藥品代碼的欄位整合進來
    並輸出成 UTF-8 格式的 CSV
    """
    # 讀取 CSV
    base_df = pd.read_csv(base_file)
    add_df = pd.read_csv(add_file)

    # 合併
    merged_df = pd.merge(
        base_df,
        add_df.drop(columns=["藥品代碼"], errors="ignore"),  # 避免重複欄位
        on="藥品代碼",
        how="left"   # 以 base_file 為主
    )

    # 輸出 UTF-8 格式
    merged_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"已生成 {output_file}，共 {len(merged_df)} 筆資料")

# 使用範例
merge_csv(
    base_file="mount_2024.csv",
    add_file="Price_ATC_S.csv",
    output_file="merged_output.csv"
)
