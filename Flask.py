from flask import Flask, render_template, request, redirect, jsonify
import json
app = Flask(__name__, template_folder='templates')
store_data = [
    {'id': 1, 'store_name': '평점4점대', 'score': 4, 'review_cnt': 120},
    {'id': 2, 'store_name': '평점3점대', 'score': 3, 'review_cnt': 95},
    {'id': 3, 'store_name': '평점2점대', 'score': 2, 'review_cnt': 150}
]
with open('tabelog_data.json', 'r', encoding='utf-8') as file:
    store_data = json.load(file)

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


@app.route('/read/<int:id>/')
def read(id):
    selected_store = next((store for store in store_data if store['id'] == id), None)
    if selected_store:
        return render_template('index.html', store_list=store_data, selected_store=selected_store)
    return "Store not found", 404


@app.route('/get_stores_by_rating/<int:rating>/', methods=['GET'])
def get_stores_by_rating(rating):
    filtered_stores = [store for store in store_data if store['score'] >= rating]
    return jsonify(filtered_stores)


@app.route('/get_all_stores/', methods=['GET'])
def get_all_stores():
    return json.dumps(store_data)


if __name__ == '__main__':
    app.run(debug=True)
