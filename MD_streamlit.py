import copy
import os
import streamlit as st
import plotly
import pandas as pd
import scipy as sp
import numpy as np
import scipy
from PIL import Image
import plotly.express as px
from streamlit_lottie import st_lottie
import requests
from io import BytesIO
from streamlit_extras.add_vertical_space import add_vertical_space


def mahalanobis(x=None, data=None, cov=None):
    x_minus_mu = x - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = sp.linalg.inv(cov)
    left_term = np.dot(x_minus_mu, inv_covmat)
    mahal = np.dot(left_term, x_minus_mu.T)
    return mahal


def md_calc(f):
    df_h1 = pd.read_csv('DRHD_health.csv')
    df_t = f

    df_h1 = df_h1.drop('id', axis=1)
    df_t = df_t.drop('ID', axis=1)
    df_h = (df_h1 - df_h1.mean())/df_h1.std()
    df_t = (df_t - df_h1.mean())/df_h1.std()

    a = mahalanobis(x=df_t, data=df_h)
    a_t = a**0.5
    MD = a_t.diagonal()
    MD_ori = MD/MD.std()
    MD_log = np.log(MD)/np.log(MD).std()
    MD_ori = np.around(MD_ori,2)
    MD_log = np.around(MD_log,2)
    return MD_ori, MD_log


# 定义一个返回该目录下所有文件的函数
def get_file_list(suffix, path):
    input_template_all = []
    input_template_all_path = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if os.path.splitext(name)[1] == suffix:
                input_template_all.append(name)
                input_template_all_path.append(os.path.join(root, name))
    return input_template_all,input_template_all_path


# 定义一个抓取图片的链接
def load_logourl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def to_excel(df: pd.DataFrame):
    in_memory_fp = BytesIO()
    df.to_excel(in_memory_fp)
    # Write the file out to disk to demonstrate that it worked.
    in_memory_fp.seek(0, 0)
    return in_memory_fp.read()


st.set_page_config(layout='wide')

# logo = load_logourl("http://www-x-gxykzx-x-com.img.abc188.com/images/logo.gif")
# st_lottie(logo, speed=1, height=200, key="initial")


image1 = Image.open('logo.png')
st.image(image1, caption=None, width=150, use_column_width=False, clamp=False, channels='RGB')
image2 = Image.open('ref.png')
st.markdown("<h1 style='text-align: center; color: black;'>DRHD Value APP</h1>", unsafe_allow_html=True)

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 1, 0.2, 1, 0.1)
)

row0_1.markdown("<h4 style='text-align: left; color: black;'>Analyzing Your Data Using DRHD value 👀 </h4>", unsafe_allow_html=True)


with row0_2:
    add_vertical_space()

row0_2.write("##### A Streamlit web app by 👉[Our Ophthalmology Reserch Group](http://www.gxhospital.com/physician_intros/1/dp/740/), get my streamlit Repository on Streamlit 👉[here!](https://github.com/BaJiaoXiaoZi/streamlit-of-DRHD)"
)

# st.markdown("# DRHD value app")  # 等价于st.title('DRHD value app')
st.sidebar.markdown(
    "**To begin, please enter the link to your data.** 👇"
)
select_file = st.sidebar.file_uploader('.csv')

