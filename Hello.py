import pandas as pd
import openpyxl as xl
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px 
from PIL import Image
from streamlit_option_menu import option_menu
from datetime import datetime



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



# Đọc dữ liệu từ file Excel
df_tonkhowms = pd.read_excel(io="Báo cáo tồn theo kho.xlsx",
                              engine="openpyxl",
                              sheet_name="Data",
                              usecols='A:FJ',
                              header=9)

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

# Hiển thị DataFrame unpivoted

df_tonkhoerp = pd.read_excel(io="tonkhoerp.xlsx",
                             engine="openpyxl",
                             sheet_name="1",
                             usecols='A:P',
                             header=0)

# Chọn các cột cần hiển thị
selected_tonkhoerp_columns = ['Mã SP', 'Kho', 'SL tồn kho']

# Tạo DataFrame mới chỉ chứa các cột được chọn
df_tonkhoerp_selected_columns = df_tonkhoerp[selected_tonkhoerp_columns]
df_tonkhoerp_selected_columns['Kho'] = df_tonkhoerp_selected_columns['Kho'].str.strip()

# Hiển thị DataFrame tonkhoerp


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


# Hiển thị kết quả

df_Khodachay = pd.read_excel(io="KHO CHẠY WMS.xlsx",
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

#Bảng kê đối chiếu dữ liệu ERP - WMS
df = pd.read_excel(io="Bảng kê đối chiếu dữ liệu ERP - WMS.xlsx",
                   engine="openpyxl",
                   sheet_name="Data",
                   usecols='B:K',
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
df_selection['Giờ tạo'] = pd.to_datetime(df_selection['Giờ tạo'], errors='coerce')

# Lấy giờ hiện tại
now = datetime.now().time()

# Tính chênh lệch thời gian
df_selection['Chênh lệch thời gian (phút)'] = df_selection['Giờ tạo'].apply(lambda x: int((datetime.combine(datetime.min, now) - datetime.combine(datetime.min, x.time())).total_seconds() / 60))




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
    st.write(df_selection[df['Trạng thái xác nhận ERP'] == 'N'])

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

left_column1, middle_column2 = st.columns(2)
# Hiển thị DataFrame mới
st.write(df_selected_columns)



# đếm những mã có nhiều vị trí
df_tonlovitri = pd.read_excel(io="Báo cáo tồn lô vị trí.xlsx",
                   engine="openpyxl",
                   sheet_name="Data",
                   usecols='A:K',
                   header=9)




# Xóa các dòng có giá trị null trong cột 'Mã vị trí'
df_tonlovitri_cleaned = df_tonlovitri.dropna(subset=['Mã vị trí'])

# Xóa các dòng có vị trí giống nhau
df_tonlovitri_cleaned = df_tonlovitri_cleaned.drop_duplicates(subset=['Mã vật tư ERP', 'Mã kho ERP', 'Mã vị trí'])
df_tonlovitri_count = df_tonlovitri_cleaned.groupby(['Mã vật tư ERP', 'Mã kho ERP'])['Mã vị trí'].count().reset_index()
df_tonlovitri_count = df_tonlovitri_count.rename(columns={'Mã vị trí': 'Số vị trí'})
df_tonlovitri_merged = pd.merge(df_tonlovitri_cleaned, df_tonlovitri_count, on=['Mã vật tư ERP', 'Mã kho ERP'], how='left')

df_maNhieuViTri = df_tonlovitri_merged[df_tonlovitri_merged['Số vị trí'] >= 2]
df_tongTonTheoViTri = df_tonlovitri_merged.groupby(['Mã kho ERP', 'Mã vị trí'])['Tồn vị trí'].sum().reset_index()
df_tongTonMoiKho = df_tongTonTheoViTri.groupby('Mã kho ERP')['Tồn vị trí'].sum().reset_index()


# Chọn các cột cần hiển thị
selected_columns_vitri = ['Mã vật tư ERP','Tên vật tư','Quy cách quản lý','ĐVT','Mã kho ERP', 'Tồn vị trí','Số vị trí']

# Tạo DataFrame mới chỉ chứa các cột được chọn
df_selected_vitri_columns = df_maNhieuViTri[selected_columns_vitri]

left_column1, middle_column2 = st.columns(2)
# Tạo biểu đồ cột số vị trí
fig = px.bar(df_tonlovitri_merged, x='Mã kho ERP', y='Số vị trí', title='Số vị trí trong kho')
fig.update_layout(xaxis_title='Kho', yaxis_title='Số vị trí')

# Hiển thị biểu đồ trong Streamlit

left_column3, middle_column4 = st.columns(2)
with left_column3:  
    st.title("Các mã có 2 vị trí trở lên")
    st.dataframe(df_selected_vitri_columns)
with middle_column4:
    st.plotly_chart(fig)


fig = px.treemap(df_tongTonTheoViTri, path=['Mã kho ERP', 'Mã vị trí'], values='Tồn vị trí')

left_column4, middle_column5 = st.columns(2)
with left_column4:  
    st.title("Tổng tồn vị trí mỗi kho")
    st.dataframe(df_tongTonTheoViTri.style.highlight_max(axis=0, color='yellow').set_table_styles([{'selector': 'tr:hover', 'props': [('background-color', 'yellow')]}]))

with middle_column5:
    st.title('Biểu đồ Treemap Tổng tồn vị trí mỗi kho')
    st.plotly_chart(fig)
