import streamlit as st
import pandas as pd

st.title("CSV 合併工具")

def load_csv(file):
    """嘗試多種編碼讀取 CSV"""
    encodings = ["utf-8", "utf-8-sig", "cp950", "big5", "latin1"]
    for enc in encodings:
        try:
            return pd.read_csv(file, encoding=enc), enc
        except Exception:
            continue
    st.error("無法讀取檔案，請確認檔案編碼格式")
    return None, None

# 上傳檔案
mount_file = st.file_uploader("請上傳 mount_2024.csv", type="csv")
price_file = st.file_uploader("請上傳 Price_ATC_S.csv", type="csv")

if mount_file and price_file:
    mount_df, mount_enc = load_csv(mount_file)
    price_df, price_enc = load_csv(price_file)

    if mount_df is not None and price_df is not None:
        st.write(f"✅ 成功讀取 mount_2024.csv (編碼: {mount_enc})")
        st.write(f"✅ 成功讀取 Price_ATC_S.csv (編碼: {price_enc})")

        # 只保留需要的欄位
        if "藥品代碼" in mount_df.columns and "含包裹支付的醫令量_合計" in mount_df.columns:
            mount_selected = mount_df[["藥品代碼", "含包裹支付的醫令量_合計"]]
        else:
            st.error("mount_2024.csv 缺少必要欄位")
            st.stop()

        # 合併
        merged_df = pd.merge(price_df, mount_selected, on="藥品代碼", how="left")

        st.success("合併完成！以下是結果預覽：")
        st.dataframe(merged_df.head(20))

        # 提供下載
        csv = merged_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            label="下載合併後的 CSV",
            data=csv,
            file_name="merged_output.csv",
            mime="text/csv",
        )
