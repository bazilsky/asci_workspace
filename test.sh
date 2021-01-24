#!/bin/bash
#BSUB -q short-serial
#BSUB -o %J.out 
#BSUB -e %J.err
#BSUB -W 02:45

mkdir model_runs/u-bf554/dump2
mv model_runs/u-bf554/All_months model_runs/u-bf554/dump2/
mv model_runs/u-bf554/L1 model_runs/u-bf554/dump2/


mkdir model_runs/u-bf559/dump2
mv model_runs/u-bf559/All_months model_runs/u-bf559/dump2/
mv model_runs/u-bf559/L1 model_runs/u-bf559/dump2/


mkdir model_runs/u-bf560/dump2
mv model_runs/u-bf560/All_months model_runs/u-bf560/dump2/
mv model_runs/u-bf560/L1 model_runs/u-bf560/dump2/



