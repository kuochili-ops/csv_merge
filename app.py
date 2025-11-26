import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV 合併工具", layout="centered")
st.title("📊 CSV 合併工具")

# 上傳檔案
uploaded_base = st.file_uploader("請上傳主檔案 (mount_2024.csv)", type="csv")
uploaded_add = st.file_uploader("請上傳要合併的檔案 (Price_ATC_S.csv)", type="csv")

if uploaded_base and uploaded_add:
    try:
        # 讀取 CSV
        base_df = pd.read_csv(uploaded_base)
        add_df = pd.read_csv(uploaded_add)

        # 清理欄位名稱
        def clean_columns(df):
            df.columns = [col.strip().replace("\ufeff", "").replace("\r", "").replace("\n", "") for col in df.columns]
            return df

        base_df = clean_columns(base_df)
        add_df = clean_columns(add_df)

        # 顯示欄位
        st.subheader("📑 主檔案欄位")
        st.write(base_df.columns.tolist())
        st.subheader("📑 合併檔案欄位")
        st.write(add_df.columns.tolist())

        # 偵測共同欄位
        common_cols = list(set(base_df.columns) & set(add_df.columns))
        if not common_cols:
            st.error("❌ 找不到共同欄位，請確認兩個檔案是否有相同的欄位名稱")
        else:
            # 預設選 drugid
            key_col = st.selectbox("請選擇要合併的共同欄位", options=common_cols, index=common_cols.index("drugid") if "drugid" in common_cols else 0)

            if st.button("合併檔案"):
                merged_df = pd.merge(
                    base_df,
                    add_df.drop(columns=[key_col], errors="ignore"),
                    on=key_col,
                    how="left"
                )
                st.success(f"✅ 合併成功，共 {len(merged_df)} 筆資料")
                st.dataframe(merged_df.head(20))

                # 提供下載
                csv_utf8 = merged_df.to_csv(index=False, encoding="utf-8")
                st.download_button(
                    label="📥 下載合併後的 CSV (UTF-8)",
                    data=csv_utf8,
                    file_name="merged_output.csv",
                    mime="text/csv"
                )
    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
