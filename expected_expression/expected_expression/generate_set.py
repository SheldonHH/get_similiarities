# extensions
import os
import csv
import re
ext = ('.txt', 'jpg')
 
# scanning the directory to get required files



def writecsv(bigger_csv):
    with open('bigger_csv.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in bigger_csv.items():
            writer.writerow([key, value])


if __name__ == "__main__":
    unique_set = {}
    all_dict = {}
    f_cont = 0

    unique_set = {}
    for files in os.scandir("/Users/mac/expected_expression/expected_expression/c3"):
        if files.path.endswith(ext):
            print("files",files)
            unique_set[files] = files
            f_cont+=1
            fp = open(files)
            fkey = fp
            subdict = {}
            for i, line in enumerate(fp):
                if i > 2:
                    # print("line:",line)
                    if ":" in line:
                        # print(line)
                        err_key = line[0:line.index(":")]
                        if err_key in unique_set == False:
                            unique_set.add(err_key)
                        value = line[line.index(":")+2:len(line)-1]
                        # print("value",value)
                        if value != "":
                            subdict[err_key] = value
                    
                    # break
            fp.close()
            all_dict[str(f_cont)] = subdict
    
    # print("all_dict",all_dict)
    # print(all_dict['1'])
    
    set_sg = {}
    bigger_csv = {}
    ccct=0
    for k,value in all_dict.items():
        ccct+=1
        #  for each file
        for sk,sv in value.items():
            if sk in bigger_csv:
                lennn = len(re.findall(",", str(bigger_csv[sk])))
                # print("lenn",lennn)
                if ccct > lennn:
                    print("trueee???")
                    for i in range(ccct-lennn):
                        print("here")
                        bigger_csv[sk]=bigger_csv[sk]+","
                bigger_csv[sk] = bigger_csv[sk]+","+sv
            else:
                bigger_csv[sk] = sv

    # print(bigger_csv)
    writecsv(bigger_csv)
