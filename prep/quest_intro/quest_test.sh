#!/bin/bash
#SBATCH --account=b1139  
#SBATCH --partition=b1139
#SBATCH --nodes=1                            ## how many computers do you need?
#SBATCH --ntasks-per-node=1                  ## how many cpus or processors do you need on each computer?
#SBATCH --time=00:10:00                      ## time needed to run (HH:MM:SS)
#SBATCH --mem-per-cpu=1G                     ## RAM per CPU, also see --mem=<XX>G for RAM per node/computer 
#SBATCH --job-name=quest_example             ## When you run squeue -u NETID this is how you can identify the job
#SBATCH --output=outlog                      ## standard output goes to this file
#SBATCH --error=errlog                       ## standard error goes to this file
#SBATCH --mail-type=ALL                      ## receive e-mail alerts from SLURM when your job begins and finishes
#SBATCH --mail-user=<email>@northwestern.edu 

module purge all
module load python

python --version
python quest_test.py --name STRANGER  # Replace with your name to supply to python script
