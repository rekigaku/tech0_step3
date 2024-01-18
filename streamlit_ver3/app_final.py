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
#current_dir = os.getcwd()
#image_path = os.path.join(current_dir, 'title.png')
#st.image(image_path)

st.markdown("""
    <h4 style='color: #FF4B4B;'>DISCOVER YOUR TOKYO LIFE</h4>
    """, unsafe_allow_html=True)
st.markdown('##### 2人の東京ライフ　検索サイト')

# 説明文章
st.caption("""
    勤続年数に応じて給料が上がり続けた時代は、「家賃は月収の3分の1」といわれました。
 それはもはや都市伝説！！最初に無理して出費すると、その後の人生設計は大きく崩れます。
 現実的にはどうなのか、新しい生活を始める2人にとっての適性価格を調べましょう。
""")

st.write()  # 空行を挿入

# ユーザー入力の受け取り
your_income = st.number_input('あなたの年収(万円)', min_value=0)
partner_income = st.number_input('パートナーの年収（万円）', min_value=0)
total_income = your_income + partner_income

# 世帯合計収入の表示
st.markdown(f'<p style="color:red; font-weight: bold;">合計年収（世帯）: {total_income}</p>', unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)  # 行間を空ける

st.markdown("""
    <h5 style='color: #FF4B4B;'>アンケート</h5>
    """, unsafe_allow_html=True)
# アンケートの質問
st.caption('※必ず、二人一緒にお応え下さい。')
dining_out = st.radio('月に4回以上は外食したい？', ['Yes', 'No'])
shopping = st.radio('2人合わせて年間10着は服を買いたい？', ['Yes', 'No'])
travel = st.radio('2泊以上の国内旅行、年に2回はしたい？', ['Yes', 'No'])
sport = st.radio('スポーツジムや習い事は続けていきたい？', ['Yes', 'No'])
friend = st.radio('友だちとの交際費、夫婦合わせて月3万以上？', ['Yes', 'No'])

# 賃貸の適性価格の計算
yes_answers = [dining_out, shopping, travel, sport, friend].count('Yes')
if yes_answers == 0:
    rent_price = (total_income * 0.30) / 12
elif yes_answers == 1:
    rent_price = (total_income * 0.28) / 12
elif yes_answers == 2:
    rent_price = (total_income * 0.26) / 12
elif yes_answers == 3:
    rent_price = (total_income * 0.24) / 12
elif yes_answers == 4:
    rent_price = (total_income * 0.22) / 12
else:  # 5つのYes
    rent_price = (total_income * 0.20) / 12

st.write()  # 空行を挿入

# 結果の表示
st.write('あなた達のGood Lifeな家賃:', unsafe_allow_html=True)
# 結果の数値部分の表示（赤文字太字で）
st.markdown(f'<p style="color:red; font-weight: bold;">{rent_price:.2f}万円</p>', unsafe_allow_html=True)


# HTMLの<br>タグでスペースを挿入
st.markdown('<br>', unsafe_allow_html=True)  # 空行を挿入


# サイドバー設定
st.sidebar.header('物件検索')
st.sidebar.caption("アンケートに答えないと検索できません")
st.sidebar.text("")

# 予算範囲の設定

st.sidebar.markdown(f'あなたの賃貸価格の上限は、**{rent_price:.2f}万円**です。')
st.sidebar.caption("*家賃を変更したければ、生活を見直す（アンケートをやり直して下さい(^_^;)）")

st.sidebar.text("")
st.sidebar.caption("全項目を入力下さい")
# エリア選択
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
        (data['Rent'] <= rent_price)&
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
        columns_to_display = ['物件番号','物件名', '住所', '築年数', '階数', '家賃', '管理費','間取','面積','敷金','礼金','路線A','駅A','徒歩A','路線B','駅B','徒歩B','路線C','駅C','徒歩C']

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

st.write('■　物件の詳細情報')


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



