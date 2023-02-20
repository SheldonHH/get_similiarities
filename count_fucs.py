import os
import csv
import re
import numpy as np

import sys


if len(sys.argv) <= 1:
   print("the arguments are not entered in the command line")
else:
   for arg in sys.argv:
      print(arg)
proj = sys.argv[1]

type_of_coms = ["c","g"]
for com in type_of_coms:
    gcc_set = set()
    folders = [com+"0",com+"1",com+"2",com+"3"]
    for fd in folders:
        directory = os.fsencode("/data/get_similiarities/"+proj+"ida/"+fd)
        for file in os.listdir(directory):
            gcc_set.add(str(file.decode()))
            
    funcs = gcc_set
    funcs = sorted(funcs, key=lambda x: x.lower())
    # https://stackoverflow.com/a/10269828/5772735

    def findf(name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
                

    # folders = []
    files_to_dict = {}
    bigger_coms_dict = {}
    fold_dict = {}
    outer_index = 0
    life_fucs = []
    for fd in folders:     # 对每一个folder遍历
        outer_index+=1
        fold_array = []
        ftcs = [] # 🌈最多4个同名文件数组
        sub_life = []
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
                        # print('found at line:', num,file)
                        line_marker = num
                    # 读取下面2行
                    if line_marker > 0 and num == line_marker + 1:
                        fold_array.append(line)
                        sub_life.append(ftc)
            ########################### 和if 部分完全一致 ########################
        
        life_fucs.append(sub_life)   
        fold_dict[fd] = fold_array


    sub_counter = 0
    for sub_life in life_fucs: 
        sub_counter += 1
        # strss = funs_str(sub_counter)
        filepath= "/data/get_similiarities/"+proj+"ida/"+com+"life_fucs_"+str(sub_counter)+".csv"
        with open(filepath, 'w') as fp:
            for item in sub_life:
                # write each item on a new line
                # fp.write("%s\n" % item)

                fp.write("%s\n" % item[item.rindex("/")+1:len(item)])
            print('Done')
