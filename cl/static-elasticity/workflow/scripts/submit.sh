jobs=`cat -`

for job_sh in $jobs
do
    workdir=`dirname $job_sh`
    script=`basename $job_sh`
    cd "$workdir"
    pwd -P
    sbatch "$script"
    cd -
done

