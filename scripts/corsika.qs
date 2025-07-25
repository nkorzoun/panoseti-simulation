#!/bin/bash
#SBATCH --job-name=corsika                  # Job name
#SBATCH --requeue			    # Requeue if preempted	
#SBATCH --mail-type=FAIL,TIME_LIMIT_90,REQUEUE      # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=nkorzoun@udel.edu       # Where to send mail	
#SBATCH --ntasks=1                          # Run a single task
#SBATCH --mem=2gb                           # Job Memory
#SBATCH --time=7-00:00:00                   # Time limit days-hrs:min:sec
#SBATCH --output=data/corsika_%a.log        # Standard output and error log
#SBATCH --array=1-1000                      # Array range

# logging
date
echo Starting run $SLURM_ARRAY_TASK_ID
echo '**********'

# requirements
vpkg_require cern-root
wait $!

# in case of requeue
rm $dir/run/DATbatch$SLURM_ARRAY_TASK_ID.telescope

# start corsika
echo Starting corsika
cd run

/home/3437/Software/corsika/corsika-77410/run/corsika77410Linux_QGSII_urqmd < "../config/batch$SLURM_ARRAY_TASK_ID.inp"
wait $!

# send to corsikaIOreader
cd ..
dir=$(pwd)
cd /home/3437/Software/corsikaIOreader
echo Starting corsikaIOreader
./corsikaIOreader -cors "$dir/run/DATbatch$SLURM_ARRAY_TASK_ID.telescope" -histo "$dir/data/batch$SLURM_ARRAY_TASK_ID.root" -abs CORSIKA
wait $!

# logging
echo '**********'
echo Finished run $SLURM_ARRAY_TASK_ID
date
