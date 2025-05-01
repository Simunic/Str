import streamlit as st
import datetime
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder,JsCode
from func import *
from var import *
from data import *
#from pages.data_stock import *
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import json
from html_code import *
import plotly.graph_objs as go
from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
from streamlit.components.v1 import html
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest
import sqlite3
import matplotlib.dates as mdates
#from streamlit_javascript import st_javascript

# Đặt cấu hình trang - Phải là lệnh đầu tiên
st.set_page_config(page_title="CHỨNG KHOÁN", page_icon="📈",layout="wide") # tạo tiêu đề hiện thị trên tab

# Gọi hàm để áp dụng CSS
add_custom_css()

# Mã CSS để ẩn sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Khởi tạo database lưu lịch sử mua bán chứng khoán
init_db()


# Tạo dòng đầu tiên
col1, col2,col3,col4,col5,col6 = st.columns([1.5,0.5,0.5,0.5,0.3,1])  # Điều chỉnh tỉ lệ chiều rộng các cột nếu cần
#Tạo dòng tiêu đề tổng trang
with col1:
    st.markdown(
        """
        <style>
        .title-text {
            line-height: 40px;  /* Điều chỉnh chiều cao dòng để căn chỉnh */
            margin: 0;  /* Loại bỏ margin nếu cần */
            padding: 16px 0px;  /* Loại bỏ padding nếu cần */
        }
        </style>
        <div class="title-text">
        <h1 style="font-size: 25px; margin: 0; padding: 0;">TỔNG HỢP THÔNG TIN MÃ CHỨNG KHOÁN</h1>
        </div>
        """, unsafe_allow_html=True
    )
# Tạo ô nhập liệu mã chứng khoán
with col5:
    # CSS tùy chỉnh để điều chỉnh độ rộng của ô input
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            width: 250px;  /* Điều chỉnh độ rộng tại đây */
            padding: 4px 8px;  /* Điều chỉnh padding để căn chỉnh chiều cao */
            margin: 0;  /* Loại bỏ margin nếu cần */
            box-sizing: border-box;  /* Đảm bảo padding không ảnh hưởng đến tổng chiều rộng */
            background-color: #e0f7fa;  /* Màu nền của ô input */
            border: 1px solid #00796b;  /* Đường viền của ô input */
            border-radius: 4px;  /* Độ bo góc của ô input */
        }
        </style>
        """, unsafe_allow_html=True)
    
    #mack = st.text_input("", placeholder="Nhập mã", value="BSR",label_visibility="collapsed")
    
    # Nhập tên sheet từ người dùng và lưu vào session state
    if 'sheet_name' not in st.session_state:
        st.session_state.sheet_name = mack_macdinh  # Giá trị mặc định

    mack = st.text_input(label='',value=st.session_state.sheet_name, placeholder="Nhập mã chứng khoán",label_visibility="collapsed")
    mack = mack.upper()
    # Chuyển đổi giá trị nhập vào thành chữ hoa và lưu vào session_state
    st.session_state.sheet_name = mack.upper()

with col2:
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            width: 250px;  /* Điều chỉnh độ rộng tại đây */
            padding: 4px 8px;  /* Điều chỉnh padding để căn chỉnh chiều cao */
            margin: 0;  /* Loại bỏ margin nếu cần */
            box-sizing: border-box;  /* Đảm bảo padding không ảnh hưởng đến tổng chiều rộng */
            background-color: #e0f7fa;  /* Màu nền của ô input */
            border: 1px solid #00796b;  /* Đường viền của ô input */
            border-radius: 4px;  /* Độ bo góc của ô input */
        }
        </style>
        """, unsafe_allow_html=True)
    with st.popover(f"Ghi chú giao dịch"):
        # Hiển thị tiêu đề
        st.title("Ghi chú của tôi")

        # Tạo một ô nhập liệu lớn cho ghi chú
        note = st.text_area("Nhập ghi chú của bạn:", "", height=200)

        # Hiển thị ghi chú đã lưu nếu có
        notes = load_notes()

        if notes:
            st.subheader("Ghi chú trước đó:")
            for note_id, note_content in notes.items():
                st.markdown(f"**{note_id}**:\n{note_content}\n")
                # Thêm nút xóa cho mỗi ghi chú
                if st.button(f"Xóa ghi chú {note_id}"):
                    delete_note(note_id)
                    st.success(f"Đã xóa ghi chú {note_id}")

        # Lưu ghi chú mới khi người dùng nhấn nút
        if st.button("Lưu ghi chú"):
            if note:
                # Tạo một ID cho ghi chú mới, ví dụ như thời gian hiện tại
                note_id = f"note_{len(notes) + 1}"
                notes[note_id] = note
                save_notes(notes)
                st.success("Đã lưu ghi chú!")
            else:
                st.warning("Vui lòng nhập ghi chú trước khi lưu.")

