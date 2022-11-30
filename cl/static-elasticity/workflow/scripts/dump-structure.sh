nat=$1
fname=$2

cat $fname | grep "End final coordinates" -B $(($nat + 6)) | sed -e "$ d"