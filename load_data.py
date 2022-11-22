import os
import pandas as pd
from sqlalchemy import text

class Metadata:
    CSV_DIR = "csv"
    indexes = [0] * 4  # index (top, bottom, outer, dress)
    dims = [0] * 4  # dimension (top, bottom, outer, dress)
    color_dim = -1
    material_dim = -1
    style_dim = -1
    dim_sum = -1

    color_name2idx = None
    material_name2idx = None
    styles_name2idx = None

    def __init__(self):
        if not os.path.exists(Metadata.CSV_DIR):
            exit(-1)

        clothes_info = pd.read_csv(os.path.join(Metadata.CSV_DIR, "clothes_info.csv"))
        top_clothes_info = clothes_info[clothes_info['category_l']=="상의"]
        bottom_clothes_info = clothes_info[clothes_info['category_l'] == "하의"]
        outer_clothes_info = clothes_info[clothes_info['category_l'] == "아우터"]
        dress_clothes_info = clothes_info[clothes_info['category_l'] == "원피스"]

        colors = pd.read_csv(os.path.join(Metadata.CSV_DIR, "colors.csv"))
        materials = pd.read_csv(os.path.join(Metadata.CSV_DIR, "materials.csv"))
        styles = pd.read_csv(os.path.join(Metadata.CSV_DIR, "style.csv"))

        # name2idx dictionary
        Metadata.color_name2idx = {row[1]:row[0] for _, row in colors.iterrows()}
        Metadata.material_name2idx = {row[1]: row[0] for _, row in materials.iterrows()}
        Metadata.styles_name2idx = {row[1]: row[0] for _, row in styles.iterrows()}

        # dimension 계산
        Metadata.color_dim = colors.shape[0]
        Metadata.material_dim = materials.shape[0]
        Metadata.style_dim = styles.shape[0]
        Metadata.dim_sum = Metadata.color_dim  + Metadata.material_dim + Metadata.style_dim

        Metadata.dims[0] = top_clothes_info.shape[0]
        Metadata.dims[1]= bottom_clothes_info.shape[0]
        Metadata.dims[2] = outer_clothes_info.shape[0]
        Metadata.dims[3] = dress_clothes_info.shape[0]


        Metadata.indexes[0] = Metadata.dims[0]
        for i in range(1, 4):
            Metadata.indexes[i] = Metadata.indexes[i-1] + Metadata.dims[i]

class StoresData:
    MAX_LOAD = 30000

    def __init__(self, app):
        self.app = app

        self.postIds = [[], [], [], []] # top, bottom, outer, dress
        self.vectors = [[],[],[],[]] # top, bottom, outer, dress

    def load_posts(self, encoder):
        rows = self.app.database.execute(text("""
                select id, clothes_info_id, colors_name, materials_name, style_name
                from stores
                where status = "SALES"
                order by created_date desc
                limit :MAX_LOAD
            """), {
            'MAX_LOAD' : StoresData.MAX_LOAD
        }).fetchall()

        for _, row in enumerate(rows):
            vec, categoryL = encoder.encode(row['clothes_info_id'],
                         row['colors_name'],
                         row['materials_name'],
                         row['style_name'])

            self.vectors[categoryL].append(vec)
            self.postIds[categoryL].append(row['id'])