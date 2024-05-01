#!/bin/bash
#SBATCH --job-name=inputs                   # Job name
#SBATCH --mail-type=FAIL                    # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=nkorzoun@udel.edu       # Where to send mail	
#SBATCH --ntasks=1                          # Run a single task
#SBATCH --mem=1gb                           # Job Memory
#SBATCH --time=0-00:03:00                   # Time limit days-hrs:min:sec
#SBATCH --output=config/_inputs.log      # Standard output and error log

# logging
date
echo Generating input files
echo '**********'

# requirements
vpkg_require anaconda

# make inputs
cd config
echo Using arguments "$@"
python /home/3437/scripts/corsikaBatchGenerator.py "$@"

# logging
echo '**********'
echo Finished generating $numFiles inputs
date