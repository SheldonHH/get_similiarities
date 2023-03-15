import os
import csv
import re
import numpy as np

import sys
def findf(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

if __name__ == "__main__": 
    if len(sys.argv) <= 1:
        print("the arguments are not entered in the command line")
    else:
        for arg in sys.argv:
            print(arg)
        proj = sys.argv[1]

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
        # https://stackoverflow.com/a/10269828/5772735


                    
        life_fucs = []
        for fname in folders:     # 对每一个folder遍历
            # fold_array = []
            func_arrays_foreach_category = [] # 🌈最多4个同名文件数组
            sub_life = []
            for fuc in funcs:
                #TODO: 需要替代 这个for loop只是为了找到match func
                oj = findf(fuc,"/data/get_similiarities/"+proj+"ida/"+fname)
                if (type(oj) != type(None)):
                    print("oj",oj)
                    func_arrays_foreach_category.append(oj)
            # print("len(func_arrays_foreach_category)",len(func_arrays_foreach_category))
            for index,ftc in enumerate(func_arrays_foreach_category):   #   func_arrays_foreach_category = [] # 最多4个同名文件数组已找到
                lines = []
                print("ftcftc",ftc)
                with open(ftc, 'r') as file:
                    # 逐行搜索
                    line_marker = -1 # 打开该文件
                    for num, line in enumerate(file, 1):
                        if "error: use of undeclared identifier" in line:
                            line_marker = num
                        # 读取下面2行
                        if line_marker > 0 and num == line_marker + 1:
                            # fold_array.append(line)
                            sub_life.append(ftc)
                ########################### 和if 部分完全一致 ########################
            
            life_fucs.append(sub_life)   
            # fold_dict[fname] = fold_array



        for sub_index,sub_life in enumerate(life_fucs): 
            # strss = funs_str(sub_index)
            filepath= "/data/get_similiarities/"+proj+"ida/"+com+str(sub_index)+"_fucs"+".csv"
            with open(filepath, 'w') as fp:
                for item in sub_life:
                    fp.write("%s\n" % item[item.rindex("/")+1:len(item)])
                # print('Done')