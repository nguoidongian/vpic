import streamlit as st
import csv
from datetime import datetime

def save_to_csv(data, filename=r'\data.csv'):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

def main():
    st.title("Ứng dụng quét và lưu vào CSV")

    # Lấy ngày và giờ hiện tại
    current_datetime = datetime.now()

    # Hiển thị ngày và giờ
    st.write(f"Ngày: {current_datetime.date()}")
    st.write(f"Giờ: {current_datetime.time()}")

    # Tạo ô input cho người dùng nhập tên, email và số điện thoại
    name = st.text_area("quét tên:", height=30)

    # Nếu người dùng nhấn nút "Lưu", lưu dữ liệu vào file CSV
    if st.button("Lưu"):
        # Format ngày và giờ thành chuỗi
        datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Tách dữ liệu thành từng dòng
        lines = name.split('\n')
        # Lưu mỗi dòng dữ liệu với ngày giờ hiện tại
        for line in lines:
            data = [datetime_str, line.strip()]
            save_to_csv(data)
        st.success("Dữ liệu đã được lưu thành công vào file CSV.")

if __name__ == "__main__":
    main()
