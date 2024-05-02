import pathlib
import os
from functools import \
    partial 
 
#idmtools   
from idmtools.assets import Asset, AssetCollection  
from idmtools.builders import SimulationBuilder
from idmtools.core.platform_factory import Platform
from idmtools.entities.experiment import Experiment


#emodpy
from emodpy.emod_task import EMODTask
from emodpy.utils import EradicationBambooBuilds
from emodpy.bamboo import get_model_files
import emod_api.config.default_from_schema_no_validation as dfs
import emod_api.campaign as camp

#emodpy-malaria
from emodpy_malaria.reporters.builtin import *
import emodpy_malaria.demographics.MalariaDemographics as Demographics
import emod_api.demographics.PreDefinedDistributions as Distributions


import manifest

sim_years=1

def set_param_fn(config):
    """
    This function is a callback that is passed to emod-api.config to set config parameters, including the malaria defaults.
    """
    import emodpy_malaria.malaria_config as conf
    config = conf.set_team_defaults(config, manifest)
    conf.add_species(config, manifest, ["gambiae", "arabiensis", "funestus"])

    config.parameters.Simulation_Duration = sim_years*365
    config.parameters.Run_Number = 5
    
    
    #Add climate files
    config.parameters.Air_Temperature_Filename = os.path.join('climate','example_air_temperature_daily.bin')
    config.parameters.Land_Temperature_Filename = os.path.join('climate','example_air_temperature_daily.bin')
    config.parameters.Rainfall_Filename = os.path.join('climate','example_rainfall_daily.bin')
    config.parameters.Relative_Humidity_Filename = os.path.join('climate', 'example_relative_humidity_daily.bin')


    return config


def build_camp():
    """
    This function builds a campaign input file for the DTK using emod_api.
    """

    camp.set_schema(manifest.schema_file)

    
    return camp


def build_demog():
    """
    This function builds a demographics input file for the DTK using emod_api.
    """

    demog = Demographics.from_template_node(lat=0.4479, lon=33.2026, pop=1000, name="Example_Site")
    demog.SetEquilibriumVitalDynamics()
    
    age_distribution = Distributions.AgeDistribution_SSAfrica
    demog.SetAgeDistribution(age_distribution)
    
    return demog


def general_sim(selected_platform):
    """
    This function is designed to be a parameterized version of the sequence of things we do 
    every time we run an emod experiment. 
    """

    # Set platform and associated values, such as the maximum number of jobs to run at one time
    platform = Platform(selected_platform, job_directory=manifest.job_directory, partition='b1139testnode', time='2:00:00',
                            account='b1139', modules=['singularity'], max_running_jobs=10)

    # create EMODTask 
    print("Creating EMODTask (from files)...")

    
    task = EMODTask.from_default2(
        config_path="config.json",
        eradication_path=manifest.eradication_path,
        campaign_builder=build_camp,
        schema_path=manifest.schema_file,
        param_custom_cb=set_param_fn,
        ep4_custom_cb=None,
        demog_builder=build_demog,
        plugin_report=None
    )
    
    
    # set the singularity image to be used when running this experiment
    task.set_sif(manifest.SIF_PATH, platform)
    
    # add weather directory as an asset
    task.common_assets.add_directory(os.path.join(manifest.input_dir, "example_weather", "out"),
                                         relative_path="climate")

    #Add reports
    add_event_recorder(task, event_list=["HappyBirthday", "Births"],
                       start_day=1, end_day=sim_years*365, node_ids=[1], min_age_years=0,
                       max_age_years=100)
                       
    # MalariaSummaryReport
    add_malaria_summary_report(task, manifest, start_day=1, end_day=sim_years*365, reporting_interval=30,
                               age_bins=[0.25, 5, 115],
                               max_number_reports=20,
                               filename_suffix="monthly",
                               pretty_format=True)

    # create experiment from task
    experiment = Experiment.from_task(task, name="example_sim_outputs")


    # The last step is to call run() on the ExperimentManager to run the simulations.
    experiment.run(wait_until_done=True, platform=platform)


    # Check result
    if not experiment.succeeded:
        print(f"Experiment {experiment.uid} failed.\n")
        exit()

    print(f"Experiment {experiment.uid} succeeded.")
    


if __name__ == "__main__":
    import emod_malaria.bootstrap as dtk
    import pathlib

    dtk.setup(pathlib.Path(manifest.eradication_path).parent)

    selected_platform = "SLURM_LOCAL"
    general_sim(selected_platform)
    
