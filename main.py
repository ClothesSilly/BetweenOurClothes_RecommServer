from flask import Flask, request, jsonify, Response
from sqlalchemy import create_engine, text
import os

from load_data import Metadata, StoresData
from faiss_utils import FaissUtils
from encoder import Encoder


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

app = Flask(__name__)
app.config.from_pyfile('config.py') # DB 연동을 위한 설정 추가

# MySQL 연동
database = create_engine(app.config['DB_URL'], encoding = 'utf-8')
app.database = database

# 데이터 로드
INDEX_DIR = "index"

metadata = Metadata()
encoder = Encoder(Metadata.indexes, Metadata.dims, Metadata.style_dim, Metadata.color_dim, Metadata.material_dim,
                  Metadata.color_name2idx, Metadata.material_name2idx, Metadata.styles_name2idx)
faiss_utils = FaissUtils()

if not os.listdir(INDEX_DIR): # index 폴더가 비었을 경우, stores index를 만듦
    print("******************************** Creating faiss index files ********************************")
    stores_data = StoresData(app)
    stores_data.load_posts(encoder) # stores post 로드
    for i in range(4):
        if stores_data.vectors[i]:
            faiss_utils.create_index(i, stores_data.vectors[i], stores_data.postIds[i], Metadata.dims[i]+Metadata.dim_sum)
else:
    faiss_utils.load_index() # index 폴더에 index가 있는 경우, index open


# Main Server에서 호출해 추천 리스트 반환
@app.route("/api/v1/recomm", methods=["POST"])
def recomm():
    params = request.get_json()
    clothes_info = params['clothes_info']
    style = params['style']
    material = params['material']
    color = params['color']

    vec, categoryL = encoder.encode(clothes_info, color, material, style)
    return jsonify(faiss_utils.search_similar_vec(categoryL, vec, 10))


# stores post를 새로 불러와 index 파일을 업데이트함
@app.route("/api/v1/update", methods=["PUT"])
def update_stores_post():
    stores_data = StoresData(app, Metadata.color_name2idx, Metadata.material_name2idx, Metadata.styles_name2idx)
    stores_data.load_posts(encoder)  # stores post 로드

    for i in range(4):
        if stores_data.vectors[i]:
            faiss_utils.create_index(i, stores_data.vectors[i], stores_data.postIds[i], Metadata.dims[i])
    return Response("index 파일 업데이트", status=200,  mimetype='application/json')

@app.route("/test", methods=["GET"])
def db_connect_test():
    row = app.database.execute(text("""
        select * from members
    """)).fetchone()
    result = {
            'name'      : row['name'],
            'email'     : row['email'],
    } if row else None
    return Response(jsonify(result), status=200, mimetype='application/json')

@app.route("/")
def home():
    return  Response("추천 서버 홈", status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000, debug=True)
