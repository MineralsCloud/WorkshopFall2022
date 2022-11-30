fname=$1
cat $fname | grep "total   stress" -A 3 | tail -3 | cut -c-40