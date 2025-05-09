#!/bin/bash
#SBATCH --job-name=panoseti_master
#SBATCH --error=../panoseti_master.err
#SBATCH --time=7-00:00:00
#SBATCH --mem=1GB
#SBATCH --ntasks=1

# Load necessary modules (if any)
# module load <module-name>

#################################
# Arg Handling
#################################

# Define a blacklist of arguments
blacklist=("scripts" "Software")

# Argument handling
while getopts ":p:e:m:z:a:s:" opt; do
  case $opt in
    p) arg_p="$OPTARG";;
    e) arg_e="$OPTARG";;
    m) arg_m="$OPTARG";;
    z) arg_z="$OPTARG";;
    a) arg_a="$OPTARG";;
    s) arg_s="$OPTARG";;
    \?) echo "Invalid option: -$OPTARG" >&2;;
    :) echo "Option -$OPTARG requires an argument." >&2;;
  esac
done

# Shift to the first non-option argument (positional argument)
shift "$((OPTIND - 1))"

# Check for the required positional argument
if [ $# -gt 0 ]; then
  positional_arg="$1"

  # Check if the positional argument is in the blacklist
  if [[ " ${blacklist[@]} " =~ " $positional_arg " ]]; then
    echo "Error: The directory name $1 is blacklisted for safety." >&2
    exit 1
  fi
else
  echo "Error: A required positional argument is missing." >&2
  echo "Usage: sbatch master.qs <directory-name>"
  exit 1
fi

# Directory setup
dir=/home/3437/$1
mkdir -p $dir/config $dir/data $dir/run

# Generate inputs
inputs=$(sbatch --chdir=$dir --parsable inputs.qs \
    ${arg_p:+ -p="$arg_p"} \
    ${arg_e:+ -e="$arg_e"} \
    ${arg_m:+ -m="$arg_m"} \
    ${arg_z:+ -z="$arg_z"} \
    ${arg_a:+ -a="$arg_a"} \
    ${arg_s:+ -s="$arg_s"}
)

# Create symlinks to necessary files
for file in /home/3437/Software/corsika/corsika-77410/run/*; do 
    ln -s "$file" "$dir/run/$(basename "$file")"; 
done

# Run corsika and corsikaIOreader
corsika=$(sbatch --wait --chdir=$dir --dependency=afterok:$inputs --parsable corsika.qs)

# Move corsika data and remove symlinks
mv "$dir/run/*.telescope" "$dir/data"
wait
rm -rf $dir/run

# Parameterize events
param=$(sbatch --wait --chdir=$dir --dependency=afterok:$corsika --parsable param.qs)

# Combine CSV files
awk 'FNR==1 && NR!=1{next;}{print}' $dir/data/*.csv > $dir/data/_merged.csv

# Combine .root files
root=$(sbatch --wait --chdir=$dir --dependency=afterok:$param --parsable root.qs)

# Zip the output directory
wait
cd /home/3437
tar -czf $1.tar.gz $1/data $1/config

# Clean up
rm -rf $dir

