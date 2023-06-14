import struct
import numpy as np
import manifest

# Defines SpatialOutput Class #
###############################
class SpatialOutput:
    def __init__(self):
        self.n_nodes = 0
        self.n_tstep = 0
        self.nodeids = []
        self.data = None
        self.start = 0
        self.interval = 1

    @classmethod # to decode .bin and return .json
    def from_bytes(cls, bytes, filtered=False):
        # The header size changes if the file is a filtered one
        headersize = 16 if filtered else 8

        # Create the class
        so = cls()

        # Retrive the number of nodes and number of timesteps
        so.n_nodes, = struct.unpack('i', bytes[0:4])
        so.n_tstep, = struct.unpack('i', bytes[4:8])

        # If filtered, retrieve the start and interval
        if filtered:
            start, = struct.unpack('f', bytes[8:12])
            interval, = struct.unpack('f', bytes[12:16])
            so.start = int(start)
            so.interval = int(interval)

        # Get the nodeids
        so.nodeids = struct.unpack(str(so.n_nodes) + 'I', bytes[headersize:headersize + so.n_nodes * 4])
        so.nodeids = np.asarray(so.nodeids)

        # Retrieve the data
        so.data = struct.unpack(str(so.n_nodes * so.n_tstep) + 'f',
                                bytes[headersize + so.n_nodes * 4:headersize + so.n_nodes * 4 + so.n_nodes * so.n_tstep * 4])
        so.data = np.asarray(so.data)
        so.data = so.data.reshape(so.n_tstep, so.n_nodes)

        return so

    def to_dict(self):
        return {'n_nodes': self.n_nodes,
                'n_tstep': self.n_tstep,
                'nodeids': self.nodeids,
                'start': self.start,
                'interval': self.interval,
                'data': self.data}



# Function to convert .json to .csv #
#####################################
from typing import Dict
import pandas as pd
def construct_spatial_output_df(rawdata: Dict, channel: str, timesteps=None) -> pd.DataFrame:
    """
    Construct spatial output data frame from a Spatial Output dictionary
    Args:
        rawdata: Spatial output file
        channel: Channel name
        timesteps: Timesteps. Defaults to empty array if not provided
    Returns:
    """
    if timesteps is None:
        timesteps = []
    n_nodes = rawdata['n_nodes']
    n_tstep = rawdata['n_tstep']
    if 'start' in rawdata:
        start = rawdata['start']
        interval = rawdata['interval']
    else:
        start, interval = 0, 1
    nodeids = rawdata['nodeids']
    data = rawdata['data']

    all_timesteps = range(start, (start + n_tstep) * interval, interval)

    df = pd.DataFrame({channel: [item for sublist in data for item in sublist],
                       'time': [item for sublist in [[x] * n_nodes for x in all_timesteps] for item in sublist],
                       'node': [item for sublist in [list(nodeids) * len(all_timesteps)] for item in sublist]})
    if not timesteps:
        return df

    timesteps = sorted(list(set(all_timesteps).intersection(timesteps)))
    return df[df['time'].isin(timesteps)]

# SpatialAnalyzer - collect outputs #
#####################################

import os
import pandas as pd
from idmtools.entities import IAnalyzer
from idmtools.entities.simulation import Simulation

