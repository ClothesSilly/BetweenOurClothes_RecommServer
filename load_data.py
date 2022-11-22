import os
import pandas as pd

CSV_DIR = "csv"

# index (top, bottom, outer, dress)
indexes = [0] * 4

# dim
dims = [0] * 4 # (top, bottom, outer, dress)
color_dim = -1
material_dim = -1
style_dim = -1

def open_stores_post():
    stores_post = pd.read_csv(os.path.join(CSV_DIR, "stores_post.csv"))
    # stores_post를 열어서 4개의 카테고리 분리
    # 4개의 카테고리에 대한 faiss index 만들기

    top_stores_post = stores_post[stores_post['clothes_info'] < indexes[0]]
    bottom_stores_post = stores_post[indexes[0] <= stores_post['clothes_info'] < indexes[1]]
    outer_stores_post = stores_post[indexes[1] <= stores_post['clothes_info'] < indexes[2]]
    dress_stores_post = stores_post[indexes[1] <= stores_post['clothes_info'] < indexes[3]]


def calculate_dim():
    if not os.path.exists(CSV_DIR):
        exit(-1)

    global indexes
    global dims
    global color_dim
    global material_dim
    global style_dim

    clothes_info = pd.read_csv(os.path.join(CSV_DIR, "clothes_info.csv"))
    top_clothes_info = clothes_info[clothes_info['category_l']=="상의"]
    bottom_clothes_info = clothes_info[clothes_info['category_l'] == "하의"]
    outer_clothes_info = clothes_info[clothes_info['category_l'] == "아우터"]
    dress_clothes_info = clothes_info[clothes_info['category_l'] == "원피스"]
    colors = pd.read_csv(os.path.join(CSV_DIR, "colors.csv"))
    materials = pd.read_csv(os.path.join(CSV_DIR, "materials.csv"))
    styles = pd.read_csv(os.path.join(CSV_DIR, "style.csv"))

    dims[0] = top_clothes_info.shape[0]
    dims[1]= bottom_clothes_info.shape[0]
    dims[2] = outer_clothes_info.shape[0]
    dims[3] = dress_clothes_info.shape[0]
    color_dim = colors.shape[0]
    material_dim = materials.shape[0]
    style_dim = styles.shape[0]

    indexes[0] = dims[0]
    for i in range(1, 4):
        indexes[i] = indexes[i-1] + dims[i]