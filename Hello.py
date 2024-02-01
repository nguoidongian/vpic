import pandas as pd
import openpyxl as xl
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px 
from PIL import Image
from streamlit_option_menu import option_menu

st.set_page_config(page_title='KHO VPIC1',layout="wide")

def main():

    main()


#Xuất nhập tồn

df_xnt = pd.read_excel(io="Tổng hợp nhập xuất tồn theo lô.xlsx",
                   engine="openpyxl",
                   sheet_name="Data",
                   usecols='A:J',
                   header=11)

df_xnt = df_xnt.fillna(0)

# Chọn ô cụ thể từ DataFrame (ví dụ: ô ở hàng 0, cột 'Tên hàng')
selected_row = 0
selected_column_tondau = 'Tồn đầu'
selected_column_soluongnhap = 'Số lượng nhập'
selected_column_soluongxuat = 'Số lượng xuất'
selected_column_toncuoi = 'Tồn cuối'
# Lấy giá trị của ô được chọn
cell_value_tondau = df_xnt.at[selected_row, selected_column_tondau]
cell_value_soluongnhap = df_xnt.at[selected_row, selected_column_soluongnhap]
cell_value_soluongxuat = df_xnt.at[selected_row, selected_column_soluongxuat]
cell_value_toncuoi = df_xnt.at[selected_row, selected_column_toncuoi]
# Hiển thị giá trị của ô được chọn

column_xnt1, column_xnt2, column_xnt3, column_xnt4 = st.columns (4)

with column_xnt1:
    st.subheader("Tồn đầu :")
    st.markdown(f'<span style="font-size: 30px">{cell_value_tondau}</span>', unsafe_allow_html=True)


with column_xnt2:
    st.subheader("Số lượng nhập :")
    st.markdown(f'<span style="font-size: 30px">{cell_value_soluongnhap}</span>', unsafe_allow_html=True)

with column_xnt3:
    st.subheader("Số lượng xuất :")
    st.markdown(f'<span style="font-size: 30px">{cell_value_soluongxuat}</span>', unsafe_allow_html=True)


with column_xnt4:
    st.subheader("Tồn cuối :")
    st.markdown(f'<span style="font-size: 30px">{cell_value_toncuoi}</span>', unsafe_allow_html=True)

#Bảng kê đối chiếu dữ liệu ERP - WMS
df = pd.read_excel(io="Bảng kê đối chiếu dữ liệu ERP - WMS.xlsx",
                   engine="openpyxl",
                   sheet_name="Data",
                   usecols='B:I',
                   header=11)


df = df.fillna(0)

with st.sidebar:
    selected = option_menu("Main Menu",["Trang Chủ", " Báo Cáo"],
                           icons=['house', 'gear'], menu_icon="cast", default_index=1)
    selected




makho = st.sidebar.multiselect("Chọn loại kho", 
                               options=df['Mã kho'].unique())


truyendulieu = st.sidebar.multiselect("Chưa xác nhận ERP",
                               options=df['Chiều truyền dữ liệu'].unique(),
                               default= df['Chiều truyền dữ liệu'].unique()
                               )



df_selection = df.query("`Mã kho` == @makho and `Chiều truyền dữ liệu` == @truyendulieu")
df_selection = df_selection.fillna(0)

# Kiểm tra và xử lý giá trị NaN


# Tính tổng số phiếu
total_sophieu = int(df_selection["Chiều truyền dữ liệu"].count())

# Lọc DataFrame theo điều kiện khác
total_phieuchuaxacnhan = int(
    (df_selection['Trạng thái xác nhận ERP'] == 'N'
     ).sum())
total_phieudaxacnhan = int(
    (df_selection['Trạng thái xác nhận ERP'] == 'Y'
     ).sum())
total_wmschuaquet = int(
    (
        (df_selection["Chiều truyền dữ liệu"] == 'ERP_WMS') &
        (df_selection["Trạng thái xác nhận ERP"] == 'Y') &
        (df_selection['Trạng thái WMS'] != 'Duyệt') &
        (df_selection['Trạng thái WMS'] != 'Hoàn thành') &
        (df_selection['Trạng thái WMS'] != 'Chuyển vào SC') &
        (df_selection['Trạng thái WMS'] != 'Hủy phiếu') 

    ).sum()
)




# Display pie chart with resized dimensions



# Hiển thị thông tin trên Streamlit
st.title("Đối chiếu dữ liệu ERP - WMS")

column1, column2, column3 = st.columns (3)
with column1:
    st.subheader("Phiếu ERP chưa xác nhận")
    st.subheader(str(total_phieuchuaxacnhan))  # Tổng số phiếu trong DataFrame

