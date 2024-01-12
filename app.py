import streamlit as st
import numpy as np
import pandas as pd

st.markdown('''
    :rainbow[Good Life＆Luck Scope].''')

# ヘッダー（h2相当）
st.markdown('### アーバンライフを見つけよう！')

# サブヘッダー（h3相当）
st.markdown("""
    <h4 style='color: #FF4B4B;'>Discover your Urban-life!</h4>
    """, unsafe_allow_html=True)

# テキスト
# テキストのサイズを指定して表示
st.markdown("""
<style>
.big-font {
    font-size:15px;
}
</style>

<div class="big-font">
便利でお洒落なアーバンエリア。<br>“都心3区”と呼ばれるのは千代田区、中央区、港区の3つ。皇居に隣接しているため、昔から商業はもちろん、政治や企業の本社機能などの中心として栄えてきました。<br><br>
副都心4区と呼ばれるのが渋谷区、新宿区、豊島区、文京区は、ターミナル駅としても機能している便利エリアです。<br>
品川区、目黒区、大田区、世田谷区、杉並区、豊島区の東京西部・城南地区は、住宅地としてファミリー層にも人気です。<br><br>
</div>
""", unsafe_allow_html=True)

# サイドバーのタイトル
st.sidebar.header('物件検索')
st.sidebar.multiselect(
  '● エリア選択',
  ['大田区', '品川区', '渋谷区', '新宿区', '杉並区', '世田谷区', '中央区', '港区', '豊島区', '中野区', '目黒区'],  # 選択肢リスト
  ['渋谷区', '港区', '世田谷区', '中央区']  # デフォルトで選択される項目のリスト
)

st.sidebar.text("")  # 空行を挿入

# 予算範囲の設定
min_price, max_price = st.sidebar.slider(
    '● 予算設定（予算）',
    100000, 300000, (150000, 250000)
)

st.sidebar.text("")  # 空行を挿入

# 敷金・礼金の選択
room_gratuity = st.sidebar.multiselect(
    '● 敷金・礼金',
    ['敷金有', '敷金無', '礼金有', '礼金無']
)

st.sidebar.text("")  # 空行を挿入

# 間取りの選択
layout = st.sidebar.multiselect(
    '● 間取り',
    ['1R', '1K', '1DK', '2K', '2DK', '3K', '3DK']
)

st.sidebar.text("")  # 空行を挿入

# 駅からの距離
station_distance = st.sidebar.slider('● 駅距離（分）', 10, 20, 10)

st.sidebar.text("")  # 空行を挿入

# 検索ボタン
if st.sidebar.button('物件を検索する'):
    st.success('検索結果がここに表示されます。')

# 地図表示
# ダミーの緯度経度データを生成して表示
# 実際のアプリでは、検索結果に基づいてデータを生成する必要があります。
dummy_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [35.681236, 139.767125],
    columns=['lat', 'lon']
)
st.map(dummy_data)

# メインコンテンツのテキスト
st.write('物件情報（エリアのみ）')
st.write('物件情報の詳細、ビジュアルやその他の情報はこちらです。')

# フッター
st.write('Copyright © Good life&lick Scope Co. All rights reserved.')