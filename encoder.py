from tensorflow import one_hot
from load_data import all_dict_dic, large_category_dic

def encode(categoryL, categoryS, fit, length, color, material):

    prefix = large_category_dic[categoryL] + "_"
    categoryS_onehot = one_hot(all_dict_dic[prefix + "categoryS"][categoryS],
                               len(all_dict_dic[prefix + "categoryS"][categoryS]))
    fit_onehot = one_hot(all_dict_dic[prefix + "fit"][fit],
                         len(all_dict_dic[prefix + "fit"][fit]))
    length_onehot = one_hot(all_dict_dic[prefix + "length"][length],
                         len(all_dict_dic[prefix + "length"][length]))
    color_onehot = one_hot(all_dict_dic[prefix + "color"][color],
                         len(all_dict_dic[prefix + "color"][color]))
    material_onehot = one_hot(all_dict_dic[prefix + "material"][material],
                         len(all_dict_dic[prefix + "material"][material]))

    vector = categoryS_onehot + fit_onehot + length_onehot + color_onehot + material_onehot
    return vector

