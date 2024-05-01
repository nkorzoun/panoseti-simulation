#!/bin/bash
#SBATCH --job-name=param                    # Job name
#SBATCH --mail-type=FAIL                    # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=nkorzoun@udel.edu       # Where to send mail	
#SBATCH --ntasks=1                          # Run a single task
#SBATCH --mem=1gb                           # Job Memory
#SBATCH --time=0-01:00:00                   # Time limit days-hrs:min:sec
#SBATCH --output=data/param_%a.log          # Standard output and error log
#SBATCH --array=1-100                      # Array range

# logging
date
echo Starting parameterization
echo '**********'

# requirements
vpkg_require cern-root
wait $!

# run script
echo -e ".L /home/3437/scripts/panodisplay.C\nreadFile(\"data/batch$SLURM_ARRAY_TASK_ID.root\")\nparamCSV(true)" | root -l -b 

# logging
echo '**********'
echo Finished parameterization
date