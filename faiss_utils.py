import faiss
import numpy as np
import os

class FaissUtils:
    INDEX_DIR = "index"
    indexes = [None, None, None, None] # top, bottom, outer, dress

    def __init__(self):
        pass

    def load_index(self):
        for i in range(4):
            FaissUtils.indexes[i] = faiss.read_index(os.path.join(FaissUtils.INDEX_DIR, "index"+str(i)+".index"))

    # index 파일 만들고 저장
    def create_index(self, categoryL, vectors, ids, dim):
        vectors = np.array(vectors).astype('float32')
        ids = np.array(ids).astype('int64')

        index = faiss.IndexFlatL2(dim)
        index = faiss.IndexIDMap2(index) # index를 ID와 mapping할 수 있게 만듦
        index.add_with_ids(vectors, ids)

        faiss.write_index(index, os.path.join(FaissUtils.INDEX_DIR, "index"+str(categoryL)+".index"))
        FaissUtils.indexes[categoryL] = index

    # search
    def search_similar_vec(self, categoryL, query, k):
        if not FaissUtils.indexes[categoryL]:
            self.load_index()

        dists, idxs, = FaissUtils.indexes[categoryL].search(query, k)
        return idxs[0]