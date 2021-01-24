#!/bin/bash
#SBATCH -p par-multi
#SBATCH -n 36
#SBATCH -t 30
#SBATCH -o %j.log
#SBATCH -e %j.err


mpirun ./demo_L0L1_parallel.sh
