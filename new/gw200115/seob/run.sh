#!/bin/bash
set -e
source /home/kkacanja/miniconda3/etc/profile.d/conda.sh
conda activate /home/kkacanja/miniconda3/envs/SEOBNRv5E
export LAL_DATA_PATH=/home/ksoni01/lalsuite/lalsuite-extra/data/lalsimulation/
export OMP_NUM_THREADS=1

pycbc_inference \
--config-file /home/kkacanja/ecc_pe/new/gw200115/seob/config.ini \
--nprocesses 64 \
--processing-scheme mkl \
--output-file /home/kkacanja/ecc_pe/new/gw200115/seob/result.hdf \
--seed 200115 \
--force \
--verbose 
