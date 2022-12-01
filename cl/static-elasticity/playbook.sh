
wget http://snf-4850.vlab.ac.ke:8000/workflow.tar.gz
mkdir test &&  tar -xvf workflow.tar.gz -C test
cd ~/test/workflow

mkdir pseudo && wget -qO- http://www.physics.rutgers.edu/gbrv/all_lda_UPF_v1.5.tar.gz | tar -xzv -C pseudo

# edit templates/relax.in, templates/elast.in

wget http://snf-4850.vlab.ac.ke:8000/mphys.tar.gz
mkdir mphys && tar -xvf mphys.tar.gz -C mphys

wget http://snf-4850.vlab.ac.ke:8000/qe.tar.gz
mkdir qe && tar -xvf qe.tar.gz -C qe

. qe/bin/activate
conda-unpack
. qe/bin/deactivate

. mphys/bin/activate
conda-unpack
. mphys/bin/deactivate

# edit the config.yml file

# create the input files for eos calculation

. mphys/bin/activate
snakemake -j4 vc_target
. mphys/bin/deactivate
 

# perform eos calculation

. qe/bin/activate
bash run-serial.sh relax
. qe/bin/deactivate

# get eos results

. mphys/bin/activate
snakemake -j4 vc_eos
. mphys/bin/deactivate

# create the input files for elasticity calculation

. mphys/bin/activate
snakemake -j4 elast_target
. mphys/bin/deactivate


# perform elasticity calculation

. qe/bin/activate
bash run-serial.sh elast
. qe/bin/deactivate

# edit config.yaml to keep only one volume (or the volume that finishes)

. mphys/bin/activate
snakemake -j4 elast_dat
. mphys/bin/deactivate

