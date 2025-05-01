import pandas as pd
from scipy.stats import pearsonr
import streamlit as st

# Tạo DataFrame mẫu
data = {
    'BQ': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'Minus': [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]
}
df = pd.DataFrame(data)

# Hàm tính hệ số tương quan Pearson động theo từng dòng (dữ liệu từ dòng hiện tại đến dòng cuối)
def dynamic_pearson(df, column1, column2):
    # Khởi tạo cột 'Pea' trong DataFrame để lưu giá trị Pearson
    df['Pea'] = None
    
    for i in range(len(df)):  # Bắt đầu từ dòng đầu tiên đến dòng cuối
        # Lấy dữ liệu từ dòng i đến dòng cuối
        x = df[column1][i:]  # Dữ liệu từ dòng i đến cuối
        y = df[column2][i:]  # Dữ liệu từ dòng i đến cuối
        
        # Tính hệ số tương quan Pearson cho cửa sổ hiện tại
        if len(x) > 1:  # Chỉ tính khi có ít nhất 2 giá trị
            corr, _ = pearsonr(x, y)  # Tính Pearson và lấy hệ số tương quan
            df.at[i, 'Pea'] = corr  # Gán giá trị Pearson vào cột 'Pea'
        else:
            df.at[i, 'Pea'] = None  # Nếu không đủ dữ liệu, trả về None
    
    return df

# Tính hệ số tương quan Pearson động theo từng dòng
df = dynamic_pearson(df, 'BQ', 'Minus')

# Hiển thị kết quả
st.write(df)