with col3:
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            width: 250px;  /* Điều chỉnh độ rộng tại đây */
            padding: 4px 8px;  /* Điều chỉnh padding để căn chỉnh chiều cao */
            margin: 0;  /* Loại bỏ margin nếu cần */
            box-sizing: border-box;  /* Đảm bảo padding không ảnh hưởng đến tổng chiều rộng */
            background-color: #e0f7fa;  /* Màu nền của ô input */
            border: 1px solid #00796b;  /* Đường viền của ô input */
            border-radius: 4px;  /* Độ bo góc của ô input */
        }
        </style>
        """, unsafe_allow_html=True)
    with st.popover(f"Cập nhật dữ liệu mua bán"):
        # Tạo tiêu đề ứng dụng
        #st.title("Quản lý giao dịch cổ phiếu")
        # Phần nhập giao dịch
        st.subheader("Thêm giao dịch mới")
        with st.form("add_trade_form"):
            stock_code = st.text_input("Mã cổ phiếu")
            trade_date = st.date_input("Ngày giao dịch")
            trade_type = st.selectbox("Loại giao dịch", ["Mua", "Bán"])
            quantity = st.number_input("Số lượng", min_value=1, step=1)
            price = st.number_input("Giá", min_value=0.0, step=100.0)
            
            # Tính thành tiền
            total_value = quantity * price
            st.write(f"**Thành tiền:** {total_value:,.0f} VND")
            
            submitted = st.form_submit_button("Thêm giao dịch")

            if submitted:
                if not stock_code.strip():
                    st.error("Mã cổ phiếu không được để trống!")
                elif price <= 0:
                    st.error("Giá phải lớn hơn 0!")
                else:
                    add_trade(stock_code, trade_date, trade_type, quantity, price)
                    st.success("Đã thêm giao dịch thành công!")
        trades = get_trades()
    #st.write(trades)
        if trades:
            # Tạo DataFrame từ các giao dịch
            df = pd.DataFrame(trades, columns=["ID", "Mã cổ phiếu", "Ngày giao dịch", "Loại giao dịch", "Số lượng", "Giá"])
            
            # Định dạng lại cột Thành Tiền
            df["Số lượng"] = df.apply(lambda row: row["Số lượng"] * 1 if row["Loại giao dịch"] == "Mua" else row["Số lượng"] * -1, axis=1)
            df["Thành Tiền"] = df["Số lượng"] * df["Giá"]
            st.dataframe(df.style.format({"Giá": "{:,.0f} VND", "Số lượng": "{:,}", "Thành Tiền": "{:,.0f} VND"}))
        # Chọn dòng cần xóa
        st.subheader("Xóa giao dịch")
        delete_id = st.number_input("Nhập ID giao dịch cần xóa", min_value=1, step=1)
        # Xóa giao dịch khi nhấn nút
        if st.button("Xóa giao dịch"):
            if delete_id:
                # Xóa giao dịch khỏi cơ sở dữ liệu
                conn = sqlite3.connect('data/stock_trades.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM trades WHERE id = ?', (delete_id,))
                conn.commit()
                conn.close()

                # Thông báo thành công và làm mới danh sách giao dịch
                st.success(f"Giao dịch có ID {delete_id} đã được xóa.")

                # Cập nhật lại danh sách giao dịch
                trades = get_trades()
                df = pd.DataFrame(trades, columns=["ID", "Mã cổ phiếu", "Ngày giao dịch", "Loại giao dịch", "Số lượng", "Giá"])
                df["Thành Tiền"] = df["Số lượng"] * df["Giá"]
                st.dataframe(df.style.format({"Giá": "{:,.0f} VND", "Số lượng": "{:,}", "Thành Tiền": "{:,.0f} VND"}))

            else:
                st.error("Vui lòng nhập ID giao dịch hợp lệ.")

with col4:
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            width: 250px;  /* Điều chỉnh độ rộng tại đây */
            padding: 4px 8px;  /* Điều chỉnh padding để căn chỉnh chiều cao */
            margin: 0;  /* Loại bỏ margin nếu cần */
            box-sizing: border-box;  /* Đảm bảo padding không ảnh hưởng đến tổng chiều rộng */
            background-color: #e0f7fa;  /* Màu nền của ô input */
            border: 1px solid #00796b;  /* Đường viền của ô input */
            border-radius: 4px;  /* Độ bo góc của ô input */
        }
        </style>
        """, unsafe_allow_html=True)
    with st.popover(f"Dữ liệu mua bán"):
        filter_code = mack
        filter_type = st.selectbox("Lọc theo loại giao dịch", ["Tất cả", "Mua", "Bán"])

        # Lọc giao dịch theo mã cổ phiếu và loại giao dịch
        filtered_trades = trades
        if filter_code.strip():
            filtered_trades = [trade for trade in filtered_trades if filter_code.lower() in trade[1].lower()]
        if filter_type != "Tất cả":
            filtered_trades = [trade for trade in filtered_trades if trade[3] == filter_type]

        # Hiển thị dữ liệu đã lọc
        df_filtered = pd.DataFrame(filtered_trades, columns=["ID", "Mã cổ phiếu", "Ngày giao dịch", "Loại giao dịch", "Số lượng", "Giá"])

        # Tính lại cột "Thành Tiền" sau khi lọc
        df_filtered["Số lượng"] = df_filtered.apply(lambda row: row["Số lượng"] * 1 if row["Loại giao dịch"] == "Mua" else row["Số lượng"] * -1, axis=1)
        df_filtered["Thành Tiền"] = df_filtered["Số lượng"] * df_filtered["Giá"]

        # Tính tổng Số lượng và tổng Thành Tiền
        total_quantity = df_filtered["Số lượng"].sum()
        total_amount = df_filtered["Thành Tiền"].sum()

        # Tính giá trung bình (Giá = Tổng Thành Tiền / Tổng Số lượng)
        average_price = total_amount / total_quantity if total_quantity != 0 else 0

        # Thêm dòng tổng vào DataFrame
        total_row = pd.DataFrame([["Tổng cộng", "", "", "", total_quantity, average_price, total_amount]],
                                columns=["ID", "Mã cổ phiếu", "Ngày giao dịch", "Loại giao dịch", "Số lượng", "Giá","Thành Tiền"])

        # Thêm dòng tổng vào DataFrame đã lọc
        df_filtered = pd.concat([df_filtered, total_row], ignore_index=True)

        # Hiển thị dữ liệu đã lọc và tính tổng
        #st.dataframe(df_filtered.reset_index().style.format({"Giá": "{:,.0f} VND", "Số lượng": "{:,}", "Thành Tiền": "{:,.0f} VND"}))
        st.table(df_filtered.reset_index(drop=True).style.format({"Giá": "{:,.0f}","Số lượng": "{:,}", "Thành Tiền": "{:,.0f}"}))


