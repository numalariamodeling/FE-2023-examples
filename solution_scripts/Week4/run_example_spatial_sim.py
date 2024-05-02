###################
# Import Packages #
###################

# generic packages
import pathlib
import os
import numpy as np
import pandas as pd
from functools import \
    partial 
import sys
 
# from idmtools   
from idmtools.assets import Asset, AssetCollection  
from idmtools.builders import SimulationBuilder
from idmtools.core.platform_factory import Platform
from idmtools.entities.experiment import Experiment

# from emodpy
from emodpy.emod_task import EMODTask
from emodpy.utils import EradicationBambooBuilds
from emodpy.bamboo import get_model_files

# from emod_api
import emod_api.config.default_from_schema_no_validation as dfs
import emod_api.campaign as camp
import emod_api.demographics.PreDefinedDistributions as Distributions
import emod_api.migration.migration as migration

# from emodpy-malaria
from emodpy_malaria.reporters.builtin import *
import emodpy_malaria.demographics.MalariaDemographics as Demographics
import emodpy_malaria.interventions.treatment_seeking as cm
import emodpy_malaria.interventions.bednet as itn
import emodpy_malaria.interventions.drug_campaign as dc
import emodpy_malaria.malaria_config as malaria_config

# from manifest
import manifest

# from utils_slurm
sys.path.append('../')
from utils_slurm import build_burnin_df

#######################
# Sim. Specifications #
#######################
user = os.getlogin()                                 # username for paths & naming files
tag = 'spatial_sim'                     # label for experiment
phase = 'pickup'                                     # burnin or pickup?
burnin_id = 'e71c708c-8a95-43e0-8753-cec161585669'   # experiment id containing serialized population (required for pickup)

burnin_years = 30        
pickup_years = 10      
if(phase=="burnin"):
    num_seeds = 1         # number stochastic realizations
    # Vary Habitat Scale Factors
    num_xTLH_samples = 10
    min_xTLH = 0
    max_xTLH = 1
     
if(phase=="pickup"): 
    num_seeds = 10        # number stochastic realizations
    # Vary Case Management

#########################
# Set Config Parameters #
#########################

def set_param_fn(config):
    """
    This function is a callback that is passed to emod-api.config to set config parameters, including the malaria defaults.
    """
    import emodpy_malaria.malaria_config as conf
    # Setup config using team defaults
    config = conf.set_team_defaults(config, manifest)
    # Vectors
    conf.add_species(config, manifest, ["gambiae"])
    # Climate
    climate_root = os.path.join('climate','FE_EXAMPLE', '2019001-2019365')
    config.parameters.Air_Temperature_Filename = os.path.join(climate_root,'dtk_15arcmin_air_temperature_daily.bin')
    config.parameters.Land_Temperature_Filename = os.path.join(climate_root, 'dtk_15arcmin_air_temperature_daily.bin')
    config.parameters.Rainfall_Filename = os.path.join(climate_root, 'dtk_15arcmin_rainfall_daily.bin')
    config.parameters.Relative_Humidity_Filename = os.path.join(climate_root, 'dtk_15arcmin_relative_humidity_daily.bin')
    # Serialization
    if(phase=="burnin"):
      config.parameters.Serialized_Population_Writing_Type = "TIMESTEP"
      config.parameters.Serialization_Time_Steps = [365 * burnin_years]
      config.parameters.Serialization_Mask_Node_Write = 0
      config.parameters.Serialization_Precision = "REDUCED"
      config.parameters.Simulation_Duration = burnin_years*365
    if(phase=="pickup"):
      config.parameters.Serialized_Population_Reading_Type = "READ"
      config.parameters.Serialization_Time_Steps = [365 * burnin_years]
      config.parameters.Serialization_Mask_Node_Read = 0
      config.parameters.Simulation_Duration = pickup_years*365
    # Output
      config.parameters.Custom_Individual_Events = ["Received_ITN", "Received_Treatment"]
    # Migration
      config.parameters.Enable_Migration_Heterogeneity = 0

    return config
    
