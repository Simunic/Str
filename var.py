#import streamlit.components.v1 as components

file_path = 'D:/Kiet/Hoc_python/Stock_Data.xlsm'
column_names = ['Ngay', 'GTGD','KLGD']
mack_macdinh = "KL_BSR"
#columns_to_hide = ["Ky_1","Ky_2","Ky_3","P1/P2","BQ/P3"]
# columns_to_hide = ['BQ_CL','KL_Sum','KL_Sum2','P_Ky1','P_Ky2','P_Ky3','S01_1','S01_2','S02_1','S02_2','R1',
#                    'R2',"P1/P2",'KL_Minus','BQ_Minus','Minus','KL_Add','BQ_Add','Add','GTGD_VNI','TL_VNI']
columns_to_hide =['KL_Sum_1','KL_Sum2_1','KL_Minus','BQ_Minus','KL_Add','BQ_Add','Minus_Per','F_KL_Minus','F_BQ_Minus','F_Minus','F_KL_Add','F_BQ_Add','F_Add','F_TL_VNI','Pea_Per','P_BQ_1','Total_BQ_CL']
columns_to_color = ["KQ_Sign01","KQ_Sign02","R1","PR1","R2","PR2",'TL_VNI']
# Màu nền cho từng cột
column_colors = {
    'KQ_Sign01': 'yellow',  # Màu vàng cho Column1
    'KQ_Sign02': 'yellow',  # Màu vàng cho Column1
    'R1': 'yellow',  # Màu vàng cho Column1,
    'R2': 'yellow',  # Màu vàng cho Column1
    "PR1": 'yellow',  # Màu vàng cho Column1
    "PR2": 'yellow',  # Màu vàng cho Column1
    "Sign01": 'pink',  # Màu vàng cho Column1
    "Sign02": 'pink',  # Màu vàng cho Column1
    "KL_Per":'yellow',
    "Minus":'orange',
    "Add":'orange',
    "TL_VNI":'yellow',
}
columns_to_format = ['GTGD','KLGD','BQ','BQ_CL','KL_Sum','KL_Sum2','P_Ky1','P_Ky2','P_Ky3',
                     'KQ_Sign01','KQ_Sign02','S01_1','S01_2','S02_1','S02_2','R1','R2','PR1',
                     'PR2','KL_Minus','BQ_Minus','Minus','KL_Add','BQ_Add','Add','GTGD_VNI','TL_VNI','BQ_Sum']

# HTML và CSS cho checkbox tùy chỉnh
checkbox_html = """
<div class="checkbox-wrapper-26">
  <input type="checkbox" id="_checkbox-26">
  <label for="_checkbox-26">
    <div class="tick_mark"></div>
  </label>
</div>

<style>
  .checkbox-wrapper-26 * {
    -webkit-tap-highlight-color: transparent;
    outline: none;
  }

  .checkbox-wrapper-26 input[type="checkbox"] {
    display: none;
  }

  .checkbox-wrapper-26 label {
    --size: 50px;
    --shadow: calc(var(--size) * .07) calc(var(--size) * .1);

    position: relative;
    display: block;
    width: var(--size);
    height: var(--size);
    margin: 0 auto;
    background-color: #f72414;
    border-radius: 50%;
    box-shadow: 0 var(--shadow) #ffbeb8;
    cursor: pointer;
    transition: 0.2s ease transform, 0.2s ease background-color,
      0.2s ease box-shadow;
    overflow: hidden;
    z-index: 1;
  }

  .checkbox-wrapper-26 label:before {
    content: "";
    position: absolute;
    top: 50%;
    right: 0;
    left: 0;
    width: calc(var(--size) * .7);
    height: calc(var(--size) * .7);
    margin: 0 auto;
    background-color: #fff;
    transform: translateY(-50%);
    border-radius: 50%;
    box-shadow: inset 0 var(--shadow) #ffbeb8;
    transition: 0.2s ease width, 0.2s ease height;
  }

  .checkbox-wrapper-26 label:hover:before {
    width: calc(var(--size) * .55);
    height: calc(var(--size) * .55);
    box-shadow: inset 0 var(--shadow) #ff9d96;
  }

  .checkbox-wrapper-26 label:active {
    transform: scale(0.9);
  }

  .checkbox-wrapper-26 .tick_mark {
    position: absolute;
    top: -1px;
    right: 0;
    left: calc(var(--size) * -.05);
    width: calc(var(--size) * .6);
    height: calc(var(--size) * .6);
    margin: 0 auto;
    margin-left: calc(var(--size) * .14);
    transform: rotateZ(-40deg);
  }

  .checkbox-wrapper-26 .tick_mark:before,
  .checkbox-wrapper-26 .tick_mark:after {
    content: "";
    position: absolute;
    background-color: #fff;
    border-radius: 2px;
    opacity: 0;
    transition: 0.2s ease transform, 0.2s ease opacity;
  }

  .checkbox-wrapper-26 .tick_mark:before {
    left: 0;
    bottom: 0;
    width: calc(var(--size) * .1);
    height: calc(var(--size) * .3);
    box-shadow: -2px 0 5px rgba(0, 0, 0, 0.23);
    transform: translateY(calc(var(--size) * -.68));
  }

  .checkbox-wrapper-26 .tick_mark:after {
    left: 0;
    bottom: 0;
    width: 100%;
    height: calc(var(--size) * .1);
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.23);
    transform: translateX(calc(var(--size) * .78));
  }

  .checkbox-wrapper-26 input[type="checkbox"]:checked + label {
    background-color: #07d410;
    box-shadow: 0 var(--shadow) #92ff97;
  }

  .checkbox-wrapper-26 input[type="checkbox"]:checked + label:before {
    width: 0;
    height: 0;
  }

  .checkbox-wrapper-26 input[type="checkbox"]:checked + label .tick_mark:before,
  .checkbox-wrapper-26 input[type="checkbox"]:checked + label .tick_mark:after {
    transform: translate(0);
    opacity: 1;
  }
</style>
"""

