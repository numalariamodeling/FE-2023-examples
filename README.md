# FE-2023-examples
Example scripts for 2023 faculty enrichment program in applied malaria modeling at Northwestern

### Technical track (EMOD)

**Overview**: 
Exercises usually consist of a simulation and an analyzer of simulation outputs. 
In some weeks, additional scripts exist to prepare simulation inputs or generate additional outputs and plots, or for model calibration as described in the instructions for the respective weeks.

**Checking results:**
For each week suggested simulation scripts for comparison or help during the exercise are provided in the folder [Solution_scripts](https://github.com/numalariamodeling/faculty-enrich-2022-examples/tree/main/Solution_scripts).

**Prerequisites**: 
Before running the weekly example scripts, please ensure that emodpy has been successfully [installed]((https://faculty-enrich-2022.netlify.app/modules/install-emod/))
and that the [repository has been cloned](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
to your home directory on quest, ideally as _/home/<.username>/FE-23-examples_.
Running your scripts will require that the emodpy virtual environment is loaded and assumes files are run from a working directory set to where the script is located.

**Week 1: Overview of EMOD**
This week we will be discussing EMOD's general structure and content as well as making sure you are reading to run the model on our linux-based HPC, QUEST. You will set up your own virtual environmet to run EMOD via emodpy and idmtools and clone this github repository to your home directory on QUEST. We will not be running any example scripts, but please familiarize yourself with the repo, website, and EMOD documentation.

**Week 2: Building Blocks**
This week's first exercise introduces the simplest version or running and analyzing a single simulation experiment in EMOD using the emodpy/idmtools infrastructure and python. Before running a simulation, one needs to check that all configurations and installations were successful and edit paths in the manifest file. The steps are generally to 1) run simulation and 2) analyze simulation outputs. 

This week's second exercise demonstrates how to create demographics and climate files and how to incorporate these into the simulation. The exercise further introduces how to modify config parameters (i.e. population size or simulation duration)

This week's final exercise will focus on observing changes in simulation results based on the InsetChart.json and MalariaSummaryReport.json model outputs.

**Week 3: Experiment Setups & Fine-Tuning**

**Week 4: Addressing Research Questions**