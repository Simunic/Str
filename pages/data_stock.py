import streamlit as st
import pandas as pd

data_stock = pd.DataFrame(
    [
        {"command": "KL_BSR", "KQ_Sign01": 0, "Red": True,"Yellow": True,"Blue": True},
        {"command": "KL_VIX", "KQ_Sign01": 0, "Red": True,"Yellow": True,"Blue": True},
        {"command": "KL_DCM", "KQ_Sign01": 0, "Red": True,"Yellow": True,"Blue": True},
    ]
)

def generate_html_code(check1, check2, check3, num1, num2, num3):
    html_code = f"""
    <div class="container">
        <div class="row">
            <div class="col-12">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th scope="col">Select Day</th>
                            <th scope="col">Article Name</th>
                            <th scope="col">Author</th>
                            <th scope="col">Words</th>
                            <th scope="col">Shares</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="customCheck1" {'checked' if check1 else ''}>
                                    <label class="custom-control-label" for="customCheck1">1</label>
                                </div>
                            </td>
                            <td>Bootstrap 4 CDN and Starter Template</td>
                            <td>Cristina</td>
                            <td>{num1}</td>
                            <td>2.846</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="customCheck2" {'checked' if check2 else ''}>
                                    <label class="custom-control-label" for="customCheck2">2</label>
                                </div>
                            </td>
                            <td>Bootstrap Grid 4 Tutorial and Examples</td>
                            <td>Cristina</td>
                            <td>{num2}</td>
                            <td>3.417</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="customCheck3" {'checked' if check3 else ''}>
                                    <label class="custom-control-label" for="customCheck3">3</label>
                                </div>
                            </td>
                            <td>Bootstrap Flexbox Tutorial and Examples</td>
                            <td>Cristina</td>
                            <td>{num3}</td>
                            <td>1.234</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    """
    return html_code



# Form để cập nhật dữ liệu
# with st.form("key1"):
#     st.subheader("Cập nhật dữ liệu")

#     name_to_update = st.text_input("Tên (cột name)", "")
#     new_column_2 = st.text_input("Giá trị mới cho cột 2", "")
#     new_column_3 = st.text_input("Giá trị mới cho cột 3", "")
    
#     # Thêm selectbox để chọn màu nền cho cột 2
#     background_color = st.selectbox("Chọn màu nền cho cột 2", ["Trắng", "Vàng", "Đỏ"], index=0)

#     submit_button = st.form_submit_button("Cập nhật JSON")

#     if submit_button:
#         if name_to_update:
#             # Đọc dữ liệu từ file JSON
#             data = load_data_from_json(file_path)
            
#             # Tìm và cập nhật giá trị nếu cột name trùng khớp
#             updated = False
#             for entry in data["data"]:
#                 if entry["name"] == name_to_update:
#                     if new_column_2:
#                         entry["column_2"] = new_column_2
#                     if new_column_3:
#                         entry["column_3"] = new_column_3
#                     # Cập nhật màu sắc
#                     color_mapping = {
#                         "Trắng": "white",
#                         "Vàng": "yellow",
#                         "Đỏ": "red"
#                     }
#                     entry["color"] = color_mapping[background_color]
#                     updated = True
            
#             if updated:
#                 # Lưu lại dữ liệu vào file JSON
#                 save_data_to_json(file_path, data)
#                 st.success(f"Dữ liệu cho các dòng có tên {name_to_update} đã được cập nhật thành công!")
#             else:
#                 st.error(f"Không tìm thấy tên {name_to_update} trong dữ liệu.")
#         else:
#             st.error("Vui lòng nhập tên trong cột name.")

# # Đọc dữ liệu từ file JSON và hiển thị bảng dữ liệu
# data = load_data_from_json(file_path)
# df = data_to_dataframe(data)

# # Tạo bản đồ màu sắc từ dữ liệu
# color_mapping = {entry['name']: entry['color'] for entry in data["data"]}

# # Hiển thị bảng dữ liệu với màu nền đã chọn cho ô cột 2 tại dòng phù hợp
# styled_df = style_dataframe(df, color_mapping)
# st.dataframe(styled_df)