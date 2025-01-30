#!/bin/bash
set -e
source /home/kkacanja/miniconda3/etc/profile.d/conda.sh
conda activate /home/kkacanja/miniconda3/envs/DALI
export LAL_DATA_PATH=/home/ksoni01/lalsuite/lalsuite-extra/data/lalsimulation/
export OMP_NUM_THREADS=1

pycbc_inference_model_stats \
--input-file /home/kkacanja/ecc_pe/gw200105/teob/0.3/no_marg/new_run/result_splotchy_increased_sampling.hdf \
--output-file /home/kkacanja/ecc_pe/gw200105/teob/0.3/no_marg/new_run/check_stats.hdf \
--nprocesses 1 \
--reconstruct-parameters \
--force \
--verbose
