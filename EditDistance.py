
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











############################################################### main ################################################################

if len(sys.argv) <= 1:
   print("the arguments are not entered in the command line")
else:
   for arg in sys.argv:
      print(arg)
proj = sys.argv[1]
os.system("mkdir -p /data/get_similiarities/"+proj+"ida/IndexEachScore")

type_of_coms = ["c","g"]
for com in type_of_coms:
    uniqueFunc_set = set()
    folders = [com+"0",com+"1",com+"2",com+"3"]
    for fname in folders:
        directory = os.fsencode("/data/get_similiarities/"+proj+"ida/"+fname)
        for file in os.listdir(directory):
            uniqueFunc_set.add(str(file.decode()))
            
    funcs = uniqueFunc_set
    funcs = sorted(funcs, key=lambda x: x.lower())
    print("sorted funcs:",funcs)
    files_to_dict = {}
    bigger_coms_dict = {}
    fold_dict = {}
    for idx, fname in enumerate(folders):     # 对每一个folder遍历
        fold_array = []
        ftcs = [] # 🌈最多4个同名文件数组
        for fuc in funcs:
            #TODO: 需要替代 这个for loop只是为了找到match func
            oj = findf(fuc,"/data/get_similiarities/"+proj+"ida/"+fname)
            if (type(oj) != type(None)):
                print("oj",oj)
                ftcs.append(oj)

        # print("len(ftcs)",len(ftcs))
        for index,ftc in enumerate(ftcs):   #   ftcs = [] # 最多4个同名文件数组已找到
            lines = []
            print("func_name",ftc)
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
            
        fold_dict[fname] = fold_array
        with open(r'/data/get_similiarities/'+proj+'ida/'+com+str(idx)+'_lines'+'.csv', 'w') as fp:
            for item in fold_array:
                # write each item on a new line
                fp.write("%s" % item)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++ c1_lines +++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # cs_cont = -1
    for cs_cont in range(1,4): # 1-3, （4不包括）
        scores_arr = []
        index_list = []
        sim_score_count = 0
        for outer_line in fold_dict[com+str(cs_cont)]:  # O1 +1
            max_simi = 0
            i_arr = [] # funcs, error_lines for inner comparsion
            print("+++++++++++++++")
            for i_index, inner_line in enumerate(fold_dict[com+str(cs_cont-1)]): # O0
                sim_score_count += 1
                # 打印出O1,O0,inner_index,sim_score_count
                print(com+str(cs_cont),com+str(cs_cont-1),"inner_index",str(i_index),"sim_score_count",sim_score_count)
                outer_line = outer_line.rstrip() # remove \n
                inner_line = inner_line.rstrip() # remove \n
                print("outer_line",outer_line)
                print("inner_line",inner_line)
                simScore = EditDistance(outer_line,inner_line)
                print("This simScore:",simScore)
                if simScore > max_simi:
                    i_arr = []
                    i_arr.append(i_index)
                    max_simi = simScore
                    print("max_simi",max_simi)
                elif max_simi > 0 and simScore == max_simi:
                    i_arr.append(i_index)
        
            scores_arr.append(max_simi)
            index_list.append(i_arr)
            print(max_simi)        

        print("+++++++++++ scores_arr ++++++++")
        print(scores_arr)

        with open(r'/data/get_similiarities/'+proj+'ida/score_'+com+str(cs_cont)+'.txt', 'w') as fp:
            for item in scores_arr:
                # write each item on a new line
                fp.write("%s\n" % item)

        with open(r'/data/get_similiarities/'+proj+'ida/IndexEachScore/index_arr_'+com+str(cs_cont)+'.txt', 'w') as fp:
            for item in index_list:
                # write each item on a new line
                fp.write("%s\n" % item)

     


