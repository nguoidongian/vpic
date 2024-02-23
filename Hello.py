import pandas as pd
import openpyxl as xl
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px 
from PIL import Image
from streamlit_option_menu import option_menu
from datetime import datetime
import numpy as np

st.set_page_config(page_title='KHO VPIC1',layout="wide")
# Báo cáo số vị trí các mã  
column1, column2, column3 = st.columns(3)
with column1:
    st.subheader("Chọn file Excel Tồn kho ERP ( Đối chiếu tồn kho ERP - WMS )")
    uploaded_file_tonkhoerp = st.file_uploader("Chọn file: ", type=["xlsx", "xls"], key="tonkhoerp")
with column2:
    st.subheader("Chọn file Excel Tồn theo kho WMS ( Đối chiếu tồn kho ERP - WMS )")
    uploaded_file_tonkhowms = st.file_uploader("Chọn file: ", type=["xlsx", "xls"], key="tonkhowms")
with column3:
    st.subheader("Lệch tồn các kho")



if uploaded_file_tonkhoerp is not None:
        # Đọc dữ liệu từ file Excel
    df_tonkhoerp = pd.read_excel(uploaded_file_tonkhoerp,
                            engine="openpyxl",
                            header=0)
    selected_tonkhoerp_columns = ['Mã SP', 'Kho', 'SL tồn kho']
    df_tonkhoerp_selected_columns = df_tonkhoerp[selected_tonkhoerp_columns]
    df_tonkhoerp_selected_columns['Kho'] = df_tonkhoerp_selected_columns['Kho'].str.strip()



