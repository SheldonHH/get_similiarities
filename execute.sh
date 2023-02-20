proj=$1
rm -r ${proj}ida/index_to_lookup && ${proj}ida/compared
rm -r ${proj}ida/*.txt
rm -r ${proj}ida/*.csv
sleep 2
python3 base_funcs.py $1 && python3 EditDistance.py $1 && python3 f_func_err.py $1