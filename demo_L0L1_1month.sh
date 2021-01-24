#!/bin/bash

model_dir='u-bx903'
mv 'model_runs'/$model_dir/'pp_files'/*.pp /group_workspaces/jasmin2/asci/eeara/
python2.7 L0_processing_forcing.py
#python2.7 L1_processing.py
mv *.pp 'model_runs'/$model_dir/'pp_files'/
mv All_months 'model_runs'/$model_dir/
#mv L1 'model_runs'/$model_dir/
mv 2017* 'model_runs'/$model_dir/
#mv Annual_mean 'model_runs'/$model_dir/
