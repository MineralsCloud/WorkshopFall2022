dname=$1

if [ ! -f "${dname}/dyn0" ] || [ ! -s "${dname}/dyn0" ]
then
    echo "${dname}/dyn0 not final!" 1>&2
fi

ndyn=`cat ${dname}/dyn0 | sed -n "2 p"`

for i in `seq 1 $ndyn`
do
    dyn="dyn${i}"
    if [ ! -f "${dname}/$dyn" ] || [ ! -s "${dname}/$dyn" ]
    then
        echo "${dname}/${dyn} not final!" 1>&2
        exit 64
        break
    fi
done
touch "${dname}/ph.final"