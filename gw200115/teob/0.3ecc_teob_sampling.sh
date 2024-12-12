#!/bin/bash
set -e
source /home/kkacanja/miniconda3/etc/profile.d/conda.sh
conda activate /home/kkacanja/miniconda3/envs/DALI
export LAL_DATA_PATH=/home/ksoni01/lalsuite/lalsuite-extra/data/lalsimulation/
export OMP_NUM_THREADS=1

pycbc_inference \
--config-file /home/kkacanja/ecc_gw190817/pe/gw200115/teob/0.3ecc_teob_sampling.ini \
--nprocesses 64 \
--processing-scheme mkl \
--output-file /home/kkacanja/ecc_gw190817/pe/gw200115/teob/result_teob_0.3ecc_sampling.hdf \
--seed 190814 \
--force \
--verbose 
