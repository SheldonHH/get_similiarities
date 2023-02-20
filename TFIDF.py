
import os
import csv
import re
import numpy as np
from numpy.linalg import norm
import math
from transformers import AutoTokenizer, AutoModel
import torch
import sys

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from simphile import jaccard_similarity, euclidian_similarity, compression_similarity


# text_a = texts[0]
# text_b = keyword

# print(f"Jaccard Similarity: {jaccard_similarity(text_a, text_b)}")
# print(f"Euclidian Similarity: {euclidian_similarity(text_a, text_b)}")
# print(f"Compression Similarity: {compression_similarity(text_a, text_b)}")



def findf(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
            


def EditDistance(word1, word2):
    """
    :type word1: str
    :type word2: str
    :rtype: int
    """
    m = len(word1)
    n = len(word2)
    dp = [[0 for __ in range(m + 1)] for __ in range(n + 1)]
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(n + 1):
        dp[i][0] = i
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            onemore = 1 if word1[j - 1] != word2[i - 1] else 0
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + onemore)
    
    return 1 - dp[i][j]/ max(m,n)


# taking the dot product and dividing it by the magnitudes of each vector, as shown by the illustration below:
def cs_tfidf(d1, d2):
    count_vect = CountVectorizer()
    corpus = [d1,d2]
    X_train_counts = count_vect.fit_transform(corpus)
    # print(X_train_counts)
    # pd.DataFrame(X_train_counts.toarray(),columns=count_vect.get_feature_names(),index=['Document 1','Document 2'])


    vectorizer = TfidfVectorizer()

    trsfm=vectorizer.fit_transform(corpus)
    # print("cs_tfidf",cosine_similarity(trsfm[0:1], trsfm))
    return cosine_similarity(trsfm[0:1], trsfm)


if len(sys.argv) <= 1:
   print("the arguments are not entered in the command line")
else:
   for arg in sys.argv:
      print(arg)
proj = sys.argv[1]

type_of_coms = ["c","g"]
# type_of_coms = ["g","c"]
for com in type_of_coms:
    sjeng_set = set()
    folders = [com+"0",com+"1",com+"2",com+"3"]
    for fd in folders:
        directory = os.fsencode("/data/get_similiarities/"+proj+"ida/"+fd)
        for file in os.listdir(directory):
            sjeng_set.add(str(file.decode()))
            
    funcs = sjeng_set
    funcs = sorted(funcs, key=lambda x: x.lower())
    print("sorted funcs:",funcs)
    files_to_dict = {}
    bigger_coms_dict = {}
    fold_dict = {}
    outer_index = 0
    for fd in folders:     # 对每一个folder遍历
        outer_index+=1
        fold_array = []
        ftcs = [] # 🌈最多4个同名文件数组
        for fuc in funcs:
            #TODO: 需要替代 这个for loop只是为了找到match func
            oj = findf(fuc,"/data/get_similiarities/"+proj+"ida/"+fd)
            if (type(oj) != type(None)):
                print("oj",oj)
                ftcs.append(oj)

        # print("len(ftcs)",len(ftcs))
        for index,ftc in enumerate(ftcs):   #   ftcs = [] # 最多4个同名文件数组已找到
            lines = []
            print("ftcftc",ftc)
            with open(ftc, 'r') as file:
                # 逐行搜索
                line_marker = -1 # 打开该文件
                for num, line in enumerate(file, 1):
                    if "error: use of undeclared identifier" in line:
                        line_marker = num
                    # 读取下面1行
                    if line_marker >0 and num == line_marker + 1:
                        fold_array.append(line)
            ########################### 和if 部分完全一致 ########################
            
        fold_dict[fd] = fold_array
        with open(r'/data/get_similiarities/'+proj+'ida/'+com+str(outer_index)+'_lines'+'.txt', 'w') as fp:
            for item in fold_array:
                # write each item on a new line
                fp.write("%s" % item)
                print('Done')



    cs_cont = 0
    while cs_cont < 3:
        b_dict = {}
        cs_arr = []
        index_list = []
        fun_list = []
        err_list = []
        real_count = 0
        for outer_line in fold_dict[com+str(cs_cont+1)]:  # O1 +1
            max_csim_baseline = 0
            # print("outer_line",outer_line)
            i_arr = []
            f_sublist = []
            # e_sublist = []
            print("+++++++++++++++")
            for i_index, inner_line in enumerate(fold_dict[com+str(cs_cont)]): # O0
                real_count += 1
                print("compiler:",com,"cs_cont",cs_cont,"i_index",i_index,"real_count",real_count)
                # if True:
                outer_line = outer_line.rstrip() # remove \n
                inner_line = inner_line.rstrip() # remove \n
                print("outer_line",outer_line)
                print("inner_line",inner_line)
                # js = cs_tfidf(outer_line,inner_line)[0][1]
                # js = EditDistance(outer_line,inner_line)
                js = compression_similarity(outer_line,inner_line)
                print("js",js)
                # js = Jaccard_Similarity(outer_line,inner_line)
                if js > max_csim_baseline:
                    i_arr = []
                    i_arr.append(i_index)
                    # e_sublist.append(inner_line)
                    max_csim_baseline = js
                    print("max_csim_baseline",max_csim_baseline)
                elif max_csim_baseline > 0 and js == max_csim_baseline:
                    i_arr.append(i_index)
                    # e_sublist.append(inner_line)
        
            b_dict[outer_line] = max_csim_baseline
            cs_arr.append(max_csim_baseline)
            index_list.append(i_arr)
            print(max_csim_baseline)        

        print("+++")
        print(cs_arr)
        # print("+++",fold_dict["c0"])
        # if "CheckBadFlow_pawnmated = 0;" in fold_dict["c0"]:
        #     print("+++++++++++++++")
        #     break
        # print("fold_dict",fold_dict)
        with open(r'/data/get_similiarities/'+proj+'ida/score_'+com+'_'+str(cs_cont)+'cs_cont.txt', 'w') as fp:
            for item in cs_arr:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done')

        with open(r'/data/get_similiarities/'+proj+'ida/indexs_'+com+str(cs_cont)+'i_arr.txt', 'w') as fp:
            for item in index_list:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done')

        cs_cont+=1


