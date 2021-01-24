#!/bin/bash
#SBATCH --partition=short-serial-4hr 
#SBATCH -o %j.out 
#SBATCH -e %j.err
#SBATCH --time=30:00


module load jaspy/2.7
model_dir='u-bz457'
python2.7 L1_processing.py
mv *.pp 'model_runs'/$model_dir/'pp_files'/
mv All_months 'model_runs'/$model_dir/
mv L1 'model_runs'/$model_dir/
mv 2017* 'model_runs'/$model_dir/
mv Annual_mean 'model_runs'/$model_dir/
