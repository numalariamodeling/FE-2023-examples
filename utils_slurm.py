import copy
import os
from typing import List, Dict
import subprocess
import re
import pandas as pd
from COMPS import AuthManager
from COMPS.Data import QueryCriteria, Simulation
from idmtools.core import ItemType
from idmtools.entities.iplatform import IPlatform
from idmtools_platform_slurm.slurm_operations.operations_interface import SlurmOperations

def _get_serialized_filenames(num_cores, timesteps):
    if num_cores == 1:
        serialized_list = [f"state-{str(timesteps).zfill(5)}.dtk"]
    else:
        serialized_list = [f"state-{str(timesteps).zfill(5)}-{str(core_count).zfill(3)}.dtk"
                           for core_count in range(num_cores)]
    return serialized_list


def _get_core_counts(sim_id, platform):
    # TODO, get num_cores from simulation in slurm
    # sim = platform.get_item(sim_id, ItemType.SIMULATION, raw=True)
    # sim.refresh(QueryCriteria().select_children('hpc_jobs'))
    # num_cores = int(sim.hpc_jobs[-1].configuration.max_cores)
    num_cores = 1
    return num_cores

def get_workdir_from_simulations(platform: 'IPlatform', comps_simulations: List[Simulation]) -> Dict[str, str]:
    """
    Get COMPS filepath
    Args:
        platform: idmtools Platform
        comps_simulations: COMPS Simulations
    Returns: dictionary with simid as key and filepath as value
    """

    if platform.environment.upper() == "SLURMSTAGE" or platform.environment.upper() == "CALCULON":
        mounts = AuthManager.get_environment_macros(platform.environment)['DOCKER_MOUNTS']
        mounts = {v[0]: v[1:4] for v in [m.split(';') for m in mounts.split('|')]}
        # pretend I'm on Linux and set the Linux mapping environment variables
        for k, v in mounts.items():
            os.environ[k] = ';'.join([v[0], v[2]])
    sim_work_dir = {str(sim.id): sim.hpc_jobs[-1].working_directory for sim in comps_simulations if sim.hpc_jobs}

    return sim_work_dir


def create_sim_directory_map(exp_id: str, platform: 'IPlatform'):
    """
        Return a dataframe which contains simulation's working_path and tags.
    Args:
        exp_id: experiment id
        platform: idmtools platform
    Returns:
        dataframe
    """
    # Get idmtools Experiment
    exp = platform.get_item(exp_id, ItemType.EXPERIMENT, raw=False)

    tags_list = []
    for sim in exp.simulations:
        tags = copy.deepcopy(sim.tags)
        tags.update(dict(simid=sim.id))
        tags_list.append(tags)
    df = pd.DataFrame(tags_list)

    if len(df) != len(exp.simulations):
        print(f'Warning: not all jobs in {exp_id} succeeded', ':', )
        print(len(exp.simulations) - len(df), 'unsucceeded')

    simulations = exp.simulations
    dir_list = []
    for sim in simulations:
        dir_dict = {"simid": str(sim.id), "serialized_file_path": platform._op_client.get_directory(sim)}
        dir_list.append(dir_dict)

    df_dir = pd.DataFrame(dir_list)
    df = pd.merge(left=df, right=df_dir, on='simid')

    return df


def build_burnin_df(exp_id: str, platform,serialize_days):
    """
    return dataframe which contains serialized_file_path, serialized_population_filenames
    Args:
        exp_id:
        platform:
    Returns:
        dataframe:
        Run_Number | Serialization_Time_Steps | task_type | sweep_tag | simid | serialized_file_path|Num_Cores|Serialized_Population_Filenames
    Note, Serialized_Population_Filenames depends on n_cores. if n_cores = 2, Serialized_Population_Filenames look
    like these: state-00050-000.dtk, state-00050-001.dtk
    """

    df = create_sim_directory_map(exp_id, platform)
    # add Num_Cores to df
    df["Num_Cores"] = df["simid"].apply(_get_core_counts, platform=platform)
    #print(list(df.columns))
    #print(df.head())

    #try:
    burnin_length_in_days = serialize_days#int(df["Serialization_Time_Steps"].iloc[0].strip('[]'))
    #except AttributeError:
        # different versions of pandas save this as either a string or a list
        #burnin_length_in_days = df["Serialization_Time_Steps"].iloc[0][-1]

    df["Serialized_Population_Filenames"] = df["Num_Cores"].apply(_get_serialized_filenames, timesteps=burnin_length_in_days)
    df = df.reset_index(drop=True)
    return df
    
### TODO idmtools probably has a predefined shell template   
def shell_header_quest(A='b1139', p='b1139', t='02:00:00', N=1, ntasks_per_node=1, memG=8, job_name='myjob',
                       arrayJob=None):
    """Requires a 'log' subfolder to write in .err and .out files, alternatively log/ needs to be removed"""
    if not os.path.exists('log'):
        os.makedirs(os.path.join('log'))
   
    header = f'#!/bin/bash\n' \
             f'#SBATCH -A {A}\n' \
             f'#SBATCH -p {p}\n' \
             f'#SBATCH -t {t}\n' \
             f'#SBATCH -N {N}\n' \
             f'#SBATCH --ntasks-per-node={ntasks_per_node}\n' \
             f'#SBATCH --mem={memG}G\n' \
             f'#SBATCH --job-name="{job_name}"\n'
    if arrayJob is not None:
        array = arrayJob
        err = '#SBATCH --error=log/slurm_%A_%a.err\n'
        out = '#SBATCH --output=log/slurm_%A_%a.out\n'
        header = header + array + err + out
    else:
        err = f'#SBATCH --error=log/{job_name}.%j.err\n'
        out = f'#SBATCH --output=log/{job_name}.%j.out\n'
        header = header + err + out
    return header
        
def submit_scheduled_analyzer(experiment, platform, analyzer_script):
    wdir = os.path.abspath(os.path.dirname(__file__))
    ## Write bash file to submit
    header_post = shell_header_quest(job_name=f'analyze_exp', t='01:00:00')
    pymodule = '\n\nmodule purge all' \
               '\nsource activate /projects/b1139/environments/pytorch-1.11-emodpy-py39/\n'
    ### pycommand(s) - additional python or R scripts to directly run after analyzer can be added below
    pycommand = f'\ncd {wdir}' \
                f'\npython {analyzer_script} --expname {experiment.name} --expid {experiment.id}' 
                
    file = open(os.path.join(wdir,f'run_analyzer_{experiment.uid}.sh'), 'w')
    file.write(header_post + pymodule + pycommand)
    file.close()
    
    ## get job_id
    job_id = platform._op_client.get_job_id(experiment.id, experiment.item_type)
    
    script_path = os.path.join(wdir,f'run_analyzer_{experiment.uid}.sh') # save under different names, will require cleanup
    result = subprocess.run([f'sbatch --dependency=afterok:{job_id} {script_path}'], shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8').strip()
    SBATCH_REGEX = re.compile('^[a-zA-Z ]+(?P<id>\d+)$')
    job_id_analyzer = SBATCH_REGEX.match(result).group('id')

    print(f"Experiment job id: {job_id}")
    print(f"Analyzer job id: {job_id_analyzer}")
    
    #return (job_id_analyzer)  # if needed to add another dependency slurm submission
    return () 
    