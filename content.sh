#!/bin/bash


#Written by Li Juan Chan in 15th August 2019 for the Summer of HPC program 2019.
#This is a bash script to run rhoPimpleFOAM with pipelines and store the results in an organised way. 

n_cores=$1     # The first argument of this script is the number of cores.
cat_conf=$2     # The second argument of this script is the name of the pipeline.

module load of-catalyst/1806-gcc-7.3.0-3w       

# Source tutorial run functions
. "$WM_PROJECT_DIR/bin/tools/RunFunctions"

# Remove all the previous results.
rm -r 2.6e-06 
rm log*
rm -r processor*

# Change the content in the decomposeParDict and catalyst files.
cd /gpfs/work/SoHPC_hpc19/nacaTest2/serverCineca.work/serverCineca_$n_cores/system/
./ncores.sh $n_cores
./catalyst.sh $cat_conf
cd /gpfs/work/SoHPC_hpc19/nacaTest2/serverCineca.work/serverCineca_$n_cores

# mv 0/ 0.end
# mv 6e-05/ 0/

# mv 0/uniform/ backup_file/

runApplication decomposePar >& log.decomposePar_rhoPimple

echo "The simulation is automatic. rhoPimpleFoam is performing."

START=`date +%s`

mpirun --mca mpi_cuda_support 0 -np $n_cores rhoPimpleFoam -parallel >& log.rhoPimple

END=`date +%s`

runtime=$((END-START))

runApplication reconstructPar -latestTime


# Store the result of simulation in a dedicated folder for future reference
mv log.rhoPimple log.rhoPimple.$cat_conf.$n_cores
mv log.rhoPimple.$cat_conf.$n_cores result/

# Store the images of Paraview Catalyst in a dedicated folder
cd /gpfs/work/SoHPC_hpc19/nacaTest2/serverCineca.work/serverCineca_$n_cores/insitu/
mkdir $cat_conf.$n_cores
mv $cat_conf* $cat_conf.$n_cores
mv $cat_conf.$n_cores/ /gpfs/work/SoHPC_hpc19/nacaTest2/insitu_compilation/$cat_conf/

# Write the execution time in an output file
echo $runtime >& /gpfs/work/SoHPC_hpc19/nacaTest2/time.out

cd /gpfs/work/SoHPC_hpc19/nacaTest2

# Copy the output time and store it in a file together with other pipelines.
./time.sh $n_cores $cat_conf