if uploaded_file_tonkhowms is not None:
        # Đọc dữ liệu từ file Excel
    df_tonkhowms = pd.read_excel(uploaded_file_tonkhowms,
                            engine="openpyxl",
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


    df_Khodachay = pd.read_excel(io="data\KHO CHẠY WMS.xlsx",
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
    column3, column4 = st.columns(2)
    with column3:
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

    with column4:
        st.subheader("Đối chiếu tồn kho chiều WMS -> ERP"+ " Lệch "+ " " + (str(total_somalechwms)) + " " + "mã")
        st.dataframe(merged_WMS_df_final)
column5, column6 = st.columns(2)
with column5:
    st.subheader("Chọn file Excel WMS tồn lô vị trí ( Các mã có 2 vị trí trở lên )")
    uploaded_file_tonlovitri = st.file_uploader("Chọn file: ", type=["xlsx", "xls"], key="tonlovitri")


if uploaded_file_tonlovitri is not None:
        # Đọc dữ liệu từ file Excel
    df_tonlovitri = pd.read_excel(uploaded_file_tonlovitri,
                            engine="openpyxl",
                            header=10)

# Xóa các dòng có giá trị null trong cột 'Mã vị trí'
    df_tonlovitri_cleaned = df_tonlovitri.dropna(subset=['Mã vị trí'])

# Xóa các dòng có vị trí giống nhau
    df_tonlovitri_cleaned = df_tonlovitri_cleaned.drop_duplicates(subset=['Mã vật tư ERP', 'Mã kho ERP', 'Mã vị trí'])
    df_tonlovitri_count = df_tonlovitri_cleaned.groupby(['Mã vật tư ERP', 'Mã kho ERP'])['Mã vị trí'].count().reset_index()
    df_tonlovitri_count = df_tonlovitri_count.rename(columns={'Mã vị trí': 'Số vị trí'})
    df_tonlovitri_merged = pd.merge(df_tonlovitri_cleaned, df_tonlovitri_count, on=['Mã vật tư ERP', 'Mã kho ERP'], how='left')

    df_maNhieuViTri = df_tonlovitri_merged[df_tonlovitri_merged['Số vị trí'] >= 2]
    selected_columns_manhieuvitri = ['Mã vật tư ERP', 'Tên vật tư','Mã kho ERP', 'Quy cách quản lý','ĐVT','Mã vị trí','Tồn vị trí','Số vị trí']
    df_manhieuvitri_selected_columns = df_maNhieuViTri[selected_columns_manhieuvitri]

    
    with column6:
        st.subheader("Những mã có 2 vị trí trở lên")
        st.dataframe(df_manhieuvitri_selected_columns) 
st.subheader("Chọn file Excel Tồn kho tem thùng theo vị trí WMS ( Các mã lệch tem thùng )")
uploaded_file_tonkhotemthung = st.file_uploader("Chọn file: ", type=["xlsx", "xls"], key="tonkhotemthung")
if uploaded_file_tonkhotemthung is not None:
        # Đọc dữ liệu từ file Excel
    df_tonkhotemthung = pd.read_excel(uploaded_file_tonkhotemthung,
                            engine="openpyxl",
                            header=10)
    df_tonkhotemthung["Chênh lệch"] = (df_tonkhotemthung["Tồn vị trí"] - df_tonkhotemthung["SL theo ĐVT tồn kho"])
    df_tonkhotemthung = df_tonkhotemthung.fillna(0)
# Lọc dữ liệu

    filtered_df = df_tonkhotemthung[(df_tonkhotemthung["Tồn vị trí"] > 0) & (df_tonkhotemthung["Chênh lệch"] != 0) & df_tonkhotemthung["Mã vật tư ERP"] !=0]
    sotemlech = int(((df_tonkhotemthung["Tồn vị trí"] > 0) & (df_tonkhotemthung["Chênh lệch"] != 0) & (df_tonkhotemthung["Mã vật tư ERP"] !=0)).sum())



# Display the filtered DataFrame
    st.title("Số tem lệch:" + " " + (str(sotemlech)) + " " + "cái")

    makho_vitri = st.multiselect("Chọn loại kho", options=filtered_df['Mã kho ERP'].unique(),default=filtered_df['Mã kho ERP'].unique())
    df_tonkhotemthung_selection = df_tonkhotemthung.query("`Mã kho ERP` == @makho_vitri")
    filtered_df_tonkhotemthung = df_tonkhotemthung_selection[(df_tonkhotemthung_selection["Tồn vị trí"] > 0) & (df_tonkhotemthung_selection["Chênh lệch"] != 0) ]

 # Chọn các cột cần hiển thị
    selected_columns = ['Mã vật tư ERP', 'Mã kho ERP', 'Tồn vị trí','SL theo ĐVT tồn kho','Chênh lệch']

# Tạo DataFrame mới chỉ chứa các cột được chọn
    df_selected_columns = filtered_df_tonkhotemthung[selected_columns]
    st.write(df_selected_columns)


st.subheader("Chọn file Excel Tổng hợp nhập xuất tồn theo lô ( FiFo sai đúng )")
uploaded_file_fifo = st.file_uploader("Chọn file: ", type=["xlsx", "xls"], key="fifo")
if uploaded_file_fifo is not None:
        # Đọc dữ liệu từ file Excel
    df_fifo = pd.read_excel(uploaded_file_fifo,
                            engine="openpyxl",
                            header=12)


# Đảm bảo rằng cột 'Mã vật tư ERP' là một Series
    df_fifo['Mã vật tư ERP'] = df_fifo['Mã vật tư ERP'].astype(str)
    count_dem_ma_fifo = df_fifo["Mã vật tư ERP"].value_counts().count()


# Xóa các dòng có giá trị null trong cột 'Mã lô'
    df_fifo = df_fifo.dropna(subset=['Mã lô'])

# Đếm số lượng mã lô cho từng mã vật tư ERP
    ma_lo_count = df_fifo.groupby('Mã vật tư ERP')['Mã lô'].nunique().reset_index(name='Số lượng mã lô')
    df_fifo_merged = pd.merge(df_fifo, ma_lo_count, on='Mã vật tư ERP', how='left')

    df_fifo_merged = df_fifo_merged.sort_values(by=['Mã vật tư ERP', 'Mã lô'], ascending=True)

  # Tạo cột 'Kết quả' dựa trên điều kiện
    df_fifo_merged['Kết quả'] = (df_fifo_merged['Mã vật tư ERP'] == df_fifo_merged['Mã vật tư ERP'].shift(-1)) & \
                            (df_fifo_merged['Tồn cuối'] != 0) & \
                            (df_fifo_merged['Số lượng xuất'].shift(-1) != 0)
    df_fifo_merged['Kết quả'] = df_fifo_merged['Kết quả'].map({True: 'Sai', False: '0'})
  
    df_filtered = df_fifo_merged.loc[df_fifo_merged['Kết quả'] == 'Sai']
    df_filtered = df_filtered.sort_values(by=['Mã vật tư ERP', 'Mã lô'], ascending=True)
    df_fifo_merged_final = pd.merge(df_fifo, df_filtered, on='Mã vật tư ERP', how='left')
    df_fifo_merged_final_1 = pd.merge(df_fifo_merged, df_filtered, on='Mã vật tư ERP', how='left')

    df_fifo_selected_columns = ['STT_x', 'Mã lô_x', 'Mã vật tư ERP','Tên vật tư_x','Quy cách quản lý_x','Tồn đầu_x','Số lượng nhập_x','Số lượng xuất_x', 'Tồn cuối_x', 'Số lượng mã lô_x','Kết quả_x','Kết quả_y']
    df_fifo_selected_columns_final = df_fifo_merged_final_1[df_fifo_selected_columns]
    df_fifo_cleaned = df_fifo_selected_columns_final.dropna(subset=['Kết quả_y'])
    total_mavattufifo= int(df_fifo_cleaned["Mã vật tư ERP"].count())
    count_dem_ma_sai = df_fifo_cleaned["Mã vật tư ERP"].value_counts().count()
    
    def highlight_sai(s):
        return ['background-color: yellow' if val == 'Sai' else '' for val in s]

    df_fifo_cleaned.style.apply(highlight_sai, subset=['Kết quả_x'])
   
# Hiển thị DataFrame
    


    fig_pie = px.pie(
    names=["Số mã sai", "Số mã xuất nhập"],
    values=[count_dem_ma_sai, count_dem_ma_fifo],
    title="Biểu đồ hình tròn so sánh số lượng mã vật tư ERP sai và fifo",
    labels={"Sai": "Số lượng mã vật tư ERP sai", "Fifo": "Số lượng mã vật tư ERP fifo"},
    hole=0.3,  # Set the size of the center hole (0.3 means 30%)
    opacity=0.8,  # Set opacity
)

# Customize text information on the chart
    fig_pie.update_traces(
    textinfo="percent+label",
    hoverinfo="label+percent+value",
    textfont_size=15,
)

# Hiển thị biểu đồ



    column11, column12 = st.columns(2)
    with column11:
        st.subheader("FiFo sai đúng")
        st.dataframe(df_fifo_cleaned.style.apply(highlight_sai, subset=['Kết quả_x']))
    with column12:
        st.subheader("Số mã sai " + ": " + str(count_dem_ma_sai) + "/ " + "Số lượng mã: " + " " + str(count_dem_ma_fifo))
        st.plotly_chart(fig_pie)


    # Biểu đồ hình tròn so sánh số lượng mã vật tư ERP sai và fifo
