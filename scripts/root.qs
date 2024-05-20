#!/bin/bash
#SBATCH --job-name=root                     # Job name
#SBATCH --mail-type=FAIL, END               # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=nkorzoun@udel.edu       # Where to send mail	
#SBATCH --ntasks=1                          # Run a single task
#SBATCH --mem=1gb                           # Job Memory
#SBATCH --time=0-01:00:00                   # Time limit days-hrs:min:sec
#SBATCH --output=data/_merge.log            # Standard output and error log

# logging
date
echo Starting merge
echo '**********'

# requirements
vpkg_require cern-root
wait $!

# combine root files
cd data
numFiles=$(ls -lR *.root| wc -l)
echo Found $numFiles .root files
echo Merging...
hadd -f _merged.root *.root
wait $!

# logging
echo '**********'
echo Finished merge
date