# input_folder = st.sidebar.text_input('输入数据所在的目录:（输入后回车）', value=os.path.abspath('.'), key=None)
# path = input_folder
# _, file_list_csv = get_file_list('.csv', path)
# file_list = file_list_csv
# if file_list:
#     select_file = st.sidebar.selectbox('请选择你的数据(仅支持csv格式)', file_list)
#     st.write('当前目录:', select_file)
st.write("---")
if select_file:
    tab0, tab1, tab2 = st.tabs(["🧾:green[Statement of DRHD]", "📠:green[Summary of Your Data]", "🖨:green[DRHD Value and Output]"])

    # 提取数据
    @st.cache_data
    def load_data(path):
        df_ = pd.read_csv(path)
        return df_
    df = load_data(select_file)

    col_list = df.columns
    col_list = col_list.to_list()
    # 对原始数据做一个备份
    col_list_bak = copy.deepcopy(col_list)
    with tab0:
        col1_2, col1_0, col1_1 = st.columns((1, 2, 3))
        col1_1.markdown(
            "<h4 style='text-align: left; color: b;'>📕The Diabetic Retinopathy-related Homeostatic Dysregulation (DRHD) value was derived based on the selected DR-related biomarkers! </h2>",
            unsafe_allow_html=True)
        col1_1.markdown(
            "<h4 style='text-align: left; color: b;'>the construction of the DRHD value relied upon a reference group of participants devoid of any retinopathy, as confirmed by retinal imaging assessments.</h2>",
            unsafe_allow_html=True)
        col1_1.markdown(
            "<h4 style='text-align: left; color: b;'>DRHD value constitutes a relative measure of risk, where elevated values indicate increased levels of homeostatic dysregulation within the individual.</h2>",
            unsafe_allow_html=True)
        col1_1.markdown(
            "<h4 style='text-align: left; color: red;'>However, it's crucial to acknowledge that comparing DRHD values computed from different batches is not feasible.</h2>",
            unsafe_allow_html=True)
        col1_1.markdown("<h3 style='text-align: left; black: gray;'>🔎Read more in our paper⭐.</h2>",
            unsafe_allow_html=True)
        image3 = Image.open('OR.png')
        col1_0.image(image3, caption=None, width=500, use_column_width=False, clamp=False, channels='RGB')

        image4 = Image.open('3.png')
        col1_2.image(image4, caption=None, width=280, use_column_width=False, clamp=False, channels='RGB')

        st.markdown('---')
        st.markdown('💻Technical Support: [**Streamlit**](https://streamlit.io/)')
        st.markdown('💴Acknowledgement: [**GuangXi Key Laboratory of Eye Health**](http://www.gxykzx.com/)')

    if len(col_list_bak) > 0:
        # 渲染数据
        with tab1:
            col4_1, col4_2 = st.columns(2)
            # st.write('### 👇:green[This page shows the summary of your data]')
            # st.markdown('---')
            sub_df = df[col_list_bak]
            with col4_1:
                st.write('#### :black[②This is your data, check it!😁]')
                st.write(sub_df)

            with col4_2:
                st.write('#### :black[①The scatter plots!]')
                sub_df = sub_df.drop('ID', axis=1)
                col_list_bak.pop(0)
                fig = px.scatter(sub_df, x=df['ID'], y=col_list_bak, width=800, height=400)
                fig.update_layout(legend=dict(orientation='h'))
                st.plotly_chart(fig, theme='streamlit')

            st.markdown('---')

            # col2_1, col2_2 = st.columns((0.1, 0.5))
            st.markdown('💻Technical Support: [**Streamlit**](https://streamlit.io/)')
            st.markdown('💴Acknowledgement: [**GuangXi Key Laboratory of Eye Health**](http://www.gxykzx.com/)')
    with tab2:
        # st.write('### 👇:green[This page shows the calculated DRHD value of your data]')
        # st.markdown('---')
        col5_1, col5_2 = st.columns((1.8, 1))
        with col5_1:
            st.write('#### :black[①This is the DRHD of your data(We add it to the last columns)]')
            a, b = md_calc(df)
            df['HD'] = b
            # df['HD_log'] = b
            excel_data = to_excel(df)
            file_name = "DRHD_result.xlsx"
            st.write(df)
            st.download_button(
                f"📥Click to download {file_name}",
                excel_data,
                file_name,
                f"text/{file_name}",
                key=file_name
            )

        with col5_2:
            # st.write('#### :black[②This is the standard of our paper]')
            # st.write('')
            # st.write('')
            # st.write('')
            st.image(image2, caption=None, width=500, use_column_width=False, clamp=False, channels='RGB')
            # st.write('***')
        st.markdown('---')

        # col3_1, col3_2 = st.columns(2)
        st.markdown('💻Technical Support: [**Streamlit**](https://streamlit.io/)')
        st.markdown('💴Acknowledgement: [**GuangXi Key Laboratory of Eye Health**](http://www.gxykzx.com/)')

else:
    # st.title('请上传文件')
    # st.write(':red[请注意：输入的变量请与论文一致，且有ID列(注意区分大小写)]')

    st.markdown("<h5 style='text-align: left; black: gray;'>😀Hey guys! Welcome to Diabetic Retinopathy-related Homeostatic Dysregulation (DRHD) value App. This app never keeps or stores! </h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left; color: gray;'>Please upload the file to be analyzed </h2>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: left; color: red;'>Warning: the input variables should be consistent with the paper and have ID columns(Casematters) </h3>", unsafe_allow_html=True)
    # col5_0, col5_1 = st.columns((0.9,0.1))

    df_demo = pd.read_csv('DRHD_demo.csv')
    st.write('### :green[📈The demo of input data:]')
    st.write(df_demo)
    st.sidebar.markdown("<h2 style='color: g;'>REMINDER</h2>",
             unsafe_allow_html=True)
    file_name1 = "upload_demo.csv"
    st.sidebar.markdown(
    "①**Please download the sample file.** 👇"
    )
    st.sidebar.download_button(
        f"📥Click to download {file_name1}",
        df_demo.to_csv(index=False),
        file_name1,
        f"text/{file_name1}",
        key=file_name1
    )
    st.sidebar.markdown(
        "②**Please fill in the csv file.** ✍"
    )
    st.sidebar.markdown(
        "③**Click the button to browse files.** 📈"
    )
    st.write('### :green[📄The details of abbreviations:]')
    col2_1, col2_2 = st.columns(2)
    col2_1.write('#### SBP:    Systolic blood pressure')
    col2_1.write('#### DBP:    Diastolic blood pressure')
    col2_1.write('#### LDH:    Lactate dehydrogenase')
    col2_2.write('#### TC:    Total Cholesterol')
    col2_2.write('#### TG:    Triglycerides')
    col2_2.write('#### RBC:    Red blood cell')
    st.markdown('---')
    st.markdown('💻Technical Support: [**Streamlit**](https://streamlit.io/)')
    st.markdown('💴Acknowledgement: [**GuangXi Key Laboratory of Eye Health**](http://www.gxykzx.com/)')
