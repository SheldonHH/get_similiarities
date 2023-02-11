from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
array_vec_1 = np.array([[12,41,60,11,21],[1,2,3,4,5]])
array_vec_2 = np.array([[40,11,4,11,14],[213,3,32,54,32]])
print(cosine_similarity(array_vec_1, array_vec_2))