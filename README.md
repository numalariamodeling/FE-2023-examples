# FE-2023-examples
Example scripts for 2023 faculty enrichment program in applied malaria modeling at Northwestern

[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/numalariamodeling/FE-2023-examples/blob/main/README.md)
[![fr](https://img.shields.io/badge/lang-fr-red.svg)](https://github.com/numalariamodeling/FE-2023-examples/blob/main/README.fr.md)


## Technical track (EMOD)

**Overview:**
Exercises usually consist of a simulation and an analyzer of simulation outputs. 
In some weeks, additional scripts exist to prepare simulation inputs or generate additional outputs and plots, or for model calibration as described in the instructions for the respective weeks.

**Checking results:**
For each week suggested simulation scripts for comparison or help during the exercise are provided in the respective week's folder.

**Prerequisites**: 
Before running the weekly example scripts, please ensure that emodpy has been successfully [installed](https://faculty-enrich-2022.netlify.app/modules/install-emod/)
and that the [repository has been cloned](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
to your home directory on QUEST, ideally as _/home/<.username>/FE-2023-examples_.
Running your scripts will require that the emodpy virtual environment is loaded and assumes files are run from a working directory set to where the script is located. Before you start on an exercise, make sure that you have pulled or fetched the latest changes from the repository (see git-guides [git-pull](https://github.com/git-guides/git-pull)).

### Week 1: Overview of EMOD
This week we will be discussing EMOD's general structure and content as well as making sure you are ready to run the model on our linux-based HPC, QUEST. You will set up your own virtual environmet to run EMOD via emodpy and idmtools and clone this github repository to your home directory on QUEST. We will not be running any example scripts, but please familiarize yourself with the repo, website, and EMOD documentation.

### Week 2: Building Blocks
This week's first exercise introduces the simplest version of running and analyzing a single simulation experiment in EMOD using the emodpy/idmtools infrastructure and python. Before running a simulation, one needs to check that all configurations and installations were successful and edit paths in the manifest file. The steps are generally to

1. run simulation, and   
2. analyze simulation outputs. 

This week's second exercise demonstrates how to create demographics and climate files and how to incorporate these into the simulation. The exercise further introduces how to modify config parameters (i.e. population size or simulation duration)

This week's final exercise will focus on observing changes in simulation results based on the InsetChart.json and MalariaSummaryReport.json model outputs.

**Instructions**

Click the arrow to expand:
<details><summary><span><em>Running a simple EMOD simulation</em></span></summary>
<p>


- Navigate to your local copy of this repository on QUEST: `cd ~/FE-2023-examples`  
- Notice your job directory path in `manifest.py`: `/projects/b1139/FE-2023-examples/experiments/<username>`. This will help your track your simulations separately from other participants.  
- Load your emodpy `SLURM_LOCAL` virtual environment  
- Run simulation via `python3 example_run.py -l`  
- Wait for simulation to finish (~2 minutes)  
- Go to the job directory (see `experiments/<your username>` above) folder to find the generated experiment - it will be under a set of 16-digit alphanumeric strings. The structure of these strings is `Suite > Experiment > Simulations`. Due to current handling systems with SLURM you will not be able to see the experiment name given within the `example_run.py` script; however, this can be found in the experiment and simulation-level metadata.json files. You may also choose to sort your files based on time such that most recent experiments will appear first. 
- Take a look through what was generated even in this simple run and get familiar with the file structure.  

</p>
</details>

<details><summary><span><em>Adding Inputs</em></span></summary>
<p>

This exercise demonstrates how to create demographics and climate files and how to incorporate these into the simulation as well as introducing how to modify config parameters (e.g. run number or simulation duration). Complete all of the steps below before running this next example.



1. Extracting climate data & adding to simulations
    - Checkout `example_site.csv` in the [inputs folder](https://github.com/numalariamodeling/FE-2023-examples/tree/main/inputs). This file contains coordinates for an example site in Uganda and establishes that this will be our "Node 1" in the model. You may use these coordinates or select a different site (and adjust the coordinates accordingly) if you like for the rest of this example.
    - Next, we'll run `extract_weather.py` - this script will run the weather generator. Notice that it reads information from `example_site.csv` to look for the right site and you can request weather for your time frame of interest. You'll also see that the platform for this is called *Calculon* - this is IDM's HPC _(requires access for climate database : ask someone from NU team)_
        - We can also run `recreate_weather.py` which will convert the weather files we just generated to a csv format that we can modify. For this example we don't need to make any modifications but this can be useful for research questions such as those relating to climate change. After running any modifications in the script we then convert the csv back to weather files.  
    - Now that you know what the scripts do, load your virtual environment and use `python3 extract_weather.py` to run the extraction.   
        - Enter the credentials to access Calculon and wait for your weather files to be generated, when that is complete check your repo's inputs to make sure the files are there.   
        - Then run `python3 recreate_weather.py` and verify that the modified weather files have been created. Make sure you check the `recreate_weather.py` script to see where they should be located.
    - Copy `example_run.py` and name it `example_run_inputs.py` and in the script change the experiment name to `f'{user}_FE_example_inputs'`
    - Update default parameters in your simulation script (`example_run_inputs.py`)'s `set_param_fn()`. You'll also need to add your folder of climate files as an asset directory to the EMODTask in general_sim(), this must be set after the task is defined and before the experiment is created. It is recommended you put it directory after the "set sif":

```py
def set_param_fn():
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
    - We also want to add equilibrium vital dynamics to our script. This will set the birth and mortality rates to be equal so we have a relatively stable population in our simulations. For some experiments it can be desirable to set these separately but for now this simple version will meet our needs. Add `SetEquilibriumVitalDynamics()` directly to the demographics file we are creating within the generator function (as seen below).
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
sim_years = 1

def set_param_fn():
    ## existing contents
    
    conf.add_species(config, manifest, ["gambiae", "arabiensis", "funestus"])

    config.parameters.Simulation_Duration = sim_years*365
    config.parameters.Run_Number = 5
```

4. Now that you've added these changes, try running your new script with `python3 example_run_input.py -l`. Once it has succeeded go check on what has run. Do you see the changes to your demographics.json and the climate folder in the experiment's `Assets` directory? How about to config.json or stdout.txt? You should also see [`InsetChart.json`](https://docs.idmod.org/projects/emod-malaria/en/latest/software-report-inset-chart.html) in the simulation's output folder - this is EMOD's default report that will give you an idea of what's going on in your simulation. We'll explore this more later in the Analysis section of Week 2.

</p>
</details>


<details><summary><span><em>Adding outputs</em></span></summary>
<p>

This exercise demonstrates how to add some of the malaria built-in reporters to our sims. These reports can help us understand what is going on in our simulations from basic targets like incidence and prevalence to more detailed pictures of events or within-host data such as parasitemia. You can read more about the possible types of analyzers in the [EMOD output file documentation](https://docs.idmod.org/projects/emod-malaria/en/latest/software-outputs.html). In this exercise we'll add the Report Event Recorder and Malaria Summary Report to the simulations.

- Copy your `example_run_inputs.py` script and name it `example_run_outputs.py`. Change the experiment name to `f'{user}_FE_example_outputs'`.
- We need to import the malaria reporters from emodpy_malaria. You'll need to add this line to the rest of your emodpy_malaria importers `from emodpy_malaria.reporters.builtin import *` at the top of your script. Notice the "*" at the end, this means we are importing all of the reporters from the builtin reporter script by their names.
- [Report Event Recorder](https://docs.idmod.org/projects/emod-malaria/en/latest/software-report-event-recorder.html) allows us to look at various events happening to each individual in our sim, as well as some basic demographic and health status information about the individual. This report is especially useful for monitoring different interventions, such as receiving treatment, but for now we'll only look at simple events such as births or existing individuals' birthdays. We can control the time period we want to report on, from `start_day` to `end_day` as well as things like target age group and nodes while we add the reporter. For now, let's add the report for the entire simulation and targeting ages 0-100 years, so likely the whole population. It can be added to our `general_sim()` with `add_event_recorder()` after the task has been defined, around line 110:

```py
def general_sim()
    ## existing contents
    
    add_event_recorder(task, event_list=["HappyBirthday", "Births"],
                       start_day=1, end_day=sim_years*365, node_ids=[1], min_age_years=0,
                       max_age_years=100)
```

- [Malaria Summary Report](https://docs.idmod.org/projects/emod-malaria/en/latest/software-report-malaria-summary.html) provides a population-level summary of malaria data grouped into different bins such as age, parasitemia, and infectiousness. This report will give us information such as PfPR, clinical incidence, and population stratified by time (as well as age bins, parasitemia, and infectiousness if desired). We can specify what time period of aggregation we are interested in, typically weekly, monthly, or annually through the reporting interval. The linked documentation will show you many other things we can specify as well, but for now we'll keep it simple and set our report to run monthly for the duration of the simulation with simple age groups: 0-0.25, 0.25-5, and 5-115 years. We'll also tell the report that we want a maximum of 20 intervals so we can make sure we get all our monthly reports for 1 year and use `pretty_format` to make the outputted report more readable to us. You should also add a filename suffix, in this case we'll use "monthly" to give some additional description to the report. This should be added directly after the Report Event Recorder, also in `general_sim()` with `add_malaria_summary_report()`:

```py
def general_sim()
    ## existing contents
    
    ## previously added event recorder
    
    add_malaria_summary_report(task, manifest, start_day=1, end_day=sim_years*365, reporting_interval=30,
                               age_bins=[0.25, 5, 115],
                               max_number_reports=20,
                               filename_suffix='monthly',
                               pretty_format=True)
```

- Now try running your new script as you learned in the past two examples and wait for it to finish before navigating to your experiment directory. When it's done running, check out the simulation outputs and your new report.

</p>
</details>


<details><summary><span><em>Analysis</em></span></summary>
<p>

Now that you've learned the basics of how to run EMOD and add inputs/outputs you can start actually analyzing some data! We use analyzer scripts to extract the data we want from our simulations' reports to understand what the simulation is doing, how it is changing, and answer research questions. This week's analyzer script, `analyzer_W2.py` contains two different analyzers:

1. InsetChartAnalyzer that extracts data from `Inset_Chart.json`. Notice the `channels_inset_chart` in line 159 - this tells defines which data channels we are interested in looking at. Six different channels are included currently but these can always be modified depending on what you want to explore. 
2. MonthlyPfPRAnalyzer that extracts data from the monthly summary report. If you look at the guts of the analyzer (lines 62 - 138), you'll see that this will particularly focus on extracting PfPR, Clinical Incidence (per person per year), Severe Incidence (per person per year), and Population, all by time (month) and age bins.

- You'll also notice `sweep_variables` being defined and going into both analyzers - we'll discuss this in more depth in Week 3, but for now you can think of this like a tag (or set of tags) for our simulation(s).

- Before we can run the analyzer script, you need to make a few changes:
    1. Set your `jdir` (short for job directory) to where your experiments are saved (*/projects/b1139/FE-2023-examples/experiments/<username>*). Notice that this is used for the platform, and we also set `wdir` (working directory) for the analyzer where the analyzers will output any results you have requested
    2. Define your experiment name and ID in the `expts` dictionary (line 147) - these should match the UID and name in the experiment level `metadata.json` for your experiment of interest:

```py
 expts = {
        '<user>_FE_example_outputs' : '<experiment UID'
    }
```

- This week's analyzer script also includes a basic python plotter for the results from InsetChartAnalyzer that will help you visualize each of the `channels_inset_chart` throughout the simulation. Take a look through the code to see if you can tell what it is doing before running it.
- Run the analyzer, you will not need the `-l` command as the platform is set to run only with `SLURM_LOCAL` right now
- Wait for the analyzer to succeed. Once it is finished check out your new outputs (see if you can find the `wdir` mentioned above without help). You should see two csvs, one from each analyzer, as well as a InsetChart.png.
- As an additional exercise, try to make a data visualization in R or python based off of the MonthlyPfPRAnalyzer output (PfPR_Clinical_Incidence_monthly.csv). You'll need to take a look through the output file and decide what kind of figure may be interesting and inform you about your simulation. *Note: there is no solution script for this, it is an exercise of creativity and data visualization skills where everyone may have unique ideas*
- Once you've completed your data visualization exercise, feel free to try changing some other [config parameters](https://docs.idmod.org/projects/emod-malaria/en/latest/parameter-configuration.html) in your example script. Run additional simulations with different durations, population sizes, agebins, etc. - whatever you think would be interesting! This is a great time to look through the EMOD documentation and explore parameters so you get to know the EMOD ecosystem better. *(Tip: change your experiment name to keep track of your simulations in both the metadata and analyzer outputs)*
    - You can also run these sims through the analyzer script by updating the experiment name and ID, as above. Do this and inspect the outputs as well as any changes compared to your first run. What do you see? 
        - How have the outcomes changed? 
        - What do you recognize about running time?
    - You may also want to run the analyzer on your very first, simple EMOD run to see how adding our input files has changed the simulation


</p>
</details>

### Week 3: Experiment Setups & Fine-Tuning
This week's exercises will focus on how to design and setup more detailed experiments. We will cover sweeping over config parameters, serialization, and calibration. 

This week's first exercise introduces the concept of "sweeping"

the simplest version of running and analyzing a single simulation experiment in EMOD using the emodpy/idmtools infrastructure and python. Before running a simulation, one needs to check that all configurations and installations were successful and edit paths in the manifest file. The steps are generally to

1. run simulation, and   
2. analyze simulation outputs. 

This week's second exercise demonstrates how to create demographics and climate files and how to incorporate these into the simulation. The exercise further introduces how to modify config parameters (i.e. population size or simulation duration)

This week's final exercise will focus on observing changes in simulation results based on the InsetChart.json and MalariaSummaryReport.json model outputs.

**Instructions**

Click the arrow to expand:
<details><summary><span><em>Parameter Sweeping</em></span></summary>
<p>

This exercise demonstrates how to "sweep" over parameters to have a set of different values across our experiment. There are a variety of reasons we may want to test out a range of parameter values, some examples include:
    - running multiple stochastic realizations (this example)
    - testing fit for calibration, such as with amount of larval mosquito habitat (calibration example, later this week)
    - testing different intervention configurations, such as coverage levels or repetitions (we'll look at this more next week) 

For now we'll start with a simple sweep over one config parameter, such as the run number. There are additional more complicated sweeping methods, particularly with creating campaigns, that we will discuss later in the program.


- Copy your `example_run_outputs.py` script and name it `example_run_sweeps.py`. Change the experiment name to `f'{user}_FE_example_sweep'`.
- To sweep over variables we'll have to switch to using a simulation builder from `idmtools` rather than creating simulations directly from the task. Add `from idmtools.builders import SimulationBuilder` to your import statements. We'll modify this simulation creation in `general_sim()` shortly.
- Beneath where you set the `sim_years`, set `num_seeds = 5`. We'll use this later to tell EMOD how many different run numbers, or stochastic realizations, we want for this experiment.
- Next, define a simple function that will allow you to set individual config parameters under the `set_param_fn()` where you define the constant config parameters. 

```py
def set_param(simulation, param, value):
    """
    Set specific parameter value
    Args:
        simulation: idmtools Simulation
        param: parameter
        value: new value
    Returns:
        dict
    """
    return simulation.task.set_parameter(param, value)
```

- As mentioned, we also need to adjust the way we create our experiments in `general_sim()`. Notice that we are currently use `Experiment.from_task()` which creates the experiment and simulations directly from the defined task. To sweep over variables we'll have to switch to using `Experiment.from_builder()` that works to setup each simulation directly rather than an entire experiment with the same parameters.
    - First, initialize the builder such that `builder = SimulationBuilder()`. This should go in `general_sim()` between adding assets and reports. 
    - Add the sweep to the builder using `add_sweep_definition()`. Here you'll create a partial of `set_param` (defined above), pass the config parameter that you'd like to set to this partial, and then provide the range of values to sweep over. In this example, tell the function to sweep over `Run_Number` over the range of the `num_seeds` defined above (will output values of 0 - `num_seeds`).
    - Finally, you'll need to remove the `Experiment.from_task()` creation and replace with `Experiment.from_builder(builder, task, name=<expname>)`. This will create experiments based on the task but with the additional information contained in the builder, including the added sweep. Make sure you keep the modified experiment name!

```py
def general_sim()
    ## existing contents

    # Create simulation sweep with builder
    builder = SimulationBuilder()
    
    builder.add_sweep_definition(partial(set_param, param='Run_Number'), range(num_seeds))
    
    ## reports are still located here
    
    # create experiment from builder
    experiment = Experiment.from_builder(builder, task, name="example_sim_sweep")
```

</p>
</details>

<details><summary><span><em>Serialization</em></span></summary>
<p>

This exercise demonstrates the concept of serializing populations in simulations. Serialization allows us to run simulations, save them at a certain point in time, and simulate another campaign/scenario starting from the point we saved. We can run multiple simulations on the same population in series.

We often use this process to save long initial simulations called burnins, during which population immunity is established. We don't want to wait for this to run everytime, so we serialize the population at the end of the burnin and then run shorter simulations, typically with additional interventions (also called "pickup" simulations).

The exercise has three parts. In part 1 you will run and save a burnin simulation. In part 2 you will "pickup" this simulation and add antimalarial interventions. In part 3 you will repeat parts 1 & 2 using a longer burnin duration, and compare the results.

1. Burning in
2. Picking up
3. Compare pickup simulations across varying burnin durations

</p>
</details>

<details><summary><span><em>Calibration</em></span></summary>
<p>

1. Running calibration sweeps
2. Parameter selection

</p>
</details>

### Week 4: Addressing Research Questions

**Instructions**

Click the arrow to expand:
<details><summary><span><em>Individual Properties</em></span></summary>
<p

</p>
</details>

<details><summary><span><em>Adding Interventions</em></span></summary>
<p>

</p>
</details>

<details><summary><span><em>Multi-node/Spatial Simulations</em></span></summary>
<p>

</p>
</details>