###########################
# Sweep Config Parameters #
###########################

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

##################
# Build Campaign #
##################

def build_camp(cm_cov_u5=0.8):
    """
    This function builds a campaign input file for the DTK using emod_api.
    """
    camp.set_schema(manifest.schema_file)
    
    ### Calibration 
    ###############################
    
    # Note: no interventions during burnin
    
    if(phase =="pickup"):                        
      ### Case Management ###
      # Treatment-Seeking Rates by age #
      cm_coverage_by_age = [{'trigger': 'NewClinicalCase',      ## For uncomplicated symptomatic cases < 5
                                        'coverage': cm_cov_u5,
                                        'agemin': 0,
                                        'agemax': 5,
                                        'seek': 1,
                                        'rate': 0.3},
                            {'trigger': 'NewClinicalCase',      ## For uncomplicated symptomatic cases 5-15
                                        'coverage': cm_cov_u5*0.6,
                                        'agemin': 5,
                                        'agemax': 15,
                                        'seek': 1,
                                        'rate': 0.3},
                            {'trigger': 'NewClinicalCase',      ## For uncomplicated symptomatic cases 15+
                                        'coverage': cm_cov_u5*0.4,
                                        'agemin': 15,
                                        'agemax': 115,
                                        'seek': 1,
                                        'rate': 0.3},
                            {'trigger': 'NewSevereCase',        ## For severe clinical cases, all-ages
                                        'coverage': 0.8,
                                        'agemin': 0,
                                        'agemax': 115,
                                        'seek': 1,
                                        'rate': 0.5}]
      # Treatment in some nodes #                                 
      cm.add_treatment_seeking(camp, 
                               start_day = 1, 
                               drug=['Artemether','Lumefantrine'],
                               targets=cm_coverage_by_age,
                               node_ids = [1,2],
                               broadcast_event_name="Received_Treatment")
      ### ITN Distributions in some nodes ###
      itn.add_itn_scheduled(camp, 
                            start_day = 165, 
                            demographic_coverage = 0.9, 
                            repetitions = 4, 
                            timesteps_between_repetitions = 365*3, 
                            node_ids = [1,3],
                            receiving_itn_broadcast_event= "Received_ITN")
    return camp
    
#################
# Serialization #
#################
def update_serialize_parameters(simulation, df, x: int):
    # Serialized file path:
    path = df["serialized_file_path"][x]    
    # Other parameters from burnin that need to be carried over:
    xTLH = df["x_Temporary_Larval_Habitat"][x]
    
    simulation.task.set_parameter("Serialized_Population_Filenames", df["Serialized_Population_Filenames"][x])  # Set serialized population filename
    simulation.task.set_parameter("Serialized_Population_Path", os.path.join(path, "output"))                   # Set serialized population path
    simulation.task.set_parameter("x_Temporary_Larval_Habitat", xTLH)                                           # Grab xTLH from burnin simulation

    return {"xTLH":xTLH}      # Return serialized parameters as tags

######################
# Build Demographics #
######################

def build_demog():
    """
    This function builds a demographics input file for the DTK using emod_api.
    """
    # From input file csv #
    demog = Demographics.from_csv(input_file = os.path.join(manifest.input_dir,"demographics","FE_example_nodes.csv"), id_ref="FE_EXAMPLE", init_prev = 0.01, include_biting_heterogeneity = True)
    demog.SetEquilibriumVitalDynamics()
    age_distribution = Distributions.AgeDistribution_SSAfrica
    demog.SetAgeDistribution(age_distribution)
    
    # Incomment to include Migration (OPTIONAL)
    # Using this gravity parameters set from Monique's MMC work 
    #migration_partial = partial(migration.from_demog_and_param_gravity, gravity_params=[7.50395776e-06, 9.65648371e-01, 9.65648371e-01, -1.10305489e+00], id_ref='FE_example', migration_type=migration.Migration.REGIONAL)
    # Uncomment end of return statement below too when turning on migration! 
    return demog#, migration_partial    

