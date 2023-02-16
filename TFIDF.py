
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


def findf(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
            


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

type_of_coms = ["g"]
# type_of_coms = ["g","c"]
for com in type_of_coms:
    sjeng_set = set()
    folders = [com+"0",com+"1",com+"2",com+"3"]
    for fd in folders:
        directory = os.fsencode("/data/get_similiarities/sjengida/"+fd)
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
            oj = findf(fuc,"/data/get_similiarities/sjengida/"+fd)
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
        with open(r'/data/get_similiarities/sjengida/'+com+str(outer_index)+'_lines'+'.txt', 'w') as fp:
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
        for outer_line in fold_dict[com+str(cs_cont+1)]: 
            max_csim_baseline = 0
            # print("outer_line",outer_line)
            i_arr = []
            f_sublist = []
            e_sublist = []
            for i_index, inner_line in enumerate(fold_dict[com+str(cs_cont)]):
                real_count += 1
                print("cs_cont",cs_cont,"i_index",i_index,"real_count",real_count)
                js = cs_tfidf(outer_line,inner_line)[0][1]
                # print("js",js)
                # js = Jaccard_Similarity(outer_line,inner_line)
                if js > max_csim_baseline:
                    i_arr = []
                    i_arr.append(i_index)
                    e_sublist.append(inner_line)
                    max_csim_baseline = js
                    print("max_csim_baseline",max_csim_baseline)
                elif max_csim_baseline > 0 and js == max_csim_baseline:
                    i_arr.append(i_index)
                    e_sublist.append(inner_line)
                # print(cosine_similarity(np.array(outer_line), np.array(inner_line)))
                    # print(cosine_similarity(df, df))
        
            b_dict[outer_line] = max_csim_baseline
            cs_arr.append(max_csim_baseline)
            index_list.append(i_arr)
            print(max_csim_baseline)        


        with open(r'/data/get_similiarities/sjengida/score_'+com+'_'+str(cs_cont)+'cs_cont.txt', 'w') as fp:
            for item in cs_arr:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done')

        with open(r'/data/get_similiarities/sjengida/indexs_'+com+str(cs_cont)+'i_arr.txt', 'w') as fp:
            for item in index_list:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done')

        cs_cont+=1



