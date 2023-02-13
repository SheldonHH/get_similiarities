import os
import csv
import re
import numpy as np
from numpy.linalg import norm
import math
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

ext = ('.txt')
str = "allocate_time bishop_mobility calc_attackers CheckBadFlow check_piece_square check_legal comp_to_coord comp_to_san develop_node display_board eval extended_in_check f_in_check gen HandlePartner HandlePtell hash_extract_pv init_game is_attacked King losers_eval l_king_mobility l_rook_mobility post_thinking main nk_attacked ProcessHoldings proofnumbercheck proofnumberscan qsearch Queen ResetHandValue reset_board reset_piece_square Rook rook_mobility search setup_attackers setup_epd_line search_root see std_eval stringize_pv suicide_mid_eval SwitchColor SwitchPromoted s_king_mobility s_knight_mobility s_rook_mobility think tree_debug"
# str = "bishop_mobility calc_attackers"
# str = "calc_attackers"
funcs = str.split(" ")
print(funcs)


tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")
def generate_embedding(str):
    code_tokens = tokenizer.tokenize(str, padding='max_length')
    tokens_ids=tokenizer.convert_tokens_to_ids(code_tokens)
    context_embeddings=model(torch.tensor(tokens_ids)[None,:])[0]

    print("context_embeddings",context_embeddings.cpu().detach().numpy())

#  多维张量变成一维张量
#  https://blog.csdn.net/zouh613/article/details/123866486
    context_embeddings = context_embeddings.reshape(-1)

    print("一维张量",context_embeddings.cpu().detach().numpy())
    print("len()",len(context_embeddings.cpu().detach().numpy()))
    print("type(context_embeddings)",type(context_embeddings))
    return [context_embeddings.cpu().detach().numpy()]

    # Issue: ValueError: Found array with dim 3. check_pairwise_arrays expected <= 2.
    # https://stackoverflow.com/a/34972736/5772735

def findf(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
            
# def Jaccard_Similarity(doc1, doc2):
#     # List the unique words in a document
#     words_doc1 = set(doc1.lower().split()) 
#     words_doc2 = set(doc2.lower().split())
    
#     # Find the intersection of words list of doc1 & doc2
#     intersection = words_doc1.intersection(words_doc2)

#     # Find the union of words list of doc1 & doc2
#     union = words_doc1.union(words_doc2)
#     if len(union) == 0:
#         return 0
        
#     # Calculate Jaccard similarity score 
#     # using length of intersection set divided by length of union set
#     else: 
#         return float(len(intersection)) / len(union)



folders = ["c0","c1","c2","c3"]
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
        oj = findf(fuc,"/data/get_similiarities/use_undefined_identifier/"+fd)
        if (type(oj) != type(None)):
            print("oj",oj)
            ftcs.append(oj)

    print("len(ftcs)",len(ftcs))
    for index,ftc in enumerate(ftcs):   #   ftcs = [] # 最多4个同名文件数组已找到
        lines = []
        print("ftcftc",ftc)
        with open(ftc, 'r') as file:
            # 逐行搜索
            line_marker = 0 # 打开该文件
            for num, line in enumerate(file, 1):
                if "error: use of undeclared identifier" in line:
                    print('found at line:', num,file)
                    line_marker = num
                # 读取下面2行
                if num == line_marker + 1:
                    fold_array.append(line)
        ########################### 和if 部分完全一致 ########################
        
    fold_dict[fd] = fold_array
    print(outer_index,"size of fold_arry",len(fold_array))

# print("files_to_dict",files_to_dict)
# print("fold_dict",fold_dict)




b_dict = {}
b_arr = []
for outer_line in fold_dict["c2"]: 

    max_csim_baseline = 0
    # print("outer_line",outer_line)
    i_cont = 0
    for inner_line in fold_dict["c1"]:
        i_cont += 1
        # print("i_cont",i_cont)
        # vectorizer = CountVectorizer()
        # X = vectorizer.fit_transform(headlines)
        js = cosine_similarity(generate_embedding(outer_line),generate_embedding(inner_line))

        # js = Jaccard_Similarity(outer_line,inner_line)
        if js > max_csim_baseline:
            max_csim_baseline = js
        # print(cosine_similarity(np.array(outer_line), np.array(inner_line)))
            # print(cosine_similarity(df, df))
 
    b_dict[outer_line] = max_csim_baseline
    b_arr.append(max_csim_baseline)
    print(max_csim_baseline)        

# print("b_arr",b_arr)
with open(r'/data/get_similiarities/12.txt', 'w') as fp:
    for item in b_arr:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')