import streamlit as st
import pandas as pd
import numpy as np
import requests
from geopy.distance import geodesic
import webbrowser

st.title('玄海町オープンデータ App')

# selectbox
option = st.selectbox(
    '検索する対象を選択してください。:',
    ['玄海町AED', '公衆無線LANアクセスポイント', '公衆トイレ']
)

if option == '玄海町AED':
    url = "https://data.bodik.jp/api/3/action/datastore_search?resource_id=c9d523b9-0a5f-4095-8c28-0fb323d5d1f0" #AED
elif option == '公衆無線LANアクセスポイント':
    url = "https://data.bodik.jp/api/3/action/datastore_search?resource_id=54dee2ca-64d3-4fe6-b0e8-e7cf87ee0ba5" #wifi
elif option == '公衆トイレ':
    url = "https://data.bodik.jp/api/3/action/datastore_search?resource_id=8329a381-52d2-49e0-8cfc-951bced684f7" #トレイ
else:
    st.write('未選択です。検索するものを選択してください。')

st.write('\nあなたが選んだデータは: ', option,'です。\n')
###st.write('現在位置から最も近い',option,'が検索できます。')

df = pd.DataFrame(columns=['名称', '緯度', '経度', '距離（m）'])
df_b = pd.DataFrame(columns=['名称', '緯度', '経度', '距離（m）'])
min_length = {}

if st.button('検索'):
    res = requests.get(url)
    data = res.json()
    now_location = []
    geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
    geo_data = requests.get(geo_request_url).json()
    now_location = (geo_data['latitude'],geo_data['longitude'])

    data = data['result']['records']
    for data in data:
        id = data['_id']
        place = data['名称']
        place_data = (data['緯度'],data['経度'])
        # place_data_ido = (data['緯度'])
        # place_data_keido = (data['経度'])
        dis = geodesic(now_location, place_data).m
        min_length.setdefault(place, round(dis))
        ##print(f'{id}．現在地から{place}まで{round(dis)}メートルです。')
        df_b = pd.DataFrame([data['名称'],data['緯度'],data['経度'],round(dis)])
        df = pd.concat([df, df_b])
        ###df = df.append([data['名称'],data['緯度'],data['経度']],round(dis))

    if st.button('検索結果を表示'):
        st.dataframe(df)
        st.write('☆☆☆最も近い場所は',min(min_length.items(), key = lambda x:x[1])[0],'です。☆☆☆')
        min_length_name = df.loc[[df['距離（m）'].idxmin('名称')]]
        min_length_ido = df.loc[[df['距離（m）'].idxmin('緯度')]]
        min_length_keido = df.loc[[df['距離（m）'].idxmin('経度')]]
        serach_url = f" https://www.google.com/maps/dir/?api=1&destination={min_length_ido},{min_length_keido}&travelmode=walking"
        
        if st.button('Say hello'):
            webbrowser.open(serach_url)
        else:
            st.write('さよなら')
    else:
        st.write('また使ってね。')
else:
    st.write('xxxx')



# options = st.multiselect(
#      'What are your favorite colors',
#      ['Green', 'Yellow', 'Red', 'Blue'],
#      ['Yellow', 'Red'])

# number = st.sidebar.slider('Pick a Num', 0, 100, 40)
# st.write(f'number: {number}')

# if number == 55:
#     st.sidebar.write('xxxxxxxxxx')

left_col, a, right_col = st.columns(3)
left_col.slider('Left', 0, 100)
right_col.write('Right Column')
a.write('Center Column')