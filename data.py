#import pandas as pd
from var import *
from func import *
from scipy.stats import pearsonr
#from sklearn.model_selection import train_test_split
#from xgboost import XGBRegressor
#from sklearn.ensemble import HistGradientBoostingRegressor
#from sklearn.model_selection import train_test_split
#from xgboost import XGBRegressor
#from sklearn.metrics import mean_squared_error
#import sklearn
#import xgboost as xgb
#from sklearn.ensemble import HistGradientBoostingRegressor
file_path = 'data/Stock_Data_1.xlsm'
def load_data(sheet_name):
    import os
    if not os.path.exists(file_path):
        st.error(f"❌ Không tìm thấy file tại: {file_path}")
        st.stop() 
    
    # Đọc dữ liệu từ file Excel
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        skiprows=3,
        usecols='B:D',
        names=column_names,
        engine='openpyxl'
    )

    vni = pd.read_excel(
        file_path,
        sheet_name='KL_VN',
        skiprows=3,
        usecols='B:D',
        names=column_names,
        engine='openpyxl'
    )
    # Loại bỏ dòng đầu tiên và đặt tên cột chỉ mục là 'STT'
    df = df.drop(df.index[0]).reset_index(drop=False)
    df.rename(columns={'index': 'STT'}, inplace=True)

    # Định dạng cột ngày
    df['Ngay'] = pd.to_datetime(df['Ngay'], format='%d/%m/%Y', errors='coerce')
    df['Ngay'] = df['Ngay'].dt.strftime('%d/%m/%y')  # Chỉnh sửa để hiển thị năm 2 chữ số
    
    # Định dạng các cột số
    df['KLGD'] = df['KLGD'].astype(str)
    df['KLGD'] = df['KLGD'].str.replace(r'[\s,]', '', regex=True)
    df['KLGD'] = pd.to_numeric(df['KLGD'], errors='coerce')
    df['GTGD'] = df['GTGD'].astype(str)
    df['GTGD'] = df['GTGD'].str.replace(r'[\s,]', '', regex=True)
    df['GTGD'] = pd.to_numeric(df['GTGD'], errors='coerce')
    # Tạo cột Bình Quân
    df['BQ'] = df['GTGD']/df['KLGD']*1000
    df['BQ'] = pd.to_numeric(df['BQ'], errors='coerce').fillna(0).astype(int)
    df['BQ_CL'] = df['BQ'] - df['BQ'].shift(-1)
    df['BQ_CL'] = df['BQ_CL'].astype(str).str.replace(',', '', regex=False)
    df['BQ_CL'] = df['BQ_CL'].fillna(0)
    df['BQ_CL'] = pd.to_numeric(df['BQ_CL'], errors='coerce') 

    # Tạo cột Ky_1
    threshold_1 = data_klgd.loc[data_klgd['Ma_CP']==sheet_name, 'KL_1'].values[0]
    klgg_1 = 0
    Ky_1_value = [0]*len(df)
    for i in range(len(df)):
        klgg_1 = 0
        count = 0
        for j in range(i, len(df)):
            klgg_1 += df.loc[j, 'KLGD']
            count += 1
            if klgg_1 > threshold_1:
                break
        Ky_1_value[i] = count
    
    df['Ky_1'] = Ky_1_value

    # Tạo cột Ky_2
    threshold_2 = data_klgd.loc[data_klgd['Ma_CP']==sheet_name, 'KL_2'].values[0]
    klgg_2 = 0
    Ky_2_value = [0]*len(df)
    for i in range(len(df)):
        klgg_2 = 0
        count = 0
        for j in range(i, len(df)):
            klgg_2 += df.loc[j, 'KLGD']
            count += 1
            if klgg_2 > threshold_2:
                break
        Ky_2_value[i] = count
    
    df['Ky_2'] = Ky_2_value

    # Khởi tạo cột kết quả

    Ky_Sum = []
    BQ_Sum = []
    for i in range(len(df)):
        # Lấy tổng hiện tại
        current_sum = df.loc[i:i + df.loc[i, 'Ky_2'] - 1, 'BQ_CL'].sum()
        
        # Nếu tổng >= 0, lưu kết quả
        if current_sum >= 0:
            Ky_Sum.append(df.loc[i, 'Ky_2'])
            BQ_Sum.append(current_sum)
        else:
            # Cộng dần các giá trị BQ_CL bên dưới cho đến khi >= 0
            total = current_sum
            j = i + df.loc[i, 'Ky_2']  # Bắt đầu từ dòng tiếp theo sau phạm vi Ky_2
            while total < 0 and j < len(df):
                total += df.loc[j, 'BQ_CL']
                j += 1
            Ky_Sum.append(j-i)  # Lưu kết quả sau khi đạt >= 0 hoặc hết dòng
            BQ_Sum.append(total)

    # Gán cột kết quả vào DataFrame
    df['Ky_Sum'] = Ky_Sum
    df['BQ_Sum'] = BQ_Sum

    #Tạo cột tính tổng giá trị từ dòng hiện tại đến dòng Ky_2
    
    df['KL_Sum'] = [df.loc[i:i+df.loc[i, 'Ky_Sum'] - 1, 'KLGD'][df.loc[i:i + df.loc[i, 'Ky_Sum'] - 1, 'BQ_CL'] < 0].sum() for i in range(len(df))]
    df['KL_Sum2'] = [df.loc[i:i+df.loc[i, 'Ky_Sum'] - 1, 'KLGD'].sum() for i in range(len(df))]
    df['KL_Per']=1-df['KL_Sum']/df['KL_Sum2']
    df['KL_Per'] = df['KL_Per'].replace([float('inf'), -float('inf')], 0)  # Xử lý chia cho 0
    # Điền giá trị từ dòng trên nếu KL_Per == 0
    df['KL_Per'] = df['KL_Per'].replace(0, pd.NA).fillna(method='ffill')
    for i in range(len(df)):
        if df.loc[i,'Ky_Sum'] > df.loc[i,'Ky_2']:
            for a in range(df.loc[i,'Ky_2'],df.loc[i,'Ky_Sum']-1):
                w = df.loc[i:i+a, 'KLGD'][df.loc[i:i+a, 'BQ_CL'] < 0].sum()
                z = df.loc[i:i+a, 'KLGD'].sum()
                t = 1-w/z
                if t<df.loc[i,'KL_Per']:
                    df.loc[i,'KL_Per'] = t

    df['Pea_Per'] = 1
    for i in range(len(df)):  # Bắt đầu từ dòng đầu tiên đến dòng cuối
        # Lấy dữ liệu từ dòng i đến dòng cuối
        x = df['BQ'][i:i+df.loc[i, 'Ky_Sum'] - 1]  # Dữ liệu từ dòng i đến cuối
        y = df['KL_Per'][i:i+df.loc[i, 'Ky_Sum'] - 1] # Dữ liệu từ dòng i đến cuối
        
        # Tính hệ số tương quan Pearson cho cửa sổ hiện tại
        if len(x) > 1:  # Chỉ tính khi có ít nhất 2 giá trị
            corr, _ = pearsonr(x, y)  # Tính Pearson và lấy hệ số tương quan
            df.at[i, 'Pea_Per'] = corr  # Gán giá trị Pearson vào cột 'Pea'
        else:
            df.at[i, 'Pea_Per'] = None  # Nếu không đủ dữ liệu, trả về None
    
    #Tạo cột tính tổng giá trị từ dòng hiện tại đến dòng Ky_2
    df['KL_Sum_1'] = [df.loc[i:i+df.loc[i, 'Ky_2'] - Ky, 'KLGD'][df.loc[i:i + df.loc[i, 'Ky_2'] - Ky, 'BQ_CL'] < 0].sum() for i in range(len(df))]
    df['KL_Sum2_1'] = [df.loc[i:i+df.loc[i, 'Ky_2'] - Ky, 'KLGD'].sum() for i in range(len(df))]
    df['KL_Per_1']=1-df['KL_Sum_1']/df['KL_Sum2_1']
    df['KL_Per_1'] = df['KL_Per_1'].replace([float('inf'), -float('inf')], 0)  # Xử lý chia cho 0
    # Điền giá trị từ dòng trên nếu KL_Per == 0
    df['KL_Per_1'] = df['KL_Per_1'].replace(0, pd.NA).fillna(method='ffill')

    # Tạo cột giá bình quân theo Kỳ 1
    df['P_Ky1'] = float('nan')
    # Tính toán và gán giá trị cho cột 'BinhQuan' dựa trên cột 'Ky_1'
    for i in range(len(df)):
        num_rows = df.loc[i, 'Ky_1']
        sum_klgd = df['GTGD'][i:i+num_rows].sum()/df['KLGD'][i:i+num_rows].sum()
        df.at[i, 'P_Ky1'] = sum_klgd*1000

    df['P_Ky1_BQ']=df['BQ']/df['P_Ky1']

    # Tạo cột giá bình quân theo Kỳ 2
    df['P_Ky2'] = float('nan')
    for i in range(len(df)):
        num_rows = df.loc[i, 'Ky_2']
        sum_klgd = df['GTGD'][i:i+num_rows].sum()/df['KLGD'][i:i+num_rows].sum()
        df.at[i, 'P_Ky2'] = sum_klgd*1000
    df['P_Ky2_BQ']=df['BQ']/df['P_Ky2']

    # Tạo cột Sign01
    df['P1/P2'] = df['P_Ky1']/df['P_Ky2']
    df['Sign01'] = df['P1/P2']/df['P1/P2'].shift(-1)
    df['Sign01'] = df['Sign01'].fillna(100)
    
    # Lặp từ dòng cuối cùng lên dòng đầu tiên để lấy kết quả lãi lỗ tín hiện P1/P2
    for i in range(len(df)-1, -1, -1):
        if df.loc[i, 'P_Ky1'] == df.loc[i, 'P_Ky2']:
        # Gán giá trị bằng 0 cho 3 dòng cuối cùng
            df.loc[i, 'S01_1'] = 0
            df.loc[i, 'S01_2'] = 0
        else:
            # Tính tổng tích lũy từ dòng kế tiếp đến dòng cuối cùng trừ giá trị tại dòng hiện tại
            if i>=0:
                cumsum_reverse = df['S01_1'][::-1].shift(1).cumsum()[::-1]
                df.loc[i, 'S01_2'] = min(0,cumsum_reverse[i])
            
            if df['Sign01'][i] < 1 and df['Sign01'][i+1] < 1 and df['Sign01'][i+2] < 1 and df['S01_2'][i] == -1:
                df.loc[i, 'S01_1'] = 1
            elif df['Sign01'][i] >= 1 and df['Sign01'][i+1] >= 1 and df['Sign01'][i+2] >= 1 and df['S01_2'][i] == 0:
                df.loc[i, 'S01_1'] = -1
            else:
                df.loc[i, 'S01_1'] = 0  
    
    df['S01_2'] = df['S01_2'].fillna(method='bfill')
    #df['S01_1'] = df['S01_1'].astype(int)
    df['KQ_Sign01']=df['S01_1']*df['BQ']
    #df['KQ_Sign01'] = pd.to_numeric(df['KQ_Sign01'], errors='coerce')
    #df = df.dropna(subset=['KQ_Sign01'])
    df['R1'] = int()
    for i in range(len(df) - 1, -1, -1):
        if i >= len(df) - 1:
            df.loc[i, 'R1'] = 0
        else:    
            if df['S01_1'][i] ==-1 :
                df.loc[i, 'R1'] = 1
            else:
                if df['S01_1'][i] ==1:
                    df.loc[i, 'R1'] = 0
                else:
                    if df['R1'][i+1] >=1:
                        df.loc[i, 'R1'] = df['R1'][i+1]+1
                    else:
                        df.loc[i, 'R1']=0
    
    df['PR1'] = int()
    for i in range(len(df)):
        if df.loc[i, 'R1'] == 0:
            df.loc[i, 'PR1'] == 0
        else:
            num_rows_3 = df.loc[i, 'R1']
            sum_klgd_3 = df['GTGD'][i:i+num_rows_3].sum()/df['KLGD'][i:i+num_rows_3].sum()
            df.loc[i, 'PR1'] = sum_klgd_3*1000

    # Lặp từ dòng cuối cùng lên dòng đầu tiên để lấy kết quả lãi lỗ tín hiện P3
    # Tạo cột Ky_3
    threshold_3 = data_klgd.loc[data_klgd['Ma_CP']==sheet_name, 'KL_3'].values[0]
    klgg_3 = 0
    Ky_3_value = [0]*len(df)
    for i in range(len(df)):
        klgg_3 = 0
        count = 0
        for j in range(i, len(df)):
            klgg_3 += df.loc[j, 'KLGD']
            count += 1
            if klgg_3 > threshold_3:
                break
        Ky_3_value[i] = count
    
    df['Ky_3'] = Ky_3_value
    
    # Tạo cột giá bình quân theo Kỳ 3
    df['P_Ky3'] = float('nan')
    for i in range(len(df)):
        num_rows_3 = df.loc[i, 'Ky_3']
        sum_klgd_3 = df['GTGD'][i:i+num_rows_3].sum()/df['KLGD'][i:i+num_rows_3].sum()
        df.at[i, 'P_Ky3'] = sum_klgd_3*1000
    
    # Tạo cột Sign02
    df['BQ/P3'] = df['BQ']/df['P_Ky3']
    df['Sign02'] = df['BQ/P3']/df['BQ/P3'].shift(-1)
    df['Sign02'] = df['Sign02'].fillna(100)
    
    for i in range(len(df) - 1, -1, -1):
        if i >= len(df) - 3:
            df.loc[i, 'S02_1'] = 0
            df.loc[i, 'S02_2'] = 0
        else:
            # Tính tổng tích lũy từ dòng kế tiếp đến dòng cuối cùng trừ giá trị tại dòng hiện tại
            if i>=0:
                cumsum_reverse = df['S02_1'][::-1].shift(1).cumsum()[::-1]
                df.loc[i, 'S02_2'] = min(0,cumsum_reverse[i])
            
            if df['Sign02'][i] < 1 and df['Sign02'][i+1] < 1 and df['Sign02'][i+2] < 1 and df['S02_2'][i] == -1:
                df.loc[i, 'S02_1'] = 1
            elif df['Sign02'][i] >= 1 and df['Sign02'][i+1] >= 1 and df['Sign02'][i+2] >= 1 and df['S02_2'][i] == 0:
                df.loc[i, 'S02_1'] = -1
            else:
                df.loc[i, 'S02_1'] = 0  
    df['S02_2'] = df['S02_2'].fillna(method='bfill')
    df['KQ_Sign02']=df['S02_1']*df['BQ']

    df['R2'] = int()
    for i in range(len(df) - 1, -1, -1):
        if i >= len(df) - 1:
            df.loc[i, 'R2'] = 0
        else:    
            if df['S02_1'][i] ==-1 :
                df.loc[i, 'R2'] = 1
            else:
                if df['S02_1'][i] ==1:
                    df.loc[i, 'R2'] = 0
                else:
                    if df['R2'][i+1] >=1:
                        df.loc[i, 'R2'] = df['R2'][i+1]+1
                    else:
                        df.loc[i, 'R2']=0
    
    df['PR2'] = int()
    for i in range(len(df)):
        if df.loc[i, 'R2'] == 0:
            df.loc[i, 'PR2'] == 0
        else:
            num_rows_3 = df.loc[i, 'R2']
            sum_klgd_3 = df['GTGD'][i:i+num_rows_3].sum()/df['KLGD'][i:i+num_rows_3].sum()
            df.loc[i, 'PR2'] = sum_klgd_3*1000
    
    #Tạo cột tính tổng giá trị từ dòng hiện tại đến dòng 30 (hoặc dòng cuối) khi QB_CL < 0
    df['KL_Minus'] = [df.loc[i:i+df.loc[i, 'Ky_2'] - 1, 'KLGD'][df.loc[i:i + df.loc[i, 'Ky_2'] - 1, 'BQ_CL'] < 0].sum() for i in range(len(df))]
    df['BQ_Minus'] = [df.loc[i:i+df.loc[i, 'Ky_2'] - 1, 'BQ_CL'][df.loc[i:i + df.loc[i, 'Ky_2'] - 1, 'BQ_CL'] < 0].sum() for i in range(len(df))]
    df['BQ_Minus']=df['BQ_Minus'].abs()
    df['Minus']=df['KL_Minus']/df['BQ_Minus']
    #df['Minus']=df['Minus']/df['Ky_2']
    # Thay thế NaN bằng 0s
    df['Minus'].fillna(0, inplace=True)

    df['F_KL_Minus'] = [df.loc[i:i+df.loc[i, 'Ky_2'] - Ky, 'KLGD'][df.loc[i:i + df.loc[i, 'Ky_2'] - Ky, 'BQ_CL'] < 0].sum() for i in range(len(df))]
    df['F_BQ_Minus'] = [df.loc[i:i+df.loc[i, 'Ky_2'] - Ky, 'BQ_CL'][df.loc[i:i + df.loc[i, 'Ky_2'] - Ky, 'BQ_CL'] < 0].sum() for i in range(len(df))]
    df['F_Minus']=-df['F_KL_Minus']/df['F_BQ_Minus']
    
    df['KL_Add'] = [df.loc[i:i+df.loc[i, 'Ky_2'] - 1, 'KLGD'][df.loc[i:i + df.loc[i, 'Ky_2'] - 1, 'BQ_CL'] > 0].sum() for i in range(len(df))]
    df['BQ_Add'] = [df.loc[i:i+df.loc[i, 'Ky_2'] - 1, 'BQ_CL'][df.loc[i:i + df.loc[i, 'Ky_2'] - 1, 'BQ_CL'] > 0].sum() for i in range(len(df))]
    df['Add']=df['KL_Add']/df['BQ_Add']
    
    df['F_KL_Add'] = [df.loc[i:i+df.loc[i, 'Ky_2'] - Ky, 'KLGD'][df.loc[i:i + df.loc[i, 'Ky_2'] - Ky, 'BQ_CL'] > 0].sum() for i in range(len(df))]
    df['F_BQ_Add'] = [df.loc[i:i+df.loc[i, 'Ky_2'] - Ky, 'BQ_CL'][df.loc[i:i + df.loc[i, 'Ky_2'] - Ky, 'BQ_CL'] > 0].sum() for i in range(len(df))]
    df['F_Add']=df['F_KL_Add']/df['F_BQ_Add']

    df['Minus_Per'] = df['Minus']/df['Add']

    df['GTGD_VNI']=vni['GTGD'].shift(-1)
    df['TL_VNI'] = df.apply(
    lambda row: df.loc[row.name:row.name + row['Ky_2'] - 1, 'GTGD'].sum() /
                df.loc[row.name:row.name + row['Ky_2'] - 1, 'GTGD_VNI'].sum(),
    axis=1
    )   
    df['F_TL_VNI'] = df.apply(
    lambda row: df.loc[row.name:row.name + row['Ky_2'] - Ky, 'GTGD'].sum() /
                df.loc[row.name:row.name + row['Ky_2'] - Ky, 'GTGD_VNI'].sum(),
    axis=1
    )   
    
    # Tạo cột P_Ky2_1 với giá trị từ cột P_Ky2 tại dòng được chỉ định bởi Ky_2
    df['P_BQ_1'] = float('nan')  # Khởi tạo cột mới

    for i in range(len(df)):
        ky_2_index = i + df.loc[i, 'Ky_2']  # Tính chỉ số dòng dựa trên giá trị Ky_2
        if 0 <= ky_2_index < len(df):  # Kiểm tra chỉ số hợp lệ
            df.loc[i, 'P_BQ_1'] = df.loc[ky_2_index, 'BQ']  # Gán giá trị từ P_Ky2

    df['Total_BQ_CL'] = df['BQ']-df['P_BQ_1']  # Khởi tạo cột mới
    df['TB_canbang']=df['Total_BQ_CL']/((df['BQ']+df['P_BQ_1'])/2)  # Khởi tạo cột mới
    df['TB_canbang'] = df['TB_canbang'].fillna(0)
    #Định dạng % các cột
    # df['P1/P2'] = df['P1/P2'].apply(format_percentage)
    # df['BQ/P3'] = df['BQ/P3'].apply(format_percentage)
    # df['P_Ky1_BQ'] = df['P_Ky1_BQ'].apply(format_percentage)
    # df['P_Ky2_BQ'] = df['P_Ky2_BQ'].apply(format_percentage)
    # df['Sign01'] = df['Sign01'].apply(format_percentage)
    # df['Sign02'] = df['Sign02'].apply(format_percentage)
    # df['KL_Per'] = df['KL_Per'].apply(format_percentage)
    # df['KL_Per_1'] = df['KL_Per_1'].apply(format_percentage)
    # df['TL_VNI'] = df['TL_VNI'].apply(format_percentage)
    # df['Pea_Per'] = df['Pea_Per'].apply(format_percentage)
    # df['Minus_Per'] = df['Minus_Per'].apply(format_percentage)
    # df['F_TL_VNI'] = df['F_TL_VNI'].apply(format_percentage)

    return df

