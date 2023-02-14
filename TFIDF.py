
import os
import csv
import re
import numpy as np
from numpy.linalg import norm
import math
from transformers import AutoTokenizer, AutoModel
import torch


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



ext = ('.txt')
funcs_str = "allocate_time bishop_mobility calc_attackers CheckBadFlow check_piece_square check_legal comp_to_coord comp_to_san develop_node display_board eval extended_in_check f_in_check gen HandlePartner HandlePtell hash_extract_pv init_game is_attacked King losers_eval l_king_mobility l_rook_mobility post_thinking main nk_attacked ProcessHoldings proofnumbercheck proofnumberscan qsearch Queen ResetHandValue reset_board reset_piece_square Rook rook_mobility search setup_attackers setup_epd_line search_root see std_eval stringize_pv suicide_mid_eval SwitchColor SwitchPromoted s_king_mobility s_knight_mobility s_rook_mobility think tree_debug"
# funcs_str = "bishop_mobility calc_attackers"
# funcs_str = "calc_attackers"
funcs = funcs_str.split(" ")
print(funcs)


tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")
def generate_embedding(strresult, len_embedd):
    code_tokens = tokenizer.tokenize(strresult, truncation='longest_first', padding='max_length', max_length=len_embedd)
    tokens_ids=tokenizer.convert_tokens_to_ids(code_tokens)
    context_embeddings=model(torch.tensor(tokens_ids)[None,:])[0]

    # print("context_embeddings",context_embeddings.cpu().detach().numpy())

#  多维张量变成一维张量
#  https://blog.csdn.net/zouh613/article/details/123866486
    context_embeddings = context_embeddings.reshape(-1)

    # print("一维张量",context_embeddings.cpu().detach().numpy())
    # print("len()",len(context_embeddings.cpu().detach().numpy()))
    # print("type(context_embeddings)",type(context_embeddings))
    return [context_embeddings.cpu().detach().numpy()]

    # Issue: ValueError: Found array with dim 3. check_pairwise_arrays expected <= 2.
    # https://stackoverflow.com/a/34972736/5772735

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
    with open(r'/data/get_similiarities/fold_dict'+str(outer_index)+'.txt', 'w') as fp:
        for item in fold_array:
            # write each item on a new line
            fp.write("%s" % item)
            print('Done')




cs_cont = 0
while cs_cont < 3:
    b_dict = {}
    cs_arr = []
    real_count = 0
    for outer_line in fold_dict["c"+str(cs_cont+1)]: 

        max_csim_baseline = 0
        # print("outer_line",outer_line)
        i_cont = 0
        for inner_line in fold_dict["c"+str(cs_cont)]:
            real_count += 1
            print("real_count",real_count)
            i_cont += 1
            js = cs_tfidf(outer_line,inner_line)[0][1]
            # print("js",js)
            # js = Jaccard_Similarity(outer_line,inner_line)
            if js > max_csim_baseline:
                max_csim_baseline = js
                print("max_csim_baseline",max_csim_baseline)
            # print(cosine_similarity(np.array(outer_line), np.array(inner_line)))
                # print(cosine_similarity(df, df))
    
        b_dict[outer_line] = max_csim_baseline
        cs_arr.append(max_csim_baseline)
        print(max_csim_baseline)        

    print("cs_arr",cs_arr)

    with open(r'/data/get_similiarities/'+str(cs_cont)+'cs_cont.txt', 'w') as fp:
        for item in cs_arr:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')



