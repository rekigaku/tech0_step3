import streamlit as st
import pandas as pd
import sqlite3

# データ取得関数
@st.cache_data
def load_data():
    # 'suumo_urban.db' に接続する
    conn = sqlite3.connect('suumo_urban.db')
    data = pd.read_sql("SELECT * FROM suumo_urban", conn)  
    conn.close()
    return data

# データベースからデータをロード
data = load_data()

# Streamlitアプリのヘッダー部分
st.markdown('''
    :rainbow: [Good Life＆Luck Scope]
''')
st.markdown('### アーバンライフを見つけよう！')
st.markdown("""
    <h4 style='color: #FF4B4B;'>Discover your Urban-life!</h4>
    """, unsafe_allow_html=True)

# 説明文章
st.caption("""
    便利でお洒落なアーバンエリア。都心3区と呼ばれるのは千代田区、中央区、港区の3つ。
    皇居に隣接しているため、昔から商業はもちろん、政治や企業の本社機能などの中心として栄えてきました。
    副都心4区と呼ばれるのが渋谷区、新宿区、豊島区、文京区は、ターミナル駅としても機能している便利エリアです。
    品川区、目黒区、大田区、世田谷区、杉並区、豊島区の東京西部・城南地区は、住宅地としてファミリー層にも人気です。
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
    '● 家賃設定　/万円',
    min_rent, max_rent, (3, 5),
    key='price_slider_key'
)

st.sidebar.text("")  # 空行を挿入
# フロア回数の設定



# 築年数の設定


# 間取の設定


# 広さの設定


# 検索ボタンの処理
if st.sidebar.button('物件を検索する', key='search_button_key'):
    # フィルタリング
    filtered_data = data[
        (data['Area'].isin(selected_areas)) & 
        (data['Rent'].between(min_price, max_price))
    ]
    
    # フィルタリングされたデータが空でないか確認
    if not filtered_data.empty:
        st.dataframe(filtered_data)  # 検索結果を表示
    else:
        st.warning("条件に一致する物件が見つかりませんでした。")

# メインコンテンツのテキスト
st.write('物件情報（エリアのみ）')
st.write('物件情報の詳細、ビジュアルやその他の情報はこちらです。')

# フッター
st.write('Copyright © Good life&lick Scope Co. All rights reserved.')


