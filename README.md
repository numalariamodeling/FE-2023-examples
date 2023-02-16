# FE-2023-examples
Example scripts for 2023 faculty enrichment program in applied malaria modeling at Northwestern

## Technical track (EMOD)

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

### Week 1: Overview of EMOD
This week we will be discussing EMOD's general structure and content as well as making sure you are reading to run the model on our linux-based HPC, QUEST. You will set up your own virtual environmet to run EMOD via emodpy and idmtools and clone this github repository to your home directory on QUEST. We will not be running any example scripts, but please familiarize yourself with the repo, website, and EMOD documentation.

### Week 2: Building Blocks
This week's first exercise introduces the simplest version or running and analyzing a single simulation experiment in EMOD using the emodpy/idmtools infrastructure and python. Before running a simulation, one needs to check that all configurations and installations were successful and edit paths in the manifest file. The steps are generally to 1) run simulation and 2) analyze simulation outputs. 

This week's second exercise demonstrates how to create demographics and climate files and how to incorporate these into the simulation. The exercise further introduces how to modify config parameters (i.e. population size or simulation duration)

This week's final exercise will focus on observing changes in simulation results based on the InsetChart.json and MalariaSummaryReport.json model outputs.

**Instructions**
<details><summary><span>Click to expand</span></summary>
<p>

Basic Run

- Navigate to your local copy of this repository on QUEST: `cd ~/FE-2023-examples`
- Adjust paths in `manifest.py` by adding your username/netID to the end of the job directory: `/projects/b1139/FE-2023-examples/experiments/<username>`. This will help your track your simulations separately from other participants.
- Load your emodpy `SLURM_LOCAL` virtual environment
- Run simulation via `python3 example_run.py -l`
- Wait simulation to finish (~2 minutes)
- Go to the `experiments/<your username>` folder to find the generated experiment - it will be under a set of 16-digit alphanumeric strings. The structure of these strings is `Suite > Experiment > Simulations`. Due to current handling systems with SLURM you will not be able to see the experiment name given within the `example_run.py` script; however, this can be found in the experiment and simulation-level metadata.json files. You may also choose to sort your files based on time such that most recent experiments will appear first. Take a look through what was generated even in this simple run.

Adding inputs

This week's exercise demonstrates how to create demographics and climate files and how to incorporate these into the simulation as well as introducing how to modify config parameters (e.g. run number or simulation duration). Complete all of the steps below before running this next example.

