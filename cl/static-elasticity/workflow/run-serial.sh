CWD=$(pwd)
for f in $(find $1 | grep job.sh | sort) 
do 
    cd $(dirname $f) 
    pwd -P 
    bash $(basename $f)
    cd $CWD 
done

module purge