import os
import datetime
import pandas as pd
import numpy as np
from idmtools.entities import IAnalyzer

"""
InsetChart Analyzer
"""

class InsetChartAnalyzer(IAnalyzer):

    @classmethod
    def monthparser(self, x):
        if x == 0:
            return 12
        else:
            return datetime.datetime.strptime(str(x), '%j').month

    def __init__(self, expt_name, sweep_variables=None, channels=None, working_dir=".", start_year=2022):
        super(InsetChartAnalyzer, self).__init__(working_dir=working_dir, filenames=["output/InsetChart.json"])
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.inset_channels = channels or ['Statistical Population', 'New Clinical Cases', 'New Severe Cases',
                                           'PfHRP2 Prevalence']
        self.expt_name = expt_name
        self.start_year = start_year

    def map(self, data, simulation):
        simdata = pd.DataFrame({x: data[self.filenames[0]]['Channels'][x]['Data'] for x in self.inset_channels})
        simdata['Time'] = simdata.index
        simdata['Day'] = simdata['Time'] % 365
        simdata['Year'] = simdata['Time'].apply(lambda x: int(x / 365) + self.start_year)
        simdata['date'] = simdata.apply(
            lambda x: datetime.date(int(x['Year']), 1, 1) + datetime.timedelta(int(x['Day']) - 1), axis=1)

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                simdata[sweep_var] = simulation.tags[sweep_var]
            elif sweep_var == 'Run_Number' :
                simdata[sweep_var] = 0
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


"""
MalariaSummaryReport Analyzer
"""

