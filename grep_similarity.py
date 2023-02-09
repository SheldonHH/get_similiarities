import os
import csv
import re
import numpy as np
ext = ('.txt')
# str = "allocate_time bishop_mobility calc_attackers CheckBadFlow check_piece_square check_legal comp_to_coord comp_to_san develop_node display_board eval extended_in_check f_in_check gen HandlePartner HandlePtell hash_extract_pv init_game is_attacked King losers_eval l_king_mobility l_rook_mobility post_thinking main nk_attacked post_thinking ProcessHoldings proofnumbercheck proofnumberscan qsearch Queen ResetHandValue reset_board reset_piece_square Rook rook_mobility search setup_attackers setup_epd_line search_root see std_eval stringize_pv suicide_mid_eval SwitchColor SwitchPromoted s_king_mobility s_knight_mobility s_rook_mobility think tree_debug"
str = "allocate_time bishop_mobility" 
funcs = str.split(" ")
print(funcs)


import os

def findf(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
            
def Jaccard_Similarity(doc1, doc2): 
    
    # List the unique words in a document
    words_doc1 = set(doc1.lower().split()) 
    words_doc2 = set(doc2.lower().split())
    
    # Find the intersection of words list of doc1 & doc2
    intersection = words_doc1.intersection(words_doc2)

    # Find the union of words list of doc1 & doc2
    union = words_doc1.union(words_doc2)
        
    # Calculate Jaccard similarity score 
    # using length of intersection set divided by length of union set
    return float(len(intersection)) / len(union)



folders = ["c0","c1","c2","c3"]
files_to_dict = {}
for fuc in funcs:
    # if fuc == "bishop_mobility":
    if True:
        ftcs = [] # 🌈最多4个同名文件数组

        # 对每一个folder遍历
        for fd in folders:
            #TODO: 需要替代 这个for loop只是为了找到match func
            oj = findf(fuc,"/Users/mac/similarities_test/use_undefined_identifier/"+fd)
            print("oj",oj)
            # if(type(oj) == type(None)):
            #     print("yaliii")
            ftcs.append(oj)
            # for fname in os.scandir("/Users/mac/similarities_test/use_undefined_identifier/"+fd):
            #     # print("fnameeee:",fname)
            #     if fuc == fname:
            #         ftcs.append(fname) # 🌈最多4个同名文
        # 对于同一个fuc
        # 对于一个cn下面的func
        # print("ftcs",ftcs)
        for index,ftc in enumerate(ftcs):   #   ftcs = [] # 最多4个同名文件数组已找到
            lines = []
            # print("use of undeclared identifier",ftc)
            line_marker = 0
            # if os.path.exists(ftc) == False:
            if type(ftc) == type(None):
                # lines.append([])
                ########################### 和else 部分完全一致 ########################
                if (fuc in files_to_dict.keys()) == False:
                    files_to_dict[fuc]=[lines]
                    print("here")
                else:
                    print("elseeee",lines)
                    oldvalue = files_to_dict[fuc]
                    print("old",oldvalue)
                    oldvalue.append(lines)
                    print("new",oldvalue)
                    files_to_dict.update({fuc:oldvalue})

            else:
                print("ftcftc",ftc)
                with open(ftc, 'r') as file:
                    # 逐行搜索
                    for num, line in enumerate(file, 1):
                        if "error: use of undeclared identifier"  in line:
                            print('found at line:', num,file)
                            line_marker = num
                        # 读取下面2行
                        if num == line_marker + 1:
                            print("num",num,"line",line)
                            lines.append(line)
                        # if num == line_marker + 2:
                        #     print("num",num,"line",line)
                    # 一个folder，一组lines
                    # print("typeof",type(ftc))
                    # print("typeof(index)",type(index))
                    # # fun_opt = str(ftc)
                    # print("index:",index)

                ########################### 和else 部分完全一致 ########################
                    if (fuc in files_to_dict.keys()) == False:
                        files_to_dict[fuc]=[lines]
                        print("here")
                    else:
                        print("elseeee",lines)
                        oldvalue = files_to_dict[fuc]
                        print("old",oldvalue)
                        oldvalue.append(lines)
                        print("new",oldvalue)
                        files_to_dict.update({fuc:oldvalue})

print("files_to_dict",files_to_dict)
    # print("files_to_dict",files_to_dict)
# print("files_to_dict",files_to_dict)
for key,err0123 in files_to_dict.items():
    # 找到最长的line，然后填充其他line
    zuichang = max(len(l) for l in err0123)
    zd = min(len(l) for l in err0123)
    # print(key,"zc",zuichang)
    # print(key,"zd",zd)
    for index, opt in enumerate(err0123):
        while len(opt) < zuichang:
            opt.append('')
        err0123[index] = opt
    files_to_dict.update({key:err0123})
    # print

# print("files_to_dict",files_to_dict)
    # break
    
print("字典长度",len(files_to_dict))
# transpose
for key,err0123 in files_to_dict.items():
    print(key,err0123)
    print("\n")
    np.array(err0123).T
    




                    
                
            # content = file.read()
            # check if string present in a file
            # if "error: use of undeclared identifier" in content:
            #     print('string exist in a file')

            # print("fuc",fuc)