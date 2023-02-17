from gensim import corpora, models, similarities
import jieba
texts = ['a_sq += setup_attackers_rook_o[i]; ']
keyword = 'v8 = setup_attackers_rook_o[v2];'


texts = ['I love reading Japanese novels. My favorite Japanese writer is Tanizaki Junichiro.', 'Natsume Soseki is a well-known Japanese novelist and his Kokoro is a masterpiece.', 'American modern poetry is good. ']
keyword = 'Japan has some great novelists. Who is your favorite Japanese writer?'


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