import streamlit as st
import pandas as pd
import sqlite3
import os


# Streamlitアプリのヘッダー部分
st.markdown('<h4 style="text-align: center;">あなたにとってのGood Lifeとは？</h4>', unsafe_allow_html=True)
st.markdown("""
    <h5 style='text-align: center; color: #FF4B4B;'>What is the Good Life for you?</h5>
    """, unsafe_allow_html=True)


# 説明文章
st.caption("""
    勤続年数に相対して給料が上がり続けた時代、「家賃は月収の3分の1がいい」とよくいわれました。
　しかし、今やそれは伝説！！
　せっかく東京に住むなら、青山や自由が丘のようなお洒落な街で暮らしたい！というのも分かります。
　まずは現実的にはどうなのか、まずは適性価格を調べましょう。
""")

st.write()  # 空行を挿入

# ユーザー入力の受け取り
your_income = st.number_input('あなたの年収(万円)', min_value=0)
partner_income = st.number_input('パートナーの年収（万円）', min_value=0)
total_income = your_income + partner_income

# 世帯合計収入の表示
st.markdown(f'<p style="color:red; font-weight: bold;">合計年収（世帯）: {total_income}</p>', unsafe_allow_html=True)

st.write()  # 空行を挿入

# アンケートの質問
st.caption('次のアンケートにお答え下さい。世帯全体の数字で選択下さい')
dining_out = st.radio('外食（月間5回以上）', ['Yes', 'No'])
shopping = st.radio('ファッション（年間12着以上の服を購入）', ['Yes', 'No'])
travel = st.radio('旅行（2泊以上の旅行を年間3回以上）', ['Yes', 'No'])

# 賃貸の適性価格の計算
yes_answers = [dining_out, shopping, travel].count('Yes')
if yes_answers == 0:
    rent_price = (total_income * 0.29) / 12
elif yes_answers == 1:
    rent_price = (total_income * 0.25) / 12
elif yes_answers == 2:
    rent_price = (total_income * 0.22) / 12
else:  # 3つのYes
    rent_price = (total_income * 0.20) / 12

st.write()  # 空行を挿入

# 結果の表示
st.write('Good Lifeな賃貸の適性価格:', unsafe_allow_html=True)
# 結果の数値部分の表示（赤文字太字で）
st.markdown(f'<p style="color:red; font-weight: bold;">{rent_price:.2f}万円</p>', unsafe_allow_html=True)

# HTMLの<br>タグでスペースを挿入
st.markdown('<br>', unsafe_allow_html=True)  # 空行を挿入

# 次段落のヘッダー部分
st.markdown("""
    <h5 style='text-align: left; color: #006e54;'>■　東京を科学しよう！</h5>
    """, unsafe_allow_html=True)

# 説明文章
st.write("""
魅力ある多様性都市、東京を様々な角度から楽しめるのも賃貸ならではです。
まずは東京について学びましょう。
""")


# 画像のパス
image_path = 'area.png'

# 画像を表示、幅を500ピクセルに設定
st.image(image_path, caption='東京エリアマップ', width=300)



# フッター
st.write('Copyright © Good life&lick Scope Co. All rights reserved.')