class SpatialAnalyzer(IAnalyzer):
    # This analyzer can handle both unfiltered and filtered SpatialReports
    def __init__(self, dir_name, f_base, f_suffix, exp_id, spatial_channels, sweep_variables, working_dir='.', snapshot=None):
        super(SpatialAnalyzer, self).__init__(working_dir=working_dir,
                                                 filenames=[f'output/SpatialReportMalariaFiltered_all_ages_{x}.bin' for x in spatial_channels])

        self.dir_name = dir_name
        self.f_base = f_base or 'SpatialReportMalariaFiltered'
        self.f_suffix = f_suffix or ''
        self.exp_id = exp_id
        # Once we fix idmtools, we should remove this
        self.parse = False
        self.sweep_variables = sweep_variables or ['Run_Number', 'x_Temporary_Larval_Habitat']
        self.spatial_channels = spatial_channels
        self.output_fname = os.path.join(self.working_dir, f"{self.f_base}_{self.f_suffix}.csv")
        self.snapshot = snapshot
        

        # make sure output folder exists
        #os.makedirs(os.path.join(self.working_dir, 'spatial_output', self.dir_name), exist_ok=True)

    def map(self, data, simulation: Simulation):
        # we have to parse our data first since it will be a raw set of binary data
        for ch in self.spatial_channels:
            fn = f'output/{self.f_base}_{self.f_suffix}_{ch}.bin'
            data[fn] = SpatialOutput.from_bytes(data[fn], 'Filtered' in fn).to_dict()
        simdata = construct_spatial_output_df(data[f'output/{self.f_base}_{self.f_suffix}_{self.spatial_channels[0]}.bin'], self.spatial_channels[0])
        if len(self.spatial_channels) > 1:
            for ch in self.spatial_channels[1:]:
                simdata = pd.merge(left=simdata,
                                   right=construct_spatial_output_df(data[f'output/{self.f_base}_{self.f_suffix}_{ch}.bin'], ch),
                                   on=['time', 'node'])
        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                simdata[sweep_var] = simulation.tags[sweep_var]
            else:
                simdata[sweep_var] = 0
        return simdata

    def reduce(self, all_data):
        data_sets_per_experiment = {}

        for simulation, associated_data in all_data.items():
            experiment_name = simulation.experiment.name
            if experiment_name not in data_sets_per_experiment:
                data_sets_per_experiment[experiment_name] = []

            data_sets_per_experiment[experiment_name].append(associated_data)

        for experiment_name, data_sets in data_sets_per_experiment.items():
            d = pd.concat(data_sets).reset_index(drop=True)
            d['experiment'] = self.exp_id
            # save full dataframe
            d.to_csv(self.output_fname, index=False)
            print("Reporting on", self.spatial_channels)
            print("Grouped by", self.sweep_variables)
            print("Full spatial report saved to", self.output_fname)
            # save snapshots
            if self.snapshot is not None:
                d_sub = d[d['time'] == self.snapshot[0]] 
                sub_fname = os.path.join(self.working_dir, 'spatial_output',self.dir_name,f"{self.f_base}_{self.f_suffix}_Snapshot.csv")
                if(len(self.snapshot)>1):
                    for snap in self.snapshot[1:]:
                        d_sub_add = d[d['time'] == snap]
                        d_sub = pd.concat([d_sub,d_sub_add])
                d_sub.to_csv(sub_fname)
                print("Snapshot from days",self.snapshot, "saved to",sub_fname) 
                
        
if __name__ == "__main__":

    from idmtools.analysis.analyze_manager import AnalyzeManager
    from idmtools.core import ItemType
    from idmtools.core.platform_factory import Platform
    
    ## Experiments Dictionary ##
    ############################
    # {'experiment label' : 'exp_id'}
    expts = {'FE_example' : '4a8d05e9-64de-4d30-bda3-2e4ae46a3c5c'}
    ## Paths ##
    ###########
    # experiments folder
    jdir = manifest.job_directory
    wdir = os.path.join(jdir, 'my_outputs', 'spatial')
    if not os.path.exists(wdir):
        os.makedirs(wdir)
    ## Analyzer Specifications ##
    #############################
    # Grouping variables (for each node & timestep)
    sweep_variables = ['Run_Number', 'x_Temporary_Larval_Habitat']   
    # Outputs to analyze - must have been requested during simulation
    spatial_channels = ['Population',           
                        'PCR_Parasite_Prevalence',
                        'New_Clinical_Cases']
    # SpatialReportMalariaFiltered or SpatialReport?
    report_type = 'SpatialReportMalariaFiltered'    
    # .bin File suffix? (use empty string '' if none) 
    report_suffix = 'all_ages'
    
    ## Run Analyzer ##
    ##################
    with Platform('SLURM_LOCAL',job_directory=jdir) as platform:
        for expname, exp_id in expts.items():
            analyzer = [SpatialAnalyzer(dir_name=expname,
                                        f_base = report_type,
                                        f_suffix = report_suffix,
                                        exp_id = exp_id,
                                        spatial_channels=spatial_channels,
                                        sweep_variables=sweep_variables,
                                        working_dir=wdir)]      
            # Create AnalyzerManager with required parameters
            manager = AnalyzeManager(configuration={},ids=[(exp_id, ItemType.EXPERIMENT)],
                                     analyzers=analyzer, partial_analyze_ok=True)
            # Run analyze
            manager.analyze()
