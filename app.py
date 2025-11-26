import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV 合併工具", layout="centered")
st.title("📊 CSV 合併工具")

# 上傳主檔案
uploaded_base = st.file_uploader("請上傳主檔案 (例如 mount_2024.csv)", type="csv", key="base")
# 上傳要合併的檔案
uploaded_add = st.file_uploader("請上傳要合併的檔案 (例如 Price_ATC_S.csv)", type="csv", key="add")

if uploaded_base and uploaded_add:
    try:
        base_df = pd.read_csv(uploaded_base)
        add_df = pd.read_csv(uploaded_add)

        # 顯示欄位清單
        st.subheader("📑 主檔案欄位")
        st.write(base_df.columns.tolist())
        st.subheader("📑 合併檔案欄位")
        st.write(add_df.columns.tolist())

        # 自動偵測共同欄位
        common_cols = list(set(base_df.columns) & set(add_df.columns))
        if not common_cols:
            st.error("❌ 找不到共同欄位，請確認兩個檔案是否有相同的欄位名稱")
        else:
            key_col = st.selectbox("請選擇要合併的共同欄位", options=common_cols)

            if st.button("合併檔案"):
                try:
                    # 避免重複 key_col 欄位
                    add_df_clean = add_df.drop(columns=[key_col], errors="ignore")

                    # 合併
                    merged_df = pd.merge(
                        base_df,
                        add_df_clean,
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
                    st.error(f"❌ 合併失敗：{e}")

    except Exception as e:
        st.error(f"❌ 檔案讀取失敗：{e}")