with col6:
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            width: 250px;  /* Điều chỉnh độ rộng tại đây */
            padding: 4px 8px;  /* Điều chỉnh padding để căn chỉnh chiều cao */
            margin: 0;  /* Loại bỏ margin nếu cần */
            box-sizing: border-box;  /* Đảm bảo padding không ảnh hưởng đến tổng chiều rộng */
            background-color: #e0f7fa;  /* Màu nền của ô input */
            border: 1px solid #00796b;  /* Đường viền của ô input */
            border-radius: 4px;  /* Độ bo góc của ô input */
        }
        </style>
        """, unsafe_allow_html=True)
    if st.button("Tải Dữ Liệu"):
        if mack != st.session_state.sheet_name:
            data_org = load_data(st.session_state.sheet_name)

data_org = load_data(st.session_state.sheet_name, file_path = 'Str/data/Stock_Data.xlsm')
data_ai = load_data(st.session_state.sheet_name, file_path = 'Str/data/Stock_Data.xlsm')
#data_ai = data_org
data_org['Ngay'] = pd.to_datetime(data_org['Ngay'], format='%d/%m/%y', errors='coerce')
data_org['Ngay'] = data_org['Ngay'].dt.strftime('%d/%m/%y')
# Áp dụng định dạng cho cột TB_canbang
#data_org = data_org.style.applymap(highlight_tb_canbang, subset=['TB_canbang'])

total_kq_sign01 = data_org['KQ_Sign01'].sum()
total_kq_sign02 = data_org['KQ_Sign02'].sum()

for i in range(len(data_org)):
    rs2 = data_org.loc[i, 'S02_1']
    s2=0
    if rs2 == 1:
        break
    if rs2 == -1:
        s2=int(data_org.loc[i, 'BQ'])
        break

for i in range(len(data_org)):
    rs1 = data_org.loc[i, 'S01_1']
    s1=0
    if rs1 == 1:
        break
    if rs1 == -1:
        s1=int(data_org.loc[i, 'BQ'])
        break

#@st.cache_data
def load_data_f():
    return style_dataframe(data_org)    #format bảng

st.markdown(
    f"""
    <p>
        Tên.........................: 
        <span style='color:red; font-weight:bold;margin-right: 20px;margin-left: 20px;'>Tổng KQ_Sign01: {f"{total_kq_sign01:,.0f}".replace(',', '.')}</span>
        <span style='color:blue; font-weight:bold;'>Tổng KQ_Sign02: {f"{total_kq_sign02:,.0f}".replace(',', '.')}</span>
        <span style='color:red; font-weight:bold;margin-right: 20px;margin-left: 20px;'>Giá hiện tại của Sign02: {f"{s2:,.0f}".replace(',', '.')}</span>
        <span style='color:blue; font-weight:bold;'>Giá hiện tại của Sign01: {f"{s1:,.0f}".replace(',', '.')}</span>
    </p>
    """, unsafe_allow_html=True
)

col_P1, col_P2 = st.columns([10,1])  # Điều chỉnh tỉ lệ chiều rộng các cột nếu cần
with col_P1:
    st.write(load_data_f(), unsafe_allow_html=True)
with col_P2:
    # Form để cập nhật dữ liệu
    with st.form("key1"):
        form_col1, form_col2 = st.columns([1,1])
        with form_col1:
            name_to_update = st.text_input("Mã",value=mack,label_visibility="collapsed")
        with form_col2:
            submit_button = st.form_submit_button("Update")
        form_col3, form_col4 = st.columns([1,1])
        with form_col3:
             Sign01 = st.text_input("Sign01", value=int(s1))  # Nhãn rỗng để không làm rối giao diện
        with form_col4:
            background_color_1 = st.selectbox("Sign01",["Xanh", "Tím", "Đỏ","Vàng","Trắng"], index=0,key="select1")
        form_col5, form_col6 = st.columns([1,1])
        with form_col5:
            Sign02 = st.text_input("Sign02", value=int(s2))
        with form_col6:
            background_color_2 = st.selectbox("Màu Sign02",["Xanh", "Tím", "Đỏ","Vàng","Trắng"], index=0,key="select2")
        
        # Thêm selectbox để chọn màu nền cho cột 2
        if submit_button:
            if name_to_update:
                # Đọc dữ liệu từ file JSON
                data = load_data_from_json(json_file)
                
                # Tìm và cập nhật giá trị nếu cột name trùng khớp
                updated = False
                for entry in data["data"]:
                    if entry["name"] == name_to_update:
                        if Sign01:
                            entry["KQ_Sign01"] = Sign01
                        if Sign02:
                            entry["KQ_Sign02"] = Sign02
                        # Cập nhật màu sắc
                        color_mapping = {
                            "Xanh": "green",
                            "Tím": "purple",
                            "Đỏ": "red",
                            "Vàng":"yellow",
                            "Trắng":"white"
                        }
                        entry["Color_Sign01"] = color_mapping[background_color_1]
                        entry["Color_Sign02"] = color_mapping[background_color_2]
                        updated = True
                
                if updated:
                    # Lưu lại dữ liệu vào file JSON
                    save_data_to_json(json_file, data)
                    #st.success(f"Dữ liệu cho các dòng có tên {name_to_update} đã được cập nhật thành công!")
                else:
                    st.error(f"Không tìm thấy tên {name_to_update} trong dữ liệu.")
            else:
                st.error("Vui lòng nhập tên trong cột name.")


################################################################################################################
    # Đọc dữ liệu từ file JSON và hiển thị bảng dữ liệu
    data = load_data_from_json(json_file)
    data = convert_to_integer(data)
    df = data_to_dataframe(data)
    color_mapping_Sign01 = {entry['name']: entry.get('Color_Sign01', 'white') for entry in data["data"]}
    color_mapping_Sign02 = {entry['name']: entry.get('Color_Sign02', 'white') for entry in data["data"]}
    df = df.drop(columns=['Color_Sign01', 'Color_Sign02'], errors='ignore')
    # df = ... # DataFrame sau khi xử lý
    styled_parts = [
        style_frame(part, {"KQ_Sign01": color_mapping_Sign01, "KQ_Sign02": color_mapping_Sign02}, "KQ_Sign01", "KQ_Sign02")
        for part in split_dataframe(df)
    ]
################################################################################################################
################################################################################################################
# Tạo popover bằng expander
with st.expander("Click để hiển thị bảng"):
    display_in_columns(styled_parts)  # Hiển thị bảng dữ liệu khi người dùng mở expander

################################################################################################################

################################################################################################################

df = data_org
df['Ngay'] = pd.to_datetime(df['Ngay'], format='%d/%m/%y')
################################################################################################################

################################################################################################################
col_R1, col_R2 = st.columns([20,1])  # Điều chỉnh tỉ lệ chiều rộng các cột nếu cần
################################################################################################################
with col_R2:
    start_date = st.date_input("Ngày bắt đầu", datetime.date(2023, 1, 1))
    end_date = st.date_input("Ngày kết thúc", data_org['Ngay'].max())
    show_price1 = st.checkbox("Giá BQ", value=True)
    show_price2 = st.checkbox("Giá Kỳ 1", value=False)
    show_price3 = st.checkbox("Giá Kỳ 2", value=False)
    show_price4 = st.checkbox("Giá Kỳ 3", value=False)
    show_buy = st.checkbox("Status Buy", value=True)
    show_buy_ky = st.checkbox("F-Status Buy", value=True)
    show_F_VNI = st.checkbox("F_VNI",value = False)
    show_Add = st.checkbox("Line Add",value = False)
    show_P1_P2 = st.checkbox("P1_P2",value = True)
    show_P_Ky2_BQ = st.checkbox("P_Ky2_BQ",value = True)
    show_P_Ky1_BQ = st.checkbox("P_Ky1_BQ",value = False)


# Kiểm tra nếu ngày bắt đầu lớn hơn ngày kết thúc
if start_date > end_date:
    st.error("Ngày bắt đầu không được lớn hơn ngày kết thúc!")

# Lấy dữ liệu để vẽ biểu đồ đường thẳng lãi suất
# Ngày cách đúng 1 năm
one_year_later = end_date + relativedelta(years=-1)
one_year_later = pd.to_datetime(one_year_later)
two_year_later = end_date + relativedelta(years=-2)
# Lọc giá trị khối lượng
date_ls = data_org[data_org['Ngay'] <= one_year_later]

# Lấy ngày lớn nhất trong các ngày thỏa mãn
time_1 = date_ls['Ngay'].max()
price_1 = data_org.loc[data_org['Ngay'] == time_1, 'BQ'].iloc[0]
price_target = int(price_1.replace(',', '')) * 1.05

# Lọc dữ liệu theo khoảng thời gian đã chọn
filtered_df = df[(df['Ngay'] >= pd.to_datetime(start_date)) & (df['Ngay'] <= pd.to_datetime(end_date))]
################################################################################################################

################################################################################################################
# Tạo biểu đồ Plotly với các lựa chọn từ checkbox


################################################################################################################

################################################################################################################
# Đánh dấu các ngày có giá trị Gross khác 0 với chấm tròn đỏ
df['KQ_Sign01'] = df['KQ_Sign01'].str.replace(',', '').str.strip()
df['KQ_Sign01'] = pd.to_numeric(df['KQ_Sign01'], errors='coerce')
P_Sign01_Ngay = df['Ngay'][(df['Ngay'] >= pd.to_datetime(start_date)) & 
                   (df['Ngay'] <= pd.to_datetime(end_date)) & 
                   (df['KQ_Sign01'] > 0)]
P_Sign01_BQ = df['BQ'][(df['KQ_Sign01'] > 0) & 
                     (df['Ngay'] >= pd.to_datetime(start_date)) & 
                     (df['Ngay'] <= pd.to_datetime(end_date))]
# Hiện thị bảng Data
#st.write(df['KQ_Sign01'], unsafe_allow_html=True)
############################################################################################################################################

# Tạo subplot với shared x-axis
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05,specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{"secondary_y": True}]]) # secondary_y cho row 2)

############################################################################################################################################
# Thêm đường biểu diễn giá cổ phiếu 1 nếu checkbox được chọn
if show_price1:
    fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['BQ'], mode='lines', name='BQ', yaxis='y1',line_color = '#DAA520',line=dict(width=1)), row=1, col=1, secondary_y=False)
# Thêm đường biểu diễn giá cổ phiếu 2 nếu checkbox được chọn
if show_price2:
    fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['P_Ky1'], mode='lines', name='Giá cổ phiếu 1', yaxis='y1',line_color='#00008B',line=dict(width=1.5)), row=1, col=1, secondary_y=False)
# Thêm đường biểu diễn giá cổ phiếu 2 nếu checkbox được chọn
if show_price3:
    fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['P_Ky2'], mode='lines', name='Giá cổ phiếu 2', yaxis='y1',line_color='#87CEEB',line=dict(width=1)), row=1, col=1, secondary_y=False)
if show_price4:
    fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['P_Ky3'], mode='lines', name='Giá cổ phiếu 3', yaxis='y1',line_color='#FF00FF',line=dict(width=1)), row=1, col=1, secondary_y=False)
# Thêm biểu diễn khối lượng giao dịch nếu checkbox được chọn
if show_buy:
    #fig.add_trace(go.Bar(x=filtered_df['Ngay'], y=filtered_df['KLGD'], name='Khối lượng giao dịch', yaxis='y2', opacity=0.6))
    fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['KL_Per'], name='Tỷ lệ', yaxis='y2',mode='lines',line_color='#008000',line=dict(width=1.2)), row=1, col=1, secondary_y=True)
if show_buy_ky:
    #fig.add_trace(go.Bar(x=filtered_df['Ngay'], y=filtered_df['KLGD'], name='Khối lượng giao dịch', yaxis='y2', opacity=0.6))
    fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['KL_Per_1'], name='Tỷ lệ', yaxis='y2',mode='lines',line_color='#00008B',line=dict(width=1.2)), row=1, col=1, secondary_y=True)

# Thêm trace cho các điểm có Gross khác 0
fig.add_trace(go.Scatter(
    x=P_Sign01_Ngay,
    y=P_Sign01_BQ,
    mode='markers',
    marker=dict(color='red', size=sizepoint),
    name='Sell'
), row=1, col=1, secondary_y=False)    

P_Sign02_Ngay = df['Ngay'][(df['Ngay'] >= pd.to_datetime(start_date)) & 
                   (df['Ngay'] <= pd.to_datetime(end_date)) & 
                   (df['KQ_Sign01'] < 0)]
P_Sign02_BQ = df['BQ'][(df['KQ_Sign01'] < 0) & 
                     (df['Ngay'] >= pd.to_datetime(start_date)) & 
                     (df['Ngay'] <= pd.to_datetime(end_date))]
# Hiện thị bảng Data

# Thêm trace cho các điểm có Gross khác 0
fig.add_trace(go.Scatter(x=P_Sign02_Ngay,y=P_Sign02_BQ,mode='markers',marker=dict(color='green', size=sizepoint),name='Buy'), row=1, col=1, secondary_y=False)    

# Thêm đường thẳng nối hai điểm
fig.add_trace(go.Scatter(
    x=[one_year_later, end_date],  # Tọa độ x của hai điểm
    y=[price_1, price_target],  # Tọa độ y của hai điểm
    mode='lines',  # Vẽ đường thẳng
    name="Đường lãi suất",  # Tên đường
    line=dict(color='#00008B', width=1, dash='dash')  # Tùy chỉnh màu sắc và độ rộng đường
), row=1, col=1, secondary_y=False)

# Thêm đường thẳng nối hai điểm
fig.add_trace(go.Scatter(
    x=[df.loc[df.loc[0,'Ky_2'], 'Ngay'],df.loc[0, 'Ngay']],  # Tọa độ x của hai điểm
    y=[df.loc[df.loc[0,'Ky_2'], 'BQ'],df.loc[0, 'BQ']],  # Tọa độ x của hai điểm
    name="Đường lãi suất",  # Tên đường
    line=dict(color='#000000', width=1, dash='dash')  # Tùy chỉnh màu sắc và độ rộng đường
), row=1, col=1, secondary_y=False)
###############################################################################################3
# # Các điểm bất thường theo mô hình K_means
# data_K_Mean = data_ai[['KLGD','BQ','KL_Per_1','BQ_CL','KL_Per','TL_VNI','P_Ky1_BQ','Sign01','Sign02']]
# # Loại bỏ các dòng có giá trị NaN
# data_K_Mean = data_K_Mean.dropna()
# # Chuẩn hóa dữ liệu
# scaler = StandardScaler()
# data_scaled = scaler.fit_transform(data_K_Mean)

# # Phương pháp Elbow để xác định số cụm tối ưu
# inertia = []
# for k in range(1, 11):  # Kiểm tra từ số cụm 1 đến 10
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     kmeans.fit(data_scaled)
#     inertia.append(kmeans.inertia_)

# # Tính độ dốc giữa các điểm inertia
# inertia_diff = np.diff(inertia)

# # Tính độ dốc thứ hai (để phát hiện điểm "elbow")
# inertia_diff2 = np.diff(inertia_diff)

# # Tìm vị trí có độ dốc thứ hai lớn nhất
# optimal_k = np.argmax(inertia_diff2) + 2  # +2 vì inertia_diff2 là độ dốc thứ hai, nên vị trí thực tế là k = index + 2

# # Phân cụm dữ liệu với số cụm tối ưu
# kmeans = KMeans(n_clusters=optimal_k, random_state=42)
# data_K_Mean['Cluster'] = kmeans.fit_predict(data_scaled)

# # Hàm để tính tỷ lệ bất thường
# def calculate_anomaly_ratio(data):
#     normal_cluster = data['Cluster'].mode()[0]  # Tìm cụm "bình thường" (cụm xuất hiện nhiều nhất)
#     data['Anomaly'] = data['Cluster'] != normal_cluster  # Đánh dấu bất thường (không thuộc cụm bình thường)
#     return data['Anomaly'].mean()  # Tính tỷ lệ bất thường   

# # Đánh giá tỷ lệ bất thường
# anomaly_ratio = calculate_anomaly_ratio(data_K_Mean)
# st.write(f"Tỷ lệ điểm bất thường sau khi phân cụm: {anomaly_ratio * 100:.2f}%")

# Thống kê số lượng True/False
# anomaly_counts = data_K_Mean['Anomaly'].value_counts()
# count_true = anomaly_counts[True] if True in anomaly_counts else 0
# count_false = anomaly_counts[False] if False in anomaly_counts else 0

# Hiển thị kết quả
# st.write(f"Số giá trị **True** (Bất thường): {count_true}")
# st.write(f"Số giá trị **False** (Bình thường): {count_false}")
################################################################################################################
# Các điểm bất thường theo mô hình Dbscan
# def find_best_dbscan_params(data_scaled, min_samples_range, eps_range):
#     best_eps = None
#     best_min_samples = None
#     min_anomalies = float('inf')  # Số điểm bất thường thấp nhất

#      # Thử các giá trị eps và min_samples trong phạm vi được chỉ định
#     for min_samples in min_samples_range:
#         for eps in eps_range:
#             # Áp dụng DBSCAN với tham số hiện tại
#             dbscan = DBSCAN(eps=eps, min_samples=min_samples)
#             labels = dbscan.fit_predict(data_scaled)

#             # Tính số điểm bất thường (Cluster = -1)
#             num_anomalies = np.sum(labels == -1)

#             # Cập nhật nếu số điểm bất thường thấp hơn
#             if num_anomalies < min_anomalies:
#                 min_anomalies = num_anomalies
#                 best_eps = eps
#                 best_min_samples = min_samples

#     return best_eps, best_min_samples, min_anomalies
# Định nghĩa phạm vi các tham số cần thử
# min_samples_range = range(3, 11)  # Thử các giá trị min_samples từ 3 đến 10
# eps_range = np.arange(0.1, 1.1, 0.1)  # Thử các giá trị eps từ 0.1 đến 1.0

# Tìm tham số tốt nhất
#best_eps, best_min_samples, min_anomalies = find_best_dbscan_params(data_scaled, min_samples_range, eps_range)

# In kết quả tham số tốt nhất
# st.write(f"Tham số tốt nhất: eps = {best_eps}, min_samples = {best_min_samples}")
# st.write(f"Số điểm bất thường: {min_anomalies}")

# dbscan = DBSCAN(eps=best_eps, min_samples=best_min_samples)
# data_K_Mean['Cluster_D'] = dbscan.fit_predict(data_scaled)
# data_K_Mean['Anomaly_D'] = (data_K_Mean['Cluster_D'] == -1).astype(int)
# st.dataframe(data_K_Mean)

##################################################################################################################333
# Hàm tìm contamination tối ưu
# def find_optimal_contamination(data, min_cont=0.01, max_cont=0.2, step=0.01):
#     results = []
    
#     for contamination in np.arange(min_cont, max_cont, step):
#         iso_forest = IsolationForest(contamination=contamination, random_state=42)
#         labels = iso_forest.fit_predict(data)
#         num_anomalies = sum(labels == -1)  # Số lượng điểm bất thường
#         results.append((contamination, num_anomalies))
    
#     # Chuyển kết quả thành DataFrame
#     results_df = pd.DataFrame(results, columns=['Contamination', 'Num_Anomalies'])
#     return results_df

# results_df = find_optimal_contamination(data_scaled)

# Chọn contamination với số lượng điểm bất thường hợp lý
#optimal_contamination = results_df.loc[results_df['Num_Anomalies'].idxmin(), 'Contamination']

# Áp dụng Isolation Forest với contamination tối ưu
# iso_forest = IsolationForest(contamination=optimal_contamination, random_state=42)
# data_K_Mean['Anomaly_I'] = iso_forest.fit_predict(data_scaled)
#data_K_Mean['Anomaly_I'] = data_K_Mean['Anomaly_I'].apply(lambda x: -1 if x == -1 else 'Normal')

# Hiển thị kết quả
# st.write(f"Optimal Contamination: {optimal_contamination:.2f}")
# st.dataframe(results_df)
# st.dataframe(data_K_Mean)

##########################################################################################################################3333
# # # Hiển thị bảng dữ liệu
# data_K_Mean['Ngay']=data_org['Ngay']
# K_Ngay = data_K_Mean['Ngay'][(data_K_Mean['Anomaly'] == 1 )&(data_K_Mean['Ngay'] >= pd.to_datetime(start_date)) & 
#                    (data_K_Mean['Ngay'] <= pd.to_datetime(end_date))]
# K_Mean_BQ = data_K_Mean['BQ'][(data_K_Mean['Anomaly'] == 1 )&(data_K_Mean['Ngay'] >= pd.to_datetime(start_date)) & 
#                    (data_K_Mean['Ngay'] <= pd.to_datetime(end_date))]
# #st.dataframe(data_K_Mean)

# fig.add_trace(go.Scatter(x=K_Ngay,y=K_Mean_BQ,mode='markers',marker=dict(color='blue', size=sizepoint),name='K_means'), row=1, col=1, secondary_y=False)
# D_Ngay = data_K_Mean['Ngay'][(data_K_Mean['Anomaly_D'] == 1 )&(data_K_Mean['Ngay'] >= pd.to_datetime(start_date)) & 
#                    (data_K_Mean['Ngay'] <= pd.to_datetime(end_date))]
# D_Mean_BQ = data_K_Mean['BQ'][(data_K_Mean['Anomaly_D'] == 1 )&(data_K_Mean['Ngay'] >= pd.to_datetime(start_date)) & 
#                    (data_K_Mean['Ngay'] <= pd.to_datetime(end_date))]

# fig.add_trace(go.Scatter(x=D_Ngay,y=D_Mean_BQ,mode='markers',marker=dict(color='blue', size=sizepoint),name='K_means'), row=1, col=1, secondary_y=False)    

# I_Ngay = data_K_Mean['Ngay'][(data_K_Mean['Anomaly_I'] == -1 )&(data_K_Mean['Ngay'] >= pd.to_datetime(start_date)) & 
#                    (data_K_Mean['Ngay'] <= pd.to_datetime(end_date))]
# I_Mean_BQ = data_K_Mean['BQ'][(data_K_Mean['Anomaly_I'] == -1 )&(data_K_Mean['Ngay'] >= pd.to_datetime(start_date)) & 
#                    (data_K_Mean['Ngay'] <= pd.to_datetime(end_date))]
# fig.add_trace(go.Scatter(x=I_Ngay,y=I_Mean_BQ,mode='markers',marker=dict(color='blue', size=sizepoint),name='I_means'), row=1, col=1, secondary_y=False)   

################################################################################################################
# Dữ liệu Chart 2
fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['TL_VNI'], mode='lines', name='Tỷ trọng', yaxis='y1',line_color = '#DAA520',line=dict(width=1)), row=2, col=1, secondary_y=False)
fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=[100]*len(filtered_df['Ngay']), mode='lines', name='100%', yaxis='y2',line_color = '#00008B',line=dict(width=1)), row=2, col=1, secondary_y=True)

if show_F_VNI:
     fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['F_TL_VNI'], mode='lines', name='F_TL_VNI', yaxis='y1',line_color = '#00008B',line=dict(width=1)), row=2, col=1, secondary_y=False)
if show_P1_P2:
    fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['P1/P2'], mode='lines', name='P_P1_P2', yaxis='y2',line_color = '#00008B',line=dict(width=1)), row=2, col=1, secondary_y=True)
if show_P_Ky2_BQ:
    fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['P_Ky2_BQ'], mode='lines', name='P_Ky2_BQ', yaxis='y2',line_color = '#8B0000',line=dict(width=1)), row=2, col=1, secondary_y=True)
if show_P_Ky1_BQ:
    fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['P_Ky1_BQ'], mode='lines', name='P_Ky1_BQ', yaxis='y2',line_color = '#00008B',line=dict(width=1)), row=2, col=1, secondary_y=True)
################################################################################################################
# Cấu hình layout cho biểu đồ với tự động điều chỉnh trục y và di chuyển legend xuống dưới cùng
fig.update_layout(
    title={
        'text': "Biểu đồ giá cổ phiếu và khối lượng giao dịch",
        'x': 0.5,  # Canh giữa tiêu đề theo trục x
        'xanchor': 'center',  # Đặt điểm neo là trung tâm theo trục x
        'y': 0.9  # Điều chỉnh khoảng cách của tiêu đề so với phần trên của biểu đồ
    },
    xaxis=dict(
        title={
            'text': "Ngày",
            'font': {
                'size': size_bold,
                'weight': 'bold'  # Tô đậm tiêu đề trục x
            }},
        rangeslider=dict(visible=False),  # Cho phép kéo và zoom theo trục x  / Tắt thanh trược khi kéo giãn biểu đồ
        type="date",  # Đảm bảo trục x là dạng thời gian
        showspikes=True,  # Hiển thị đường dọc (spike) trên trục x,
        spikesnap="cursor",  # Đường spike sẽ theo con trỏ chuột
        #type='category',  # Đặt trục x thành dạng phân loại để loại bỏ các khoảng trống xaxis=dict(type='category'): Khi cài đặt trục x ở chế độ category, Plotly sẽ coi mỗi ngày trong dữ liệu là một giá trị riêng biệt và không hiển thị khoảng trống cho các ngày không có dữ liệu.
        spikemode="across",  # Hiển thị spike đồng bộ theo trục x
    ),
    height=900,
    grid=dict(rows=2, columns=1, pattern="independent"),
    #row_heights=[0.5, 0.5],  # Cân bằng chiều cao giữa hai hàng (row 1 và row 2)
    autosize=True,  # Đảm bảo biểu đồ responsive
    yaxis=dict(
        #title="Giá cổ phiếu", 
        title={
            'text': "Giá cổ phiếu",
            'font': {
                'size': size_bold,
                'weight': 'bold'  # Tô đậm tiêu đề trục x
            }},
        side='left', 
        autorange=True,  # Tự động điều chỉnh trục y theo dữ liệu hiển thị
        showspikes=True,  # Hiển thị đường dọc (spike) trên trục y
        spikesnap="cursor",  # Đường spike sẽ theo con trỏ chuột
        spikemode="across",  # Hiển thị spike đồng bộ
    ),
    yaxis2=dict(
        title={
            'text': "Trạng thái quá bán",
            'font': {
                'size': size_bold,
                'weight': 'bold'  # Tô đậm tiêu đề trục x
            }},
        overlaying='y', 
        side='right', 
        autorange=True,  # Tự động điều chỉnh trục y2 theo dữ liệu hiển thị
        showgrid=False,  # Bỏ đường kẻ ngang của trục y2
        showspikes=True,
        spikesnap="cursor",
        spikemode="across",  # Hiển thị spike đồng bộ
    ),
    legend=dict(
        orientation="h",  # Đặt legend nằm ngang
        y=-0.1,  # Đặt legend nằm dưới cùng
        x=0.5,   # Canh giữa theo trục x
        xanchor='center',  # Đặt điểm neo là trung tâm theo trục x
        yanchor='top'  # Neo vào phía trên trục y
    ),
    # Thêm tiêu đề cho trục y chính và y phụ ở hàng thứ 2
    yaxis3=dict(
        title={
            'text': "Tỷ Trọng",
            'font': {
                'size': size_bold,
                'weight': 'bold'  # Tô đậm tiêu đề trục x
            }},  # Tiêu đề cho trục y chính (row 2)
        side='left',
        autorange=True,
        showspikes=True,
        spikesnap="cursor",
        spikemode="across",  # Hiển thị spike đồng bộ
    ),
    yaxis4=dict(
        title={
            'text': "Lực bán",
            'font': {
                'size': size_bold,
                'weight': 'bold'  # Tô đậm tiêu đề trục x
            }},  # Tiêu đề cho trục y phụ (row 2)
        overlaying='y3',
        side='right',
        autorange=True,
        showgrid=False,
        showspikes=True,
        spikesnap="cursor",
        spikemode="across",  # Hiển thị spike đồng bộ
    ),
        # Thêm tiêu đề cho trục y chính và y phụ ở hàng thứ 3
    yaxis5=dict(
        title={
            'text': "Tỷ Trọng",
            'font': {
                'size': size_bold,
                'weight': 'bold'  # Tô đậm tiêu đề trục x
            }},  # Tiêu đề cho trục y chính (row 2)
        side='left',
        autorange=True,
        showspikes=True,
        spikesnap="cursor",
        spikemode="across",  # Hiển thị spike đồng bộ
    ),
    dragmode='pan',  # Chế độ kéo dễ dàng qua lại
    hovermode="x unified",  # Hiển thị thông tin khi rê chuột đến
    spikedistance=-1,  # Hiển thị spike trên tất cả các hàng
    margin=dict(t=10, b=80, l=0, r=0)  # Điều chỉnh khoảng cách của biểu đồ so với các cạnh
    # t: Khoảng cách trên cùng của biểu đồ.
    # b: Khoảng cách dưới cùng của biểu đồ.
    # l: Khoảng cách bên trái của biểu đồ.
    # r: Khoảng cách bên phải của biểu đồ.
)

fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['BQ'], mode='lines', name='BQ', yaxis='y1',line_color = '#DAA520',line=dict(width=1)), row=3, col=1, secondary_y=False)
fig.add_trace(go.Scatter(x=filtered_df['Ngay'], y=filtered_df['Ky_2'], mode='lines', name='Ky_2', yaxis='y2',line_color = '#800080',line=dict(width=1)), row=3, col=1, secondary_y=True)

with col_R1:
    #st.plotly_chart(fig,use_container_width=True)
    # Sử dụng st.markdown để thêm CSS trực tiếp
    st.markdown("""
        <style>
            #plotly-chart {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 2000px;
            }
        </style>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)