### PER AGEBIN
# AnnualAgebinPfPRAnalyzer
class AnnualAgebinPfPRAnalyzer(IAnalyzer):

    def __init__(self, expt_name, sweep_variables=None, working_dir='./', start_year=2022,
                 end_year=2025, burnin=None):

        super(AnnualAgebinPfPRAnalyzer, self).__init__(working_dir=working_dir,
                                                       filenames=[
                                                           f"output/MalariaSummaryReport_Annual_Agebin.json"])
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.expt_name = expt_name
        self.start_year = start_year
        self.end_year = end_year
        self.burnin = burnin

    def map(self, data, simulation):

        adf = pd.DataFrame()

        nyears = (self.end_year - self.start_year)
        age_bins = data[self.filenames[0]]['Metadata']['Age Bins']
        pfpr2to10 = data[self.filenames[0]]['DataByTime']['PfPR_2to10'][:nyears]

        for age in range(len(age_bins)):
            d = data[self.filenames[0]]['DataByTimeAndAgeBins']['PfPR by Age Bin'][:nyears]
            pfpr = [x[age] for x in d]
            d = data[self.filenames[0]]['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin'][:nyears]
            clinical_cases = [x[age] for x in d]
            d = data[self.filenames[0]]['DataByTimeAndAgeBins']['Annual Severe Incidence by Age Bin'][:nyears]
            severe_cases = [x[age] for x in d]
            d = data[self.filenames[0]]['DataByTimeAndAgeBins']['Average Population by Age Bin'][:nyears]
            pop = [x[age] for x in d]

            simdata = pd.DataFrame({'year': range(self.start_year, self.end_year),
                                    'PfPR': pfpr,
                                    'Cases': clinical_cases,
                                    'Severe cases': severe_cases,
                                    'Pop': pop})
            simdata['agebin'] = age_bins[age]
            simdata['pfpr2to10'] = pfpr2to10
            adf = pd.concat([adf, simdata])

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    adf[sweep_var] = simulation.tags[sweep_var]
                except:
                    adf[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
            elif sweep_var == 'Run_Number' :
                adf[sweep_var] = 0

        return adf

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("\nWarning: No data have been returned... Exiting...")
            return
        adf = pd.concat(selected).reset_index(drop=True)

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        # Discard early years used as burnin
        if self.burnin is not None:
            adf = adf[adf['year'] >= self.start_year + self.burnin]
        adf = adf.loc[adf['agebin'] <= 100]
        adf.to_csv(os.path.join(self.working_dir, self.expt_name, 'Agebin_PfPR_ClinicalIncidence_annual.csv'), index=False)


# MonthlyAgebinPfPRAnalyzer
class MonthlyAgebinPfPRAnalyzer(IAnalyzer):

    def __init__(self, expt_name, sweep_variables=None, working_dir='./', start_year=2020,
                 end_year=2023,
                 burnin=None, filter_exists=False):

        super(MonthlyAgebinPfPRAnalyzer, self).__init__(working_dir=working_dir,
                                                        filenames=[
                                                            f"output/MalariaSummaryReport_Monthly_Agebin_{x}.json"
                                                            for x in range(start_year, end_year)]
                                                        )
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.expt_name = expt_name
        self.start_year = start_year
        self.end_year = end_year
        self.burnin = burnin
        self.filter_exists = filter_exists

    def filter(self, simulation):
        if self.filter_exists:
            file = os.path.join(simulation.get_path(), self.filenames[0])
            return os.path.exists(file)
        else:
            return True

    def map(self, data, simulation):

        adf = pd.DataFrame()
        for year, fname in zip(range(self.start_year, self.end_year), self.filenames):

            age_bins = data[fname]['Metadata']['Age Bins']

            for age in list(range(0, len(age_bins))):
                d = data[fname]['DataByTimeAndAgeBins']['PfPR by Age Bin'][:12]
                pfpr = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin'][:12]
                clinical_cases = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Annual Severe Incidence by Age Bin'][:12]
                severe_cases = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Annual Mild Anemia by Age Bin'][:12]
                mild_anaemia = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Annual Moderate Anemia by Age Bin'][:12]
                moderate_anaemia = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Annual Severe Anemia by Age Bin'][:12]
                severe_anaemia = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Average Population by Age Bin'][:12]
                pop = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['New Infections by Age Bin'][:12]
                new_infect = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Mean Log Parasite Density by Age Bin'][:12]
                log_parasite_density = [x[age] for x in d]

                simdata = pd.DataFrame({'month': range(1, 13),
                                        'PfPR': pfpr,
                                        'Cases': clinical_cases,
                                        'Severe cases': severe_cases,
                                        'Mild anaemia': mild_anaemia,
                                        'Moderate anaemia': moderate_anaemia,
                                        'Severe anaemia': severe_anaemia,
                                        'New infections': new_infect,
                                        'Mean Log Parasite Density': log_parasite_density,
                                        'Pop': pop})
                simdata['year'] = year
                simdata['agebin'] = age_bins[age]
                adf = pd.concat([adf, simdata])

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    adf[sweep_var] = simulation.tags[sweep_var]
                except:
                    adf[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
            elif sweep_var == 'Run_Number' :
                adf[sweep_var] = 0

        return adf

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("\nWarning: No data have been returned... Exiting...")
            return
        df = pd.concat(selected).reset_index(drop=True)

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        if self.burnin is not None:
            df = df[df['year'] > self.start_year + self.burnin]
        df = df.loc[df['agebin'] < 100]  # less than 100 years
        df.to_csv((os.path.join(self.working_dir, self.expt_name, f'Agebin_PfPR_ClinicalIncidence.csv')),
                  index=False)


### PER AGE GROUP
# MonthlyPfPRAnalyzerU5
class MonthlyPfPRAnalyzerU5(IAnalyzer):

    def __init__(self, expt_name, sweep_variables=None, working_dir='./', start_year=2020, end_year=2023,
                 burnin=None, filter_exists=False):

        super(MonthlyPfPRAnalyzerU5, self).__init__(working_dir=working_dir,
                                                    filenames=[
                                                        f"output/MalariaSummaryReport_Monthly_U5_{x}.json"
                                                        for x in range(start_year, end_year)]
                                                    )
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.expt_name = expt_name
        self.start_year = start_year
        self.end_year = end_year
        self.burnin = burnin
        self.filter_exists = filter_exists

    def filter(self, simulation):
        if self.filter_exists:
            file = os.path.join(simulation.get_path(), self.filenames[0])
            return os.path.exists(file)
        else:
            return True

    def map(self, data, simulation):

        adf = pd.DataFrame()
        for year, fname in zip(range(self.start_year, self.end_year), self.filenames):
            d = data[fname]['DataByTimeAndAgeBins']['PfPR by Age Bin'][:12]
            pfpr = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin'][:12]
            clinical_cases = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Annual Severe Incidence by Age Bin'][:12]
            severe_cases = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Average Population by Age Bin'][:12]
            pop = [x[1] for x in d]
            d = data[fname]['DataByTime']['PfPR_2to10'][:12]
            PfPR_2to10 = d
            d = data[fname]['DataByTime']['Annual EIR'][:12]
            annualeir = d
            simdata = pd.DataFrame({'month': range(1, 13),
                                    'PfPR U5': pfpr,
                                    'Cases U5': clinical_cases,
                                    'Severe cases U5': severe_cases,
                                    'Pop U5': pop,
                                    'PfPR_2to10': PfPR_2to10,
                                    'annualeir': annualeir})
            simdata['year'] = year
            adf = pd.concat([adf, simdata])

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    adf[sweep_var] = simulation.tags[sweep_var]
                except:
                    adf[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
            elif sweep_var == 'Run_Number' :
                adf[sweep_var] = 0

        return adf

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("\nWarning: No data have been returned... Exiting...")
            return

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        adf = pd.concat(selected).reset_index(drop=True)
        if self.burnin is not None:
            adf = adf[adf['year'] > self.start_year + self.burnin]
        adf.to_csv((os.path.join(self.working_dir, self.expt_name, 'U5_PfPR_ClinicalIncidence.csv')), index=False)


class MonthlyPfPRAnalyzerU10(IAnalyzer):

    def __init__(self, expt_name, sweep_variables=None, working_dir='./', start_year=2020, end_year=2023,
                 burnin=None, filter_exists=False):

        super(MonthlyPfPRAnalyzerU10, self).__init__(working_dir=working_dir,
                                                     filenames=[
                                                         f"output/MalariaSummaryReport_Monthly_U10_{x}.json"
                                                         for x in range(start_year, end_year)]
                                                     )
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.expt_name = expt_name
        self.start_year = start_year
        self.end_year = end_year
        self.burnin = burnin
        self.filter_exists = filter_exists

    def filter(self, simulation):
        if self.filter_exists:
            file = os.path.join(simulation.get_path(), self.filenames[0])
            return os.path.exists(file)
        else:
            return True

    def map(self, data, simulation):

        adf = pd.DataFrame()
        for year, fname in zip(range(self.start_year, self.end_year), self.filenames):
            d = data[fname]['DataByTimeAndAgeBins']['PfPR by Age Bin'][:12]
            pfpr = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin'][:12]
            clinical_cases = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Annual Severe Incidence by Age Bin'][:12]
            severe_cases = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Average Population by Age Bin'][:12]
            pop = [x[1] for x in d]
            simdata = pd.DataFrame({'month': range(1, 13),
                                    'PfPR U10': pfpr,
                                    'Cases U10': clinical_cases,
                                    'Severe cases U10': severe_cases,
                                    'Pop U10': pop})
            simdata['year'] = year
            adf = pd.concat([adf, simdata])

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    adf[sweep_var] = simulation.tags[sweep_var]
                except:
                    adf[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
            elif sweep_var == 'Run_Number' :
                adf[sweep_var] = 0

        return adf

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("\nWarning: No data have been returned... Exiting...")
            return

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        adf = pd.concat(selected).reset_index(drop=True)
        if self.burnin is not None:
            adf = adf[adf['year'] > self.start_year + self.burnin]
        adf.to_csv((os.path.join(self.working_dir, self.expt_name, 'U10_PfPR_ClinicalIncidence.csv')), index=False)


### FOR EXERCISE, WEEKLY REPORTING
# WeeklyPfPRAnalyzerU5
class WeeklyPfPRAnalyzerU5(IAnalyzer):

    def __init__(self, expt_name, sweep_variables=None, working_dir='./', start_year=2020, end_year=2023,
                 burnin=None, filter_exists=False):

        super(WeeklyPfPRAnalyzerU5, self).__init__(working_dir=working_dir,
                                                   filenames=[
                                                       f"output/MalariaSummaryReport_Weekly_U5_{x}.json"
                                                       for x in range(start_year, end_year)]
                                                   )
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.expt_name = expt_name
        self.start_year = start_year
        self.end_year = end_year
        self.burnin = burnin
        self.filter_exists = filter_exists

    def filter(self, simulation):
        if self.filter_exists:
            file = os.path.join(simulation.get_path(), self.filenames[0])
            return os.path.exists(file)
        else:
            return True

    def map(self, data, simulation):

        adf = pd.DataFrame()
        for year, fname in zip(range(self.start_year, self.end_year), self.filenames):
            d = data[fname]['DataByTimeAndAgeBins']['PfPR by Age Bin'][:52]
            pfpr = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin'][:52]
            clinical_cases = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Annual Severe Incidence by Age Bin'][:52]
            severe_cases = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Average Population by Age Bin'][:52]
            pop = [x[1] for x in d]
            d = data[fname]['DataByTime']['PfPR_2to10'][:52]
            PfPR_2to10 = d
            d = data[fname]['DataByTime']['Annual EIR'][:52]
            annualeir = d
            simdata = pd.DataFrame({'week': range(1, 53),
                                    'PfPR U5': pfpr,
                                    'Cases U5': clinical_cases,
                                    'Severe cases U5': severe_cases,
                                    'Pop U5': pop})
            simdata['year'] = year
            adf = pd.concat([adf, simdata])

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    adf[sweep_var] = simulation.tags[sweep_var]
                except:
                    adf[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
            elif sweep_var == 'Run_Number' :
                adf[sweep_var] = 0

        return adf

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("\nWarning: No data have been returned... Exiting...")
            return

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        adf = pd.concat(selected).reset_index(drop=True)
        if self.burnin is not None:
            adf = adf[adf['year'] > self.start_year + self.burnin]
        adf.to_csv((os.path.join(self.working_dir, self.expt_name, 'U5_PfPR_ClinicalIncidence_weekly.csv')),
                   index=False)


"""
ReportEventRecorder ANALYZER
"""


class IndividualEventsAnalyzer(IAnalyzer):

    @classmethod
    def monthparser(self, x):
        if x == 0:
            return 12
        else:
            return datetime.datetime.strptime(str(x), '%j').month

    def __init__(self, expt_name, sweep_variables=None, working_dir='./', start_year=2022,
                 selected_year=None, filter_exists=False):
        super(IndividualEventsAnalyzer, self).__init__(working_dir=working_dir,
                                                       filenames=["output/ReportEventRecorder.csv"]
                                                       )
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.expt_name = expt_name
        self.start_year = start_year
        self.selected_year = selected_year
        self.filter_exists = filter_exists  # flag used for NUCLUSTER

    def filter(self, simulation):
        if self.filter_exists:
            file = os.path.join(simulation.get_path(), self.filenames[0])
            return os.path.exists(file)
        else:
            return True

    def map(self, data, simulation):

        simdata = pd.DataFrame(data[self.filenames[0]])
        simdata['Day'] = simdata['Time'] % 365
        simdata['Month'] = simdata['Day'].apply(lambda x: self.monthparser((x + 1) % 365))
        simdata['Year'] = simdata['Time'].apply(lambda x: int(x / 365) + self.start_year)
        if self.selected_year is not None:
            simdata = simdata.loc[(simdata['Year'] == self.selected_year)]

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    simdata[sweep_var] = simulation.tags[sweep_var]
                except:
                    simdata[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
            elif sweep_var == 'Run_Number':
                simdata[sweep_var] = 0
        return simdata

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("\nWarning: No data have been returned... Exiting...")
            return

        if self.selected_year is not None:
            selected_year_suffix = f'_{self.selected_year}'
        else:
            selected_year_suffix = '_all_years'

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        adf = pd.concat(selected).reset_index(drop=True)
        adf.to_csv(os.path.join(self.working_dir, self.expt_name, f'IndividualEvents{selected_year_suffix}.csv'),
                   index=False)


class TransmissionReport(IAnalyzer):

    @classmethod
    def monthparser(self, x):
        if x == 0:
            return 12
        else:
            return datetime.datetime.strptime(str(x), '%j').month

    def __init__(self, expt_name, channels=None, sweep_variables=None, working_dir='./', start_year=2022,
                 selected_year=None, daily_report=False, monthly_report=False, filter_exists=False):
        super(TransmissionReport, self).__init__(working_dir=working_dir,
                                                 filenames=["output/ReportMalariaFiltered.json"])
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.channels = channels or ['Daily Bites per Human', 'Daily EIR', 'Mean Parasitemia', 'PfHRP2 Prevalence',
                                     'Rainfall']
        self.start_year = start_year
        self.selected_year = selected_year
        self.daily_report = daily_report
        self.monthly_report = monthly_report
        self.expt_name = expt_name
        self.filter_exists = filter_exists

    def filter(self, simulation):
        if self.filter_exists:
            file = os.path.join(simulation.get_path(), self.filenames[0])
            return os.path.exists(file)
        else:
            return True

    def map(self, data, simulation):
        simdata = pd.DataFrame({x: data[self.filenames[0]]['Channels'][x]['Data'] for x in self.channels})
        # simdata = simdata[-365:]
        simdata['Time'] = simdata.index
        simdata['Day'] = simdata['Time'] % 365
        simdata['Month'] = simdata['Day'].apply(lambda x: self.monthparser((x + 1) % 365))
        simdata['Year'] = simdata['Time'].apply(lambda x: int(x / 365) + self.start_year)
        simdata['date'] = simdata.apply(lambda x: datetime.date(int(x['Year']), int(x['Month']), 1), axis=1)
        if self.selected_year is not None:
            simdata = simdata.loc[(simdata['Year'] == self.selected_year)]

        simdata = simdata.groupby(['Time', 'date', 'Day', 'Month', 'Year'])[self.channels].agg(np.mean).reset_index()

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    simdata[sweep_var] = simulation.tags[sweep_var]
                except:
                    simdata[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
            elif sweep_var == 'Run_Number':
                simdata[sweep_var] = 0
        return simdata

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("\nWarning: No data have been returned... Exiting...")
            return

        adf = pd.concat(selected).reset_index(drop=True)

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))
        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        if self.selected_year is not None:
            selected_year_suffix = f'_{self.selected_year}'
        else:
            selected_year_suffix = '_all_years'

        ## Aggregate Run_Number
        grp_channels = [x for x in self.sweep_variables if x != "Run_Number"]
        adf = adf.groupby(['Time', 'date', 'Day', 'Month', 'Year'] + grp_channels)[self.channels].agg(
            np.mean).reset_index()

        sum_channels = ['Daily Bites per Human', 'Daily EIR', 'Rainfall']
        mean_channels = ['Mean Parasitemia', 'PfHRP2 Prevalence']
        ### DAILY TRANSMISSION
        if self.daily_report:
            adf.to_csv(
                os.path.join(self.working_dir, self.expt_name, f'daily_transmission_report{selected_year_suffix}.csv'),
                index=False)

        ### MONTHLY TRANSMISSION
        if self.monthly_report:
            df = adf.groupby(['date', 'Year', 'Month'] + grp_channels)[sum_channels].agg(np.sum).reset_index()
            pdf = adf.groupby(['date', 'Year', 'Month'] + grp_channels)[mean_channels].agg(np.mean).reset_index()
            mdf = pd.merge(left=pdf, right=df, on=['date', 'Year', 'Month'] + grp_channels)
            mdf = mdf.rename(columns={'Daily Bites per Human': 'Monthly Bites per Human', 'Daily EIR': 'Monthly EIR'})
            mdf.to_csv(os.path.join(self.working_dir, self.expt_name,
                                    f'monthly_transmission_report{selected_year_suffix}.csv'), index=False)

        ### ANNUAL TRANSMISSION
        df = adf.groupby(['Year'] + grp_channels)[sum_channels].agg(np.sum).reset_index()
        pdf = adf.groupby(['Year'] + grp_channels)[mean_channels].agg(np.mean).reset_index()
        adf = pd.merge(left=pdf, right=df, on=['Year'] + grp_channels)
        adf = adf.rename(columns={'Daily Bites per Human': 'Annual Bites per Human', 'Daily EIR': 'Annual EIR'})
        adf.to_csv(
            os.path.join(self.working_dir, self.expt_name, f'annual_transmission_report{selected_year_suffix}.csv'),
            index=False)


class BednetUsageAnalyzer(IAnalyzer):

    @classmethod
    def monthparser(self, x):
        if x == 0:
            return 12
        else:
            return datetime.datetime.strptime(str(x), '%j').month

    def __init__(self, expt_name, channels=None, sweep_variables=None, working_dir='./', start_year=2022,
                 selected_year=None, filter_exists=False):
        super(BednetUsageAnalyzer, self).__init__(working_dir=working_dir,
                                                  filenames=["output/ReportEventCounter.json",
                                                             "output/ReportMalariaFiltered.json"])
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.channels = channels or ['Bednet_Using', 'Bednet_Got_New_One']
        self.inset_channels = ['Statistical Population']
        self.start_year = start_year
        self.selected_year = selected_year
        self.expt_name = expt_name
        self.filter_exists = filter_exists

    def filter(self, simulation):
        if self.filter_exists:
            file = os.path.join(simulation.get_path(), self.filenames[0])
            return os.path.exists(file)
        else:
            return True

    def map(self, data, simulation):

        simdata = pd.DataFrame({x: data[self.filenames[1]]['Channels'][x]['Data'] for x in self.inset_channels})
        simdata['Time'] = simdata.index

        if self.channels:
            d = pd.DataFrame({x: data[self.filenames[0]]['Channels'][x]['Data'] for x in self.channels})
            # d = pd.DataFrame({x: data[self.filenames[0]]['Channels'][x]['Data'][:len(simdata)] for x in self.channels})
            d['Time'] = d.index
            simdata = pd.merge(left=simdata, right=d, on='Time')

        simdata['Day'] = simdata['Time'] % 365
        simdata['Month'] = simdata['Day'].apply(lambda x: self.monthparser((x + 1) % 365))
        simdata['Year'] = simdata['Time'].apply(lambda x: int(x / 365) + self.start_year)

        if self.selected_year is not None:
            simdata = simdata.loc[(simdata['Year'] == self.selected_year)]

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    simdata[sweep_var] = simulation.tags[sweep_var]
                except:
                    simdata[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
            elif sweep_var == 'Run_Number':
                simdata[sweep_var] = 0
        return simdata

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("\nWarning: No data have been returned... Exiting...")
            return

        adf = pd.concat(selected).reset_index(drop=True)
        adf['date'] = adf.apply(lambda x: datetime.date(int(x['Year']), int(x['Month']), 1), axis=1)

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))
        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        ## Aggregate time to months
        sum_channels = ['Bednet_Got_New_One']
        for x in [y for y in sum_channels if y not in adf.columns.values]:
            adf[x] = 0
        mean_channels = ['Statistical Population', 'Bednet_Using']
        df = adf.groupby(['date'] + self.sweep_variables)[sum_channels].agg(np.sum).reset_index()
        pdf = adf.groupby(['date'] + self.sweep_variables)[mean_channels].agg(np.mean).reset_index()

        adf = pd.merge(left=pdf, right=df, on=['date'] + self.sweep_variables)
        adf['mean_usage'] = adf['Bednet_Using'] / adf['Statistical Population']
        adf['new_net_coverage'] = adf['Bednet_Got_New_One'] / adf['Statistical Population']
        adf.to_csv(os.path.join(self.working_dir, self.expt_name, f'BednetUsageAnalyzer.csv'), index=False)


class ReceivedCampaignAnalyzer(IAnalyzer):

    @classmethod
    def monthparser(self, x):
        if x == 0:
            return 12
        else:
            return datetime.datetime.strptime(str(x), '%j').month

    def __init__(self, expt_name, channels=None, sweep_variables=None, working_dir='./', start_year=2022):
        super(ReceivedCampaignAnalyzer, self).__init__(working_dir=working_dir,
                                                       filenames=["output/ReportEventCounter.json",
                                                                  "output/InsetChart.json"])
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.channels = channels or ['Received_Treatment']
        self.start_year = start_year
        self.expt_name = expt_name

    def map(self, data, simulation):

        simdata = pd.DataFrame({x: data[self.filenames[0]]['Channels'][x]['Data'] for x in self.channels})
        simdata['Population'] = data[self.filenames[1]]['Channels']['Statistical Population']['Data']
        simdata['Time'] = simdata.index
        simdata['Day'] = simdata['Time'] % 365
        simdata['Year'] = simdata['Time'].apply(lambda x: int(x / 365) + 2022)
        simdata['date'] = simdata.apply(
            lambda x: datetime.date(int(x['Year']), 1, 1) + datetime.timedelta(int(x['Day']) - 1), axis=1)

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    simdata[sweep_var] = simulation.tags[sweep_var]
                except:
                    simdata[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
            elif sweep_var == 'Run_Number':
                simdata[sweep_var] = 0
        return simdata

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("\nWarning: No data have been returned... Exiting...")
            return

        adf = pd.concat(selected).reset_index(drop=True)

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))
        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        events = [ch.replace('Received_', '') for ch in self.channels if 'Received' in ch]
        for event in events:
            adf[f'{event}_Coverage'] = adf[f'Received_{event}'] / adf['Population']
        adf.to_csv(os.path.join(self.working_dir, self.expt_name, f'Event_Count.csv'), index=False)


"""
ReportEventCounter Analyzer
"""


# MonthlyTreatedCasesAnalyzer
class MonthlyTreatedCasesAnalyzer(IAnalyzer):

    @classmethod
    def monthparser(self, x):
        if x == 0:
            return 12
        else:
            return datetime.datetime.strptime(str(x), '%j').month

    def __init__(self, expt_name, channels=None, sweep_variables=None, working_dir=".", start_year=2010,
                 end_year=2020, filter_exists=False):
        super(MonthlyTreatedCasesAnalyzer, self).__init__(working_dir=working_dir,
                                                          filenames=["output/ReportEventCounter.json",
                                                                     "output/ReportMalariaFiltered.json"]
                                                          )
        self.sweep_variables = sweep_variables or ["LGA", "Run_Number"]
        self.channels = channels or ['Received_Treatment']
        self.inset_channels = ['Statistical Population', 'New Infections', 'Newly Symptomatic', 'New Clinical Cases',
                               'New Severe Cases', 'PfHRP2 Prevalence']
        self.expt_name = expt_name
        self.start_year = start_year
        self.end_year = end_year
        self.filter_exists = filter_exists

    def filter(self, simulation):
        if self.filter_exists:
            file = os.path.join(simulation.get_path(), self.filenames[0])
            return os.path.exists(file)
        else:
            return True

    def map(self, data, simulation):
        simdata = pd.DataFrame({x: data[self.filenames[1]]['Channels'][x]['Data'] for x in self.inset_channels})
        simdata['Time'] = simdata.index
        if self.channels:
            d = pd.DataFrame({x: data[self.filenames[0]]['Channels'][x]['Data'] for x in self.channels})
            d['Time'] = d.index
            simdata = pd.merge(left=simdata, right=d, on='Time')
        simdata['Day'] = simdata['Time'] % 365
        simdata['Month'] = simdata['Day'].apply(lambda x: self.monthparser((x + 1) % 365))
        simdata['Year'] = simdata['Time'].apply(lambda x: int(x / 365) + self.start_year)
        if self.start_year > 0:
            simdata['date'] = simdata.apply(lambda x: datetime.date(int(x['Year']), int(x['Month']), 1), axis=1)
        else:
            simdata['date'] = simdata["Year"].astype(str) + '-' + simdata["Month"].astype(str) + '-' + simdata[
                "Day"].astype(str)

        sum_channels = self.channels + ['New Clinical Cases',
                                        'New Severe Cases']  # 'New Infections', 'Newly Symptomatic',
        mean_channels = ['Statistical Population', 'PfHRP2 Prevalence']
        for x in [y for y in sum_channels if y not in simdata.columns.values]:
            simdata[x] = 0

        df = simdata.groupby(['date'])[sum_channels].agg(np.sum).reset_index()
        pdf = simdata.groupby(['date'])[mean_channels].agg(np.mean).reset_index()

        simdata = pd.merge(left=pdf, right=df, on=['date'])

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    simdata[sweep_var] = simulation.tags[sweep_var]
                except:
                    simdata[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
            elif sweep_var == 'Run_Number':
                simdata[sweep_var] = 0
        return simdata

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("No data have been returned... Exiting...")
            return

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        adf = pd.concat(selected).reset_index(drop=True)
        adf.to_csv(os.path.join(self.working_dir, self.expt_name, 'All_Age_Monthly_Cases.csv'), index=False)


# MonthlySevereTreatedByAgeAnalyzer
class MonthlySevereTreatedByAgeAnalyzer(IAnalyzer):
    @classmethod
    def monthparser(self, x):
        if x == 0:
            return 12
        else:
            return datetime.datetime.strptime(str(x), '%j').month

    def __init__(self, expt_name, event_name='Received_Severe_Treatment', agebins=None,
                 sweep_variables=None, working_dir=".", start_year=2010, end_year=2020):
        super(MonthlySevereTreatedByAgeAnalyzer, self).__init__(working_dir=working_dir,
                                                                filenames=["output/ReportEventRecorder.csv"]
                                                                )
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.event_name = event_name
        self.agebins = agebins or [1, 5, 200]
        self.expt_name = expt_name
        self.start_year = start_year
        self.end_year = end_year

    def map(self, data, simulation):

        output_data = data[self.filenames[0]]
        output_data = output_data[output_data['Event_Name'] == self.event_name]

        simdata = pd.DataFrame()
        if len(output_data) > 0:  # there are events of this type
            output_data['Day'] = output_data['Time'] % 365
            output_data['month'] = output_data['Day'].apply(lambda x: self.monthparser((x + 1) % 365))
            output_data['year'] = output_data['Time'].apply(lambda x: int(x / 365) + self.start_year)
            output_data['age in years'] = output_data['Age'] / 365

            for agemax in self.agebins:
                if agemax < 200:
                    agelabel = 'U%d' % agemax
                else:
                    agelabel = 'all_ages'
                if agemax == 5:
                    agemin = 0.25
                else:
                    agemin = 0
                d = output_data[(output_data['age in years'] < agemax) & (output_data['age in years'] > agemin)]
                g = d.groupby(['year', 'month'])['Event_Name'].agg(len).reset_index()
                g = g.rename(columns={'Event_Name': 'Num_%s_Received_Severe_Treatment' % agelabel})
                if simdata.empty:
                    simdata = g
                else:
                    if not g.empty:
                        simdata = pd.merge(left=simdata, right=g, on=['year', 'month'], how='outer')
                        simdata = simdata.fillna(0)

            for sweep_var in self.sweep_variables:
                if sweep_var in simulation.tags.keys():
                    simdata[sweep_var] = simulation.tags[sweep_var]
                elif sweep_var == 'Run_Number':
                    simdata[sweep_var] = 0
        else:
            simdata = pd.DataFrame(columns=['year', 'month', 'Num_U5_Received_Severe_Treatment',
                                            'Num_U1_Received_Severe_Treatment',
                                            'Num_all_ages_Received_Severe_Treatment'] + self.sweep_variables)
        return simdata

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("No data have been returned... Exiting...")
            return

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        adf = pd.concat(selected, sort=False).reset_index(drop=True)
        adf = adf.fillna(0)
        adf.to_csv(os.path.join(self.working_dir, self.expt_name, 'Treated_Severe_Monthly_Cases_By_Age.csv'),
                   index=False)

        for agelabel in ['U5']:
            severe_treat_df = adf[
                ['year', 'month', 'Num_%s_Received_Severe_Treatment' % agelabel] + self.sweep_variables]
            # cast to int65 data type for merge with incidence df
            severe_treat_df = severe_treat_df.astype({'month': 'int64', 'year': 'int64', 'Run_Number': 'int64'})

            # combine with existing columns of the U5 clinical incidence and PfPR dataframe
            incidence_df = pd.read_csv(
                os.path.join(self.working_dir, self.expt_name, '%s_PfPR_ClinicalIncidence.csv' % agelabel))
            merged_df = pd.merge(left=incidence_df, right=severe_treat_df,
                                 on=self.sweep_variables + ['year', 'month'],
                                 how='left')
            merged_df = merged_df.fillna(0)

            # fix any excess treated cases!
            merged_df['num severe cases %s' % agelabel] = merged_df['Severe cases %s' % agelabel] * merged_df[
                'Pop %s' % agelabel] * 30 / 365
            merged_df['excess sev treat %s' % agelabel] = merged_df['Num_%s_Received_Severe_Treatment' % agelabel] - \
                                                          merged_df['num severe cases %s' % agelabel]
            merged_df['sweep_id'] = merged_df.groupby(self.sweep_variables, sort=False).ngroup().apply(
                '{:010}'.format)

            for (rn, sweep), rdf in merged_df.groupby(['Run_Number', 'sweep_id']):
                for r, row in rdf.iterrows():
                    if row['excess sev treat %s' % agelabel] < 1:
                        continue
                    # fix Jan 2020 (start of sim) excess treated severe cases
                    if row['year'] == self.start_year and row['month'] == 1:
                        merged_df.loc[(merged_df['year'] == self.start_year) & (merged_df['month'] == 1) & (
                                merged_df['Run_Number'] == rn) & (merged_df[self.sweep_id] == sweep),
                                      'Num_%s_Received_Severe_Treatment' % agelabel] = np.sum(
                            merged_df[(merged_df['year'] == self.start_year) &
                                      (merged_df['month'] == 1) &
                                      (merged_df['Run_Number'] == rn) &
                                      (merged_df[self.sweep_id] == sweep)]['num severe cases %s' % agelabel])
                    else:
                        # figure out which is previous month
                        newyear = row['year']
                        newmonth = row['month'] - 1
                        if newmonth < 1:
                            newyear -= 1
                        excess = row['excess sev treat %s' % agelabel]
                        merged_df.loc[(merged_df['year'] == self.start_year) & (merged_df['month'] == 1) & (
                                merged_df['Run_Number'] == rn) & (merged_df[
                                                                      self.sweep_id] == sweep), 'Num_%s_Received_Severe_Treatment' % agelabel] = \
                            merged_df.loc[(merged_df['year'] == self.start_year) & (merged_df['month'] == 1) & (
                                    merged_df['Run_Number'] == rn) & (merged_df[self.sweep_id] == sweep),
                                          'Num_%s_Received_Severe_Treatment' % agelabel] - excess
                        merged_df.loc[(merged_df['year'] == self.start_year) & (merged_df['month'] == 1) & (
                                merged_df['Run_Number'] == rn) & (merged_df[
                                                                      self.sweep_id] == sweep), 'Num_%s_Received_Severe_Treatment' % agelabel] = \
                            merged_df.loc[(merged_df['year'] == self.start_year) & (merged_df['month'] == 1) & (
                                    merged_df['Run_Number'] == rn) & (merged_df[self.sweep_id] == sweep),
                                          'Num_%s_Received_Severe_Treatment' % agelabel] + excess
            merged_df['excess sev treat %s' % agelabel] = merged_df['Num_%s_Received_Severe_Treatment' % agelabel] - \
                                                          merged_df['num severe cases %s' % agelabel]
            merged_df.loc[
                merged_df['excess sev treat %s' % agelabel] > 0.5, 'Num_%s_Received_Severe_Treatment' % agelabel] = \
                merged_df.loc[merged_df['excess sev treat %s' % agelabel] > 0.5, 'num severe cases %s' % agelabel]

            del merged_df['num severe cases %s' % agelabel]
            del merged_df['excess sev treat %s' % agelabel]
            merged_df.to_csv(os.path.join(self.working_dir, self.expt_name,
                                          '%s_PfPR_ClinicalIncidence_severeTreatment.csv' % agelabel), index=False)


# MonthlyAgebinSevereTreatedAnalyzer
class MonthlyAgebinSevereTreatedAnalyzer(IAnalyzer):
    @classmethod
    def monthparser(self, x):
        if x == 0:
            return 12
        else:
            return datetime.datetime.strptime(str(x), '%j').month

    def __init__(self, expt_name, event_name='Received_Severe_Treatment', agebins=None,
                 sweep_variables=None, IP_variable=None, working_dir=".", start_year=2000, end_year=2020,
                 filter_exists=False):
        super(MonthlyAgebinSevereTreatedAnalyzer, self).__init__(working_dir=working_dir,
                                                                 filenames=["output/ReportEventRecorder.csv"]
                                                                 )
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.IP_variable = IP_variable
        self.event_name = event_name
        self.agebins = agebins or [2, 5, 10, 20, 100]
        self.expt_name = expt_name
        self.start_year = start_year
        self.end_year = end_year
        self.filter_exists = filter_exists

    def filter(self, simulation):
        if self.filter_exists:
            file = os.path.join(simulation.get_path(), self.filenames[0])
            return os.path.exists(file)
        else:
            return True

    def map(self, data, simulation):

        output_data = data[self.filenames[0]]
        output_data = output_data[output_data['Event_Name'] == self.event_name]

        simdata = pd.DataFrame()
        if len(output_data) > 0:  # there are events of this type
            output_data['Day'] = output_data['Time'] % 365
            output_data['month'] = output_data['Day'].apply(lambda x: self.monthparser((x + 1) % 365))
            output_data['year'] = output_data['Time'].apply(lambda x: int(x / 365) + self.start_year)
            output_data['age in years'] = output_data['Age'] / 365

            for i, agemax in enumerate(self.agebins):
                if i == 0:
                    agemin = 0
                else:
                    agemin = self.agebins[i - 1]

                d = output_data[(output_data['age in years'].between(agemin, agemax))]
                g = d.groupby(list(filter(None, ['year', 'month'] + [self.IP_variable])))['Event_Name'].agg(
                    len).reset_index()
                g = g.rename(columns={'Event_Name': 'Num_Received_Severe_Treatment'})
                if simdata.empty:
                    simdata = g
                    simdata['agebin'] = agemax
                else:
                    if not g.empty:
                        g['agebin'] = agemax
                        simdata = pd.concat([g, simdata])
                        simdata = simdata.fillna(0)

            for sweep_var in self.sweep_variables:
                if sweep_var in simulation.tags.keys():
                    try:
                        simdata[sweep_var] = simulation.tags[sweep_var]
                    except:
                        simdata[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
                elif sweep_var == 'Run_Number':
                    simdata[sweep_var] = 0
        else:
            simdata = pd.DataFrame(
                columns=list(filter(None, ['year', 'month', 'agebin', 'Num_Received_Severe_Treatment'] +
                                    self.sweep_variables + [self.IP_variable])))
        return simdata

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("No data have been returned... Exiting...")
            return

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        adf = pd.concat(selected, sort=False).reset_index(drop=True)
        adf = adf.fillna(0)

        merged_df_all = pd.DataFrame()
        for i, agebin in enumerate(self.agebins):

            # Does not support IPfilter, currently also not needed
            if os.path.exists(os.path.join(self.working_dir, 'Agebin_PfPR_ClinicalIncidence.csv')):
                severe_treat_df = adf[
                    ['year', 'month', 'agebin', 'Num_Received_Severe_Treatment'] + self.sweep_variables]
                severe_treat_df = severe_treat_df[(severe_treat_df['agebin'] == agebin)]
                # cast to int65 data type for merge with incidence df
                severe_treat_df = severe_treat_df.astype({'month': 'int64', 'year': 'int64', 'Run_Number': 'int64'})

                # combine with existing columns of the clinical incidence and PfPR dataframe
                incidence_df = pd.read_csv(
                    os.path.join(self.working_dir, f'{self.agebin_name}_PfPR_ClinicalIncidence.csv'))
                incidence_df = incidence_df[(incidence_df['agebin'] == agebin)]
                merged_df = pd.merge(left=incidence_df, right=severe_treat_df,
                                     on=self.sweep_variables + ['year', 'month', 'agebin'],
                                     how='left')
                merged_df = merged_df.fillna(0)

                # fix any excess treated cases!
                merged_df['num severe cases'] = merged_df['Severe cases'] * merged_df['Pop'] * 30 / 365
                merged_df['excess sev treat'] = merged_df['Num_Received_Severe_Treatment'] - merged_df[
                    'num severe cases']
                merged_df['sweep_id'] = merged_df.groupby(self.sweep_variables, sort=False).ngroup().apply(
                    '{:010}'.format)

                for (rn, sweep), rdf in merged_df.groupby(['Run_Number', 'sweep_id']):
                    for r, row in rdf.iterrows():
                        if row['excess sev treat'] < 1:
                            continue
                        # fix Jan 2020 (start of sim) excess treated severe cases
                        if row['year'] == self.start_year and row['month'] == 1:
                            merged_df.loc[(merged_df['year'] == self.start_year) & (merged_df['month'] == 1) & (
                                    merged_df['Run_Number'] == rn) & (merged_df['sweep_id'] == sweep),
                                          'Num_Received_Severe_Treatment'] = np.sum(
                                merged_df[(merged_df['year'] == self.start_year) &
                                          (merged_df['month'] == 1) &
                                          (merged_df['Run_Number'] == rn) &
                                          (merged_df['sweep_id'] == sweep)]['num severe cases'])
                        else:
                            # figure out which is previous month
                            newyear = row['year']
                            newmonth = row['month'] - 1
                            if newmonth < 1:
                                newyear -= 1
                            excess = row['excess sev treat']
                            merged_df.loc[(merged_df['year'] == self.start_year) & (merged_df['month'] == 1) & (
                                    merged_df['Run_Number'] == rn) & (merged_df[
                                                                          'sweep_id'] == sweep), 'Num_Received_Severe_Treatment'] = \
                                merged_df.loc[(merged_df['year'] == self.start_year) & (merged_df['month'] == 1) & (
                                        merged_df['Run_Number'] == rn) & (merged_df['sweep_id'] == sweep),
                                              'Num_Received_Severe_Treatment'] - excess
                            merged_df.loc[(merged_df['year'] == self.start_year) & (merged_df['month'] == 1) & (
                                    merged_df['Run_Number'] == rn) & (merged_df[
                                                                          'sweep_id'] == sweep), 'Num_Received_Severe_Treatment'] = \
                                merged_df.loc[(merged_df['year'] == self.start_year) & (merged_df['month'] == 1) & (
                                        merged_df['Run_Number'] == rn) & (merged_df['sweep_id'] == sweep),
                                              'Num_Received_Severe_Treatment'] + excess
                merged_df['excess sev treat'] = merged_df['Num_Received_Severe_Treatment'] - \
                                                merged_df['num severe cases']
                merged_df.loc[
                    merged_df['excess sev treat'] > 0.5, 'Num_Received_Severe_Treatment'] = \
                    merged_df.loc[merged_df['excess sev treat'] > 0.5, 'num severe cases']

                del merged_df['num severe cases']
                del merged_df['excess sev treat']
                if merged_df_all.empty:
                    merged_df_all = merged_df
                else:
                    merged_df_all = pd.concat([merged_df_all, merged_df])
            else:
                pass
        merged_df_all.to_csv(os.path.join(self.working_dir, self.expt_name,
                                          'Agebin_PfPR_ClinicalIncidence_severeTreatment.csv'),
                             index=False)


"""
With IP filter
"""


class MonthlyPfPRAnalyzerU5IP(IAnalyzer):

    def __init__(self, expt_name, sweep_variables=None, working_dir='./', start_year=2020, end_year=2023,
                 burnin=None, filter_exists=False, ipfilter=''):

        super(MonthlyPfPRAnalyzerU5IP, self).__init__(working_dir=working_dir,
                                                    filenames=[
                                                        f"output/MalariaSummaryReport_Monthly_U5{ipfilter}_{x}.json"
                                                        for x in range(start_year, end_year)]
                                                    )
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.expt_name = expt_name
        self.start_year = start_year
        self.end_year = end_year
        self.burnin = burnin
        self.filter_exists = filter_exists
        self.ipfilter = ipfilter

    def filter(self, simulation):
        if self.filter_exists:
            file = os.path.join(simulation.get_path(), self.filenames[0])
            return os.path.exists(file)
        else:
            return True

    def map(self, data, simulation):

        adf = pd.DataFrame()
        for year, fname in zip(range(self.start_year, self.end_year), self.filenames):
            d = data[fname]['DataByTimeAndAgeBins']['PfPR by Age Bin'][:12]
            pfpr = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin'][:12]
            clinical_cases = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Annual Severe Incidence by Age Bin'][:12]
            severe_cases = [x[1] for x in d]
            d = data[fname]['DataByTimeAndAgeBins']['Average Population by Age Bin'][:12]
            pop = [x[1] for x in d]
            d = data[fname]['DataByTime']['PfPR_2to10'][:12]
            PfPR_2to10 = d
            d = data[fname]['DataByTime']['Annual EIR'][:12]
            annualeir = d
            simdata = pd.DataFrame({'month': range(1, 13),
                                    'PfPR U5': pfpr,
                                    'Cases U5': clinical_cases,
                                    'Severe cases U5': severe_cases,
                                    'Pop U5': pop,
                                    'PfPR_2to10': PfPR_2to10,
                                    'annualeir': annualeir})
            simdata['year'] = year
            adf = pd.concat([adf, simdata])

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    adf[sweep_var] = simulation.tags[sweep_var]
                except:
                    adf[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])
            elif sweep_var == 'Run_Number':
                adf[sweep_var] = 0

        return adf

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("\nWarning: No data have been returned... Exiting...")
            return

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        adf = pd.concat(selected).reset_index(drop=True)
        if self.burnin is not None:
            adf = adf[adf['year'] > self.start_year + self.burnin]
        adf.to_csv((os.path.join(self.working_dir, self.expt_name, f'U5{self.ipfilter}_PfPR_ClinicalIncidence.csv')), index=False)


class MonthlyAgebinPfPRAnalyzerIP(IAnalyzer):

    def __init__(self, expt_name, sweep_variables=None, working_dir='./', start_year=2020,
                 end_year=2023, ipfilter='',
                 burnin=None, filter_exists=False):

        super(MonthlyAgebinPfPRAnalyzerIP, self).__init__(working_dir=working_dir,
                                                          filenames=[
                                                              f"output/MalariaSummaryReport_Monthly_Agebin{ipfilter}_{x}.json"
                                                              for x in range(start_year, end_year)]
                                                          )
        self.sweep_variables = sweep_variables or ["Run_Number"]
        self.expt_name = expt_name
        self.start_year = start_year
        self.end_year = end_year
        self.burnin = burnin
        self.filter_exists = filter_exists
        self.ipfilter = ipfilter

    def filter(self, simulation):
        if self.filter_exists:
            file = os.path.join(simulation.get_path(), self.filenames[0])
            return os.path.exists(file)
        else:
            return True

    def map(self, data, simulation):

        adf = pd.DataFrame()
        for year, fname in zip(range(self.start_year, self.end_year), self.filenames):

            age_bins = data[fname]['Metadata']['Age Bins']

            for age in list(range(0, len(age_bins))):
                d = data[fname]['DataByTimeAndAgeBins']['PfPR by Age Bin'][:12]
                pfpr = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin'][:12]
                clinical_cases = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Annual Severe Incidence by Age Bin'][:12]
                severe_cases = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Annual Mild Anemia by Age Bin'][:12]
                mild_anaemia = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Annual Moderate Anemia by Age Bin'][:12]
                moderate_anaemia = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Annual Severe Anemia by Age Bin'][:12]
                severe_anaemia = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Average Population by Age Bin'][:12]
                pop = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['New Infections by Age Bin'][:12]
                new_infect = [x[age] for x in d]
                d = data[fname]['DataByTimeAndAgeBins']['Mean Log Parasite Density by Age Bin'][:12]
                log_parasite_density = [x[age] for x in d]

                simdata = pd.DataFrame({'month': range(1, 13),
                                        'PfPR': pfpr,
                                        'Cases': clinical_cases,
                                        'Severe cases': severe_cases,
                                        'Mild anaemia': mild_anaemia,
                                        'Moderate anaemia': moderate_anaemia,
                                        'Severe anaemia': severe_anaemia,
                                        'New infections': new_infect,
                                        'Mean Log Parasite Density': log_parasite_density,
                                        'Pop': pop})
                simdata['year'] = year
                simdata['agebin'] = age_bins[age]
                adf = pd.concat([adf, simdata])

        for sweep_var in self.sweep_variables:
            if sweep_var in simulation.tags.keys():
                try:
                    adf[sweep_var] = simulation.tags[sweep_var]
                except:
                    adf[sweep_var] = '-'.join([str(x) for x in simulation.tags[sweep_var]])

        return adf

    def reduce(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("\nWarning: No data have been returned... Exiting...")
            return
        df = pd.concat(selected).reset_index(drop=True)

        if not os.path.exists(os.path.join(self.working_dir, self.expt_name)):
            os.mkdir(os.path.join(self.working_dir, self.expt_name))

        print(f'\nSaving outputs to: {os.path.join(self.working_dir, self.expt_name)}')

        if self.burnin is not None:
            df = df[df['year'] > self.start_year + self.burnin]
        df = df.loc[df['agebin'] < 100]  # less than 100 years
        df.to_csv((os.path.join(self.working_dir, self.expt_name, f'Agebin{self.ipfilter}_PfPR_ClinicalIncidence.csv')),
                  index=False)
