import sys
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
    for opt_level in [0,1,2]:
        # if fd_name == 1:
        #     break
        fun_list = []
        err_list = []
        with open('/data/get_similiarities/'+proj+'ida/index_arr_'+com+str(opt_level+1)+'.txt', 'r') as file:  # 🌟 opt_level for base(outer/higher opt_level)
            # 逐行搜索
            line_marker = -1 # 打开该文件
            for num, line in enumerate(file, 1):
                # if num == 6:
                #     break
                line_list = line[1:len(line)-2].split(",")
                sub_fun_list = []
                sub_err_list = []
                if line != "[]\n":
                    for i_to_look in line_list:
                        print("line",line, "len(line)",len(line))
                        print("i_to_look",i_to_look)
                        i_to_look = int(i_to_look)
                        # func
                        with open("/data/get_similiarities/"+proj+"ida/"+com+str(opt_level)+"_fucs"+".csv", 'r') as fun_file: # 🌟 opt_level for comparee (inner/lower opt_level)
                            fun_lines = fun_file.readlines()
                            sub_fun_list.append(fun_lines[i_to_look].rstrip()) # remove \n
                        with open("/data/get_similiarities/"+proj+"ida/"+str(folders[opt_level])+"_lines.csv", 'r') as err_file:
                            err_lines = err_file.readlines()
                            sub_err_list.append(err_lines[i_to_look].rstrip()) # remove \n
                    fun_list.append(sub_fun_list)
                    err_list.append(sub_err_list)
                else:
                    # print("nummmmmm",num)
                    print("line_list",line_list)

                    print("line[1:len(line)-2]",line)
                    print("num",num,"line",line,"len(line_list)",len(line_list))
                    fun_list.append(sub_fun_list)
                    err_list.append(sub_err_list)
                    # continue


            

            


        with open(r'/data/get_similiarities/'+proj+'ida/'+str(folders[opt_level])+'_fuc_list.txt', 'w') as fp:
            for item in fun_list:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done')

        with open(r'/data/get_similiarities/'+proj+'ida/'+str(folders[opt_level])+'_ERR_list.txt', 'w') as fp:
            for item in err_list:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done')
