import pickle
import os

PICKLE_DIR = "pickle"
all_dict_dic = {}
large_category_dic = {"상의":"top", "하의":"bottom", "아우터":"outer", "원피스":"dress"}
all_name_list = ["top_categoryS", "bottom_categoryS", "outer_categoryS", "dress_categoryS",
                     "top_fit", "bottom_fit", "outer_fit", "dress_fit",
                     "top_length", "bottom_length", "outer_length", "dress_length",
                     "color", "material"]

def make_dic():
    if not os.path.exists(PICKLE_DIR):
        os.makedirs(PICKLE_DIR)

    top_categoryS = ['탑', '블라우스', '티셔츠', '니트웨어', '셔츠', '브라탑', '후드티']
    bottom_categoryS = ['청바지', '팬츠', '스커트', '레깅스', '조거팬츠']
    outer_categoryS = ['코트', '재킷', '점퍼', '패딩', '베스트', '가디건', '집업']
    dress_categoryS = ['드레스', '점프수트']

    top_fit = ['타이트', '노멀', '루즈', '오버사이즈']
    bottom_fit = ['스키니', '노멀', '와이드', '루즈', '벨보텀']
    outer_fit = ['타이트', '노멀', '루즈', '오버사이즈']
    dress_fit = ['타이트', '노멀', '루즈', '오버사이즈']

    top_length = ['크롭', '노멀', '롱']
    bottom_length = ['미니', '니렝스', '미디', '발목', '맥시']
    outer_length = ['크롭', '노멀', '하프', '롱', '맥시']
    dress_length = ['미니', '니렝스', '미디', '발목', '맥시']

    color = ['블랙','화이트','그레이','레드','핑크','오렌지','베이지','브라운','옐로우','그린',
         '카키','민트','블루','네이비','스카이블루','퍼플','라벤더','와인','네온','골드']
    material = ['퍼', '니트','무스탕'  '레이스', '스웨이드', '린넨', '앙고라' , '메시', '코듀로이' , '플리스', '시퀸/글리터' ,'네오프렌'
'데님', '실크' ,'저지'  ,'스판덱스', '트위드'  '자카드', '벨벳'  '가죽', '비닐/PVC' , '면' ,'울/캐시미어' , '시폰', '합성섬유']

    all_list = [top_categoryS, bottom_categoryS, outer_categoryS, dress_categoryS,
                top_fit, bottom_fit, outer_fit, dress_fit,
                top_length, bottom_length, outer_length, dress_length, color, material]

    for list, name in zip(all_list, all_name_list):
        dic = list2dict(list)
        with open(os.path.join(PICKLE_DIR, name+".pkl"), "wb") as f:
            pickle.dump(dic, f)

def load_dic():
    for name in all_name_list:
        with open(os.path.join(PICKLE_DIR, name+".pkl"), "rb") as f:
            all_dict_dic[name] = pickle.load(f)

def list2dict(list):
    return {value:idx for idx, value in enumerate(list)}

