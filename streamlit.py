import streamlit as st
from geopy.distance import geodesic
import webbrowser
import requests

st.title('玄海町オープンデータ App')

# selectbox
option = st.selectbox(
    '検索する対象を選択してください。:',
    ['玄海町AED', '公衆無線LANアクセスポイント', '公衆トイレ','子育て施設','観光施設','指定緊急避難場所']
)

if option == '玄海町AED':
    url = "https://data.bodik.jp/api/3/action/datastore_search?resource_id=c9d523b9-0a5f-4095-8c28-0fb323d5d1f0" #AED
elif option == '公衆無線LANアクセスポイント':
    url = "https://data.bodik.jp/api/3/action/datastore_search?resource_id=54dee2ca-64d3-4fe6-b0e8-e7cf87ee0ba5" #wifi
elif option == '公衆トイレ':
    url = "https://data.bodik.jp/api/3/action/datastore_search?resource_id=8329a381-52d2-49e0-8cfc-951bced684f7" #トレイ
elif option == '子育て施設':
    url = "https://data.bodik.jp/api/3/action/datastore_search?resource_id=f5803abb-efb7-40bb-8bc4-360e9ecffaa6" #子育て施設
elif option == '観光施設':
    url = "https://data.bodik.jp/api/3/action/datastore_search?resource_id=64e98170-dcf7-4362-9420-22e9de792bd4" #観光施設
elif option == '指定緊急避難場所':
    url = "https://data.bodik.jp/api/3/action/datastore_search?resource_id=fc77bcee-d373-4981-9f93-45ef1ce53908" #指定緊急避難場所
else:
    st.write('未選択です。検索するものを選択してください。')

st.write('あなたが選んだデータは: ', option,'です。')
st.subheader('\n一番近い場所を検索します。')

min_length_name = {}
min_length_ido = {}
min_length_keido = {}

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

        dis = geodesic(now_location, place_data).m
        min_length_name.setdefault(place, round(dis)) #表示用
        ##print(f'{id}．現在地から{place}まで{round(dis)}メートルです。')
        min_length_ido.setdefault(data['緯度'], round(dis)) #緯度
        min_length_keido.setdefault(data['経度'], round(dis)) #経度

    st.write('☆☆☆最も近い場所は',min(min_length_name.items(), key = lambda x:x[1])[0],'です。☆☆☆')
    min_length_ido = min(min_length_ido.items(), key = lambda x:x[1])[0]
    min_length_keido = min(min_length_keido.items(), key = lambda x:x[1])[0]
    serach_url = f" https://www.google.com/maps/dir/?api=1&destination={min_length_ido},{min_length_keido}&travelmode=walking"
    st.write('↓↓目的地までの経路を検索する。')
    st.markdown(serach_url, unsafe_allow_html=True)
    webbrowser.open(serach_url,1)
    print(serach_url)
else:
    st.write('')