checkbox_html_02 = """
<div class="checkbox-wrapper-46">
  <input class="inp-cbx" id="cbx-46" type="checkbox" />
  <label class="cbx" for="cbx-46"><span>
    <svg width="12px" height="10px" viewbox="0 0 12 10">
      <polyline points="1.5 6 4.5 9 10.5 1"></polyline>
    </svg></span><span>Bỏ check box chỗ này</span>
  </label>
</div>

<style>
  .checkbox-wrapper-46 input[type="checkbox"] {
    display: none;
    visibility: hidden;
  }

  .checkbox-wrapper-46 .cbx {
    margin: auto;
    -webkit-user-select: none;
    user-select: none;
    cursor: pointer;
  }
  .checkbox-wrapper-46 .cbx span {
    display: inline-block;
    vertical-align: middle;
    transform: translate3d(0, 0, 0);
  }
  .checkbox-wrapper-46 .cbx span:first-child {
    position: relative;
    width: 18px;
    height: 18px;
    border-radius: 3px;
    transform: scale(1);
    vertical-align: middle;
    border: 1px solid #9098A9;
    transition: all 0.2s ease;
  }
  .checkbox-wrapper-46 .cbx span:first-child svg {
    position: absolute;
    top: 3px;
    left: 2px;
    fill: none;
    stroke: #FFFFFF;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
    stroke-dasharray: 16px;
    stroke-dashoffset: 16px;
    transition: all 0.3s ease;
    transition-delay: 0.1s;
    transform: translate3d(0, 0, 0);
  }
  .checkbox-wrapper-46 .cbx span:first-child:before {
    content: "";
    width: 100%;
    height: 100%;
    background:#f72414;
    display: block;
    transform: scale(0);
    opacity: 1;
    border-radius: 50%;
  }
  .checkbox-wrapper-46 .cbx span:last-child {
    padding-left: 8px;
  }
  .checkbox-wrapper-46 .cbx:hover span:first-child {
    border-color: #f72414;
  }

  .checkbox-wrapper-46 .inp-cbx:checked + .cbx span:first-child {
    background: #f72414;
    border-color: #f72414;
    animation: wave-46 0.4s ease;
  }
  .checkbox-wrapper-46 .inp-cbx:checked + .cbx span:first-child svg {
    stroke-dashoffset: 0;
  }
  .checkbox-wrapper-46 .inp-cbx:checked + .cbx span:first-child:before {
    transform: scale(3.5);
    opacity: 0;
    transition: all 0.6s ease;
  }

  @keyframes wave-46 {
    50% {
      transform: scale(0.9);
    }
  }
</style>
"""

# Đường dẫn đến file JSON
json_file = "data.json"  # Thay đổi đường dẫn file nếu cần

sizepoint = 5

Ky = 6

size_bold = 20

