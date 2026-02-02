import streamlit as st
import pandas as pd
import numpy as np

st.title('業種別給与額の比較')

df=pd.read_csv('FEH_00351000_260203021711.csv', encoding='utf-8')


#サイドバー
with st.sidebar:
    menu=st.selectbox('メニュー', ['アプリの説明','データ表示・グラフ表示'])

    if menu=='データ表示・グラフ表示':
        option=st.radio('表示形式を選択してください',
                         ['表','グラフ'])
        
        item=st.radio('表示項目を選択してください',
                      ['給与額','給与所得者数'])
        
        year=st.selectbox('年代を選択してください',
                          df['年'].unique())
        
        
#アプリの説明ページ
if menu=='アプリの説明':
        st.header('アプリの概要')
        st.write('このアプリは、業種別の給与額や給与所得者数を表またはグラフで表すことができます。また、年代別に比較することも可能です。')
    
        st.header('アプリの目的')
        st.write('このアプリは、業種別の給与額や給与所得者数の傾向を視覚的に把握し、分析することを目的としています。')

        st.header('アプリの使い方')
        st.write('アプリの左側のサイドバーから、表示したい項目や年代を選択してください。')

#データ表示・グラフ表示ページ    
elif menu=='データ表示・グラフ表示':
        df=df[df['年']==year]

        if item=='給与額':
            df_item=df[['業種','給与額(平均)【千円】']]
        elif item=='給与所得者数':
            df_item=df[['業種','給与所得者数(年間月平均)【人】']]

        df_item.set_index('業種', inplace=True)
        df_item.iloc[:, 0] = (
        df_item.iloc[:, 0]
        .astype(str)
        .str.replace(',', '', regex=False)
        .astype(float)
    )

        st.write(f'### {year}年の全業種平均{item}データ')

        avg_val = df_item.iloc[:, 0].mean()

        if item == '給与額':
            label_text = "全業種平均給与"
            value_text = f"{avg_val:,.0f} 千円"
        else:  
            label_text = "全業種平均所得者数"
            value_text = f"{avg_val:,.0f} 人"

        st.metric(label=label_text, value=value_text)


        if option=='表':
            st.dataframe(df_item, width=800, height=400)
        elif option=='グラフ':
            st.bar_chart(df_item,sort=False)