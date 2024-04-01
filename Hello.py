import streamlit as st
import pandas as pd
st.set_page_config(page_title='KHO VPIC1', layout="wide")

st.title("Chụp ảnh từ điện thoại và cập nhật bảng kiểm soát")

# Tạo DataFrame mẫu
df = pd.read_excel(io="anhtonghop.xlsx",
                   header=4,
                   sheet_name='Tổng',
                   engine="openpyxl",)

# Hiển thị DataFrame
st.write("DataFrame:", df)

# Người dùng nhập giá trị cần tìm
search_KH = st.selectbox("Tìm kiếm theo khũng xe:", options=df['Số lượng xe chuyên dùng/tình trạng'].unique())

# Tìm kiếm dòng có giá trị tương ứng
selected_row_index = df[df["Số lượng xe chuyên dùng/tình trạng"] == search_KH].index

if len(selected_row_index) > 0:
    selected_row_index = selected_row_index[0]
    st.write("khung xe được chọn:", selected_row_index)
    
    # Tải lên ảnh từ iPhone
    uploaded_file = st.file_uploader("Tải lên ảnh", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Lưu ảnh tải lên
        image_path = f"D:/New folder/{search_KH}.jpg"  # Đường dẫn lưu ảnh

        with open(image_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Cập nhật đường dẫn ảnh vào DataFrame
         # Cập nhật đường dẫn ảnh vào DataFrame
        df["Link Ảnh"] = f'<a href="{image_path}">Xem Ảnh</a>'

    # Hiển thị DataFrame sau khi đã cập nhật
        st.write("DataFrame sau khi cập nhật:", df)
else:
    st.write("Không tìm thấy dòng có giá trị tương ứng.")