results=svm(data_ai)

with col_P2:
    with st.popover(f"Độ chính xác {results['accuracy']*100:.2f}%"):
        # Hiển thị báo cáo phân loại
        st.subheader("Báo cáo phân loại")
        st.text(results["classification_report"])
        st.subheader("Ma trận nhầm lẫn")
        conf_matrix_df = pd.DataFrame(
            results["confusion_matrix"],
            columns=["Giảm (Thực)", "Tăng (Thực)"],
            index=["Giảm (Dự đoán)", "Tăng (Dự đoán)"]
        )
        # Hiển thị bảng và điều chỉnh độ rộng cột bằng cách thêm CSS
        st.markdown(
            """
            <style>
            .dataframe td, .dataframe th {
                padding: 10px;
                text-align: center;
            }
            .dataframe {
                width: 1500px;
                height: 500px;  /* Thêm chiều cao */
                
            }
            .dataframe .col0 {
                width: 250px;
            }
            .dataframe .col1 {
                width: 200px;
            }
            .dataframe .col2 {
                width: 200px;
            }
            </style>
            """, unsafe_allow_html=True
        )
        st.table(conf_matrix_df)

        st.subheader("Dự đoán cho 5 giao dịch gần nhất")
        future_predictions_df = pd.DataFrame({
            "Ngày": [f"{date}" for date in data_org['Ngay'].dt.strftime('%d/%m/%y')
.head(5)],
            "Dự đoán": ["Tăng" if pred == 1 else "Giảm" for pred in results["future_predictions"]]
        })
        st.table(future_predictions_df)