with column2:
    st.subheader(" Phiếu WMS chưa quét")
    st.subheader(str(total_wmschuaquet))   # Hiển thị chi tiết các phiếu có trạng thái 'N'
with column3:
    st.subheader("Tổng số phiếu")
    st.subheader(str(total_sophieu))


left_column, middle_column = st.columns(2)

with left_column:
    st.dataframe(df_selection[df['Trạng thái xác nhận ERP'] == 'N'])

with middle_column:
    st.dataframe(df_selection[(df_selection["Chiều truyền dữ liệu"] == 'ERP_WMS') &
        (df_selection["Trạng thái xác nhận ERP"] == 'Y') &
        (df_selection['Trạng thái WMS'] != 'Duyệt') &
        (df_selection['Trạng thái WMS'] != 'Hoàn thành') &
        (df_selection['Trạng thái WMS'] != 'Chuyển vào SC') &
        (df_selection['Trạng thái WMS'] != 'Hủy phiếu')

        ]
        )
    
left_column1, middle_column2 = st.columns(2)
with left_column1:
    df_phieu_chuaxacnhan = df_selection[df_selection['Trạng thái xác nhận ERP'] == 'N']
    df_phieu_chuaxacnhan_kho = df_phieu_chuaxacnhan.groupby('Mã kho').size().reset_index(name='Số phiếu chưa xác nhận')

# Vẽ biểu đồ hình tròn
    fig = px.pie(df_phieu_chuaxacnhan_kho, values='Số phiếu chưa xác nhận', names='Mã kho', title='Số Phiếu Chưa Xác Nhận ERP Cho Từng Kho')
    st.plotly_chart(fig)


with middle_column2:
    df_phieu_chuaquet = df_selection[(df_selection["Chiều truyền dữ liệu"] == 'ERP_WMS') &
                                  (df_selection["Trạng thái xác nhận ERP"] == 'Y') &
                                  (df_selection['Trạng thái WMS'] != 'Duyệt') &
                                  (df_selection['Trạng thái WMS'] != 'Hoàn thành') &
                                  (df_selection['Trạng thái WMS'] != 'Chuyển vào SC') &
                                  (df_selection['Trạng thái WMS'] != 'Hủy phiếu')]

    df_phieu_chuaquet_kho = df_phieu_chuaquet.groupby('Mã kho').size().reset_index(name='Số phiếu ERP chưa quét')

# Vẽ biểu đồ hình tròn
    fig = px.pie(df_phieu_chuaquet_kho, values='Số phiếu ERP chưa quét', names='Mã kho', title='Số Phiếu ERP Chưa Quét Cho Từng Kho')
    st.plotly_chart(fig)


## lech tem
df_vitri = pd.read_excel(io="Báo cáo tồn kho tem thùng theo vị trí.xlsx",
                   engine="openpyxl",
                   sheet_name="Data",
                   usecols='B:O',
                   header=9)
   
df_vitri["Chênh lệch"] = (df_vitri["Tồn vị trí"] - df_vitri["SL theo ĐVT tồn kho"])



df_vitri = df_vitri.fillna(0)


 # Lọc dữ liệu

filtered_df = df_vitri[(df_vitri["Tồn vị trí"] > 0) & (df_vitri["Chênh lệch"] != 0) & df_vitri["Mã vật tư ERP"] !=0]
sotemlech = int(((df_vitri["Tồn vị trí"] > 0) & (df_vitri["Chênh lệch"] != 0) & (df_vitri["Mã vật tư ERP"] !=0)).sum())



# Display the filtered DataFrame
st.title("Số tem lệch:" + " " + (str(sotemlech)) + " " + "cái")

makho_vitri = st.multiselect("Chọn loại kho", options=filtered_df['Mã kho ERP'].unique(),default=filtered_df['Mã kho ERP'].unique())
df_vitri_selection = df_vitri.query("`Mã kho ERP` == @makho_vitri")
filtered_df_vitri = df_vitri_selection[(df_vitri_selection["Tồn vị trí"] > 0) & (df_vitri_selection["Chênh lệch"] != 0) ]

 # Chọn các cột cần hiển thị
selected_columns = ['Mã vật tư ERP', 'Mã kho ERP', 'Tồn vị trí','SL theo ĐVT tồn kho','Chênh lệch']

# Tạo DataFrame mới chỉ chứa các cột được chọn
df_selected_columns = filtered_df_vitri[selected_columns]

# Hiển thị DataFrame mới
st.dataframe(df_selected_columns)

