from tensorflow import one_hot
import numpy as np


class Encoder:
    def __init__(self,  indexes, dims, style_dim, color_dim, material_dim):
        self.indexes = indexes
        self.dims = dims
        self.style_dim = style_dim
        self.color_dim = color_dim
        self.material_dim = material_dim

    def encode(self, clothes_info, style, material, color):

        clothes_info_onehot = None
        categoryL = None
        for i in range(4):
            if clothes_info < self.indexes[i]:
                clothes_info_onehot = one_hot(clothes_info, self.dims[i]).numpy()
                categoryL = i
                break

        style_onehot = one_hot(style, self.style_dim).numpy()
        color_onehot = one_hot(color, self.color_dim).numpy()
        material_onehot = one_hot(material, self.material_dim).numpy()

        vector = np.concatenate([clothes_info_onehot, style_onehot, color_onehot, material_onehot]).tolist()
        return vector, categoryL

