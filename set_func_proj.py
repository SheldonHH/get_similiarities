import os

    
gcc_set = set()
folders = ["c0","c1","c2","c3"]
for fd in folders:
    directory = os.fsencode("/data/get_similiarities/gccida/"+fd)
    for file in os.listdir(directory):
        gcc_set.add(str(file.decode()))
        


# print("gcc_set",sorted(gcc_set))
set_to_str = ""
for gitem in sorted(gcc_set):
    set_to_str += gitem + ","


print("set_to_str:",set_to_str)