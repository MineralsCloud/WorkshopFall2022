{% include "partials/hpc/" + machine + "/job_header_short.sh" %}

{% include "partials/hpc/" + machine + "/load_qe.sh" %}

LOG=log.txt

pwd > $LOG
date >> $LOG

echo "CPU_SET=${CPU_SET}" >> $LOG
echo "NP=${NP}" >> $LOG

if [[ ! -z "${CPU_SET}" ]] && [[ ! -z "${NP}" ]]
then
    MPI_ARGS="--bind-to core -n $NP --cpu-set $CPU_SET --mca btl_openib_if_include 'mlx5_2:1' --mca btl openib,self,vader --report-bindings"
else
    MPI_ARGS="--map-by core --mca btl_openib_if_include 'mlx5_2:1' --mca btl openib,self,vader --report-bindings"
fi

STEM=scf
INPUT=$STEM.in
OUTPUT=$STEM.out
ERR=$STEM.err

echo $MPI_ARGS
echo $MPI_ARGS >> $LOG

mpirun $MPI_ARGS pw.x -npool 4 -input $INPUT 1>$OUTPUT 2>$ERR

sleep 5
date >> $LOG