from tensorflow import one_hot, concat
import load_data as ld

def encode(clothes_info, style, material, color):

    clothes_info_onehot = None
    for i in range(4):
        if clothes_info < ld.indexes[i]:
            clothes_info_onehot = one_hot(clothes_info, ld.dims[i])
            break

    style_onehot = one_hot(style, ld.style_dim)
    color_onehot = one_hot(color, ld.color_dim)
    material_onehot = one_hot(material, ld.material_dim)

    vector = concat([clothes_info_onehot, style_onehot, color_onehot, material_onehot], axis=1)
    return vector

