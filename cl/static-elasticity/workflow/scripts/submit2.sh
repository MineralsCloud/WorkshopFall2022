jobs=`cat -`

for job_sh in $jobs
do
    workdir=`dirname $job_sh`
    script=`basename $job_sh`
    cd "$workdir"
    pwd -P
    if [[ $(ls | grep "slurm" | wc -l) == 0 ]]
    then
        sbatch "$script"
    fi
    cd -
done

