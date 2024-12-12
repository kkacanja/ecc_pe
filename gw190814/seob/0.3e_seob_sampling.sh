#!/bin/bash
set -e
source /home/kkacanja/miniconda3/etc/profile.d/conda.sh
#conda activate /home/kkacanja/miniconda3/envs/SEOBNRv5E
conda activate /home/kkacanja/miniconda3/envs/seob_test
export LAL_DATA_PATH=/home/ksoni01/lalsuite/lalsuite-extra/data/lalsimulation/
export OMP_NUM_THREADS=1

pycbc_inference \
--config-file /home/kkacanja/ecc_gw190817/pe/gw190814/seob/0.3e_seob_sampling.ini \
--nprocesses 1 \
--processing-scheme mkl \
--output-file /home/kkacanja/ecc_gw190817/pe/gw190814/seob/result_seob_0.3e_sampling_public.hdf \
--seed 190814 \
--force \
--verbose 