###################################################################################3
# # Đảo ngược dữ liệu để quét từ dưới lên
# data_sw = data_org.iloc[::-1]

# # 2. Xác định vùng sideway
# results = []
# start_date = None
# end_date = None
# low_price = float('inf')
# high_price = 0
# volume = 0

# for i, row in data_sw.iterrows():
#     price = row['BQ']
#     date = row['Ngay']
    
#     # Loại bỏ dấu phẩy trong giá trị KLGD và chuyển thành số
#     try:
#         # Kiểm tra kiểu dữ liệu và chuyển đổi KLGD
#         volume = float(str(row['KLGD']).replace(',', ''))  # Loại bỏ dấu phẩy và chuyển thành float
#     except ValueError:
#         volume = 0  # Nếu không thể chuyển đổi thì gán volume là 0
    
#     if start_date is None:  # Bắt đầu vùng mới
#         start_date = date
#         low_price = price
#         high_price = price
#     else:
#         # Trước khi sử dụng biến price, low_price, và high_price, hãy chuyển chúng thành kiểu số (float)
#         price = float(row['BQ'].replace(',', ''))  # Loại bỏ dấu phẩy và chuyển thành float
#         low_price = float(low_price.replace(',', '')) if isinstance(low_price, str) else low_price
#         high_price = float(high_price.replace(',', '')) if isinstance(high_price, str) else high_price
#         # Kiểm tra biên độ sideway
#         if abs(price - low_price) <= 0.05 * low_price and abs(price - high_price) <= 0.05 * high_price:
#             # Cập nhật vùng sideway
#             end_date = date
#             low_price = min(low_price, price)
#             high_price = max(high_price, price)
#             volume += float(row['KLGD'].replace(',', ''))  # Cộng thêm KLGD vào tổng volume, đảm bảo là số
#         else:
#             # Kết thúc vùng sideway
#             if end_date:
#                 # Tính số ngày trong vùng sideway (chênh lệch giữa Ngày bắt đầu và Ngày kết thúc)
#                 delta_days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
#                 results.append({
#                     "Ngày bắt đầu": start_date,
#                     "Ngày kết thúc": end_date,
#                     "KLGD": volume,
#                     "Giá thấp nhất": low_price,
#                     "Giá cao nhất": high_price,
#                     "Kỳ": delta_days  # Thêm cột "Kỳ"
#                 })
#             # Bắt đầu vùng mới
#             start_date = date
#             low_price = price
#             high_price = price
#             volume = float(row['KLGD'].replace(',', ''))  # Lưu lại KLGD đầu tiên của vùng mới
#             end_date = None

