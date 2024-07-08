# FE-2023-examples
Example scripts for 2023 faculty enrichment program in applied malaria modeling at Northwestern

[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/numalariamodeling/FE-2023-examples/blob/main/README.md)
[![fr](https://img.shields.io/badge/lang-fr-red.svg)](https://github.com/numalariamodeling/FE-2023-examples/blob/main/README.fr.md)

⚠️ - Tips

❓ - Self-Check Questions

➕ - Bonus Exercises

### Technical track (EMOD)

**Overview:**
Exercises usually consist of a simulation and an analyzer of simulation outputs. In some weeks, additional scripts exist to prepare simulation inputs or generate additional outputs and plots, or for model calibration as described in the instructions for the respective weeks.

**Supplied scripts & checking results:**
A few primary scripts are provided at the main level of this repository including running examples and analyzers. Most of the work for this course will be done by you building your own scripts based on the instructions with the help of these scripts. For each week, suggested simulation scripts for comparison or help during the exercise are provided in the respective week's [solution scripts](https://github.com/numalariamodeling/FE-2023-examples/tree/main/solution_scripts) folder. There is also an analyzer collection file in the solutions scripts that includes many commonly used analyzers that you may want to explore in more depth for your project. 

*Note: if you use an analyzer from the collection, be sure to add the right reporters to create the necessary output files.*

**Prerequisites:** 
Running your scripts will require that the emodpy virtual environment is loaded and assumes files are run from a working directory set to where the script is located. Create this environment using these [installation instructions](https://numalariamodeling.github.io/FE-2023-quarto-website/guides/install_guide.html). We recommend creating an "environments" folder in your home directory and creating the environment there. 

You will also need to configure your `.bashrc` file (located in your home directory). We use this file to automatically load modules, such as python, that are needed to run EMOD. We can include an alias for the virtual environment described above. The template, below, creates an alias command called `load_emodpy` that we can run in the terminal to activate the emodpy virtual environment - update the activation command to reflect the environment you created in the previous step. 

Click the arrow to expand:
<details><summary><span><em>Template `.bashrc` file</em></span></summary>
<p>

This template can be copied directly into your `.bashrc` file on QUEST: 

```bash
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
alias load_emodpy='source /home/<user>/environments/<emodpy-venv>/bin/activate'
module purge all
module load singularity/3.8.1
module load git/2.8.2
module load python/3.8.4
module load R/4.1.1
```

</p>
</details>

Before running the weekly example scripts, please ensure that the emodpy virtual environment has been successfully loaded and that this [repository has been cloned](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to the project directory on QUEST, ideally as */projects/b1139/FE_<username>/FE-2023-examples*.
- Navigate to the project: `cd /projects/b1139`
- Make your personal directory for the program: `mkdir FE_<username>` then navigate into it using `cd FE_<username>`
- Clone this repository with your ssh address for the repo. Click the green "code" button above and copy the ssh address then run the following on QUEST: `git clone <ssh address>`
	
Before you start on an exercise, make sure that you have pulled or fetched the latest changes from the repository (see git-guides [git-pull](https://github.com/git-guides/git-pull)).
	
For additional help on using SLURM on QUEST, checkout the [resources](https://numalariamodeling.github.io/FE-2023-quarto-website/resources/coding_resources/quest_resources.html) on the program website.

## Week 1: Overview of EMOD
This week we will be discussing EMOD's general structure and content as well as making sure you are ready to run the model on our linux-based HPC, QUEST. You will set up your own virtual environment to run EMOD via emodpy and idmtools and clone this github repository to your FE directory on our QUEST project allocation, b1139. Please familiarize yourself with the repo, website, and EMOD documentation before running the simple example at the end of this week.

**What to Expect**

Click the arrow to expand:
<details><summary><span><em><h3>Running EMOD from the terminal</h3></em></span></summary>
<p>

When you run an EMOD simulation script on QUEST, it will generate a set of initial messages. You will see a warning about no "idmtools.ini" - this is perfectly normal as we do not typically need the ini file to run with emodpy. Following this warning, you will see a segment that tells you some basic details about the idmtools platform you are using to run the script as well as the job directory, where all your simulation outputs will be stored.

![](static/example_run.png)

After a short waiting period, you will also see additional lines providing information on the commissioning of your simulation(s). You can expect to see a line saying that the EMODTask is being created, a few warnings and notices about file creation, then the bars showing progress on asset discovery and simulation commissioning. Once fully commissioned, you will also see the QUEST job ID, job directory, suite ID, and experiment ID. A line in the [run_example.py](https://github.com/numalariamodeling/FE-2023-examples/blob/main/run_example.py) tells the terminal to wait until all of the simulations are finished running, so there is an additional progress bar and assertion that the experiment succeeded, or failed, (once complete) that may not be present in all runs if this line is excluded. Notice that we have commissioned and successfully run 1 simulation here (see 1/1 at end of progress bars).

![](static/example_commission.png)

</p>
</details>

<details><summary><span><em><h3>File Structure</h3></em></span></summary>
<p>

If you navigate to the job directory, the file structure should look similar to that below. It can be summarized as:

- Job Directory
    - Suite ID
        - Experiment ID
            - Experiment Assets (e.g. demographics, EMOD executable, climate files, etc)
            - Simulation ID(s)
                - Output folder (e.g. reporters specified in run script)
                - General simulation outputs (e.g. campaign and config files, status/error tracking, simulation metadata)
            - General experiment outputs (e.g. status/error tracking, experiment metadata)
        - Suite metadata file
            
*Note: All of the ID folders are the 16-digit alphanumeric strings generated by idmtools, there is currently no way to modify them to use more human readable names*

![](static/example_file_structure.png)

</p>
</details>

**Example**

This week's exercise introduces the simplest version of running and analyzing a single simulation experiment in EMOD using the emodpy/idmtools infrastructure and python. Before running a simulation, one needs to check that all configurations and installations were successful and edit paths in the manifest file. The steps are generally to

1. run the simulation, and   
2. analyze simulation outputs 

**Instructions**

Click the arrow to expand:
<details><summary><span><em><h3>Running a simple EMOD simulation</h3></em></span></summary>
<p>

- Navigate to your local copy of this repository on QUEST: `cd /projects/b1139/FE_<username>/FE-2023-examples`  
- Notice your job directory path in `manifest.py`: `/projects/b1139/FE_<username>/FE-2023-examples/experiments/`. This will help your track your simulations separately from other participants.
    - *Note: any time you see items in between `< >`, they should be replaced ENTIRELY with whatever the item is labeled to be. For example, if your username was `abc123` then this job directory would be:* `/projects/b1139/FE_abc123/FE-2023-examples/experiments`
- Load your emodpy virtual environment (see prerequisites)  
- Run simulation via `python3 run_example.py`
- Wait for simulation to finish (~2 minutes)  
- Go to the job directory (see `experiments` above) folder to find the generated experiment - it will be under a set of 16-digit alphanumeric strings. The structure of these strings is `Suite > Experiment > Simulations`. Due to current handling systems with SLURM you will not be able to see the experiment name given within the `run_example.py` script; however, this can be found in the experiment and simulation-level metadata.json files. You may also choose to sort your files based on time such that most recent experiments will appear first. 
- Take a look through what was generated even in this simple run and get familiar with the file structure. You should always check your simulation-level outputs after running simulations to make sure they did what you expected. 
    - *Note: be sure to go all the way into the folder structure to see your simulations & their outputs. For more information on what to expect, see [Week 1's "What to Expect"](https://github.com/numalariamodeling/FE-2023-examples#week-1-overview-of-emod)*
    - You should see [`InsetChart.json`](https://docs.idmod.org/projects/emod-malaria/en/latest/software-report-inset-chart.html) in the simulation's output folder - this is EMOD's default report that will give you an idea of what's going on in your simulation. We'll do a basic, sample analysis of this data next.
- Copy the experiment UID, located in the experiment-level `metadata.json`. Update the experiment name to match the one used above and paste the experiment UID in the "expts" dictionary (line 71) of `analyzer_W1.py` (located at the main level of the repository with the other provided scripts). It should look like the examples below and in the script. 
    - ⚠️ *If you're not sure which is the experiment metadata, check the "item_type" and "name" in the file - do they say "experiment" and what you expect your experiment name to be, respectively? If yes, then you're in the right metadata file and can find the UID at the bottom. If you're still stuck, revist [Week 1's "What to Expect"](https://github.com/numalariamodeling/FE-2023-examples#week-1-overview-of-emod) on file structure.*
	
```python
    expts = {
        '<experiment name>' : '<experiment UID>'
    }
```
- Save and run the anlyzer using `python3 analyzer_W1.py` at the command line. We'll discuss in more depth next week how EMOD analyzers work and what you can do with them.
- When the analyzer finishes running, navigate to the working directory where you saved your results (*Hint: check line 76 to start identifying where this might be*) and checkout the output of this analyzer - there should be a file called "All_Age_Inset_Chart.csv".
- If the file was created succesfully, we can plot some basic data on the simulation. We'll use RStudio on the [QUEST Analytics Nodes](https://rstudio.questanalytics.northwestern.edu/) to run the plotter, but you can also choose to download your output file and run on RStudio locally. 
    - Once logged into QUEST's RStudio you can navigate to this repository by clicking `Session` (in the toolbar) > `Set Working Directory` > `Choose Directory` > `...` > type  `/projects/b1139/FE_<username>/FE-2023-examples` > `Choose`
- Open `plot_InsetChart.Rmd`, update the paths to match your output directory (`root`) and the experiment `subfolder` (should be the experiment name supplied to the analyzer) where the "All_Age_Inset_Chart.csv" is located.

```r
root <- "<output directory>"
subfolder <- "<experiment name>"
```
- At the top right of each code chunk there is a small green triangle - this will run the respective chunk when clicked. Run the first chunk to load libraries (lines 8-12). If you get an error that the libraries are missing, use `install.packages("<library name>")` to install them and then retry loading. Once they are loaded, run the plotter code chunk (lines 14-85). Check the saved plots in your output directory.
    - This plotter produces four groups of `InsetChart` channels generally relating to incidence, prevalence, climate/vectors, and the population/demogaphics. Explore each of the sets of plots and see what you can learn about this first simulation!
    - *Note: these plots can be helpful diagnostics to see how your simulation is performing, such as monitoring population levels; however, they should not be used to present results as they are just an example visualization not meant to address specific questions.*
	
</p>
</details>

## Week 2: Building Blocks

This week's first exercise demonstrates how to create input files, such as demographics and climate files, and how to incorporate these into the simulation. The exercise further introduces how to modify config parameters (i.e. population size or simulation duration)

This week's second exercise focuses on adding reporters and observing changes in simulation results based on the `InsetChart.json` and `MalariaSummaryReport.json` model outputs.

**Instructions**

Click the arrow to expand:
<details><summary><span><em><h3>Adding Inputs</h3></em></span></summary>
<p>

This exercise demonstrates how to create demographics and climate files and how to incorporate these into the simulation as well as introducing how to modify config parameters (e.g. run number or simulation duration). Complete all of the steps below before running this next example.


1. Extracting climate data & adding to simulations
    - Checkout `example_site.csv` in the [inputs folder](https://github.com/numalariamodeling/FE-2023-examples/tree/main/inputs). This file contains coordinates for an example site in Uganda and establishes that this will be our "Node 1" in the model. You may use these coordinates or select a different site (and adjust the coordinates accordingly) if you like for the rest of this example.
    - Next, we'll run `extract_weather.py` - this script will run the weather generator. Notice that it reads information from `example_site.csv` to look for the right site and you can request weather for your time frame of interest. You'll also see that the platform for this is called *Calculon* - this is IDM's HPC _(requires access for climate database : ask someone from NU team)_
        - We can also run `recreate_weather.py` which will convert the weather files we just generated to a csv format that we can modify. For this example we don't need to make any modifications but this can be useful for research questions such as those relating to climate change. After running any modifications in the script we then convert the csv back to weather files.  
    - Now that you know what the scripts do, load your virtual environment and use `python3 extract_weather.py` to run the extraction.   
        - Enter the credentials to access Calculon and wait for your weather files to be generated. When that is complete check your repo's inputs to make sure the files have been created.   
        - Then run `python3 recreate_weather.py` and verify that the modified weather files have been created. Make sure you check the `recreate_weather.py` script to see where they should be located.
    - Copy `run_example.py` and name it `run_example_inputs.py` and in the script change the experiment name to `f'{user}_FE_example_inputs'`
    - Update default parameters in your simulation script (`run_example_inputs.py`)'s `set_param_fn()`. You'll also need to add your folder of climate files as an asset directory to the EMODTask in `general_sim()`, this must be set after the task is defined and before the experiment is created. It is recommended you put it directory after the "set sif":

    ```python
    def set_param_fn():
	    ## existing contents
	    config.parameters.Climate_Model = "CLIMATE_BY_DATA"
	    config.parameters.Air_Temperature_Filename = os.path.join('climate',
	    'example_air_temperature_daily.bin')
	    config.parameters.Land_Temperature_Filename = os.path.join('climate',
	    'example_air_temperature_daily.bin')
	    config.parameters.Rainfall_Filename = os.path.join('climate',
	    'example_rainfall_daily.bin')
	    config.parameters.Relative_Humidity_Filename = os.path.join('climate',
	    'example_relative_humidity_daily.bin')

    ```
    ```python
    def general_sim():   
        ## existing contents
        task.set_sif(manifest.SIF_PATH, platform)
    
        # add weather directory as an asset
        task.common_assets.add_directory(os.path.join(manifest.input_dir,
            "example_weather", "out"), relative_path="climate")
    ```

2. Adding demographics
    - You may have noticed a `build_demog()` function in the first example, now we'll look at it in more detail. There are a few ways to add demographics details to our simulations, primarily with a new generator where we add details as we go or from a csv or we can read in a pre-made json file. Here we'll use the `from_template_node` command in emodpy_malaria demographics with some basic information, such as latitude and longitude. We need to import this functionality directly from emodpy_malaria - you should see this at the top of your script
    - In the `build_demog()` function, you should see the template node command, add the latitude and longitude for your example site and increase the sample size to 1000.
    - We also want to add equilibrium vital dynamics to our script. This will set the birth and mortality rates to be equal so we have a relatively stable population in our simulations. For some experiments it can be desirable to set these separately but for now this simple version will meet our needs. Add `SetEquilibriumVitalDynamics()` directly to the demographics file we are creating within the generator function (as seen below).
    - There are many aspects of demographics we are able to specify, such as the previously mentioned vital dynamics, risk distributions, and age distributions. The emod_api contains some existing age distributions. We'll need to import these PreDefined Distributions and then add it with `SetAgeDistribution` to our demographics file. Let's try adding the general distribution for Sub-Saharan Africa.
    
    ```python
    import emodpy_malaria.demographics.MalariaDemographics as Demographics
    import emod_api.demographics.PreDefinedDistributions as Distributions

    def build_demog():
        """
        This function builds a demographics input file for the DTK using emod_api.
        """

        demog = Demographics.from_template_node(lat=0.4479, lon=33.2026,
                                                pop=1000, name="Example_Site")
        demog.SetEquilibriumVitalDynamics()
    
        age_distribution = Distributions.AgeDistribution_SSAfrica
        demog.SetAgeDistribution(age_distribution)

        return demog
    ```

3. Modifying configs
    - We also often want to modify some of the [config parameters](https://docs.idmod.org/projects/emod-malaria/en/latest/parameter-configuration.html) that control things like the within-host model, vectors, and simulation setup. In `run_example.py` we set the malaria team defaults using `config = conf.set_team_defaults(config, manifest)`, but we can also specify individual parameters like we did with the climate file names. Let's start with some simple things like adding setting the `Simulation_Duration` (how long the simulation should run in days) and the `Run_Number` (the random seed for the simulation) in `set_param_fn()`. Both of these can be done directly by referencing them as `config.parameters.<param_name>` and setting them to the desired value. The team typically uses a structure of `sim_years*365` with sim_years defined globally, at the top of the script beneath all imports, to set the duration.
    - Set the duration to 1 year and the run number to any number of your choosing
        - *Note: this run number value is just the random seed value, NOT the number of stochastic realizations to run.*
    - Next, we'll add some mosquito species. There is a specific function for this, `add_species()` in emodpy_malaria malaria config. Try adding *A. gambiae*, *A. arabiensis*, and *A. funestus* to your config file:
        
    ```python    
    sim_years = 1

    def set_param_fn():
        ## existing contents
    
        conf.add_species(config, manifest, ["gambiae", "arabiensis", "funestus"])

        config.parameters.Simulation_Duration = sim_years*365
        config.parameters.Run_Number = 0
    ```

4. Now that you've added these changes, try running your new script with `python3 run_example_inputs.py`. Once it has succeeded go check on what has run. Do you see the changes to your demographics.json and the climate folder in the experiment's `Assets` directory? How about to config.json or stdout.txt? 

</p>
</details>


<details><summary><span><em><h3>Adding outputs</h3></em></span></summary>
<p>

This exercise demonstrates how to add some of the malaria built-in reporters to our sims. These reports can help us understand what is going on in our simulations from basic targets like incidence and prevalence to more detailed pictures of events or within-host data such as parasitemia. You can read more about the possible types of analyzers in the [EMOD output file documentation](https://docs.idmod.org/projects/emod-malaria/en/latest/software-outputs.html). In this exercise we'll add the Report Event Recorder and Malaria Summary Report to the simulations.

- Copy your `run_example_inputs.py` script and name it `run_example_outputs.py`. Change the experiment name to `f'{user}_FE_example_outputs'`.
- We need to import the malaria reporters from emodpy_malaria. You'll need to add this line to the rest of your emodpy_malaria importers `from emodpy_malaria.reporters.builtin import *` at the top of your script. Notice the "*" at the end, this means we are importing all of the reporters from the builtin reporter script by their names.
- [Report Event Recorder](https://docs.idmod.org/projects/emod-malaria/en/latest/software-report-event-recorder.html) allows us to look at various events happening to each individual in our sim, as well as some basic demographic and health status information about the individual. This report is especially useful for monitoring different interventions, such as receiving treatment, but for now we'll only look at simple events such as births or existing individuals' birthdays. We can control the time period we want to report on, from `start_day` to `end_day` as well as things like target age group and nodes while we add the reporter. For now, let's add the report for the entire simulation and targeting ages 0-100 years, so likely the whole population. It can be added to our `general_sim()` with `add_event_recorder()` after the task has been defined, around line 110:
    
    ```python
    def general_sim()
        ## existing contents
    
        add_event_recorder(task, event_list=["HappyBirthday", "Births"],
                           start_day=1, end_day=sim_years*365, 
                           node_ids=[1], min_age_years=0,
                           max_age_years=100)
    ```

- [Malaria Summary Report](https://docs.idmod.org/projects/emod-malaria/en/latest/software-report-malaria-summary.html) provides a population-level summary of malaria data grouped into different bins such as age, parasitemia, and infectiousness. This report will give us information such as PfPR, clinical incidence, and population stratified by time (as well as age bins, parasitemia, and infectiousness if desired). We can specify what time period of aggregation we are interested in, typically weekly, monthly, or annually through the reporting interval. The linked documentation will show you many other things we can specify as well, but for now we'll keep it simple and set our report to run monthly for the duration of the simulation with simple age groups: 0-0.25, 0.25-5, and 5-115 years. We'll also tell the report that we want a maximum of 20 intervals so we can make sure we get all our monthly reports for 1 year and use `pretty_format` to make the outputted report more readable to us. You should also add a filename suffix, in this case we'll use "monthly" to give some additional description to the report. This should be added directly after the Report Event Recorder, also in `general_sim()` with `add_malaria_summary_report()`:
    
    ```python
    def general_sim()
        ## existing contents
    
        ## previously added event recorder
    
        add_malaria_summary_report(task, manifest, start_day=1, 
                                   end_day=sim_years*365, 
                                   reporting_interval=30,
                                   age_bins=[0.25, 5, 115],
                                   max_number_reports=20,
                                   filename_suffix='monthly',
                                   pretty_format=True)
    ```

- Try running your new script as you learned in the past two examples and wait for it to finish before navigating to your experiment directory. When it's done running, check out the simulation outputs and your new report. You should both verify that the files were created and look at what they contain. What do you notice?
    - ⚠️ *It's especially important to check all of your outputs when you are making big changes to your script. If you don't examine them, you may miss problems that aren't actually causing your simulations to fail (but are doing something you don't want them to).*

</p>
</details>


<details><summary><span><em><h3>Analysis</h3></em></span></summary>
<p>

Now that you've learned the basics of how to run EMOD and add inputs/outputs you can start actually analyzing some data! We use analyzer scripts to extract the data we want from our simulations' reports to understand what the simulation is doing, how it is changing, and answer research questions. This week's analyzer script, `analyzer_W2.py` contains two different analyzers:

1. `InsetChartAnalyzer` that extracts data from `Inset_Chart.json`. Notice the `channels_inset_chart` in line 164 - this tells defines which data channels we are interested in looking at. Six different channels are included currently but these can always be modified depending on what you want to explore. This is a modified version of the simple inset chart analyzer that pulls all channels in Week 1.
2. `MonthlyPfPRAnalyzer` that extracts data from the monthly summary report. If you look at the guts of the analyzer (lines 63 - 140), you'll see that this will particularly focus on extracting PfPR, Clinical Incidence (per person per year), Severe Incidence (per person per year), and Population, all by time (month, year) and age bins.

- There are start_years included in both analyzers to match simulation time to real time. You can provide any relevant values that will be helpful to your processing (such as 2000 - 2009 for a 10 year simulation).
- You'll also notice `sweep_variables` being defined and going into both analyzers - we'll discuss this in more depth in Week 3, but for now you can think of this like a tag (or set of tags) for our simulation(s). These sweep variable tags are useful for grouping the simulations for aggregation and understanding differences between them. 
    - Because we are only using the "Run_Number" (random seed for stochastic realization) in this week's example, you may see a warning message : `FutureWarning: In a future version of pandas, a length 1 tuple will be returned when iterating over a groupby with a grouper equal to a list of length 1. Don't supply a list with a single grouper to avoid this warning.` This warning is just to say you should preferably provide more than one variable for grouping.

- Before we can run the analyzer script, you need to make a few changes:
    1. Set your `jdir` (short for job directory) to where your experiments are saved, this can be done by referencing `manifest.job_directory`. Notice that this is used for the platform, and we also set `wdir` (working directory) for the analyzer where the analyzers will output any results you have requested
    2. Define your experiment name and ID in the `expts` dictionary (line 149) - these should match the UID and name in the experiment level `metadata.json` for your experiment of interest, in this case the `f'{user}_FE_example_outputs'` experiment you just ran.
    
    ```python
    expts = {
            '<user>_FE_example_outputs' : '<experiment UID>'
        }
    ```
- This week's analyzer script also includes a basic python plotter for the results from `InsetChartAnalyzer` that will help you visualize each of the `channels_inset_chart` throughout the simulation. Take a look through the code to see if you can tell what it is doing before running it.
- Run the analyzer
- Wait for the analyzer to succeed. Once it is finished check out your new processed outputs (see if you can find the `wdir` mentioned above without help). You should see two csvs, one from each analyzer, as well as a InsetChart.png. Make sure these files have been created and examine the data they contain.
    - *Note: this InsetChart.png is a similar plot to that of Week 1 but is written in python and included at the end of the analyzer script directly. This is meant to showcase the ability to create similar plots using R or python, to your comfort.*
- ➕ As an additional exercise, try to make a data visualization in R or python based off of the MonthlyPfPRAnalyzer output (PfPR_Clinical_Incidence_monthly.csv), based on the `MalariaSummaryReport`. You'll need to take a look through the output file and decide what kind of figure may be interesting and inform you about your simulation. *Note: there is a [solution script](https://github.com/numalariamodeling/FE-2023-examples/blob/main/solution_scripts/Week2/plot_SummaryReport.Rmd) for this that is similar to the Week 1 InsetChart plotter, but it is highly recommended to try making your own version first as an exercise of creativity and data visualization skills where everyone may have unique ideas. Check out the [plotting resources](https://numalariamodeling.github.io/FE-2023-quarto-website/resources/coding_resources.html), then discuss with your colleagues or the instructional staff if you get stuck. If you use the solution script, remember that it is only meant as a sample plot and not a key way to show results as that will be dependent on specific research questions and model configurations.*
- ➕ Once you've completed your data visualization exercise, feel free to try changing some other [config parameters](https://docs.idmod.org/projects/emod-malaria/en/latest/parameter-configuration.html) in your example script. Run additional simulations with different durations, population sizes, agebins, etc. - whatever you think would be interesting! This is a great time to look through the EMOD documentation and explore parameters so you get to know the EMOD ecosystem better. 
    - ⚠️ *Change your experiment name to keep track of your simulations in both the metadata and analyzer outputs*
    - You should also run these sims through the analyzer script by updating the experiment name and ID, as above. Inspect the outputs as well as any changes compared to your first run. What do you see? 
        - ❓ How have the outcomes changed? 
        - ❓ What do you recognize about running time?

</p>
</details>

## Week 3: Experiment Setups & Fine-Tuning
This week's exercises will focus on how to design and setup more detailed experiments. We will cover sweeping over config parameters, calibration, and serialization. 

This week's first exercise introduces the concept of "sweeping" over ranges of values for different parameters.  There are a variety of reasons we may want to test out a range of parameter values, some examples include:
    - running multiple stochastic realizations (this example)
    - testing fit for calibration, such as with amount of larval mosquito habitat (calibration example, later this week)
    - testing different intervention configurations, such as coverage levels or repetitions (we'll look at this more next week) 
    
The next exercise will walk you through a basic model calibration workflow in EMOD. We don't always know some of the parameters in our model, yet these parameters play important role in shaping our model output. We "fit" or "calibrate" the parameters to some real data that are available to us. Essentially, we propose a range of values for these parameters, and run the model to see if the output matches the actual observed data. We do this using the "sweeping" described in the last exercise. The set of proposed values is compared to reference data and those that allow the model to best match the actual data would be chosen for subsequent modeling steps.


This week's final exercise demonstrates the concept of serializing populations in simulations. Serialization allows us to run simulations, save them at a certain point in time, and simulate another campaign/scenario starting from the point we saved. We can run multiple simulations on the same population in series. We often use this process to save long initial simulations called burnins, during which population immunity is established. We don't want to wait for this to run everytime, so we serialize the population at the end of the burnin and then run shorter simulations, typically with additional interventions (also called "pickup" simulations).

**Instructions**

Click the arrow to expand:
<details><summary><span><em><h3>Parameter Sweeping</h3></em></span></summary>
<p>

This exercise demonstrates how to "sweep" over parameters to have a set of different values across simulations in our experiment.

For now we'll start with a simple sweep over one config parameter, such as the run number. As previously discussed, the run number controls the random seed value for the simulation. By setting the simulations to a range of run number/random seed values, we can produce more stochastic replicates. Each replicate will produce slightly different results for the same overall simulation due to this draw from the random probability distribution; therefore, it is important to run multiple replicates for scientifically valid results.

There are additional more complicated sweeping methods, particularly with creating campaigns, that we will discuss later in the program.


- Copy your `run_example_outputs.py` script and name it `run_example_sweeps.py`. Change the experiment name to `f'{user}_FE_example_sweep'`.
- To sweep over variables we'll have to switch to using a simulation builder from `idmtools` rather than creating simulations directly from the task. Add `from idmtools.builders import SimulationBuilder` to your import statements. We'll modify this simulation creation in `general_sim()` shortly.
- Beneath where you set the `sim_years`, set `num_seeds = 5`. We'll use this later to tell EMOD how many different run numbers, or stochastic realizations, we want for this experiment.
- Next, define a simple function that will allow you to set individual config parameters under the `set_param_fn()` where you define the constant config parameters. 

  ```python
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
    - Finally, you'll need to remove the `Experiment.from_task()` experiment creation and replace with `Experiment.from_builder(builder, task, name=<expt_name>)`. This will create experiments based on the task but with the additional information contained in the builder, including the added sweep. Make sure you keep the modified experiment name!
  
      ```python
      def general_sim()
          ## existing contents

          # Create simulation sweep with builder
          builder = SimulationBuilder()
    
          builder.add_sweep_definition(partial(set_param, param='Run_Number'), range(num_seeds))
    
         ## reports are still located here
    
         # create experiment from builder
         experiment = Experiment.from_builder(builder, task, name="example_sim_sweep")
      ```

- Run the script, wait for it to finish, and checkout your simulation outputs.
    - ❓ Do your outputs look like you expect? 
    - *Hint: there should be five simulations as we created five stochastic realizations*
- Update the experiment name and ID in `analyzer_W2.py`. You'll notice that the `sweep_variable` parameter is already set to `Run_Number` so the analyzer will pull out this tag for each simulation. This list can take more parameters/tags as necessary when you start adding more complex sweeps. Run the analyzer & check the csv/png processed outputs.
    - Checkout the `InsetChart` plot generated by the analyzer 
        - ❓ How does it look different now that we've swept over the run number?
- Try adding the output of the sweep to your MonthlyPfPRAnalyzer visualization script from last time. How might you account for adding this to your plot?

</p>
</details>

<details><summary><span><em><h3>Calibration</h3></em></span></summary>
<p>

Depending on our project and site there are a variety of different parameters you may be interested in calibrating on due to different uncertainties, including those having to do with vectors and interventions. In this example, we want to calibrate a parameter called `x_Temporary_Larval_Habitat` that controls the amount of larval mosquito habitat, and the amount of mosquitoes, accordingly. This is a common parameter in calibration efforts. We'll use our example site with some data that mimics a household survey (DHS) conducted in the site. In this hypothetical survey, a number of children under 5 years old were tested for malaria, and we know how many of them are positive. We'll use these reference points to select the best fit.


1. Running calibration sweeps
    - Copy `run_example_sweeps.py` to a new script named `run_example_calibration.py`
    - Update `sim_years` to run for at least 20 years with `sim_start_year=2000`. This start year is just meant to help us place our simulations in time, as with the analyzer, rather than actually change any of the time steps in the simulation.
    - Beneath the sweep we added last time, add another one for `x_Temporary_Larval_Habitat` (default = 1). This parameter multiplies the default larval habitat value, so we'll want to start over a relatively small range of values. One nice way of doing this is to use a numpy command, `logspace`, that will divide the range evenly in logspace - we'll try -0.5 to 1 in logspace (0.316 to 10 in terms of actual parameter value) for 10 separate values. Logspace is particularly useful for this parameter as the actual larval habitat values can be quite large so we tend to want to explore the lower values in our range more closely. Be sure to also `import numpy as np` with the rest of your import statements.
    
      ```python
      builder.add_sweep_definition(partial(set_param, param='x_Temporary_Larval_Habitat'), np.logspace(-0.5,1,10))
      ```
    - In this example we'll use yearly summary reports rather than one large one through a for loop over the years. We'll also add `filename_suffix=f'Monthly_U5_{sim_year}'` to the end of the summary reporter. This command adds a descriptor to the report output file - it is particularly useful when you want to output multiple different reports from the same type of reporter (such as a weekly, monthly, and annual report).
    
      ```python
        for year in range(sim_years):
        	start_day = 0 + 365 * year
        	sim_year = sim_start_year + year
        	add_malaria_summary_report(task, manifest, start_day=start_day,
                               		   end_day=365+year*365, reporting_interval=30,
                               		   age_bins=[0.25, 5, 115],
                               		   max_number_reports=13,
                               		   pretty_format=True, 
                               		   filename_suffix=f'Monthly_U5_{sim_year}')
      ```
    - In the `general_sim()`, find the command `experiment.run(wait_until_done=True, platform=platform)` (line 148 in the solution script). This is the command that submits and runs our simulations. Notice that it has an argument to "wait until done" - this is what gives us the progress bar for the completion of our simulations after submission. Now that we are running longer simulations, set that to `False` to free up your terminal.
        - ⚠️ *You should also remove the print messages following this line about whether or not the experiment has succeeded as we are no longer waiting for it to finish before continuing through the script. This will cause you to get the "experiment failed" warning message as the simulations will still be running (and thus not succeeded) when the submission script (`run_example_calibration.py`) runs this line. Instead, use `squeue -A b1139` to check the status of your running jobs on QUEST and then use stderr.txt and stdout.txt to determine if your simulations succeeded or failed when they finish running.*
    - Update the `expt_name` and run your simulations.
            - These simulations may take longer due to the longer simulation duration. You can check the progress of your jobs and what else is running on the same allocation using `squeue -A b1139` or just the progress of your jobs with `squeue -u <username>`.
            - Once the simulations finish running, check your outputs. Is everything there? Do all your reports look like you expect?
    - Update the `expt_name`, `exp_id`, and years to analyze in the `analyzer_calibration.py` then run the script when your simulations finish - check out the differences between this and previous analyzers (and their outputs).

    
2. Parameter selection
    - The `example_calibration_selection.py` script is a simple example of how we may select the best match parameter value for calibration. It calculates the average log-likelihood of each `x_Temporary_Larval_Habitat` based on simulation outputs and produces some plots to visualize the parameter selection.
    - Update the `expt_name` to match that of your calibration sweeps that you just ran.
    - Before you run the selection script, take a look through it and see if you can understand how it works and what it will produce. Keep this in mind and then run and compare to the results after it's finished.
	- Note: you may need to install `idmtools-calibra` & `seaborn` if you are using your own virtual environment - the shared environment on QUEST should already have these. The `idmtools-calibra` package can be installed using the following and should also install the `seaborn` dependency:
	
	  ```python
	  pip install idmtools-calibra --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple
	  ```
    - ❓ How does the parameter fit look? If you didn't get a good fit, what might you do to fix it? Feel free to make changes and try running part 1 again!
</p>
</details>

<details><summary><span><h3><em>Serialization</em></h3></span></summary>
<p>

This serialization exercise has three parts. In part 1 you will run and save a burnin simulation. In part 2 you will "pickup" this simulation to run for a shorter time. In part 3 you will repeat parts 1 & 2 using a longer burnin duration, and compare the results.

1. Burning in
    - Description: Typically, we create 50-year burnin simulations to initialize transmission and immunity in our population of interest prior to trying to answer our research questions. For this example, we will start by only running the burnin for 10 years with 500 people to make sure everything is running correctly. For now we will also want to run 3 replicates. Be sure to use your calibrated `x_Temporary_Larval_Habitat` from the previous example.
     - Create a new python script named `run_example_burnin.py`
     - Based on what you've learned from previous examples, add the basic code chunks needed to run a simulation. Check the details below for suggestions and additional comments. Feel free to refer to any old scripts you've been using to help write this one but be sure not just to copy and paste the whole thing!
        - Import modules
        - Config setup & simulation duration
        - Campaign setup
        - Demographics
        - EMODTask & experiment builder
        - Reporters: Reporting during the burnin simulation is optional, it depends on the simulation duration and what you want to track or to check. If not disabled, `InsetChart` is automatically included, and can be plotted, alternatively one can disable the `InsetChart` and include an annual summary report to keep track of malaria metrics in an age group that is also plotted during the main simulation. *HINT: you may want to check the max number of reports generated in the summary reporter*
        - Code execution/run script
     - Now that you've got the basics of your script, we'll add the parameters needed for serialization so that you can "pick up" from them again later. Add the code chunk below to update the serialization "writing" configuration parameters. (see [Simple Burnin](https://faculty-enrich-2022.netlify.app/modules/emod-how-to/emod-how-to/#simple-burn-in) in EMOD How-To's). The section ideally would be placed at the end of your `set_param_fn()`.
        - `Serialization_Population_Writing_Type` sets the format we want to serialize in, typically "timestep" that will save the population at a particular time step (days)
        - `Serialization_Time_Steps` sets that point in time that we want to serialize. We define `serialize_years` to reference this length of time at the top of our script. For consistency, you can use this same value to set your simulation duration.
        - `Serialization_Mask_Node_Write` determines whether or not larval habitats are serialized, `0` means we are saving everything.
        - `Serialization_Precision` dictates what level of precision is used in the saved files - `REDUCED` will reduce the file size and is used for most of our burnins to save space

          ```python
          # as a global variable at the top of the script, like sim_years that we use to define simulation duration:
          serialize_years = 10

          def set_param_fn():
              ## existing contents
    
              #Add serialization - add burnin "write" parameters to config.json
              config.parameters.Serialized_Population_Writing_Type = "TIMESTEP"
              config.parameters.Serialization_Time_Steps = [365 * serialize_years]
              config.parameters.Serialization_Mask_Node_Write = 0
              config.parameters.Serialization_Precision = "REDUCED"
          ```
    - Run the script and checkout your outputs when it finishes running.
        - Notice that we have `InsetChart.json` as it is the default for all sims (if you did not include other reporters) and a new `state-03650.dtk` file. This state file is the "burnin" file that saves all of the information needed about this simulation (such as population, immunity, etc) at the point in time we requested, in this case day 3650 (the last day of a 10 year sim). 
            -️ ⚠️ *The name of the state file should change with different burnin lengths*
    - While waiting for your simulations to finish, we can adapt the `analyzer_w2.py` to better meet the needs of serialization. Copy this script and name it `analyzer_serialization.py`
        - Start by adding a section to the executable `if __name__ == "__main__":` section of the analyzer that defines the serialization duration and which step (burnin or pickup) you'd like to analyze, in this case the burnin.
        
          ```python
          #import statements, setting directories
	
          serialize_years = 10  # Same as in run_example_burnin.py
          step = 'burnin'
          ```
        - We may also want to adjust our sweep variables and `InsetChart` channels. Let's try changing the channels to the four below and adding an if statement to set sweep variables for the pickup. Right now this is the same as the burnin and only sweeps over Run_Number, but this can be used for additional parameters, such as intervention coverage, as you add complexity to the pickup. 
        
          ```python
          ## Set sweep_variables and event_list as required depending on experiment
          channels_inset_chart = ['Statistical Population', 'New Clinical Cases', 
                                  'Adult Vectors', 'Infected']
          sweep_variables = ['Run_Number']
          if step == 'pickup':
              sweep_variables = ['Run_Number'] # for times when you add additional items to the pickup, you can add more sweep variables here
          ```
        - It is also recommended to remove some of the `MalariaSummaryReport` channels from the `map` function in the `MonthlyPfPRAnalyzer` as they will be less commonly used in projects and we don't need to extract data that is not needed for the questions at hand. Most of the time, we only need the PfPR, Annual Clinical Incidence, Annual Severe Incidence, and Average Population (all by Age Bin) channels. Recall from last week's exercise that all of these are [`MalariaSummaryReport` output channels](https://docs.idmod.org/projects/emod-malaria/en/latest/software-report-malaria-summary.html#databytimeandagebins) and that this analyzer is only processing data from this report (as seen in the "super init" filename list at the start of the analyzer - the filenames here are the only one the analyzer will open). 
	      - To use the "step" system we will want to also modify our analyzers run statement. Assuming you included only the default report, `InsetChart`, in your burnin then you will want to run only that analyzer for the burnin step. For the pickup you will likely also want to include a version of the summary report we've been using so we'll include that in the pickup step in the analyzer. Be sure to update the `start_year` for the analyzer such that our burnin will end in 2023 (and should start the number of `serialize_years` prior) and the pickup will start where the burnin leaves off in 2023. The simulations themselves have no linkage to real time; rather, they track simulation timesteps. Applying the the year in the analyzer in this way is simply meant to turn those simulation timesteps into a more understandable framework for our work. We then run the analyzer based on the step we set above. We can keep the basic plotter after this just to get an idea of what is going on in our simulations. 
            - **Note: In certain cases, such as monitoring PfPR across all simulation time, you will also want to include a summary report (or another report) in the burnin. Be thoughtful about the questions you are trying to address and what reports you'll need at each step, there is no one right way!**
        
          ```python
          with Platform('SLURM_LOCAL',job_directory=jdir) as platform:

              for expt_name, exp_id in expts.items():
                  analyzers_burnin = [InsetChartAnalyzer(expt_name=expt_name,
                                           channels=channels_inset_chart,
                                           start_year=2023 - serialize_years,
                                           sweep_variables=sweep_variables,
                                           working_dir=wdir),
                                      ]

                  analyzers_pickup = [InsetChartAnalyzer(expt_name=expt_name,
                                           channels=channels_inset_chart,
                                           start_year=2023,
                                           sweep_variables=sweep_variables,
                                           working_dir=wdir),
                                      MonthlyPfPRAnalyzer(expt_name=expt_name,
                                            start_year=2023,
                                            sweep_variables=sweep_variables,
                                            working_dir=wdir)
                                      ]
  
              if step == 'burnin':
              	  am = AnalyzeManager(configuration={}, ids=[(exp_id, ItemType.EXPERIMENT)],
                                     analyzers=analyzers_burnin, partial_analyze_ok=True)
                  am.analyze()

              elif step == 'pickup':
                  am = AnalyzeManager(configuration={}, ids=[(exp_id, ItemType.EXPERIMENT)],
                                     analyzers=analyzers_pickup, partial_analyze_ok=True)
                  am.analyze()
            
              else:
                  print('Please define step, options are burnin or pickup') 
          ```
    - Run the analyzer script & check outputs.
    
2. Picking up
    - Create a new script, `run_example_pickup.py` that will be used to run a simulation picking up from the 10-year burnin simulations you ran in Part 1. You may choose to copy over the contents of your burnin or start fresh, being thoughtful about which parts are necessary or you expect may change for the pickup.
        - Be sure to update or add any reporters that may be of interest to see what is happening in during the pickup. It is recommended to at least include the summary reporter we have been using in previous examples.
        - As mentioned above, pickups are often the most useful when thinking about different intervention scenarios. We will discuss adding these interventions in greater depth in later exercises and focus primarily on the process of creating the pickup in this exercise. 
        - *Note that the start/end days for items such as reports and interventions are relative to the beginning of the pick-up simulation - in other words, they re-start at zero.*
    - Import `build_burnin_df` from the `utils_slurm` helper file - this function helps us access the saved burnin information and build our pickup off of it
    - Add custom or new parameters that define the pickup simulation and burnin duration as well as ID of the burnin experiment. Add these at the top of your new script after your import statements:
        - `pickup_years` to define your `Simulation_Duration` (i.e. # of years run post-burnin). This will replace the duration that you had previously in the script so make sure you update the `Simulation_Duration` accordingly!
        - `serialize_years` to define the year of the burnin that serves as the start of the pickup and should be equal to the value of `serialize_years` in the burnin.
        - `burnin_exp_id = '<exp_id>'` with the experiment_id from the burnin experiment you want to pick up from

          ```python
          from utils_slurm import build_burnin_df

          serialize_years= 10
          pickup_years=5
          burnin_exp_id = '<exp_id>'
          ```
    - Update your serialization config params, mostly by switching them from "write" to "read" mode as we are now picking up where we left off in the burnin. The `Serialization_Time_Steps` should remain the same as we want to pick up at that serialized spot at the end of our burnin. Be sure to completely modify or remove any of the "writing"/burnin parameters in this script. 
        - Note that you may also need to carry through config parameters, such as `x_Temporary_Larval_Habitat`, from the burnin as the `config = conf.set_team_defaults(config, manifest)` that happens at the beginning of `set_param_fn` will reset these to the team defaults.

      ```python
      def set_param_fn():
          ## existing contents 
    
          #Add serialization - add pickup "read" parameters to config.json
          config.parameters.Serialized_Population_Reading_Type = "READ"
          config.parameters.Serialization_Mask_Node_Read = 0
          config.parameters.Serialization_Time_Steps = [serialize_years*365]
          
          #Add calibrated larval habitat
          config.parameters.x_Temporary_Larval_Habitat = <calib_value>
      ```
    - Next, add the simulation specific serialization parameter updates. This function helps us match burnin and pickup simulations by filenames and paths, as well as any parameters that we want to carry over. In this example, the only such parameter is `Run_Number` but this could be many other configuration or campaign type parameters. Parameters that may be important for sweeps need to be included in the returned output of the function, such as `Run_Number` is here, so we can reference them in later analysis.
       
      ```python
      def update_serialize_parameters(simulation, df, x: int):

         path = df["serialized_file_path"][x]
         seed = int(df["Run_Number"][x])
    
         simulation.task.set_parameter("Serialized_Population_Filenames", df["Serialized_Population_Filenames"][x])
         simulation.task.set_parameter("Serialized_Population_Path", os.path.join(path, "output"))
         simulation.task.set_parameter("Run_Number", seed) #match pickup simulation run number to burnin simulation

         return {"Run_Number":seed}
      ```
    - Finally, we need to add a few commands to find the serialized state files and add them to our simulation builder. Use the `build_burnin_df` to create the data frame that will contain all of the information needed about our burnin using the burnin experiment ID, the platform where we are running everything, and the serialized time point. Then we can sweep over the `update_serialize_parameters` function we created in the last step, referencing the burnin dataframe as where we are getting the information for our sims from and sweeping over the index values of the dataframe so we read the whole thing line-by-line.
    
      ```python
      def general_sim():
          ## existing contents, builder defined
          
          #Create burnin df, retrieved from burnin ID (defined above)
          burnin_df = build_burnin_df(burnin_exp_id, platform, serialize_years*365)

          builder.add_sweep_definition(partial(update_serialize_parameters, df=burnin_df), range(len(burnin_df.index)))
      ```
    - *Note: Be sure that you aren't creating additional stochastic replicates in the pickup. Because we are matching the "Run_Number" in `update_serialize_parameters` there is no need to do this additional run number sweep.*
    - Run the experiment. Once it finishes running, checkout your outputs. Do you see what you expect? 
        - *Hint: think about what reporters you added, or didn't.*
        - Notice that there is no state file in the pickup. When we choose to read rather than the write with the serialization config parameters, it will only read the burnin's state file rather than writing a new one for the pickup. It is possible to do both steps during serialization if needed.
        - Remember that you should check all of your outputs, including things like `config.json` and `campaign.json` to make sure they are doing what you expect. In this example, it is especially pertinent to make sure that any parameters, such as `x_Temporary_Larval_Habitat`, that should be the same in both the burnin and the pickup actually are. You can compare them side by side or copy and paste into some like [diffchecker](https://www.diffchecker.com/) to ensure everything looks how it is supposed to.
    - While waiting for it to finish, make any modifications to the analyzer that you need such as the `expt_name`, `exp_id`, `step`, and pickup `start_year`. Once the experiment finishes you can run `analyzer_serialization.py` & check its outputs.
    
3. Compare pickup simulations across varying burnin durations
    - Run a longer burnin of 50 years using `run_example_burnin.py`
    - When it finishes running (it may take a while), update the `burnin_exp_id` in `run_example_pickup.py`. Check your outputs to make sure everything ran correctly.
    - Before running the experiment, update the `exp_name` (i.e. add 'burnin50'), to keep track of your simulation iterations. Do not change anything else in the pickup simulation, to allow for comparison across iterations picking up from different burnin durations.
    - Run the pickup experiment, wait for it to finish, and checkout your outputs.
    - Using `analyzer_serialization.py`, run the `InsetChartAnalyzer` for both burnin and pickup. Make sure to modify your `serialization_years` and the `step` you are analyzing. Feel free to change the `channels_inset_chart` to other ones depending on what differences you may be most interested in exploring. Check the outputs.
    - Try plotting your results to show both burnin and pickup on the same plot for your channels of interest over time. You may use R or python to do so - if you get stuck there is a sample python plotting script in `Solution_scripts/Week3` called `plot_example_serialization.py` but we strongly recommend trying to make your own version of a plot first.
        - *Note: these plots and analyzer scripts are just baselines for you to go off! You may want to make changes or include additional things, such as additional sweep variable, confidence intervals, or additional reports with new analyzers (and outputs), as you develop your project, especially as you add complexity to the pickup.*
    - ❓ Compare the plots between the experiments with 10 and 50 year burnins. Do you notice any differences?
    
</p>
</details>

## Week 4: Addressing Research Questions

This week will focus adding complexity to our simulations to better address our research questions through interventions, individual properties, and multi-node/spatial simulations. Each of these tools brings something beneficial to the table for many of the questions that you may be interested in answering using EMOD. There are many pre-defined interventions that can be added in EMOD -  we'll specifically focus on adding case management in these example exercises. Detailed descriptions of how-to add other interventions such as drug campaigns (SMC, PMC, MSAT, etc) and ITNs can be found in the [EMOD How-Tos](https://faculty-enrich-2022.netlify.app/modules/emod-how-to/emod-how-to/). 
Individual properties present a way that we can categorize and add heterogeneity to our population, such as through intervention access, study enrollment, and drug response groups. We can target specific interventions and reports to individuals who meet the criteria of these 'tags', making these particularly useful to controlling aspects of the simulations that need not reach the entire population. Additionally, individual properties are fully customizable, so you can adapt them to fit the needs of your project. 

Likewise, the final exercise of this week will focus on spatial simulations which allow for multiple, separate nodes in our experimental setup. In many cases we don't need multiple nodes as we are focused on a particular area, but sometimes we are interested in multiple, notably different areas for the same questions and want to maintain their spatial relationships, particularly migration of both human and mosquito hosts. In these cases, we can add a spatial setup to the model that will work in largely the same way the individual nodes do, just in multiple locations.

**Instructions**

Click the arrow to expand:
<details><summary><span><em><h3>Adding Interventions</h3></em></span></summary>
<p>

As we start thinking about adding interventions to our simulations, we should also think about how to construct the timeline. This is particularly useful for project work as you match to specific sites with data on incidence and prevalence, when (and what) interventions were implemented, etc. For now, let's think about it more simply, building off of what we learned last week. We'll first want to initialize the population through a 50 year burnin with no interventions. Increase your population size back to 1000 for 5 replicates and re-run the burnin while you work on this exercise's scripts (the pickup).

- Copy the `run_example_pickup.py` script you made last week, rename it `run_example_pickup_CM.py`. *Note: we are adding interventions to a pickup in this example, but you do not have to serialize to use interventions, individual properties, or multi-node simulations*
- You'll need to import the treatment seeking/case management functionalities to your script from emodpy-malaria in order to use this intervention function:
  ```python
  import emodpy_malaria.interventions.treatment_seeking as cm
  ```

- Once you have the case management functions imported, you can add them to your `build_camp()` function. We'll use `add_treatment_seeking()`, specifically - this function passes all of the important parameters for case management to our broader campaign file. There is a small set of parameters that we commonly use, below, but to see all of the available controls you can explore the [source code](https://github.com/numalariamodeling/emodpy-malaria/blob/main/emodpy_malaria/interventions/treatment_seeking.py).
    - `start_day`: indicates when the intervention should begin relative to the beginning of the simulation. This is particularly useful when you want interventions to start at different times in the simulations.
    - `drug`: indicates which drugs are to be used for case management. Artemether and Lumefantrine are the default, but all available drugs are defined in emodpy-malaria's [`malaria_drug_params`](https://github.com/numalariamodeling/emodpy-malaria/blob/main/emodpy_malaria/malaria_drug_params.csv)
    - `targets`: controls the target populations and triggers for case management. You'll notice that we typically use the events `NewClinicalCase` and `NewSevereCase` to trigger case management. We can further add coverage levels and minimum/maximum age targets. In this example, we assume we a certain case management level for children under 5 years old (U5) and reduce coverage for everyone over 5 years of age to 75% of the U5 coverage. We also assume that coverage for severe cases (all ages) is 115% of U5 coverage, up to a maximum of 100% coverage. This means that we'll want to add multiple target dictionaries to our target parameter to capture both groups. Finally, the target dictionary also includes seek (the delay rate, in 1/days, to seeking care) and rate (the delay rate, in days, from time to seeking care to receiving care, typically 0.3 for uncomplicated cases meaning that there is a three day delay on average).  
    
	    | Under_5 (cm_cov_u5)| Over_5    | Severe   |
	    |:-------:|:------:|:-----:|
	    | 80%       |60%  | 92% |
	    | ... | ... | ... |
    
		❓ Based on this example, **what would the corresponding Over_5 and Severe case management coverage levels be for Under_5 coverage of 100%?**   
		
		❓ **What about 0%?**
		
    - `broadcast_event_name`: indicates the name of the event to be broadcast at each event for reporting purposes. This is particularly helpful if you have multiple or changing versions of the same intervention, such as with using different case management drugs, in a single simulation.
- Add case management to your `build_camp()` function using the script below. Notice that we include `cm.` before `add_treatment_seeking()` - this is because we imported this function as `cm` so it is helpful to reference to make sure we are using the function we think we are. You'll also notice that we are adding `cm_cov_U5=0.80` and `cm_start=1` to the arguments that `build_camp()` takes - we do this so we can pass it values from a sweep over coverage and the start date for case management later in the script. The values included are defaults that you can adjust as needed but are available so you don't have to provide a sweep value if unnecessary.

  ```python
  def build_camp(cm_cov_U5=0.80, cm_start = 1):

      camp.schema_path = manifest.schema_file

      # Add case management
      # This example assumes adults will seek treatment 75% as often as U5s and severe cases will seek treatment 15% more than U5s (up to 100% coverage)
      cm.add_treatment_seeking(camp, start_day=cm_start, drug=['Artemether', 'Lumefantrine'],
                        targets=[{'trigger': 'NewClinicalCase', 'coverage': cm_cov_U5, 
                                  'agemin': 0, 'agemax': 5,
                                  'seek': 1,'rate': 0.3},
                                 {'trigger': 'NewClinicalCase', 'coverage': cm_cov_U5*0.75, 
                                  'agemin': 5, 'agemax': 115,
                                  'seek': 1,'rate': 0.3},
                                 {'trigger': 'NewSevereCase', 'coverage': min(cm_cov_U5*1.15,1), 
                                  'agemin': 0, 'agemax': 115,
                                  'seek': 1,'rate': 0.5}],
                        broadcast_event_name="Received_Treatment")            
                       
      return camp
  ```


	
- To help sweep over multiple campaign parameters at once, we will also add a function to update these values together after `build_camp()`. In this update function, we include a partial of `build_camp()` that takes values for both of the variables we defined in the last step. It then creates the campaign for a particular simulation from a callback of the partial. Finally, this function returns a dictionary of the parameters and values that we are updating here to add a tag for each to the simulation metadata.
  ```python
  def update_campaign_multiple_parameters(simulation, cm_cov_U5, cm_start):

      build_campaign_partial = partial(build_camp, cm_cov_U5=cm_cov_U5, cm_start=cm_start)
      simulation.task.create_campaign_from_callback(build_campaign_partial)
    
      return dict(cm_cov_U5=cm_cov_U5, cm_start=cm_start)
  ```

- As discussed in last week's exercise on adding parameter sweeps, we'll need to add a sweep to the builder in `general_sim()` for the campaign in addition to the config params. However, this time we will need to use `add_multiple_parameter_sweep_definition()` instead of `add_sweep_definition()` since we are updating both the coverage and start day. If you were to use `add_sweep_definition` directly with a partial of `build_camp()` for each parameter individually, the second time you call the partial would override the first so only one parameter would be updated. On the other hand, `add_multiple_parameter_sweep_definition()` allows us to sweep over the entire parameter space in a cross-product fashion. It takes our update function and we provide a dictionary of our parameters and their list of values we want to sweep over. We'll sweep over three coverage values (0, 50%, and 95%), and three intervention start dates (1, 100, and 365). For now these are relatively arbitrary values that are just meant to illustrate the functionality in EMOD. In this example we will get 3x3x5 = 45 total simulations (coverage levels x start days x run numbers) that model each unique parameter combination.

    ℹ️ 
    
    | Under_5 (cm_cov_u5)| Over_5    | Severe   |
    |:-------:|:------:|:-----:|
    | 0%       |0%  | 0% |
    | 50% | 37.5% | 57.5% |
    | 95% | 71.25% | 100% |
	
	
  ```python
  def general_sim()
      ## existing contents
    
      ## case management sweep 
      builder.add_multiple_parameter_sweep_definition(
          update_campaign_multiple_parameters,
          dict(
              cm_cov_U5=[0.0, 0.5, 0.95],
              cm_start=[1, 100, 365]
          )
      )
  ```
- Update the `ReportEventRecorder` event list to include `Received_Treatment` from our case management campaign (either in addition to the event list we've used previously or as the only event).
- Update the experiment name to `example_sim_pickup_CM`.
- Run the script. While you wait, update `analyzer_serialization.py` with your new experiment name, ID, and sweep variables.
- When the simulations finish, check your outputs. They should largely look the same as before, but you should now see the `Received_Treatment` even in the `ReportEventRecorder`. Examine the `campaign.json` as well to see details about the campaign you've added to the simulations - each will look slightly different depending on which sweep parameters it received.
    - Does your campaign file look how you expect? This is a good way to verify if your simulations are distributing interventions correctly or if something isn't set up correctly (such as if it is giving out 100x the case management expected).
- If your outputs look good, run the analyzer & check its outputs.
- Try plotting your results. You can build off of the scripts you made for the previous serialization example, but how might you consider the changes we've made this week?      
    - *Hint: Think about changes related to adding interventions and the additional parameter sweeps.*
- Check out some of the other [interventions](https://github.com/numalariamodeling/emodpy-malaria/tree/main/emodpy_malaria/interventions) in emodpy-malaria. [Drug campaigns](https://github.com/numalariamodeling/emodpy-malaria/blob/main/emodpy_malaria/interventions/drug_campaign.py), [ITNs](https://github.com/numalariamodeling/emodpy-malaria/blob/main/emodpy_malaria/interventions/bednet.py), and [IRS](https://github.com/numalariamodeling/emodpy-malaria/blob/main/emodpy_malaria/interventions/irs.py) may be of particular interest. 
    - ➕ For an added challenge, try adding one (or more!) of these interventions to this simulation on your own or with the help of the How-Tos. An example script with multiple interventions is located in the solution scripts **IN PROGRESS**

</p>
</details>

<details><summary><span><em><h3>Individual Properties</h3></em></span></summary>
<p>

Individual properties (IPs) can be added to any simulation to add additional information useful to specific projects. Depending on the research question individual properties might only be needed for interventions and not for the reports, or vice versa, if not both.

In this example, we'll continue building off of the serialization structure, adding a case management access IP to our previous workflow.  We'll use individual properties to create 2 subgroups for this access: low access, high access. For simplicity, it is assumed that their relative size is equal (50% low access, 50% high access).

1. Burnin - Adding IPs to demographics and reports
    - Copy the `run_example_burnin.py` script to a blank python script and name it `run_example_burnin_IP.py`
    - In the demographics builder, we can define and add a custom individual property that will be applied to the simulation's population. In this example, we want to include high and low levels of access to care. 
        - Start by defining the `initial_distribution` for the property in a list where each value is the proportion of the population that will be distributed to each property level, 50% low access and 50% high access.
        - Next use the `AddIndividualPropetyAndHINT()` from the imported `Demographics` package to add our access property to the demographics file we are building. In this function, set the `Property="Access"`, `Values=["Low","High"]`, and `InitialDistribution=initial_distribution`. The property is our high level label whereas the values represent the levels (such as high and low) of the property. The initial distribution uses the distribution we used in the last step to apply the values to the population, respectively.
        
      ```python
      def build_demog():
          demog = Demographics.from_template_node(lat=1, lon=2, pop=1000, name="Example_Site")
          demog.SetEquilibriumVitalDynamics()
          
          
          # Add age distribution
          age_distribution = Distributions.AgeDistribution_SSAfrica
          demog.SetAgeDistribution(age_distribution)
      
          # Add custom IP to demographics                              
          initial_distribution = [0.5, 0.5]
          demog.AddIndividualPropertyAndHINT(Property="Access", Values=["Low", "High"],
                                              InitialDistribution=initial_distribution)                                  
                                            
          return demog
      ```
    - We can also add individual properties to our reporters. The methods for doing this between the event recorder and summary report are slightly different. For the burnin, we'll only add the event recorder but we'll see the changes to summary report in the pickup.
        - In event recorder we can simply add `ips_to_record=['<property>']` which tells the report that we also want it to tell us what access level the individual experiencing the event belongs to. You are able to add multiple IPs to this list if needed.
    - Update the experiment name and run your simulations
    - When the burnin finishes running, check your outputs including the event recorder and existence of the state file.
        - ❓ How does the event recorder change with IPs?
        - *Note: we typically don't run analyzers on burnins once we know that they are working correctly unless there are specific questions of interest for this portion of the experiment, so we will skip that step in this example.*
    
2. Pickup - Adding IPs to interventions
    - Copy the `run_example_pickup_CM.py` script to a blank python script and name it `run_example_pickup_CM_withIP.py`.
    - Update the `burnin_exp_id` to the experiment you ran in part 1.
    - In `build_camp()` we will add IPs to the case management intervention setup. A key part of this will be adjusting the coverage level to reflect the differences that the low and high access groups experience, based on a population-level coverage. Try writing your own helper to do this and when you're ready check your work below.
      <details><summary><span><em>Check your coverage adjustment</em></span></summary>
      <p>
        - Add the following to `build_camp()` after defining the schema path:
          
          ```python
          def build_camp():
              ## existing contents
        
              # Calculating the coverage for low and high access groups
              # We assume high access group = 0.5 of total population (see demographics setup)
              frac_high = 0.5
            
              # Use an if/else to define high vs low coverage based on the proportion
              # of the population who have high access to care
              if cm_cov_U5 > frac_high:
                  cm_cov_U5_high = 1
                  cm_cov_U5_low = (cm_cov_U5 - frac_high) / (1 - frac_high)
              else:
                  cm_cov_U5_low = 0
                  cm_cov_U5_high = cm_cov_U5 / frac_high
          ```
          - The if/else statement here uses the proportion of the population with high access to care to help define coverage levels. Based on our assumptions we expect that the high access group should reach 100% coverage before the low access group has any coverage. Under this, the low access group will get leftover coverage to get the population-level coverage to the expected level (e.g. 75% all U5 coverage = 100% high access & 50% low access coverage). Likewise, if population coverage is less than the proportion of individuals with high access, the low access group will have 0% coverage and high access will be calculated to the level to reach the expected population coverage (e.g. 25% all U5 coverage = 50% high access & 0% low access)
          - One could include more complex relationships between individual property levels if supported by data
      </p>
      </details>
      
    - Once the high and low coverage levels are defined we can modify the case management intervention to reflect the variation between the groups. 
        - Adjust each of the coverage levels to use `cm_cov_U5_low` from your coverage adjustment
        - After the targets, add `ind_property_restrictions=[{'Access': 'Low'}]` - this will restrict the intervention to only those in the low access group. Multiple IPs can be used here if desired.
          <details><summary><span><em>Check your case management intervention</em></span></summary>
          <p>
          - Add the following to `build_camp()` after defining the coverage levels:
          
            ```python
            cm.add_treatment_seeking(camp, start_day=cm_start, drug=['Artemether', 'Lumefantrine'],
                       targets=[{'trigger': 'NewClinicalCase', 'coverage': cm_cov_U5_low, 
                                 'agemin': 0, 'agemax': 5,
                                 'seek': 1,'rate': 0.3},
                                 {'trigger': 'NewClinicalCase', 'coverage': cm_cov_U5_low*0.75, 
                                  'agemin': 5, 'agemax': 115,
                                  'seek': 1,'rate': 0.3},
                                 {'trigger': 'NewSevereCase', 'coverage': min(cm_cov_U5_low*1.15,1), 
                                  'agemin': 0, 'agemax': 115,
                                  'seek': 1,'rate': 0.5}],          
                       ind_property_restrictions=[{'Access': 'Low'}],
                       broadcast_event_name="Received_Treatment")
            ```
          </p>
          </details>
        - Duplicate the low access intervention and modify to apply case management to the high access group as well
    - Add the same IP details from the burnin to the pickup demographics
    - Add the IP specifications for the event recorder reports discussed in part 1
    - Next we'll modify the summary report and use the for loop system for years from the calibration exercise (to use a different analyzer). We ask it to include only individuals of a particular level through `must_have_ip_key_value='<property>:<value>'`. This means that the report requested below will only include individuals with high access to care. In these cases, it is also beneficial to add `filename_suffix` such as '_highaccess' to tag the output for analysis. Be sure to include a report for both access levels in your script, an example is included for "high access" below.
    
        ```python
        for i in range(pickup_years):
            add_malaria_summary_report(task, manifest, start_day=1+365*i,
                                   end_day=365 + i * 365, reporting_interval=30,
                                   age_bins=[0.25, 5, 115],
                                   max_number_reports=serialize_years,
                                   must_have_ip_key_value='Access:High',
                                   filename_suffix=f'Monthly_highaccess_{sim_start_year+i}',
                                   pretty_format=True)
        ```
    - Update the experiment name, run the script.
    - Update the experiment name and ID in `analyzer_IP.py`. Be sure to check if you need to update anything such as `sweep_variables` or analyzer years. 
    - Once the pickup finishes, check your outputs to make sure everything was created. Do you have both high and low access summary reports? If everything looks good, run the analyzer & check its outputs.
    - Try plotting your results. Feel free to start with old scripts and adapt them to try to understand differences between the IP levels.
        - ⚠️*Think about what type of indicators access to case management may impact and how you might want to show comparisons between the high and low access groups. Make sure to include any grouping on parameter sweeps as they can impact the results!*
        - ❓ If you had included the summary report in the burnin, would you expect these results to look different? If so, how and why?
            - ⚠️*Think especially about the different IP levels and what has changed between the burnin and pickup scenarios.*
    
</p>
</details>

<details><summary><span><em><h3>Multi-node/Spatial Simulations</h3></em></span></summary>
<p>

Most of the time, we consider our geographical units of interest (the 'nodes' - whether they represent districts, regions, countries, or abstract populations) to be independent from one another. Usually, it's better to simulate different locales separately, but you may want to run 'spatial' simulations involving multiple nodes and the connections between them (ex. migration). 

We will cover advanced applications of spatial modeling in another exercise. This exercise will allow you to practice combining parts from previous examples to run a simple spatial simulation and produce spatial outputs. Afterward, you can add code to introduce migration between nodes, and see how that changes things, but we will not deal with this in any detail here.

**Part 1. Setup Inputs**

1. Create a spreadsheet **nodes.csv** with the columns *node_id*, *lat*, *lon*, and *pop*. EMODpy will be expecting these column names! <br>
        - This spreadsheet will be used to generate the climate and demographics files later  
        - save the file inside a new folder inside `/inputs/demographics`
2. Fill in the spreadsheet with the information for 4 nodes

    Example:

    | node_id | lat    | lon   | pop  |
    |:-------:|:------:|:-----:|:----:|
    | 1       | 12.11 | -1.47 | 1000 |
    | 2 | 12.0342 | -1.44 | 1000 | 
    | 3 | 12.13 | -1.59 | 1000 | 
    | 17 | 12.06 | -1.48 | 1000 |
        
   - ⚠️ **node_id** must be positive numbers, but do not have to be sequential.  
   - ℹ️ lat/lon values should represent real places with climates suitable for malaria transmission (for step 3).  
   - ⚠️ the column names for are expected to be "node_id", "lat", "lon", and "pop" by default 
3. Using a separate script, `get_climate.py`, request and save climate files based on **nodes.csv**  <br>
   *For simplicity: use a single-year series from 2019, using the function definition and call to `get_climate()` below* <br>
        - Just update the `"tag"` and `"demo_fname"` arguments appropriately
        
```python  
from emodpy_malaria.weather import *
import os

def get_climate(tag = "default", start_year="2015", start_day="001", end_year="2016", end_day="365", demo_fname="demographics.csv", fix_temp=None):
    # Specifications #
    ##################
    # Date Range
    start = "".join((start_year,start_day))  
    end = "".join((end_year,end_day))     
    
    # Demographics
    demo = "".join(("inputs/demographics/",demo_fname))
    
    # Output folder to store climate files
    dir1 = "/".join(("inputs/climate",tag,"-".join((start,end))))
    
    if os.path.exists(dir1):
        print("Path already exists. Please check for existing climate files.")
        return
    else:
        print("Generating climate files from {} for day {} of {} to day {} of {}".format(demo,start_day,start_year,end_day,end_year))
        os.makedirs(dir1)
        csv_file=os.path.join(dir1,"weather.csv")
        # Request weather files
        wa = WeatherArgs(site_file= demo,
                         start_date=int(start),
                         end_date=int(end),
                         node_column="node_id",
                         id_reference=tag)
        
        wr: WeatherRequest = WeatherRequest(platform="Calculon")
        wr.generate(weather_args=wa, request_name=tag)
        wr.download(local_dir=dir1)
        
        print(f"Original files are downloaded in: {dir1}") 
        
        df, wa = weather_to_csv(weather_dir = dir1, csv_file=csv_file)
        df.to_csv(csv_file)

if __name__ == "__main__":
    get_climate(tag="FE_EXAMPLE", start_year="2019", end_year="2019", demo_fname="nodes.csv")
```

We will reference the generated climate files later inside `set_param_fn()` and via `Task.common_assets.add_directory` inside `general_sim()`.
	
	
**Part 2. Run Spatial Simulations**
	
Now, referring to the scripts you wrote for previous examples, you should be able to start with a blank `run_spatial.py` and outline - or in some cases complete - the code sections needed to run simulations, with the following **additional specifications**:  

1. Import modules
    - `import pandas as pd`  
3. **Set Configuration Parameters**  
    - You can keep the simulation duration short (1-2 years) while testing / debugging.  
    - Remember to add vectors
        -  `conf.add_species(config, manifest, ["gambiae", "arabiensis", "funestus"])`
    - Point to your new climate files
      ```python
      climate_root = os.path.join("climate",'FE_EXAMPLE','2019001-2019365')
      
      config.parameters.Air_Temperature_Filename = os.path.join(climate_root, 'dtk_15arcmin_air_temperature_daily.bin')
      config.parameters.Land_Temperature_Filename = os.path.join(climate_root, 'dtk_15arcmin_air_temperature_daily.bin')
      config.parameters.Rainfall_Filename = os.path.join(climate_root, 'dtk_15arcmin_rainfall_daily.bin')
      config.parameters.Relative_Humidity_Filename = os.path.join(climate_root, 'dtk_15arcmin_relative_humidity_daily.bin')
      ```  
4. **Sweep configuration parameters**  
5. **Build campaign**  
6. Sweep campaign parameters (optional for this exercise)  
7. Serialize burnin & pickup  
8. **Build demographics**   
    a. inside `build_demog()` use this code to generate demographics from your "nodes.csv" file (you may need to edit the path to input_dir inside manifest.py)
    ```python
    demog = Demographics.from_csv(input_file = os.path.join(manifest.input_dir,"demographics","nodes.csv"), 
                                                            id_ref="EXAMPLE", 
                                                            init_prev = 0.01, 
                                                            include_biting_heterogeneity = True)
    # NOTE: The id_ref used to generate climate and demographics must match!
    ```
9. **Run Experiment [`general_sim()`]**  
    a. Set platform  
    b. Create EMODTask  
    c. Set singularity image  (using `set_sif()`)  
    d. Add weather directory asset:  
   	`task.common_assets.add_directory(os.path.join(manifest.input_dir, "climate"), relative_path="climate")`   
    e. Use `SimulationBuilder()`  
    f. **Reports**  
    g. Create, run, and check result of experiment  

**Additional Specifications for Spatial Model Example**

*Burnin*  

- Duration: 30 years  
- Vary `x_Temporary_Larval_Habitat` using  `set_param()` 
    - `np.logspace(0,1,10)` will use 10 evenly log-spaced values between 10<sup>0</sup> and 10<sup>1</sup> (1-10x)
- No interventions  
- 1 stochastic realization / random seed
- *Hint: check `set_param_fn()` to make sure you added vectors, point to the corresponding demographics/climate files, and allow for serialization.*

*Pickup* 

- Duration: 10 years  
- Carry `x_Temporary_Larval_Habitat` over from burnin using `update_serialization_parameters()`  
- Interventions deployed differently in each node by providing a list of nodes to the `node_ids` argument <br> (ex. `treatment_seeking(... node_ids=[1,2])`):  
    - One node receives case management, and ITNs every 3 years  
    - One node receives case management only  
    - One node receives ITNs every 3 years only  
    - One node receives no interventions
    - *Note: For simplicity, you can choose fixed "optimal" coverages (~80%) for these interventions, instead of sweeping over these campaign parameters.* 
    - ℹ️ To add ITNs (in Nodes 1 and 3, in mid-June for example):
	
	```python
	import emodpy_malaria.interventions.bednet as itn
	
	def build_camp(...):
	     ### ITN Distributions in nodes 1 and 3, for example ###
      	     itn.add_itn_scheduled(camp, start_day = 165, 
				   demographic_coverage = 0.9, 
				   repetitions = 4, 
				   timesteps_between_repetitions = 365*3, 
				   node_ids = [1,3],
				   receiving_itn_broadcast_event= "Received_ITN",
				   killing_initial_effect = 0.25,
				   killing_decay_time_constant = 1460,
				   blocking_initial_effect = 0.75,
				   blocking_decay_time_constant = 730)
	    ...
	```
- 10 stochastic realizations / random seeds each (sweep over `Run_Number`)  
- add Filtered Spatial Reports and Event Counters to outputs, inside `general_sim()`   
    - `add_spatial_report_malaria_filtered(...)`  
        - Only report on the last 3 years of the simulation   
        - For a daily report, use `reporting_interval = 1`  
        - Filter to ages 0.25-100  
        - include spatial_output_channels 'Population', 'PCR_Parasite_Prevalence', and 'New_Clinical_Cases' (though any InsetChart Channels will work)
	  
	  ```python
	  add_spatial_report_malaria_filtered(task, manifest, 
					      start_day = start_report, end_day = end_report,
					      reporting_interval = 1, 
					      node_ids =None,
					      min_age_years = 0.25, max_age_years = 100, 
					      spatial_output_channels = ["Population",
									 "PCR_Parasite_Prevalence",
									 "New_Clinical_Cases"],
					      filename_suffix = "all_ages")
	  ```
    - Use the code below to `add_report_event_counter(...)` **by node** 
        - the `event_trigger_list` should include 'Received_Treatment' and 'Received_ITN'  
        - *Note: These events need to be added to `config.parameters.Custom_Individual_Events=[...]` inside `set_param_fn()` as well.*
        
          ```python
          demo_df = pd.read_csv(os.path.join(manifest.input_dir, "demographics", "nodes.csv"))
          for node in demo_df['node_id']:
              add_report_event_counter(task, manifest,
                                   start_day = start_report,
                                   end_day = end_report,
                                   node_ids = [node],
                                   min_age_years = 0,
                                   max_age_years = 100,
                                   event_trigger_list = ["Received_ITN", "Received_Treatment"],
                                   filename_suffix = "_".join(("node",str(node))))
        
          ```
        
**Part 3. Analyze Spatial Simulations** 

To analyze the `SpatialReportMalariaFiltered_.bin` files generated for each channel and simulation, use the script `analyzer_spatial.py`

Edit **only** the section at the bottom of the script before running:

```python
...
...
...

if __name__ == "__main__":
    ...
    ...
    ...
    ## Experiments Dictionary ##
    ############################
    # {'experiment label' : 'exp_id'}
    expts = {'<EXPERIMENT_LABEL>' : '<EXPERIMENT_ID>'}
   
    ## Paths ##
    ###########
    # experiments folder
    jdir =  manifest.job_directory
    # output folder
    wdir=os.path.join(jdir,'<OUTPUTS_FOLDER>', '<SUBFOLDER>')
    if not os.path.exists(wdir):
        os.mkdir(wdir) 

    ...
    
```

This will produce a file inside `working_dir/my_outputs/experiment_name/SpatialReportMalariaFiltered.csv` with columns:  
* Time
* Node
* Run_Number
* x_Temporary_Larval_Habitat
* Population
* PCR_Parasite_Prevalence
* New_Clinical_Cases

To analyze the event counts from each `ReportEventCounter_node_#.json`, run the script `analyzer_events.py`

Edit **only** the following lines at the bottom of the script before running:

```python
...
...
...

if __name__ == "__main__":
    ...
    ...
    ...
    
    ## Experiments Dictionary ##
    ############################
    # {'experiment label' : 'exp_id'}
    expts = {'<EXPERIMENT_LABEL>' : '<EXPERIMENT_ID>'}
   
    ## Paths ##
    ###########
    # experiments folder
    jdir =  manifest.job_directory
    # output folder
    wdir=os.path.join(jdir,'<OUTPUTS_FOLDER>', '<SUBFOLDER>')
    if not os.path.exists(wdir):
        os.mkdir(wdir) 
    ...
	
    with Platform('SLURM_LOCAL',job_directory=jdir) as platform:
        for expname, exp_id in expts.items():  
            
            analyzer = [EventCounterAnalyzer(exp_name = expname, 
                                             exp_id = exp_id, 
                                             sweep_variables = sweep_variables, 
	############### UPDATE THIS LINE TO MATCH YOUR NODE IDS ###############
                                             nodes = ["1","2","3","17"],
	#######################################################################
                                             events = events,
                                             working_dir = wdir)]
    ...
   

```

This will produce a file inside `/OUTPUTS_FOLDER/SUBFOLDER/CountedEvents.csv' with columns: 

* Time  
* Node  
* Run_Number  
* x_Temporary_Larval_Habitat 
* Received Treatment  
* Received ITN  


**Part 4. Plot Spatial Results**

1. Open 'spatial_plotter.rmd' in RStudio
2. Update the `root` in the first chunk with the path to folder containing the `SpatialReportMalariaFiltered.csv` and `CountedEvents.csv` generated above. This is also where the output plot will be saved. 
3. Run the `spatial_plotter.rmd` file

View the `SpatialSummary.png` that was created.

</p>
</details>
