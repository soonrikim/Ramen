from flask import Flask, render_template, request, redirect, jsonify
import json
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