# # Lưu vùng cuối cùng (nếu có)
# if end_date:
#     # Tính số ngày trong vùng sideway (chênh lệch giữa Ngày bắt đầu và Ngày kết thúc)
#     delta_days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
#     results.append({
#         "Ngày bắt đầu": start_date,
#         "Ngày kết thúc": end_date,
#         "KLGD": volume,
#         "Giá thấp nhất": low_price,
#         "Giá cao nhất": high_price,
#         "Kỳ": delta_days  # Thêm cột "Kỳ"
#     })

# # Tạo DataFrame kết quả
# sideway_df = pd.DataFrame(results)

# # Hiển thị kết quả
# print("=== Báo cáo Vùng Sideway ===")
# st.write(sideway_df)

# Tạo giao diện Streamlit
#st.title("Biểu đồ Ichimoku trong Streamlit")

# # Áp dụng Ichimoku và tín hiệu giao dịch
# df = ichimoku(data_ai)
# df = generate_signals(data_ai)

# # Tạo một subplot (có 1 hàng và 1 cột)
# fig_ichi = make_subplots(rows=1, cols=1)

# # Vẽ các đường Ichimoku trên subplot
# fig_ichi.add_trace(go.Scatter(x=df['Ngay'], y=df['BQ'], mode='lines', name='Close Price', line=dict(color='black', width=0.25)))
# fig_ichi.add_trace(go.Scatter(x=df['Ngay'], y=df['Tenkan-sen'], mode='lines', name='Tenkan-sen (9)', line=dict(color='red', width=0.25)))
# fig_ichi.add_trace(go.Scatter(x=df['Ngay'], y=df['Kijun-sen'], mode='lines', name='Kijun-sen (26)', line=dict(color='blue', width=0.25)))
# fig_ichi.add_trace(go.Scatter(x=df['Ngay'], y=df['Senkou Span A'], mode='lines', name='Senkou Span A', line=dict(color='green', dash='dash', width=0.25)))
# fig_ichi.add_trace(go.Scatter(x=df['Ngay'], y=df['Senkou Span B'], mode='lines', name='Senkou Span B', line=dict(color='brown', dash='dash', width=0.25)))

