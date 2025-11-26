import streamlit as st
import pandas as pd

st.title("CSV 合併工具")

# 上傳檔案
uploaded_base = st.file_uploader("請上傳主檔案 (mount_2024.csv)", type="csv")
uploaded_add = st.file_uploader("請上傳要合併的檔案 (Price_ATC_S.csv)", type="csv")

# 指定共同欄位
key_col = st.text_input("請輸入共同欄位名稱 (例如 drug_code)")

if uploaded_base and uploaded_add and key_col:
    try:
        # 讀取 CSV
        base_df = pd.read_csv(uploaded_base)
        add_df = pd.read_csv(uploaded_add)

        # 合併
        merged_df = pd.merge(
            base_df,
            add_df.drop(columns=[key_col], errors="ignore"),  # 避免重複欄位
            on=key_col,
            how="left"   # 以主檔為基準
        )

        st.success(f"合併完成，共 {len(merged_df)} 筆資料")

        # 顯示前幾筆
        st.dataframe(merged_df.head())

        # 提供下載
        csv_utf8 = merged_df.to_csv(index=False, encoding="utf-8")
        st.download_button(
            label="下載合併後的 CSV (UTF-8)",
            data=csv_utf8,
            file_name="merged_output.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"合併失敗：{e}")
