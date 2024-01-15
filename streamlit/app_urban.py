import streamlit as st
import pandas as pd
import sqlite3

# データ取得関数
@st.cache_data
def load_data():
    conn = sqlite3.connect('suumo_urban.db')
    data = pd.read_sql("SELECT * FROM suumo_urban2", conn)  
    conn.close()
    return data

# 築年数と階数を整数に変換する前処理関数
def preprocess(data):
    data['BuildAge'] = pd.to_numeric(data['BuildAge'], errors='coerce')
    data['FlrNo'] = pd.to_numeric(data['FlrNo'], errors='coerce')
    data['BuildAge'].fillna(0, inplace=True)
    data['FlrNo'].fillna(1, inplace=True)
    return data

# データベースからデータをロード
data = load_data()

# データの前処理を実行
data = preprocess(data)



# Streamlitアプリのヘッダー部分
st.markdown('''
    :rainbow: [Good Life＆Luck Scope]
''')
st.markdown('### TOKYO Lifeを見つけよう！')
st.markdown("""
    <h4 style='color: #FF4B4B;'>Discover your life!</h4>
    """, unsafe_allow_html=True)

# 説明文章
st.caption("""
    都心3区と呼ばれるのは千代田区、中央区、港区。
    皇居に隣接しているため、政治の中心地でもあり、企業の本社など日本の中枢です。
    副都心4区と呼ばれるのが渋谷区、新宿区、豊島区、文京区。文化発信の中心です。
    東京西部・城南地区は、住宅地としてファミリー層にも人気です。
    江戸といったら下町エリア。外国人にも人気です。
""")

# サイドバー設定
st.sidebar.header('物件検索')
selected_areas = st.sidebar.multiselect(
  '● エリア選択',
  options=data['Area'].unique(),
  key='area_select_key'
)

st.sidebar.text("")  # 空行を挿入

# 予算範囲の設定
min_rent = int(data['Rent'].min())
max_rent = int(data['Rent'].max())
min_price, max_price = st.sidebar.slider(
'● 家賃/Rent（万円）',
min_rent, max_rent, (min_rent, max_rent),
key='price_slider_key'
)

st.sidebar.text("")  # 空行を挿入


# 築年数の設定
min_age = data['BuildAge'].min()
max_age = data['BuildAge'].max()
selected_age = st.sidebar.slider(
'● 築年数/BuildAge',
min_age, max_age, (min_age, max_age),
key='age_slider_key'
)

st.sidebar.text("")  # 空行を挿入

# 階数の設定

min_floor = data['FlrNo'].min()
max_floor = data['FlrNo'].max()
selected_floor = st.sidebar.slider(
'● 階数/FlrNo',
min_floor, max_floor, (min_floor, max_floor),
key='floor_slider_key'
)

st.sidebar.text("")  # 空行を挿入

# 間取の設定
selected_layout = st.sidebar.multiselect(
    '● 間取り/Layout',
    options=data['Layout'].unique(),
    key='layout_select_key'
)

st.sidebar.text("")  # 空行を挿入


# 広さの設定

min_size = data['Size'].min()
max_size = data['Size'].max()
selected_size = st.sidebar.slider(
'● 広さ（㎡）/Size',
min_size, max_size, (min_size, max_size),
key='size_slider_key'
)

st.sidebar.text("")  # 空行を挿入


# 管理費の設定
min_manage_fee = int(data['ManageFee'].min())
max_manage_fee = int(data['ManageFee'].max())
selected_manage_fee = st.sidebar.slider(
    '● 管理費(円）/ManageFee',
    min_manage_fee, max_manage_fee, (min_manage_fee, max_manage_fee),
    key='manage_slider_key'
)



# 検索ボタンの処理
if st.sidebar.button('物件を検索する', key='search_button_key'):
    # フィルタリング
    filtered_data = data[
        (data['Area'].isin(selected_areas)) &
        (data['BuildAge'].between(*selected_age)) &
        (data['FlrNo'].between(*selected_floor)) &
        (data['Size'].between(*selected_size)) &
        (data['Rent'].between(min_price, max_price)) &
        (data['Layout'].isin(selected_layout)) &
        (data['ManageFee'].between(*selected_manage_fee)) 

    ]


    # フィルタリングされたデータが空でないか確認
    if not filtered_data.empty:
        # インデックスを通常のカラムに変換し、カラム名を「物件名」とする
        filtered_data.reset_index(inplace=True)
        filtered_data.rename(columns={'index': '物件番号'}, inplace=True)


        # 変更後のデータを表示
        st.dataframe(filtered_data)
    
    else:
        st.warning("条件に一致する物件が見つかりませんでした。")
else:
    # ボタンが押されていない場合はfiltered_dataが定義されていないので、何も表示しない
    filtered_data = pd.DataFrame()  # 空のDataFrameを用意するか、または何もしない



# メインコンテンツのテキスト

st.write('物件情報の詳細、ビジュアルやその他の情報はこちらです。')

# フッター
st.write('Copyright © Good life&lick Scope Co. All rights reserved.')