# # Tô màu khu vực của Senkou Span A và B
# fig_ichi.add_trace(go.Scatter(x=df['Ngay'], y=df['Senkou Span A'], mode='lines', fill='tonexty', name='Senkou Span Area', fillcolor='rgba(144, 238, 144, 0.4)', line=dict(width=0)))

# fig_ichi.add_trace(go.Scatter(x=df['Ngay'], y=df['Senkou Span B'], mode='lines', fill='tonexty', name='Senkou Span Area', fillcolor='rgba(255, 99, 71, 0.4)', line=dict(width=0)))

# # Cập nhật layout để có trục x là ngày tháng và điều chỉnh kích thước
# fig_ichi.update_layout(
#     title='Ichimoku Cloud',
#     xaxis_title='Date',
#     yaxis_title='Price',
#     xaxis=dict(
#         tickformat='%b %Y',  # Chỉ hiển thị tháng và năm
#         tickangle=45,
#         autorange='reversed',  # Đảo ngược trục x để hiển thị từ cuối df lên trên
#         #type="date",  # Đảm bảo trục x là dạng thời gian
#     ),
#     height=800,  # Chiều cao của biểu đồ
# )

# # Hiển thị biểu đồ trong Streamlit
# st.plotly_chart(fig_ichi)
# # Hiển thị DataFrame trong Streamlit
# st.dataframe(df)






