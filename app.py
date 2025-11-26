import streamlit as st
import pandas as pd

st.title("CSV 合併工具")

# 上傳檔案
mount_file = st.file_uploader("請上傳 mount_2024.csv", type="csv")
price_file = st.file_uploader("請上傳 Price_ATC_S.csv", type="csv")

if mount_file and price_file:
    # 讀取 CSV
    mount_df = pd.read_csv(mount_file, encoding="utf-8")
    price_df = pd.read_csv(price_file, encoding="utf-8")

    # 只保留需要的欄位
    mount_selected = mount_df[["藥品代碼", "含包裹支付的醫令量_合計"]]

    # 合併
    merged_df = pd.merge(price_df, mount_selected, on="藥品代碼", how="left")

    st.success("合併完成！以下是結果預覽：")
    st.dataframe(merged_df.head(20))

    # 提供下載
    csv = merged_df.to_csv(index=False, encoding="utf-8").encode("utf-8")
    st.download_button(
        label="下載合併後的 CSV",
        data=csv,
        file_name="merged_output.csv",
        mime="text/csv",
    )
