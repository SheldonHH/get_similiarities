 get_similiarities

1. EditDistance.py
function to edit distance


```bash
docker path: /data/Feb_2_2023/
physical path: /data/xiping/data/Feb_2_2023/
```
Purpose:
generate similiarity for every type of errors under a project

## prerequisite
`/data/Feb_2_2023/occurances`
1. manually create cc0.txt, cc1.txt, cc2.txt, cc3.txt,  gg0.txt  gg1.txt  gg2.txt  gg3.txt
- clang and gcc for 4 optimization
2. 
![image](https://user-images.githubusercontent.com/16319106/229024136-87496e4b-86e8-4fe7-9125-e6da13e32e5c.png)
![image](https://user-images.githubusercontent.com/16319106/229024268-a217ca66-ad59-4f66-ae1e-54abc0662f23.png)


## main steps
1. call `cp_files.py` to copy files to respective folders under `projectTEs`
- generated error source: `/data/compilation_error/patch/`
- destination: `/data/gccTEs`


2. subfolder example
under gccTEs
```
IndexEachScore  c1            c2_lines.csv  g0            g1_lines.csv  g3            score_c2.txt  score_g2.txt
c0              c1_lines.csv  c3            g0_lines.csv  g2            g3_lines.csv  score_c3.txt  score_g3.txt
c0_lines.csv    c2            c3_lines.csv  g1            g2_lines.csv  score_c1.txt  score_g1.txt
```
![image](https://user-images.githubusercontent.com/16319106/229022674-b2ee9f38-2af4-4448-9470-7413ef84cf11.png)

