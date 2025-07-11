#!/bin/bash
#SBATCH --job-name=final                    # Job name
#SBATCH --mail-type=FAIL,END                # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=nkorzoun@udel.edu       # Where to send mail	
#SBATCH --ntasks=1                          # Run a single task
#SBATCH --mem=1gb                           # Job Memory
#SBATCH --time=0-08:00:00                   # Time limit days-hrs:min:sec
#SBATCH --output=../panoseti_master.log     # Stabdard output and error log
#SBATCH --open-mode=append                  # Append to log
# logging
date
echo Starting final compression and merge
echo '**********'

# compress and merge
dir=$(pwd)
dirname=${dir##*/}
cd /home/3437
tar -czf $dirname.tar.gz $dirname/data $dirname/config
rm -rf $dirname

# logging
echo '**********'
echo Finished final
date
