import streamlit as st
import pandas as pd
import openpyxl as xl
import matplotlib.pyplot as plt
import plotly.express as px 
from PIL import Image
from streamlit_option_menu import option_menu
from datetime import datetime

st.set_page_config(page_title='KHO VPIC1',layout="wide")

def main():
    st.title("Ứng dụng Streamlit")
# Tạo sidebar với các tùy chọn menu
with st.sidebar:
    selected_option = option_menu("Main Menu",["Trang Chủ", " Báo Cáo"],
                           icons=['house', 'gear'], menu_icon="cast", default_index=0)
    selected_option

# Hiển thị nội dung chính tương ứng với tùy chọn được chọn
if selected_option == "Trang Chủ":
    trangchu()
    # Hiển thị nội dung trang chủ ở đây
elif selected_option == "Báo Cáo":
    uploadbaocao()
    # Hiển thị nội dung báo cáo ở đây
elif selected_option == "Cài Đặt":
    show_page_2()
    # Hiển thị nội dung cài đặt ở đây

if __name__ == "__main__":
    main()