#####################
# Build Simulations #
#####################

def general_sim(selected_platform):
    """
    This function is designed to be a parameterized version of the sequence of things we do 
    every time we run an emod experiment. 
    """
    # Platform #
    ############
    # Set platform and associated values, such as the maximum number of jobs to run at one time
    # Use b1139 for longer simulations (do not exveed 100 max_running_jobs)
    platform = Platform(selected_platform, job_directory=manifest.job_directory, partition='b1139testnode', time='6:00:00',
                        account='b1139', modules=['singularity'], max_running_jobs=100)
    # Task #
    ########
    # create EMODTask #
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
    # set the singularity image to be used when running this experiment #
    task.set_sif(manifest.SIF_PATH, platform)
    # add weather directory as an asset #
    task.common_assets.add_directory(os.path.join(manifest.input_dir, "climate"), relative_path="climate")
    # Builder #
    ########### 
    # add builder #
    builder = SimulationBuilder()
    if(phase=="burnin"):
      ### Parameters to sweep over in burnin ###
      # Run number
      builder.add_sweep_definition(partial(set_param, param='Run_Number'), range(num_seeds))
      # x_Temporary_Larval_Habitat
      builder.add_sweep_definition(partial(set_param, param='x_Temporary_Larval_Habitat'), np.logspace(min_xTLH, max_xTLH, num_xTLH_samples))
    if(phase=="pickup"):
      ### Connect to burnin ###
      ## Read in serialized data
      burnin_df = build_burnin_df(burnin_id, platform, burnin_years*365) 
      ## Pick up parameters
      # x_Temporary_Larval_Habitat
      builder.add_sweep_definition(partial(update_serialize_parameters, df=burnin_df), range(len(burnin_df.index)))
      ### New parameters to sweep over in pickup ###
      # Run number
      builder.add_sweep_definition(partial(set_param, param='Run_Number'), range(num_seeds))
    # Reporting #
    #############
    if(phase =="pickup"):
      # Report over last 3 years
      start_report = (pickup_years-3)*365
      end_report = pickup_years*365
      demo_df = pd.read_csv(os.path.join(manifest.input_dir, "demographics", "FE_example_nodes.csv"))
      # Event Counter Reports
      for node in demo_df['node_id']:
          add_report_event_counter(task, manifest,
                                   start_day = start_report,
                                   end_day = end_report,
                                   node_ids = [node],
                                   min_age_years = 0,
                                   max_age_years = 100,
                                   event_trigger_list = ["Received_ITN", "Received_Treatment"],
                                   filename_suffix = "_".join(("node",str(node))))
           
      # filtered spatial malaria report
      add_spatial_report_malaria_filtered(task, manifest, 
                                          start_day = start_report, end_day = end_report, 
                                          reporting_interval = 1, 
                                          node_ids =None, 
                                          min_age_years = 0.25, max_age_years = 100, 
                                          spatial_output_channels = ["Population",
                                                                     "PCR_Parasite_Prevalence",
                                                                     "New_Clinical_Cases"] ,
                                        filename_suffix = "all_ages")
    # create experiment from builder #
    ##################################
    experiment = Experiment.from_builder(builder, task, name=f'{user}_{tag}_{phase}')
    # Run Experiment #
    ##################
    # The last step is to call run() on the ExperimentManager to run the simulations. #
    experiment.run(wait_until_done=False, platform=platform)



if __name__ == "__main__":
    import emod_malaria.bootstrap as dtk
    import pathlib

    dtk.setup(pathlib.Path(manifest.eradication_path).parent)

    selected_platform = "SLURM_LOCAL"
    general_sim(selected_platform)
