#!/bin/bash
#SBATCH -p par-multi
#SBATCH -n 36
#SBATCH -t 30
#SBATCH -o %j.log
#SBATCH -e %j.err

module load jaspy/2.7
model_dir='u-cb557'
mv 'model_runs'/$model_dir/'pp_files'/*.pp /group_workspaces/jasmin2/asci/eeara/
python2.7 L0_processing_forcing.py
python2.7 L1_processing.py
mv *.pp 'model_runs'/$model_dir/'pp_files'/
mv All_months 'model_runs'/$model_dir/
mv L1 'model_runs'/$model_dir/
mv 2017* 'model_runs'/$model_dir/
mv Annual_mean 'model_runs'/$model_dir/
