import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV/TSV 合併工具", layout="centered")
st.title("📊 CSV/TSV 合併工具")

# 穩健讀取 CSV/TSV
def robust_read_csv(file):
    for sep in [None, "\t", ","]:
        for encoding in ["utf-8", "utf-8-sig", "big5", "cp950"]:
            try:
                df = pd.read_csv(file, sep=sep, engine="python", encoding=encoding)
                # 清理欄位名稱
                df.columns = [c.strip().replace("\ufeff", "").replace("\r", "").replace("\n", "") for c in df.columns]
                if len(df.columns) == 1:
                    continue
                # 如果第一列是檔名雜訊，略過
                if str(df.iloc[0, 0]).lower().endswith(".csv") and "drugid" not in df.columns:
                    df = df.iloc[1:].reset_index(drop=True)
                return df
            except Exception:
                continue
    raise ValueError("無法讀取檔案：請確認分隔符（逗號或Tab）與編碼是否正確")

# 上傳檔案
uploaded_base = st.file_uploader("請上傳主檔案 (mount_2024.csv / .tsv)", type=["csv","tsv"])
uploaded_add  = st.file_uploader("請上傳要合併的檔案 (Price_ATC_S.csv / .tsv)", type=["csv","tsv"])

if uploaded_base and uploaded_add:
    try:
        base_df = robust_read_csv(uploaded_base)
        add_df  = robust_read_csv(uploaded_add)

        st.subheader("📑 主檔案欄位")
        st.write(base_df.columns.tolist())
        st.subheader("📑 合併檔案欄位")
        st.write(add_df.columns.tolist())

        # 偵測共同欄位
        common_cols = list(set(base_df.columns) & set(add_df.columns))
        if not common_cols:
            st.error("❌ 找不到共同欄位，請確認兩個檔案是否有相同的欄位名稱")
            st.stop()

        # 預設選 drugid
        key_col = st.selectbox("請選擇要合併的主鍵", options=common_cols,
                               index=common_cols.index("drugid") if "drugid" in common_cols else 0)

        if st.button("合併檔案"):
            # 直接保留合併鍵，不刪除
            merged_df = pd.merge(
                base_df,
                add_df,
                on=key_col,
                how="left",
                suffixes=("", "_right")  # 避免重複欄位衝突
            )
            st.success(f"✅ 合併成功，共 {len(merged_df)} 筆資料")
            st.dataframe(merged_df.head(20))

            # 顯示缺失比對
            missing = base_df[~base_df[key_col].isin(add_df[key_col])]
            st.info(f"🔎 在附檔缺少的 {key_col} 數量：{len(missing)}")
            if len(missing) > 0:
                st.dataframe(missing[[key_col]].drop_duplicates().head(50))

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