1. Extracting climate data & adding to simulations
    - Checkout `example_site.csv` in the [inputs folder](https://github.com/numalariamodeling/FE-2023-examples/tree/main/inputs). This file contains coordinates for an example site in Uganda and establishes that this will be our "Node 1" in the model. You may use these coordinates or select a different site (and adjust the coordinates accordingly) if you like for the rest of this example.
    - Next, we'll run `extract_weather.py` - this script will run the weather generator. Notice that it reads information from `example_site.csv` to look for the right site and you can request weather for your time frame of interest. You'll also see that the platform for this is called *Calculon* - this is IDM's HPC _(requires access for climate database : ask someone from NU team)_
    - We can also run `recreate_weather.py` which will convert the weather files we just generated to a csv format that we can modify. For this example we don't need to make any modifications but this can be useful for research questions such as those relating to climate change. After running any modifications in the script we then convert the csv back to weather files.
    - Now that you know what the scripts do, load your virtual environment and use `python3 extract_weather.py` to run the extraction. Enter the credentials to access Calculon and wait for your weather files to be generated, when that is complete check your repo's inputs to make sure the files are there. Then run `python3 recreate_weather.py` and verify that the modified weather files have been created. Make sure you check the `recreate_weather.py` script to see where they should be located.
    - Copy `example_run.py` and name it `example_run_inputs.py` and in the script change the experiment name to `f'{user}_FE_example_inputs'`
    - Update default parameters in your simulation script (`example_run_inputs.py`)'s set_param_fn(). You'll also need to add your folder of climate files as an asset directory to the EMODTask in general_sim(), this must be set after the task is defined and before the experiment is created. It is recommended you put it directory after the "set sif":

```py
def set_param_fn(config):
    ## existing contents
    config.parameters.Air_Temperature_Filename = os.path.join('climate','example_air_temperature_daily.bin')
    config.parameters.Land_Temperature_Filename = os.path.join('climate','example_air_temperature_daily.bin')
    config.parameters.Rainfall_Filename = os.path.join('climate','example_rainfall_daily.bin')
    config.parameters.Relative_Humidity_Filename = os.path.join('climate', 'example_relative_humidity_daily.bin')

```
    
```py
def general_sim():   
    ## existing contents
    task.set_sif(manifest.SIF_PATH, platform)
    
    # add weather directory as an asset
    task.common_assets.add_directory(os.path.join(manifest.input_dir, "example_weather", "out"), relative_path="climate")
```
2. Adding demographics
    - You may have noticed a `build_demog()` function in the first example, now we'll look at it in more detail. There are a few ways to add demographics details to our simulations, primarily with a new generator where we add details as we go or from a csv or we can read in a pre-made json file. Here we'll use the `from_template_node` command in emodpy_malaria demographics with some basic information, such as latitude and longitude. We need to import this functionality directly from emodpy_malaria - you should see this at the top of your script
    - In the `build_demog()` function, you should see the template node command, add the latitude and longitude for your example site and increase the sample size to 1000.
    - We also want to add equilibrium vital dynamics to our script. This will set the birth and mortality rates to be equal so we have a relatively stable population in our simulations. For some experiments it can be desirable to set these seperately but for now this simple version will meet our needs. Add `SetEquilibriumVitalDynamics()` directly to the demographics file we are creating within the generator function (as seen below).
    - There are many aspects of demographics we are able to specify, such as the previously mentioned vital dynamics, risk distributions, and age distributions. The emod_api contains some existing age distributions. We'll need to import these PreDefined Distributions and then add it with `SetAgeDistribution` to our demographics file. Let's try adding the general distribution for Sub-Saharan Africa.
    
```py
import emodpy_malaria.demographics.MalariaDemographics as Demographics
import emod_api.demographics.PreDefinedDistributions as Distributions

def build_demog():
    """
    This function builds a demographics input file for the DTK using emod_api.
    """

    demog = Demographics.from_template_node(lat=0.4479, lon=33.2026, pop=1000, name="Example_Site")
    demog.SetEquilibriumVitalDynamics()
    
    age_distribution = Distributions.AgeDistribution_SSAfrica
    demog.SetAgeDistribution(age_distribution)

    return demog
```

3. Modifying configs
    - We also often want to modify some of the [config parameters](https://docs.idmod.org/projects/emod-malaria/en/latest/parameter-configuration.html) that control things like the within-host model, vectors, and simulation setup. In `example_run.py` we set the malaria team defaults using `config = conf.set_team_defaults(config, manifest)`, but we can also specify individual parameters like we did with the climate file names. Let's start with some simple things like adding setting the `Simulation_Duration` (how long the simulation should run in days) and the `Run_Number` (the random seed for the simulation) in `set_param_fn()`. Both of these can be done directly by referencing them as `config.parameters.<param_name>` and setting them equal to the desired value. The team typically uses a structure of `sim_years*365` with sim_years defined globally, at the top of the script beneath all imports, to set the duration.
    - Set the duration to 1 year and the run number to any number of your choosing.
    - Next, we'll add some mosquito species. There is a specific function for this, `add_species()` in emodpy_malaria malaria config. Try adding *A. gambiae*, *A. arabiensis*, and *A. funestus* to your config file:
    
```py    
def set_param_fn(config):
    ## existing contents
    
    conf.add_species(config, manifest, ["gambiae", "arabiensis", "funestus"])

    config.parameters.Simulation_Duration = sim_years*365
    config.parameters.Run_Number = 5
```
4. Now that you've added these changes, try running your new script with `python3 example_run_input.py -l`. Once it has succeeded go check on what has run. Do you see the changes to your demographics.json and the climate folder in the experiment's `Assets` directory? How about to config.json?

</p>
</details>

### Week 3: Experiment Setups & Fine-Tuning

### Week 4: Addressing Research Questions