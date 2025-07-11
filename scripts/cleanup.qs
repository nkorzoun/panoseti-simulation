#!/bin/bash
#SBATCH --job-name=cleanup                  # Job name
#SBATCH --mail-type=FAIL                    # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=nkorzoun@udel.edu       # Where to send mail	
#SBATCH --ntasks=1                          # Run a single task
#SBATCH --mem=1gb                           # Job Memory
#SBATCH --time=0-08:00:00                   # Time limit days-hrs:min:sec
#SBATCH --output=../panoseti_master.log     # Stabdard output and error log
#SBATCH --open-mode=append                  # Append to log

# logging
date
echo Starting corsika cleanup
echo '**********'

# Move corsika data and remove symlinks
mv run/*.telescope data
rm -rf run 

# logging
echo '**********'
echo Finished cleanup
date
