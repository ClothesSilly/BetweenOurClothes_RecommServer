from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text

from load_data import Metadata, StoresData
from encoder import encode

app = Flask(__name__)
app.config.from_pyfile('config.py') # DB 연동을 위한 설정 추가

# MySQL 연동
database = create_engine(app.config['DB_URL'], encoding = 'utf-8')
app.database = database

# 데이터 로드
metadata = Metadata()

stores_data = StoresData(app, Metadata.color_name2idx, Metadata.material_name2idx, Metadata.styles_name2idx)
stores_data.load_posts() # stores post 로드


'''
@app.route("/recomm", methods=["POST"])
def recomm():
    post_id = request.form['post_id']
    clothes_info = request.form['clothes_info']
    style = request.form['style']
    material = request.form['material']
    color = request.form['color']

    vec = encode(clothes_info, style, material, color)
    #return faiss_search(vec)
'''

@app.route("/test", methods=["GET"])
def db_connect_test():
    row = app.database.execute(text("""
        select * from members
    """)).fetchone()

    result = {
            'name'      : row['name'],
            'email'     : row['email'],
        } if row else None

    return jsonify(result)

@app.route("/")
def home():
    return "추천 서버 홈"

if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=True)
