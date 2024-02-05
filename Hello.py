import streamlit as st
import pandas as pd
import openpyxl as xl
import matplotlib.pyplot as plt
import plotly.express as px 
from PIL import Image
from streamlit_option_menu import option_menu
from datetime import datetime

st.set_page_config(page_title='KHO VPIC1',layout="wide")
# Báo cáo số vị trí các mã  

st.subheader("Chọn file Excel Tồn kho ERP")
uploaded_file_tonkhoerp = st.file_uploader("Chọn file: ", type=["xlsx", "xls"], key="tonkhoerp")


if uploaded_file_tonkhoerp is not None:
        # Đọc dữ liệu từ file Excel
    df_tonkhoerp = pd.read_excel(uploaded_file_tonkhoerp,
                            engine="openpyxl",
                            usecols='A:P',
                            header=0)
    selected_tonkhoerp_columns = ['Mã SP', 'Kho', 'SL tồn kho']
    df_tonkhoerp_selected_columns = df_tonkhoerp[selected_tonkhoerp_columns]
    df_tonkhoerp_selected_columns['Kho'] = df_tonkhoerp_selected_columns['Kho'].str.strip()




st.subheader("Chọn file Excel Tồn theo kho WMS")
uploaded_file_tonkhowms = st.file_uploader("Chọn file: ", type=["xlsx", "xls"], key="tonkhowms")

if uploaded_file_tonkhowms is not None:
        # Đọc dữ liệu từ file Excel
    df_tonkhowms = pd.read_excel(uploaded_file_tonkhowms,
                            engine="openpyxl",
                            usecols='A:FJ',
                            header=10)
    df_tonkhowms_unpivoted = pd.melt(df_tonkhowms, id_vars=['Mã vật tư ERP', 'Mã vật tư', 'Tên vật tư', 'Quy cách quản lý'],
                                  var_name='Mã Kho', value_name='Giá trị')

# Loại bỏ các dòng có giá trị 0.000
    df_tonkhowms_unpivoted = df_tonkhowms_unpivoted[df_tonkhowms_unpivoted['Giá trị'] != 0.000]
    df_tonkhowms_cleaned = df_tonkhowms_unpivoted.dropna(subset=['Mã vật tư ERP'])

# Chọn các cột cần hiển thị
    selected_tonkhowms_columns = ['Mã vật tư ERP', 'Tên vật tư', 'Quy cách quản lý', 'Mã Kho', 'Giá trị']

# Tạo DataFrame mới chỉ chứa các cột được chọn
    df_tonkhowms_selected_columns = df_tonkhowms_cleaned[selected_tonkhowms_columns]
    df_tonkhowms_selected_columns['Mã Kho'] = df_tonkhowms_selected_columns['Mã Kho'].str.strip()

# Merge hai DataFrame dựa trên cột 'Mã vật tư ERP' và 'Kho'

    merged_df = pd.merge(df_tonkhoerp_selected_columns, df_tonkhowms_selected_columns,
                     left_on=['Mã SP', 'Kho'], right_on=['Mã vật tư ERP', 'Mã Kho'],
                     how='outer', suffixes=('_tonkhoerp', '_tonkhowms'))

# Tạo cột chênh lệch
    merged_df = merged_df.fillna(0)
    merged_df['Chênh lệch'] = merged_df['Giá trị'] - merged_df['SL tồn kho']
    filtered_df = merged_df[(merged_df['Chênh lệch'] != 0)
                        & (merged_df['Kho'] != 'Tất:')
                        & (merged_df['Kho'] != 'TS:')]


    df_Khodachay = pd.read_excel(io="data/KHO CHẠY WMS.xlsx",
                             engine="openpyxl",
                             sheet_name="Data",
                             usecols='A:D',
                             header=0)
    df_Khodachay['Mã kho'] = df_Khodachay['Mã kho'].str.strip()

    df_Khodachay = df_Khodachay.dropna(subset=['WMS'])

    merged_df_final = pd.merge(filtered_df, df_Khodachay,
                     left_on=['Kho'], right_on=['Mã kho'],
                     how='outer', suffixes=('_tonkhoerp', '_Khodachay'))

    merged_df_final = merged_df_final.dropna(subset=['Mã kho', 'Mã SP'])
    total_somalecherp = int(merged_df_final["Mã SP"].count())

    st.subheader("Đối chiếu tồn kho chiều ERP -> WMS"+ " Lệch "+ " " + (str(total_somalecherp)) + " " + "mã")
    st.dataframe(merged_df_final)

# Đối chiếu tồn kho WMS - ERP

    merged_WMS_df = pd.merge(df_tonkhowms_selected_columns,df_tonkhoerp_selected_columns,
                     left_on=['Mã vật tư ERP', 'Mã Kho'], right_on=['Mã SP', 'Kho'],
                     how='outer', suffixes=('_tonkhowms', '_tonkhoerp'))
    merged_WMS_df = merged_WMS_df.fillna(0)
    merged_WMS_df['Chênh lệch'] = merged_WMS_df['SL tồn kho'] - merged_WMS_df['Giá trị']
    filtered_WMS_df = merged_WMS_df[(merged_WMS_df['Chênh lệch'] != 0)
                        & (merged_WMS_df['Kho'] != 'Tất:')
                        & (merged_WMS_df['Kho'] != 'TS:')]

    merged_WMS_df_final = pd.merge(filtered_WMS_df, df_Khodachay,
                     left_on=['Mã Kho'], right_on=['Mã kho'],
                     how='outer', suffixes=('_tonkhowms', '_Khodachay'))

    merged_WMS_df_final = merged_WMS_df_final.dropna(subset=['Mã kho', 'Mã SP'])
    total_somalechwms = int(merged_WMS_df_final["Mã vật tư ERP"].count())

    st.subheader("Đối chiếu tồn kho chiều WMS -> ERP"+ " Lệch "+ " " + (str(total_somalechwms)) + " " + "mã")

    st.dataframe(merged_WMS_df_final)
