
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
js = cs_tfidf("v34 = &dword_66359C[wking_loc];","v32 = &dword_66759C[wking_loc];")
print("JS",js)

# js = cs_tfidf("if ( pawnmates != CheckBadFlow_pawnmated )","if ( v3 != CheckBadFlow_pawnmated )")[0][1]
# print("JS",js)


# sec_js = cs_tfidf("else if ( !CheckBadFlow_pawnmated ) ","if ( v3 != CheckBadFlow_pawnmated )")[0][1]
# print("sec_js",sec_js)


# third_js = cs_tfidf("if ( board[l_king_mobility_king_o[d] + square] == 13 ) ","result += board[square + ( __int64)*( int *)( ( char *)jpt_401814 + v18)] == 4;")[0][1]
# print("sec_js",third_js)

# fourth_js = cs_tfidf("ndir = nk_attacked_bishop_o[i]; ","result += board[square + ( __int64)*( int *)( ( char *)jpt_401814 + v18)] == 4;")[0][1]
# print("sec_js",third_js)



# fifth_js = cs_tfidf("v20 = setup_attackers_bishop_o[v19];","a_sqa += setup_attackers_bishop_o[ia]; ")[0][1]
# print("fifth_js",fifth_js)

# ext = ('.txt')
# funcs_str = "allocate_time bishop_mobility calc_attackers CheckBadFlow check_piece_square check_legal comp_to_coord comp_to_san develop_node display_board eval extended_in_check f_in_check gen HandlePartner HandlePtell hash_extract_pv init_game is_attacked King losers_eval l_king_mobility l_rook_mobility post_thinking main nk_attacked ProcessHoldings proofnumbercheck proofnumberscan qsearch Queen ResetHandValue reset_board reset_piece_square Rook rook_mobility search setup_attackers setup_epd_line search_root see std_eval stringize_pv suicide_mid_eval SwitchColor SwitchPromoted s_king_mobility s_knight_mobility s_rook_mobility think tree_debug"
# # funcs_str = "bishop_mobility calc_attackers"
# # funcs_str = "calc_attackers"
# funcs = funcs_str.split(" ")
# print(funcs)


# tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
# model = AutoModel.from_pretrained("microsoft/codebert-base")
# def generate_embedding(strresult, len_embedd):
#     code_tokens = tokenizer.tokenize(strresult, truncation='longest_first', padding='max_length', max_length=len_embedd)
#     tokens_ids=tokenizer.convert_tokens_to_ids(code_tokens)
#     context_embeddings=model(torch.tensor(tokens_ids)[None,:])[0]

#     # print("context_embeddings",context_embeddings.cpu().detach().numpy())

# #  多维张量变成一维张量
# #  https://blog.csdn.net/zouh613/article/details/123866486
#     context_embeddings = context_embeddings.reshape(-1)

#     # print("一维张量",context_embeddings.cpu().detach().numpy())
#     # print("len()",len(context_embeddings.cpu().detach().numpy()))
#     # print("type(context_embeddings)",type(context_embeddings))
#     return [context_embeddings.cpu().detach().numpy()]

#     # Issue: ValueError: Found array with dim 3. check_pairwise_arrays expected <= 2.
#     # https://stackoverflow.com/a/34972736/5772735

# def findf(name, path):
#     for root, dirs, files in os.walk(path):
#         if name in files:
#             return os.path.join(root, name)
            


