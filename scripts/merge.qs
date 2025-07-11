#!/bin/bash
#SBATCH --job-name=merge                    # Job name
#SBATCH --mail-type=FAIL                    # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=nkorzoun@udel.edu       # Where to send mail	
#SBATCH --ntasks=1                          # Run a single task
#SBATCH --mem=1gb                           # Job Memory
#SBATCH --time=0-08:00:00                   # Time limit days-hrs:min:sec
#SBATCH --output=../panoseti_master.log     # Stabdard output and error log
#SBATCH --open-mode=append                  # Append to log

# logging
date
echo Starting csv merge
echo '**********'

# combine CSV files
awk 'FNR==1 && NR!=1{next;}{print}' data/*.csv > data/_merged.csv

# logging
echo '**********'
echo Finished merge
date
