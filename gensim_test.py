from gensim import corpora, models, similarities
import jieba
texts = ['a_sq += setup_attackers_rook_o[i];']
keyword = 'v8 = setup_attackers_rook_o[v2];'
# texts = ['a_sqa += setup_attackers_bishop_o[ia]; ']
# keyword = 'v20 = setup_attackers_bishop_o[v19];'


texts = ['for ( l = rook_mobility_dir[diridx] + square; board[l] == 13; l += rook_mobility_dir[diridx] ) ']
keyword = 'v8 = setup_attackers_rook_o[v2];'


from simphile import jaccard_similarity, euclidian_similarity, compression_similarity

text_a = texts[0]
text_b = keyword

print(f"Jaccard Similarity: {jaccard_similarity(text_a, text_b)}")
print(f"Euclidian Similarity: {euclidian_similarity(text_a, text_b)}")
print(f"Compression Similarity: {compression_similarity(text_a, text_b)}")



# texts = ['I love reading Japanese novels. My favorite Japanese writer is Tanizaki Junichiro.', 'Natsume Soseki is a well-known Japanese novelist and his Kokoro is a masterpiece.', 'American modern poetry is good. ']
# keyword = 'Japan has some great novelists. Who is your favorite Japanese writer?'


texts = [jieba.lcut(text) for text in texts]
dictionary = corpora.Dictionary(texts)
feature_cnt = len(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus) 
kw_vector = dictionary.doc2bow(jieba.lcut(keyword))
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)
sim = index[tfidf[kw_vector]]
for i in range(len(sim)):
    print('keyword is similar to text%d: %.2f' % (i + 1, sim[i]))


# TF-IDF (and similar text transformations) are implemented in the Python packages Gensim and scikit-learn.
#  In the latter package, computing cosine similarities is as easy as
from sklearn.feature_extraction.text import TfidfVectorizer
corpus = ["a_sq += setup_attackers_rook_o[i];", "v8 = setup_attackers_rook_o[v2];"]       
vect = TfidfVectorizer(min_df=1, stop_words="english")                                                                                                                                                                                             
documents = [open(f).read() for f in text_files]
tfidf = TfidfVectorizer().fit_transform(documents)
# no need to normalize, since Vectorizer will return normalized tf-idf
pairwise_similarity = tfidf * tfidf.T