from flask import Flask, render_template, request, redirect, jsonify
import json

from tabelog_scraper import Tabelog

app = Flask(__name__, template_folder='templates')


# JSON 파일에서 데이터 로드
def load_data_from_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# JSON 파일에서 데이터 로드
store_data = load_data_from_json('tabelog_data.json')

@app.route('/')
def index():
    return render_template('index.html', store_list=store_data)
@app.route('/get_stores_by_station_and_rating/<station>/<rating>')
def get_stores_by_station_and_rating(station, rating):
    with open('tabelog_data.json') as file:
        data = json.load(file)
        filtered_data = [store for store in data if store.get('station') == station and store.get('score') >= float(rating)]
    return jsonify(filtered_data)

@app.route('/get_data/shinjuku')
def get_data_shinjuku():
    tabelog_shinjuku = Tabelog(p_ward='新宿')
    data_shinjuku = tabelog_shinjuku.crawl_data()
    return jsonify(data_shinjuku)

@app.route('/get_data/shinokubo')
def get_data_shinokubo():
    tabelog_shinokubo = Tabelog(p_ward='新大久保')
    data_shinokubo = tabelog_shinokubo.crawl_data()
    return jsonify(data_shinokubo)

@app.route('/get_data/ogikubo')
def get_data_ogikubo():
    tabelog_ogikubo = Tabelog(p_ward='荻窪')
    data_ogikubo = tabelog_ogikubo.crawl_data()
    return jsonify(data_ogikubo)

@app.route('/get_data/shinagawa')
def get_data_shinagawa():
    tabelog_shinagawa = Tabelog(p_ward='品川')
    data_shinagawa = tabelog_shinagawa.crawl_data()
    return jsonify(data_shinagawa)


@app.route('/read/<int:id>/')
def read(id):
    selected_store = next((store for store in store_data if store['id'] == id), None)
    if selected_store:
        return render_template('index.html', store_list=store_data, selected_store=selected_store)
    return "Store not found", 404



@app.route('/get_stores_by_rating/<int:rating>/', methods=['GET'])
def get_stores_by_rating(rating):
    # 점수가 지정된 범위 내에 있는지 확인하여 필터링합니다.
    if rating == 4:
        filtered_stores = [store for store in store_data if 4 <= store['score'] < 5]
    elif rating == 3:
        filtered_stores = [store for store in store_data if 3 <= store['score'] < 4]
    elif rating == 2:
        filtered_stores = [store for store in store_data if 2 <= store['score'] < 3]
    else:
        filtered_stores = []

    return jsonify(filtered_stores)



@app.route('/get_all_stores/', methods=['GET'])
def get_all_stores():
    return jsonify(store_data)



if __name__ == '__main__':
    app.run(debug=True)
