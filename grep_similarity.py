import os
import csv
import re
ext = ('.txt')
str = "allocate_time bishop_mobility calc_attackers CheckBadFlow check_piece_square check_legal comp_to_coord comp_to_san develop_node display_board eval extended_in_check f_in_check gen HandlePartner HandlePtell hash_extract_pv init_game is_attacked King losers_eval l_king_mobility l_rook_mobility post_thinking main nk_attacked post_thinking ProcessHoldings proofnumbercheck proofnumberscan qsearch Queen ResetHandValue reset_board reset_piece_square Rook rook_mobility search setup_attackers setup_epd_line search_root see std_eval stringize_pv suicide_mid_eval SwitchColor SwitchPromoted s_king_mobility s_knight_mobility s_rook_mobility think tree_debug"
funcs = str.split(" ")
print(funcs)


folders = ["c0","c1","c2","c3"]
for fuc in funcs:
    ftcs = [] # 🌈最多4个同名文件数组

    # 对每一个folder遍历
    for fd in folders:
        # 这个for loop只是为了找到match func
        for fname in os.scandir("/Users/mac/similarities_test/use_undefined_identifier/"+fd):
            # print("fnameeee:",fname.name)
            if fuc == fname.name:
                ftcs.append(fname) # 🌈最多4个同名文件数组
    # 对于同一个fuc
    # 对于一个cn下面的func
    files_to_dict = {}
    for index,ftc in enumerate(ftcs):   #   ftcs = [] # 最多4个同名文件数组已找到
        files_to_dict = {}
        lines = []
        print("use of undeclared identifier",ftc)
        line_marker = 0
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
                if num == line_marker + 2:
                    print("num",num,"line",line)
            # 一个folder，一组lines
            print("typeof",type(ftc.name))
            print("typeof(index)",type(index))
            # fun_opt = str(ftc.name)
            print("index:",index)
            if (ftc.name in files_to_dict.keys()) == False:
                files_to_dict[ftc.name]=[lines]
            else:
                oldvalue = files_to_dict[ftc.name]
                oldvalue.append(lines)
                files_to_dict[ftc.name] = oldvalue


    print("files_to_dict",files_to_dict)

                    
                
            # content = file.read()
            # check if string present in a file
            # if "error: use of undeclared identifier" in content:
            #     print('string exist in a file')

            # print("fuc",fuc)