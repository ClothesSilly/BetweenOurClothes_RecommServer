from flask import Flask, request
from load_data import make_dic
from encoder import encode

make_dic()

app = Flask(__name__)

@app.route("/recomm", methods=["POST"])
def recomm():
    categoryL = request.form['categoryL']
    categoryS = request.form['categoryS']
    length = request.form['length']
    fit = request.form['fit']
    material = request.form['material']
    color = request.form['color']

    #vec = encode(categoryL, categoryS, length, fit, material, color)
    #return faiss_search(vec)

@app.route("/")
def home():
    return "추천 서버 홈"

if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=True)
