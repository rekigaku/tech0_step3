import streamlit as st
import pandas as pd
import sqlite3
import os

# データベースファイルへのパスを構築
current_dir = os.getcwd()
db_path = os.path.join(current_dir, 'suumo_urban2.db')

# データ取得関数
@st.cache_data
def load_data():
    conn = sqlite3.connect('suumo_urban2.db')
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
current_dir = os.getcwd()
image_path = os.path.join(current_dir, 'title.png')
st.image(image_path)

st.markdown('#### あなたのTOKYO Lifeを見つけよう！')
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
st.sidebar.caption("全項目を入力下さい")
selected_areas = st.sidebar.multiselect(
  '● エリア選択',
  options=data['Area'].unique(),
  key='area_select_key'
)

st.sidebar.text("")  # 空行を挿入
# 間取の設定
selected_layout = st.sidebar.multiselect(
    '● 間取',
    options=data['Layout'].unique(),
    key='layout_select_key'
)

st.sidebar.text("")  # 空行を挿入


# 予算範囲の設定
min_rent = int(data['Rent'].min())
max_rent = int(data['Rent'].max())
min_price, max_price = st.sidebar.slider(
'● 家賃（万円）',
min_rent, max_rent, (min_rent, max_rent),
key='price_slider_key'
)

st.sidebar.text("")  # 空行を挿入


# 築年数の設定
min_age = data['BuildAge'].min()
max_age = data['BuildAge'].max()
selected_age = st.sidebar.slider(
'● 築年数',
min_age, max_age, (min_age, max_age),
key='age_slider_key'
)

st.sidebar.text("")  # 空行を挿入

# 階数の設定

min_floor = data['FlrNo'].min()
max_floor = data['FlrNo'].max()
selected_floor = st.sidebar.slider(
'● 階数',
min_floor, max_floor, (min_floor, max_floor),
key='floor_slider_key'
)

st.sidebar.text("")  # 空行を挿入



# 広さの設定

min_size = data['Size'].min()
max_size = data['Size'].max()
selected_size = st.sidebar.slider(
'● 広さ（㎡）',
min_size, max_size, (min_size, max_size),
key='size_slider_key'
)

st.sidebar.text("")  # 空行を挿入


# 管理費の設定
min_manage_fee = int(data['ManageFee'].min())
max_manage_fee = int(data['ManageFee'].max())
selected_manage_fee = st.sidebar.slider(
    '● 管理費(円）',
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

        # カラム名の日本語変換のための辞書を作成
        columns_japanese = {
            'Name': '物件名',
            'Add': '住所',
            'BuildAge': '築年数',
            'FlrNo': '階数',
            'Rent': '家賃',
            'ManageFee': '管理費',
            'Layout': '間取',
            'Size': '面積',
            'Deposit': '敷金',
            'Reikin': '礼金',
            'Ac1_Line': '路線A',
            'Ac1_Station': '駅A',
            'Ac1_Walk': '徒歩A',
            'Ac2_Line': '路線B',
            'Ac2_Station': '駅B',
            'Ac3_Walk': '徒歩B',
            'Ac3_Line': '路線C',
            'Ac3_Station': '駅C',
            'Ac3_Walk.1': '徒歩C'
            
        }

        # カラム名を日本語に変換
        filtered_data.rename(columns=columns_japanese, inplace=True)

        # 表示するカラムの選択
        columns_to_display = ['物件番号','物件名', '住所', '築年数', '階数', '家賃', '管理費','間取','面積','敷金','礼金','路線A','駅A','徒歩A']

        # 選択したカラムだけを持つ新しいデータフレームを作成
        filtered_data_display = filtered_data[columns_to_display]

        # 変更後のデータを表示
        st.dataframe(filtered_data_display)

    
    else:
        st.warning("条件に一致する物件が見つかりませんでした。")
else:
    # ボタンが押されていない場合はfiltered_dataが定義されていないので、何も表示しない
    filtered_data = pd.DataFrame()  # 空のDataFrameを用意するか、または何もしない



# メインコンテンツのテキスト

st.write('物件の詳細情報はこちらです。')


# 物件番号の入力
property_number_input = st.number_input('物件番号を入力（「,」は必要なし）', min_value=int(data.index.min()), max_value=int(data.index.max()), step=1)
st.caption("※新しい情報の表示⇒再度【物件を検索する】を押して下さい")

# 物件情報の表示
if property_number_input:
    property_data = data.loc[data.index == property_number_input]
    
    if not property_data.empty:
        # Image URLとDetail URLの表示
        st.image(property_data['ImageURL'].values[0], caption='物件画像')
        st.write(f"詳細URL: {property_data['DetailURL'].values[0]}")





# フッター
st.write('Copyright © Good life&lick Scope Co. All rights reserved.')



