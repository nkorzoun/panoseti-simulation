#!/bin/bash
#SBATCH --job-name=panoseti_master
#SBATCH --error=../panoseti_master.err
#SBATCH --time=7-00:00:00
#SBATCH --mem=1GB
#SBATCH --ntasks=1
#SBATCH --output=../panoseti_master.log

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
corsika=$(sbatch --chdir=$dir --dependency=afterok:$inputs --parsable corsika.qs)
echo "corsika job ID:$corsika"
sleep 10

# Move corsika data and remove symlinks
array_range=$(grep "#SBATCH.*--array" corsika.qs | sed 's/.*--array=\([0-9-]*\).*/\1/')
cleanup=$(sbatch --chdir=$dir --dependency=afterok:${corsika}_[${array_range}] --parsable cleanup.qs)
echo "cleanup job ID:$cleanup"
sleep 10

# Parameterize events
param=$(sbatch --chdir=$dir --dependency=afterok:$cleanup --parsable param.qs)
echo "param job ID:$param"
sleep 10

# Combine CSV files
merge=$(sbatch --chdir=$dir --dependency=afterok:$param --parsable merge.qs)
echo "merge job ID:$merge"
sleep 10

# Combine .root files
root=$(sbatch --chdir=$dir --dependency=afterok:$merge --parsable root.qs)
echo "root job ID:$root"
sleep 10

# Zip the output directory
final=$(sbatch --chdir=$dir --dependency=afterok:$root --parsable final.qs)
echo "final job ID:$final"

echo "Pipeline submitted"
echo "Monitor with: squeue -j <job ID>"
