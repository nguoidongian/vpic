import streamlit as st
import pandas as pd
import openpyxl as xl
import matplotlib.pyplot as plt
import plotly.express as px 
from PIL import Image
from streamlit_option_menu import option_menu
from datetime import datetime
from pages.trangchu import trangchu

st.set_page_config(page_title='KHO VPIC1',layout="wide")
# Báo cáo số vị trí các mã  
st.subheader("Chọn file Excel WMS tồn lô vị trí")
uploaded_file_tonlovitri = st.file_uploader("Chọn file: ", type=["xlsx", "xls"])

if uploaded_file_tonlovitri is not None:
        # Đọc dữ liệu từ file Excel
    df_tonlovitri = pd.read_excel(uploaded_file_tonlovitri,
                            engine="openpyxl",
                            sheet_name="Data",
                            usecols='A:J',
                            header=10)

# Xóa các dòng có giá trị null trong cột 'Mã vị trí'
    df_tonlovitri_cleaned = df_tonlovitri.dropna(subset=['Mã vị trí'])

# Xóa các dòng có vị trí giống nhau
    df_tonlovitri_cleaned = df_tonlovitri_cleaned.drop_duplicates(subset=['Mã vật tư ERP', 'Mã kho ERP', 'Mã vị trí'])
    df_tonlovitri_count = df_tonlovitri_cleaned.groupby(['Mã vật tư ERP', 'Mã kho ERP'])['Mã vị trí'].count().reset_index()
    df_tonlovitri_count = df_tonlovitri_count.rename(columns={'Mã vị trí': 'Số vị trí'})
    df_tonlovitri_merged = pd.merge(df_tonlovitri_cleaned, df_tonlovitri_count, on=['Mã vật tư ERP', 'Mã kho ERP'], how='left')

    df_maNhieuViTri = df_tonlovitri_merged[df_tonlovitri_merged['Số vị trí'] >= 2]
    st.dataframe(df_maNhieuViTri)

# Báo cáo lech ton kho erp - wms  
   
