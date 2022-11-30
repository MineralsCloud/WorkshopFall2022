fname=$1
if grep -q "final" $fname
then
    touch "${fname}.final"
else
    echo "${fname} not final!" 1>&2
    exit 64
fi