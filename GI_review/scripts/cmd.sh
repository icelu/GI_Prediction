declare -a arr=("islandpath3" "islandpickv3" "islandviewerv3" "sigighmmv3" "GIHunter" "EGID" "gisvm" "trnacc")
for i in "${arr[@]}"
do
echo "$i"
python ./scripts/IntervalOverlap.py -c 0.5 -q ./predictions/"$i".gilist -i ./predictions/ct18_ref.gilist -p ./genome/NC_003198.ptt > ./evaluations/eval_std_"$i"_ct18_overlap
done

# get the output in a table
python ./scripts/parseEval.py -d ./evaluations