import os
import datetime
import pandas as pd
import numpy as np
import sys
import re
import random
from idmtools.entities import IAnalyzer	
from idmtools.entities.simulation import Simulation
import manifest

## For plotting
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates


class SimpleInsetChartAnalyzer(IAnalyzer):

    @classmethod
    def monthparser(self, x):
        if x == 0:
            return 12
        else:
            return datetime.datetime.strptime(str(x), '%j').month

    def __init__(self, expt_name, working_dir=".", start_year=0):
        super(SimpleInsetChartAnalyzer, self).__init__(working_dir=working_dir, filenames=["output/InsetChart.json"])
        self.expt_name = expt_name
        self.start_year = start_year
        self.inset_channels = ["30-day Avg Infection Duration", "Adult Vectors", "Air Temperature", "Avg Num Infections",
                               "Births", "Blood Smear Gametocyte Prevalence", "Blood Smear Parasite Prevalence", "Campaign Cost",
                               "Daily Bites per Human", "Daily EIR", "Disease Deaths", "Fever Prevalence", "Human Infectious Reservoir",
                               "Infected", "Infectious Vectors", "Log Prevalence", "Mean Parasitemia", "New Clinical Cases",
                               "New Infections", "New Severe Cases", "Newly Symptomatic", "PCR Gametocyte Prevalence",
                               "PCR Parasite Prevalence", "PfHRP2 Prevalence", "Rainfall", "Relative Humidity", "Statistical Population",
                               "Symptomatic Population", "True Prevalence", "Variant Fraction-PfEMP1 Major"]

    def map(self, data, simulation: Simulation):
        simdata = pd.DataFrame({x: data[self.filenames[0]]['Channels'][x]['Data'] for x in self.inset_channels})
        simdata['Time'] = simdata.index
        simdata['Day'] = simdata['Time'] % 365
        simdata['Year'] = simdata['Time'].apply(lambda x: int(x / 365) + self.start_year)
        simdata['date'] = simdata.apply(
            lambda x: datetime.date(int(x['Year']), 1, 1) + datetime.timedelta(int(x['Day']) - 1), axis=1)

        return simdata

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("No data have been returned... Exiting...")
            return

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        adf = pd.concat(selected).reset_index(drop=True)
        adf.to_csv(os.path.join(self.working_dir, self.expt_name, 'All_Age_InsetChart.csv'), index=False)

        
if __name__ == "__main__":

    from idmtools.analysis.analyze_manager import AnalyzeManager
    from idmtools.core import ItemType
    from idmtools.core.platform_factory import Platform

    
    expts = {
        'example_basic' : 'd6992a9f-bc38-4162-9e27-177adfc906c5'
    }
    

    jdir = manifest.job_directory
    wdir = os.path.join(jdir, 'my_outputs')
    
    if not os.path.exists(wdir):
        os.mkdir(wdir)
    
    
    with Platform('SLURM_LOCAL',job_directory=jdir) as platform:

        for expt_name, exp_id in expts.items():
          
            analyzer = [SimpleInsetChartAnalyzer(expt_name=expt_name,
                                      start_year = 2023,
                                      working_dir=wdir)]
            
            # Create AnalyzerManager with required parameters
            manager = AnalyzeManager(configuration={}, ids=[(exp_id, ItemType.EXPERIMENT)],
                                     analyzers=analyzer, partial_analyze_ok=True)
            # Run analyze
            manager.analyze()
            