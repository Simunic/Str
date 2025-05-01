import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Tạo DataFrame từ dữ liệu
data = {
    "Ngày tháng": ["04/11/2024", "01/11/2024", "31/10/2024", "30/10/2024", "29/10/2024", "28/10/2024"],
    "GT": [118787000, 70207000, 51425000, 68495000, 199309000, 76844000],
    "KLGG": [3276700, 1891900, 1370500, 1817500, 5266600, 2076700],
    "Bình quân": [36252, 37109, 37523, 37686, 37844, 37003],
    "Ky_1": [71, 71, 71, 70, 69, 69],
    "BQ_Ky1": [37348, 37333, 37305, 37304, 37301, 37265],
    "Ky_2": [106, 106, 105, 104, 104, 104],
    "BQ_Ky2": [37526, 37519, 37521, 37521, 37511, 37502],
    "BQ_KY1/BQ_KY2": ["99,52%", "99,51%", "99,43%", "99,42%", "99,44%", "99,37%"],
    "Target_1": ["100,0197%", "100,0794%", "100,0031%", "99,9829%", "100,0708%", "99,9945%"],
    "Tinhieu_1": [-1, 0, 0, 0, 0, 0],
    "Check": [0, 0, 0, 0, 0, 0],
    "Gross": [-36252, None, None, None, None, None]
}

df = pd.DataFrame(data)

# Chuyển đổi cột 'Ngày tháng' thành kiểu datetime để hỗ trợ trực quan hóa
df['Ngày tháng'] = pd.to_datetime(df['Ngày tháng'], format='%d/%m/%Y')

# Tạo biểu đồ line cho cột 'Bình quân'
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Ngày tháng'], df['Bình quân'], marker='o', label='Bình quân', color='b')

# Đánh dấu các ngày có giá trị Gross khác 0 với chấm tròn đỏ
highlight_dates = df['Ngày tháng'][df['Gross'].notna()]
highlight_values = df['Bình quân'][df['Gross'].notna()]

# Vẽ scatter chỉ khi có dữ liệu hợp lệ
if not highlight_dates.empty and not highlight_values.empty:
    ax.scatter(highlight_dates, highlight_values, color='red', s=100, zorder=5, label="Gross khác 0")

# Cài đặt nhãn và tiêu đề
ax.set_xlabel('Ngày tháng')
ax.set_ylabel('Bình quân')
ax.set_title('Biểu đồ Line của cột Bình quân với dấu chấm tròn cho ngày có Gross khác 0')
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)

# Hiển thị biểu đồ trong Streamlit
st.pyplot(fig)