# Dữ liệu khối lượng giao dịch dưới dạng danh sách các hàng
data_klgd = [
    ['KL_BSR', 62000000, 182000000, 50000000],
    ['KL_BCG', 170000000, 220000000, 240000000],
    ['KL_ANV', 10000000, 60000000, 33000000],
    ['KL_HUT', 250000000, 350000000, 40000000],
    ['KL_NT2', 120000000, 140000000, 120000000],
    ['KL_DCM', 250000000, 450000000, 80000000],
    ['KL_VIX', 690000000, 1390000000, 680000000],
    ['KL_CEO', 180000000, 330000000, 54000000],
    ['KL_NVL', 440000000, 540000000, 150000000],
    ['KL_SBT', 140000000, 170000000, 10000000],
    ['KL_EIB', 90000000, 110000000, 20000000],
    ['KL_VCG', 80000000, 110000000, 30000000],
    ['KL_HPG', 550000000, 2650000000, 2110000000],
    ['KL_BID', 30000000, 430000000, 20000000],
    ['KL_GAS', 20000000, 100000000, 54000000],
    ['KL_QNS', 30000000, 120000000, 46000000],
    ['KL_CMX', 22000000, 62000000, 55000000],
    ['KL_VND', 571000000, 1142000000, 114000000],
    ['KL_HAH', 44000000, 61000000, 45000000],
    ['KL_CII', 35000000, 135000000, 45000000],
    ['KL_VHM', 210000000, 1310000000, 160000000],
    ['KL_VIX', 1434000000, 2868000000, 1220000000],
    ['KL_KHG', 160000000, 210000000, 80000000],
    ['KL_SSI', 670000000, 1020000000, 200000000],
    ['KL_HQC', 110000000, 260000000, 290000000],
    ['KL_IDI', 110000000, 230000000, 60000000],
    ['KL_DIG', 270000000, 510000000, 335000000],
    ['KL_MSN', 40000000, 90000000, 100000000],
    ['KL_PAN', 30000000, 170000000, 55000000],
    ['KL_PC1', 140000000, 170000000, 80000000],
    ['KL_KBC', 160000000, 260000000, 25000000],
    ['KL_VCI', 220000000, 280000000, 45000000],
    ['KL_MBB', 33000000, 1530000000, 895000000],
    ['KL_DPG', 24000000, 47000000, 7000000],
    ['KL_GEX', 160000000, 260000000, 320000000],
    ['KL_KDH', 70000000, 120000000, 419000000],
    ['KL_GIL', 30000000, 50000000, 16000000],
    ['KL_DRC', 50000000, 60000000, 51000000],
    ['KL_CTS', 110000000, 140000000, 40000000],
    ['KL_MBS', 100000000, 130000000, 20000000],
    ['KL_ANV', 10000000, 60000000, 30000000],
    ['KL_TNG', 11000000, 31000000, 25000000],
    ['KL_PVS', 240000000, 270000000, 45000000],
    ['KL_SZC', 110000000, 160000000, 28000000],
    ['KL_VNM', 110000000, 310000000, 155000000],
    ['KL_GVR', 430000000, 1380000000, 30000000],
    ['KL_DBC', 100000000, 120000000, 25000000],
    ['KL_PVT', 160000000, 190000000, 20000000],
    ['KL_HAG', 330000000, 830000000, 170000000],
    ['KL_PVD', 260000000, 280000000, 40000000],
    ['KL_IJC', 180000000, 240000000, 30000000],
    ['KL_POW', 787000000, 1756000000, 110000000],
    ['KL_ITC', 36000000, 72000000, 7000000],
    ['KL_VGC', 90000000, 390000000, 50000000],
    ['KL_VIC', 1434000000, 2868000000, 1220000000],
    ['KL_VOS', 6000000, 26000000, 14500000],
    ['KL_PET', 7600000, 17600000, 10000000],
    ['KL_VSC', 39500000, 69500000, 21000000],
    ['KL_HCM', 210000000, 360000000, 90000000],
    ['KL_DRI', 34000000, 44000000, 23000000],
    ['KL_MWG', 350000000, 500000000, 520000000],
    ['KL_V30', 15600000, 18600000, 1800000],
    ['KL_FTS', 61000000, 301000000, 145000000],
    ['KL_HDG', 15000000, 35000000, 168000000],
    ['KL_BCM', 10000000, 12000000, 22000000],
    ['KL_CTD', 20000000, 30000000, 50000000],
    ['KL_PLX', 96000000, 99000000, 93000000]
]

# Chuyển đổi danh sách thành DataFrame
data_klgd = pd.DataFrame(data_klgd, columns=['Ma_CP', 'KL_1', 'KL_2', 'KL_3'])

