# extensions
import os
import csv
import re        
from pathlib import Path
ext = ('.txt', 'jpg')
 
# scanning the directory to get required files



def writecsv(bigger_csv):
    with open('bigger_csv.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in bigger_csv.items():
            writer.writerow([key, value])


if __name__ == "__main__":
    unique_set = set()
    all_dict = {}
    f_cont = 0



    p = Path('./')

    # All subdirectories in the current directory, not recursive.
    print(" [f for f in p.iterdir() if f.is_dir()]:", [f for f in p.iterdir() if f.is_dir()])
    for fitem in [f for f in p.iterdir() if f.is_dir()]:
        for files in os.scandir(fitem):
            # if files.path.endswith(ext):
            if True:
                print("files",files)
                unique_set.add(files.name)

    print("unique_set",unique_set)
           
    

