###オープンデータAPI取得

from doctest import DocTestFinder
import requests
import pandas as pd
from geopy.distance import geodesic
import webbrowser

def main():
    global url
    url = "https://data.bodik.jp/api/3/action/datastore_search?resource_id=c9d523b9-0a5f-4095-8c28-0fb323d5d1f0" #AED

    res = requests.get(url)
    data = res.json()

    now_location = []
    geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
    geo_data = requests.get(geo_request_url).json()
    now_location = (geo_data['latitude'],geo_data['longitude'])

    ##df = pd.DataFrame(columns=['名称', '緯度', '経度', '距離（m）'])
    ###building_data = []

    min_length = {}

    data = data['result']['records']
    for data in data:
        id = data['_id']
        place = data['名称']
        place_data = (data['緯度'],data['経度'])
        dis = geodesic(now_location, place_data).m
        print(f'{id}．現在地から{place}まで{round(dis)}メートルです。')
        #df = df.append([data['名称'],data['緯度'],data['経度'],round(dis)])
        min_length.setdefault(place, round(dis))
        
    print(f'☆☆☆最も近い場所は{min(min_length.items(), key = lambda x:x[1])[0]}です。☆☆☆')

if __name__ == "__main__":
    main()

def op_app():
    res = requests.get(url)
    data = res.json()

    now_location = []
    geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
    geo_data = requests.get(geo_request_url).json()
    now_location = (geo_data['latitude'],geo_data['longitude'])

    ##df = pd.DataFrame(columns=['名称', '緯度', '経度', '距離（m）'])
    ###building_data = []

    min_length = {}

    data = data['result']['records']
    for data in data:
        id = data['_id']
        place = data['名称']
        place_data = (data['緯度'],data['経度'])
        dis = geodesic(now_location, place_data).m
        print(f'{id}．現在地から{place}まで{round(dis)}メートルです。')
        df = df.append([data['名称'],data['緯度'],data['経度'],round(dis)])
        min_length.setdefault(place, round(dis))
        st.dataframe(df)
        st.wirte('☆☆☆最も近い場所は',min(min_length.items(), key = lambda x:x[1])[0],'です。☆☆☆')
        min_length_name = df.loc[[df['距離（m）'].idxmin('名称')]]
        min_length_ido = df.loc[[df['距離（m）'].idxmin('緯度')]]
        min_length_keido = df.loc[[df['距離（m）'].idxmin('経度')]]
        serach_url = f" https://www.google.com/maps/dir/?api=1&destination={min_length_ido},{min_length_keido}&travelmode=walking"
        if st.button('Say hello'):
            webbrowser.open(url)
        else:
            st.write('さよなら')
            
        ##print(f'☆☆☆最も近い場所は{min(min_length.items(), key = lambda x:x[1])[0]}です。☆☆☆')

    ##dfの距離が一番小さい行の緯度経度の抽出して、URLに組み込む
    ##そのURLをクリックするボタンをstreamlitで作る。


    https://www.google.com/maps/dir/?api=1&destination=35.710189,139.810473&travelmode=walking
