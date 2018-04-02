import numpy as np

class LSI:
    def __init__(self, docs, query):
        self.docs = map(lambda d: d.split(), docs)
        self.words = sorted(set.union(*map(set, self.docs)))
        self.query = np.array([1 if w in query else 0 for w in self.words])
        self.term_doc_matrix = self._build_term_doc_matrix()

    def process(self):
        u_k, s_k, v_k = self._svd_with_dimensionality_reduction()
        s_k = np.linalg.pinv(s_k)
        q = self.query.reshape(1, -1).dot(u_k).dot(s_k)
        d = self.term_doc_matrix.T.dot(u_k).dot(s_k)

        res = np.apply_along_axis(lambda row: self._sim(q, row), axis=1, arr=d)
        print res
        return np.argsort(-res) + 1

    def _build_term_doc_matrix(self):
        model = np.zeros((len(self.words), len(self.docs)), dtype=int)
        for i, word in enumerate(self.words):
            for j, doc in enumerate(self.docs):
                model[i, j] = doc.count(word)
        return model

    def _svd_with_dimensionality_reduction(self):
        u, s, v = np.linalg.svd(self.term_doc_matrix)
        s = np.diag(s)
        k = 2
        return u[:, :k], s[:k, :k], v[:, :k]

    def _sim(self, x, y):
        res = x.dot(y.reshape(-1, 1)) / (np.linalg.norm(x) * np.linalg.norm(y))
        return res[0][0]