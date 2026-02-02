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
        
        year_list = df['年'].unique()
        year=st.selectbox('年代を選択してください',
                          year_list)
        
        
#アプリの説明ページ
if menu=='アプリの説明':
        col1, col2, col3 = st.columns(3)

        with col1:
             with st.container():
                  st.subheader('アプリの概要')
                  st.write('このアプリは、業種別の給与額や給与所得者数を表またはグラフで表すことができます。また、年代別に比較することも可能です。')
    
        with col2:
             with st.container():
                  st.subheader('アプリの目的')
                  st.write('このアプリは、業種別の給与額や給与所得者数の傾向を視覚的に把握し、分析することを目的としています。')

        with col3:
                with st.container():
                     st.subheader('アプリの使い方')
                     st.write('アプリの左側のサイドバーから、表示したい項目や年代を選択してください。')


#データ表示・グラフ表示ページ    
elif menu=='データ表示・グラフ表示':
        # 選択された年のデータを抽出
        df_current = df[df['年']==year].copy()

        if item=='給与額':
            df_item = df_current[['業種','給与額(平均)【千円】']]
        elif item=='給与所得者数':
            df_item = df_current[['業種','給与所得者数(年間月平均)【人】']]

        df_item.set_index('業種', inplace=True)
        # 数値変換処理
        df_item.iloc[:, 0] = (
            df_item.iloc[:, 0]
            .astype(str)
            .str.replace(',', '', regex=False)
            .astype(float)
        )

        st.write(f'### {year}年の全業種平均{item}データ')

        # 当年度の平均値
        avg_val = df_item.iloc[:, 0].mean()

        # 前年度比（delta）の計算
        delta_val = None
        try:
            # 「2024年」から「2024」を取り出して1を引く
            current_year_num = int(year.replace('年', ''))
            prev_year_str = f"{current_year_num - 1}年"
            
            if prev_year_str in df['年'].values:
                df_prev = df[df['年'] == prev_year_str].copy()
                if item == '給与額':
                    prev_col = '給与額(平均)【千円】'
                else:
                    prev_col = '給与所得者数(年間月平均)【人】'
                
                # 前年度の数値を数値化して平均を出す
                prev_series = df_prev[prev_col].astype(str).str.replace(',', '', regex=False).astype(float)
                avg_prev = prev_series.mean()
                delta_val = avg_val - avg_prev
        except:
            pass

        if item == '給与額':
            label_text = "全業種平均給与"
            value_text = f"{avg_val:,.0f} 千円"
            delta_text = f"{delta_val:,.0f} 千円" if delta_val is not None else None
        else:  
            label_text = "全業種平均所得者数"
            value_text = f"{avg_val:,.0f} 人"
            delta_text = f"{delta_val:,.0f} 人" if delta_val is not None else None

        # metricの表示
        st.metric(label=label_text, value=value_text, delta=delta_text)

        if option=='表':
            st.dataframe(df_item)
        elif option=='グラフ':
            st.bar_chart(df_item)
        
        st.subheader('グラフの説明')
        st.write('2014年～2024年では常に「電気・ガス・熱供給・水道業」が最も高い給与額を示している。しかし、給与所得者数に関しては「電気・ガス・熱供給・水道業」が最も少ない。これは、この業種が高収入である一方で、従業員数が少ないことを示している。また2014年年から2024年年にかけて、全体的に給与額は増加傾向にあるが、給与所得者数は大きな変動が見られない。これは、給与の上昇が必ずしも雇用の増加につながっていないことを示唆している。')