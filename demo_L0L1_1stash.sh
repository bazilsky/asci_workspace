#!/bin/bash

module load jaspy/2.7
model_dir='u-cb448'
mv 'model_runs'/$model_dir/'pp_files'/*.pp /gws/nopw/j04/asci/eeara/
python2.7 L0_processing_1stash.py
#python2.7 L1_processing.py
mv *.pp 'model_runs'/$model_dir/'pp_files'/
mv 2017* 'model_runs'/$model_dir/
mv All_months 'model_runs'/$model_dir/
#mv L1 'model_runs'/$model_dir/
#mv 2017* 'model_runs'/$model_dir/
mv Annual_mean 'model_runs'/$model_dir/
