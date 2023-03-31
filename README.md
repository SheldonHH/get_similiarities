 get_similiarities

1. EditDistance.py
function to edit distance


```bash
docker path: /data/Feb_2_2023/
physical path: /data/xiping/data/Feb_2_2023/
```
Purpose:
generate similiarity for every type of errors under a project

## 1. prerequisite
`/data/Feb_2_2023/occurances/$PROJECT`

1. manually create cc0.txt, cc1.txt, cc2.txt, cc3.txt,  gg0.txt  gg1.txt  gg2.txt  gg3.txt
- clang and gcc for 4 optimization
2. 
![image](https://user-images.githubusercontent.com/16319106/229024136-87496e4b-86e8-4fe7-9125-e6da13e32e5c.png)
![image](https://user-images.githubusercontent.com/16319106/229024268-a217ca66-ad59-4f66-ae1e-54abc0662f23.png)


## 2. Copy Files
1. call `cp_files.py` to copy files to respective folders under `projectTEs`
- generated error source: `/data/compilation_error/patch/`
- destination: `/data/gccTEs`
```bash
python3 cp_files.py sjeng
```

2. subfolder example
under gccTEs
```
IndexEachScore  c1            c2_lines.csv  g0            g1_lines.csv  g3            score_c2.txt  score_g2.txt
c0              c1_lines.csv  c3            g0_lines.csv  g2            g3_lines.csv  score_c3.txt  score_g3.txt
c0_lines.csv    c2            c3_lines.csv  g1            g2_lines.csv  score_c1.txt  score_g1.txt
```
![image](https://user-images.githubusercontent.com/16319106/229022674-b2ee9f38-2af4-4448-9470-7413ef84cf11.png)


3. Output folder  `/data/gccTEs`

`/data/sjengTEs`
`/data/gobmkTEs`

- expected output
- ![image](https://user-images.githubusercontent.com/16319106/229026838-ebac44b8-6ce8-4ab8-b273-92ad7bdf5f52.png)

## 3. Calculate Similiarity Scores
```bash
cd /data/get_similiarities

```
1. call `base_funcs.py`
under `/data/get_similiarities/` to generate base functions
```python
python3 base_funcs.py gcc
```

2. Specify the nameNumOfFoldersDict for total type of Errors for one application
![image](https://user-images.githubusercontent.com/16319106/229033438-4b40b929-0d77-4c35-94d6-7d1d4b665b4b.png)


3. call `EditDistance.py` 
```python
python3 EditDistance.py gcc
```



4. Use `bigger.py` to generate `bigger.csv` to create excel file for bigger output
for functions and occurances bigger picture respectively
![image](https://user-images.githubusercontent.com/16319106/229034342-5a72fd62-0c85-4055-80de-daeea40fe531.png)
- choice proj and occ_of_ff
- ![image](https://user-images.githubusercontent.com/16319106/229034454-f57ec58d-fcb5-472d-b2ad-0a0eeddab77a.png)


input the cc0.txt ...
output: bigger_result.csv
from here we know the number of errors to input in EditDistance.py

5. Output will be in (INDEX)
```bash
cd /data/gccTEs/$INDEX/
```
![image](https://user-images.githubusercontent.com/16319106/229033638-58d58134-82ea-49a3-a7de-93157bc3ad7f.png)


6. score_c1.txt means clang O0 vs clang O1
score_c2.txt means clang O1 vs clang O2
score_c3.txt means clang O2 vs clang O3

score_g1.txt means gcc O0 vs gcc O1
score_g2.txt means gcc O1 vs gcc O2
score_g3.txt means gcc O2 vs gcc O3
![image](https://user-images.githubusercontent.com/16319106/229034871-d9ae1d4d-7f6d-4d30-8c2e-67e77f93ac56.png)

7. KEEP in mind the bigger optimization level is the base for comparision (for score)

e.g. 
`score_c1.txt = c0 vs c1(base)`
```
line of score_c1.txt is 59
line of c1 should be 59

```
![image](https://user-images.githubusercontent.com/16319106/229037011-e87c1276-3ec6-4b62-96e7-967ef0b6841a.png)


## fine-grained becompared

- ![image](https://user-images.githubusercontent.com/16319106/229038325-7083a3e1-2831-4ed9-acab-40b4f714db5b.png)
- ![image](https://user-images.githubusercontent.com/16319106/229038365-3fd55186-6c9f-4288-97ce-65d8b87f9e52.png)
### the script is `/data/get_similiarities/f_func_err.py
![image](https://user-images.githubusercontent.com/16319106/229038470-66caafb2-0f02-4381-b31f-393b9ad24ec4.png)

## TODO
change the `ida` to `TEs` for all types of errors if we need fine-grained analysis
![image](https://user-images.githubusercontent.com/16319106/229038986-9df3d3f9-c43d-478b-8ea4-e5e92c2068a9.png)

### in EditDistance 
- to specify the index of Type error that we want to perform fine-grained analysis
![image](https://user-images.githubusercontent.com/16319106/229039581-20857967-b62b-4d68-9266-5b03c25601a1.png)


# II. scripts_decompile
- recompile without patch
- recompile with patch
```bash
cd /data/scripts_decompile
```
![image](https://user-images.githubusercontent.com/16319106/229041045-76837bbe-f53a-4428-b725-b37f8436e6eb.png)


```bash
./mtest.sh sjeng nop # without patch
./mtest.sh sjeng patch # with patch
```
![image](https://user-images.githubusercontent.com/16319106/229041682-56e78984-4ee4-450a-aebd-40ccc5c84485.png)


#### Output `/data/compilation_errors`

![image](https://user-images.githubusercontent.com/16319106/229042410-42ba4290-6400-43a0-88e5-c85f092f940e.png)

![image](https://user-images.githubusercontent.com/16319106/229042344-847b4c7b-330f-428c-9c15-34cb0b586756.png)

