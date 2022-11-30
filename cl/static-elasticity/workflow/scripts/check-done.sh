fname=$1
if grep -q "DONE" $fname
then
    touch "${fname}.done"
else
    echo "${fname} not done!" 1>&2
    exit 64
fi