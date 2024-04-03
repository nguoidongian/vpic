import streamlit as st
import csv
from datetime import datetime

def save_to_csv(data, filename=r'data.csv'):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def main():
    st.title("Ứng dụng quét và lưu vào CSV")

    current_datetime = datetime.now()

    st.write(f"Ngày: {current_datetime.date()}")
    st.write(f"Giờ: {current_datetime.time()}")

    with st.form(key='my_form'):
        name = st.text_area("quét tên:", height=30)
        order_code = st.text_input("Mã đơn:")
        
        option = st.selectbox("Chọn loại:", ["Nhập", "Xuất"])

        submitted = st.form_submit_button("Lưu")

        if submitted:
            datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            lines_name = name.split('\n')
            data = [[datetime_str, line.strip(), order_code.strip(), option] for line in lines_name]
            save_to_csv(data)
            st.success("Dữ liệu đã được lưu thành công vào file CSV.")

    if st.button("Xuất"):
        with open(r'D:\New folder\data.csv', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                st.write(row)

if __name__ == "__main__":
    main()
