import streamlit as st
import pandas as pd
from var import *
import json
import os
import numpy as np
#from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
#from xgboost import XGBRegressor
#from sklearn.metrics import mean_squared_error
#import sklearn
#import xgboost as xgb
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
# Tạo hàm để thêm CSS tùy chỉnh
def add_custom_css():
    st.markdown(
    """
    <style>
    /* Điều chỉnh khoảng cách từ phần đầu trang */
    .main > div {
        padding-top: 15px; /* Giảm khoảng cách top */
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
# định dạng cho dữ liệu HTML
def row_highlight(df):
    # Tạo bảng HTML
    html = df.to_html(index=False,classes='dataframe')
    
    # Thay đổi CSS cho dòng đầu tiên
    html = html.replace(
        '<tr style="text-align: right;">',
        '<tr style="text-align: center; background-color: #FFFF00; font-family: \'Times New Roman\', Times, serif;">', 1
    )
    
    # Format dữ liệu bảng
    # Thêm div để kiểm soát kích thước và thanh cuộn  => check kiến thức bên html để đưa thêm vào định dạng
    html = f"""
    <div class="tabledata force-overflow" style="max-height: 400px; max-width: 400px; overflow: auto; border: 1px solid #ddd;">
        {html}
    </div> 
    <style>
        /* Điều chỉnh thanh cuộn */
        .tabledata {{
            background-color: #F5F5F5;
            float: left;
            height: 300px;
            margin-bottom: 25px;
            margin-left: 22px;
            margin-top: 40px;
            width: 100%; /* Điều chỉnh độ rổng của bảng */ 
            overflow-y: scroll;
        }}

        .force-overflow {{
            min-height: 450px;
        }}

        .tabledata::-webkit-scrollbar {{
            width: 16px;
        }}

        .tabledata::-webkit-scrollbar-track {{
            background-color: #e4e4e4;
            border-radius: 100px;
        }}

        .tabledata::-webkit-scrollbar-thumb {{
            background-color: #d4aa70;
            border-radius: 100px;
        }}
        /* CSS cho bảng */
        .tabledata table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            margin: 0;  /* Loại bỏ margin nếu cần */
            padding: 0;  /* Loại bỏ padding nếu cần */
        }}
        /* th áp dụng cho tiêu đề, td áp dụng cho dữ liệu trong bảng
        /* Áp dụng CSS cho tiêu đề bảng */
        .tabledata table th {{
            background-color: #FF0000 !important;  /* Màu nền tiêu đề đỏ */
            color: #FFFFFF !important;             /* Màu chữ tiêu đề trắng */
            font-family: "Times New Roman", Times, serif !important; /* Font chữ tiêu đề */
            font-weight: bold !important; /* Đậm chữ tiêu đề */
            text-align: center !important; /* Căn giữa chữ tiêu đề */
            line-height: 1.5; /* Điều chỉnh độ cao dòng tiêu đề */
            height: 30px; /* Điều chỉnh độ cao cụ thể cho dòng tiêu đề */
            position: sticky; /* Cố định vị trí dòng tiêu đề */
            top: 0; /* Cố định ở đầu bảng */
            z-index: 1000; /* Đảm bảo tiêu đề luôn nằm trên các thành phần khác */
        }}
        
        .tabledata table td {{
            width: 150px;  /* Chiều rộng cột mặc định */
            text-align: right;  /* Canh lề phải cho dữ liệu số */
            line-height: 0.5; /* Điều chỉnh độ cao dòng */
            height: 25px; /* Điều chỉnh độ cao cụ thể cho dòng */
            font-size: 15px; /* Font chữ 10 cho dữ liệu */
            color: #0000FF; /* Màu chữ xanh cho dữ liệu */
        }}
        
        .tabledata tr:nth-child(even) {{
            background-color: #f2f2f2; /*Thêm nền khác nhau cho các dòng chẵn để dễ phân biệt các dòng dữ liệu*/
        }}
        
        

    </style>
    """
    return html 

# Định dạng các cột số theo kiểu #.###
def format_number(x):
    if isinstance(x, (int, float)):
        return f"{x:,.0f}"
    return x

format_dict = {col: format_number for col in columns_to_format}

# định dạng %
def format_percentage(value, decimals=2):
    percentage = f"{value * 100:.{decimals}f}%"
    return percentage

# Hàm áp dụng màu nền cho từng cột
def color_columns(col):
    color = column_colors.get(col.name, '')  # Lấy màu từ từ điển, mặc định là màu trắng nếu không có màu
    return [f'background-color: {color}' for _ in col]
    
# Định dạng Dataframe trong streamlit
def style_dataframe(df):
    columns_to_percent = ['P1/P2', 'BQ/P3','P_Ky1_BQ','P_Ky2_BQ','Sign01','Sign02','KL_Per','KL_Per_1','TL_VNI','Pea_Per','Minus_Per','F_TL_VNI','TB_canbang']
    for col in columns_to_percent:
        df[col] = df[col].apply(format_percentage)
    #df[columns_to_percent]=df[columns_to_percent].apply(format_percentage)

    #df[columns_to_format] = df[columns_to_format].apply(lambda x: x.apply(lambda y: f"{y:,}" if isinstance(y, (int, float)) else y))

    df['Ngay'] = pd.to_datetime(df['Ngay'], format='%d/%m/%y', errors='coerce')
    # Chỉ lấy phần ngày, bỏ giờ
    df['Ngay'] = df['Ngay'].dt.strftime('%d/%m/%y')
    # Định dạng các cột số
    for col in columns_to_format:
           df[col] = df[col].apply(lambda x: '{:,.0f}'.format(x) if isinstance(x, (int,float)) else x)
           #df[col] = df[col].fillna(0)  # Thay NaN bằng 0
           #df[col] = df[col].apply(lambda x: int(x) if isinstance(x, (int, float)) else x)
    # Ẩn cột
    df = df.drop(columns=columns_to_hide)

    styles = [
        {
            'selector': 'th',
            'props': [
                ('background-color', '#4CAF50'),
                ('color', 'white'),
                ('font-family', 'Arial, sans-serif'),
                ('font-size', '16px'),
                ('position', 'sticky'),  # Làm cho tiêu đề cố định
                ('top', '0'),  # Vị trí cố định ở trên cùng
                ('z-index', '1'),  # Đảm bảo tiêu đề nằm trên các nội dung khác khi cuộn
                ('text-align', 'center')  # Căn giữa tiêu đề
            ]
        },
        {
            'selector': 'td, th',
            'props': [
                ('border', '2px solid #4CAF50'),
                ('height', '15px'),  # Điều chỉnh độ cao của mỗi ô
                ('font-size', '14px'),  # Điều chỉnh cỡ chữ cho tất cả các ô dữ liệu
                ('padding', '2px')  # Điều chỉnh padding cho tiêu đề cột
            ]
        },
        {
            'selector': 'td',
            'props': [
                ('text-align', 'right'),  # Căn lề phải cho tất cả các ô dữ liệu
                ('color', 'blue')  # Màu chữ là màu xanh nước biển
            ]
        },
    ]
    
    
    ## Áp dụng style
    df = df.style.set_table_styles(styles).apply(color_columns, axis=0).hide(axis='index').to_html(index=False)
    
    # Sử dụng một div để tạo thanh cuộn
    scrollable_div = f"""
    <div style='overflow: auto; height: 300px; border: 1px solid #ddd;; padding: 0;'>
        <style>
            /* CSS tùy chỉnh cho thanh cuộn */
            div::-webkit-scrollbar {{
                width: 12px;
                height: 12px;
            }}
            div::-webkit-scrollbar-thumb {{
                background-color: #4CAF50; /* Màu của thanh cuộn */
                border-radius: 10px;
            }}
            div::-webkit-scrollbar-track {{
                background: #f1f1f1;
            }}
            /* CSS để đảm bảo bảng tự động fit với bảng và hiển thị thanh cuộn */
            table {{
                width: 100%; /* Đảm bảo bảng chiếm hết chiều rộng của div */
            }}
            /* CSS để điều chỉnh độ cao của dòng */
            tr {{
                height: 5px; /* Điều chỉnh độ cao của mỗi dòng dữ liệu */
            }}
            /* CSS để điều chỉnh độ rộng của mỗi cột */
            .dataframe th.colSTT, .dataframe td.colSTT {{
                min-width: 20px;
            }}
            .dataframe th.colNgay, .dataframe td.colNgay {{
                min-width: 80px;
            }}
            .dataframe th.colGTGD, .dataframe td.colGTGD {{
                min-width: 120px;
            }}
            .dataframe th.colKLGD, .dataframe td.colKLGD {{
                min-width: 120px;
            }}
            .dataframe th.colKQ_Sign01, .dataframe td.colKQ_Sign01 {{
                min-width: 80px;
            }}
        </style>
        {df}
    </div>
    """
    
    return scrollable_div
 
# Đọc dữ liệu từ file JSON với mã hóa chính xác
def load_data_from_json(file_path, encoding='utf-8'):
    try:
        with open(file_path, "r", encoding=encoding) as file:
            content = file.read().strip()
            if content:
                return json.loads(content)
            else:
                st.error("Tệp JSON trống.")
                return {"data": []}  # Trả về dữ liệu mặc định nếu tệp trống
    except UnicodeDecodeError as e:
        st.error(f"Lỗi mã hóa: {e}")
        return {"data": []}  # Trả về dữ liệu mặc định nếu có lỗi mã hóa
    except json.JSONDecodeError as e:
        st.error(f"Lỗi phân tích JSON: {e}")
        return {"data": []}  # Trả về dữ liệu mặc định nếu có lỗi phân tích
    except Exception as e:
        st.error(f"Lỗi khi đọc tệp JSON: {e}")
        return {"data": []}

# Hàm để lưu dữ liệu vào file JSON
def save_data_to_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Chuyển dữ liệu thành DataFrame
def data_to_dataframe(data):
    return pd.DataFrame(data["data"])

# Tạo bảng dữ liệu với màu sắc cho cột 2 chỉ tại dòng có giá trị name_to_update
# def style_frame(df, color_mapping,cot):
#     def color_row(row):
#         color = color_mapping.get(row['name'], 'white')
#         return ['background-color: {}'.format(color) if col == cot else '' for col in df.columns]
#     return df.style.apply(color_row, axis=1)

def style_frame(df, color_mapping, cot1, cot2):
    
    def color_row(row):
        color1 = color_mapping[cot1].get(row['name'], 'white')  # Màu cho cột cot1
        color2 = color_mapping[cot2].get(row['name'], 'white')  # Màu cho cột cot2
        return [
            'background-color: {}'.format(color1) if col == cot1 else
            'background-color: {}'.format(color2) if col == cot2 else '' 
            for col in df.columns
        ]
    # Áp dụng định dạng cơ bản và màu sắc cho các ô
    styled_df = df.style.apply(color_row, axis=1)
    
    # Áp dụng CSS cho độ rộng và kẻ khung
    # styled_df = styled_df.set_table_styles(
    #     [
    #         {'selector': 'th', 'props': [('border', '1px solid black'), ('width', '200px'), ('text-align', 'center')]},
    #         {'selector': 'td', 'props': [('border', '1px solid black'), ('width', '200px'), ('text-align', 'center')]}
    #     ]
    # )
    
    return styled_df

# Hàm để chuyển đổi giá trị thành số nguyên
def convert_to_integer(data):
    for entry in data["data"]:
        if "column_2" in entry:
            try:
                entry["column_2"] = "{:,}".format(int(float(entry["column_2"])))
            except ValueError:
                entry["column_2"] = "0"  # Giá trị mặc định nếu không thể chuyển đổi
        if "column_3" in entry:
            try:
                entry["column_3"] = "{:,}".format(int(float(entry["column_3"])))
            except ValueError:
                entry["column_3"] = "0"  # Giá trị mặc định nếu không thể chuyển đổi
    return data

# Chia DataFrame thành 3 phần
def split_dataframe(df, num_parts=7):
    return np.array_split(df, num_parts)

def add_scrollable_table(html_table):
    return f"""
    <div style="overflow-x: auto; max-width: 100%; border: 1px solid #ddd; padding: 10px;">
        {html_table}
    </div>
    """
def display_in_columns(styled_parts):
    cols = st.columns(len(styled_parts), gap="medium")
    for col, styled_html in zip(cols, styled_parts):
        with col:
            # Chuyển đổi Styled DataFrame thành HTML nếu cần
            if hasattr(styled_html, "to_html"):
                styled_html = styled_html.to_html()
            st.write(add_scrollable_table(styled_html), unsafe_allow_html=True)

# Hàm tính hệ số tương quan Pearson động theo từng dòng (dữ liệu từ dòng hiện tại đến dòng cuối)
def dynamic_pearson(df, column1, column2):
    # Khởi tạo cột 'Pea' trong DataFrame để lưu giá trị Pearson
    df['Pea'] = None
    
    for i in range(len(df)):  # Bắt đầu từ dòng đầu tiên đến dòng cuối
        # Lấy dữ liệu từ dòng i đến dòng cuối
        x = df[column1][i:]  # Dữ liệu từ dòng i đến cuối
        y = df[column2][i:] # Dữ liệu từ dòng i đến cuối
        
        # Tính hệ số tương quan Pearson cho cửa sổ hiện tại
        if len(x) > 1:  # Chỉ tính khi có ít nhất 2 giá trị
            corr, _ = pearsonr(x, y)  # Tính Pearson và lấy hệ số tương quan
            df.at[i, 'Pea'] = corr  # Gán giá trị Pearson vào cột 'Pea'
        else:
            df.at[i, 'Pea'] = None  # Nếu không đủ dữ liệu, trả về None
    
    return df
def adj_minus(train_test_data):
    #train_test_data = df.head('Ky_2')
    x = train_test_data[['BQ_Minus','BQ_Add','KL_Minus','KL_Add','BQ_CL','KL_Sum2','TL_VNI']]
    y = train_test_data['Minus'].values
    # 6. Chia dữ liệu thành tập huấn luyện và kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = HistGradientBoostingRegressor()
    model.fit(X_train, y_train)
    # Dự đoán
    y_pred = model.predict(X_test)
    return y_pred

def svm(df):
    #df['BQ_CL'] = df['BQ_CL'].fillna(0)
    future_data = df.head(5)  # 20 giao dịch cần dự đoán
    train_test_data = df.iloc[6:]  # Dữ liệu train và test
    # Định nghĩa tập đặc trưng và nhãn
    x = train_test_data[['KLGD', 'BQ', 'P_Ky1', 'P_Ky2','KL_Per','TL_VNI','P_Ky2_BQ','P1/P2','Sign01','Sign02']].values
    #y = np.where(train_test_data['BQ_CL'])
    y = np.where(train_test_data['BQ_CL'] > 0, 1, 0)
    future_data_scaled = future_data[['KLGD', 'BQ', 'P_Ky1', 'P_Ky2','KL_Per','TL_VNI','P_Ky2_BQ','P1/P2','Sign01','Sign02']].values
    # 6. Chia dữ liệu thành tập huấn luyện và kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    # 4. Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    future_data_scaled = scaler.transform(future_data_scaled)
    # 7. Huấn luyện mô hình SVM
    model = SVC(kernel='linear', random_state=42)
    model.fit(X_train_scaled, y_train)
    # 1. Dự đoán trên tập kiểm tra
    y_test_pred = model.predict(X_test_scaled)
    
    # 2. Tính toán độ chính xác
    accuracy = accuracy_score(y_test, y_test_pred)
    #print(f"Accuracy: {accuracy:.2f}")

    
    
    # 6. Dự đoán trên 20 giao dịch gần nhất
    future_predictions = model.predict(future_data_scaled)
    # 3. Báo cáo phân loại
    classification_rep = classification_report(y_test, y_test_pred, target_names=["Giảm", "Tăng"])
    #print("Classification Report:")
    #print(classification_rep)

    # 4. Ma trận nhầm lẫn
    conf_matrix = confusion_matrix(y_test, y_test_pred)
    
    return {
        "accuracy": accuracy,
        "classification_report": classification_rep,
        "confusion_matrix": conf_matrix,
        "future_predictions": future_predictions,
    }

import sqlite3
def init_db():
    conn = sqlite3.connect('data/stock_trades.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_code TEXT,
            trade_date TEXT,
            trade_type TEXT,
            quantity INTEGER,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_trade(stock_code, trade_date, trade_type, quantity, price):
     # Tính Amount = quantity * price
    amount = quantity * price
    conn = sqlite3.connect('data/stock_trades.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO trades (stock_code, trade_date, trade_type, quantity, price)
        VALUES (?, ?, ?, ?, ?)
    ''', (stock_code, trade_date, trade_type, quantity, price))
    conn.commit()
    conn.close()

def get_trades():
    conn = sqlite3.connect('data/stock_trades.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM trades')
    trades = cursor.fetchall()
    conn.close()
    return trades

# Hàm tính toán các đường Ichimoku
def ichimoku(df, period_tenkan=9, period_kijun=26, period_senkou=52, shift_senkou=26):
    df['Tenkan-sen'] = (df['BQ'].rolling(window=period_tenkan).max() + df['BQ'].rolling(window=period_tenkan).min()) / 2
    df['Kijun-sen'] = (df['BQ'].rolling(window=period_kijun).max() + df['BQ'].rolling(window=period_kijun).min()) / 2
    df['Senkou Span A'] = ((df['Tenkan-sen'] + df['Kijun-sen']) / 2).shift(shift_senkou)
    df['Senkou Span B'] = ((df['BQ'].rolling(window=period_senkou).max() + df['BQ'].rolling(window=period_senkou).min()) / 2).shift(shift_senkou)
    df['Chikou Span'] = df['BQ'].shift(-shift_senkou)  # Dịch lùi về sau
    return df

# Hàm xác định tín hiệu mua/bán
def generate_signals(df):
    df['Buy Signal'] = (df['Tenkan-sen'] > df['Kijun-sen']) & (df['BQ'] > df['Senkou Span A']) & (df['BQ'] > df['Senkou Span B'])
    df['Sell Signal'] = (df['Tenkan-sen'] < df['Kijun-sen']) & (df['BQ'] < df['Senkou Span A']) & (df['BQ'] < df['Senkou Span B'])
    return df

# Đường dẫn tới file lưu trữ ghi chú
notes_file = "notes.json"
def load_notes():
    if os.path.exists(notes_file):
        with open(notes_file, "r") as f:
            return json.load(f)
    else:
        return {}
# Hàm lưu ghi chú vào file JSON
def save_notes(notes):
    with open(notes_file, "w") as f:
        json.dump(notes, f)
# Hàm xóa ghi chú theo ID
def delete_note(note_id):
    notes = load_notes()
    if note_id in notes:
        del notes[note_id]
        save_notes(notes)

# Định dạng màu sắc cho cột TB_canbang
def highlight_tb_canbang(val):
    """
    Định dạng màu sắc cho giá trị:
    - Màu xanh lá cây nếu giá trị > 0
    - Màu đỏ nếu giá trị <= 0
    """
    color = 'green' if val > 0 else 'red'
    return f'color: {color}'