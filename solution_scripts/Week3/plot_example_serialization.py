import os
import datetime
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import seaborn as sns

import manifest

mpl.rcParams['pdf.fonttype'] = 42
palette = sns.color_palette("tab10")


def plot_inset_chart(expt_name_burnin, expt_name_pickup, channels_inset_chart, sweep_variables, serialize_years):
    # read in analyzed InsetChart data

    df_burnin = pd.read_csv(os.path.join(working_dir, expt_name_burnin, 'All_Age_InsetChart.csv'))
    df_burnin['date'] = pd.to_datetime(df_burnin['date'])
    df_burnin = df_burnin.groupby(['date'])[channels_inset_chart].agg(np.mean).reset_index()

    df_pickup = pd.read_csv(os.path.join(working_dir, expt_name_pickup, 'All_Age_InsetChart.csv'))
    df_pickup['date'] = pd.to_datetime(df_pickup['date'])
    df_pickup = df_pickup.groupby(['date'] + sweep_variables)[channels_inset_chart].agg(np.mean).reset_index()

    # make InsetChart plot
    fig1 = plt.figure('InsetChart', figsize=(12, 6))
    fig1.subplots_adjust(hspace=0.5, left=0.08, right=0.97)
    fig1.suptitle(f'Time-series with {serialize_years} years of burnin')
    axes = [fig1.add_subplot(2, 2, x + 1) for x in range(4)]
    for ch, channel in enumerate(channels_inset_chart):
        ax = axes[ch]

        if channel == 'PfHRP2 Prevalence':
            ax.set_ylim(0, 1)
        else:
            ax.set_ylim(0, 1.1 * np.max(df_burnin[channel]))

        ax.plot(df_burnin['date'], df_burnin[channel], '-', linewidth=0.8, color='#5c5859')

        for p, pdf in df_pickup.groupby(sweep_variables):
            ax.plot(pdf['date'], pdf[channel], '-', linewidth=0.8, label=p)
        ax.set_title(channel)
        ax.set_ylabel(channel)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=36))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    axes[-1].legend(title=sweep_variables)
    fig1.savefig(os.path.join(working_dir, expt_name_pickup, f'InsetChart_withBurnin{serialize_years}.png'))

def plot_inset_chart_annual(expt_name_burnin, expt_name_pickup, channels_inset_chart, sweep_variables, serialize_years):
    # read in analyzed InsetChart data

    df_burnin = pd.read_csv(os.path.join(working_dir, expt_name_burnin, 'All_Age_InsetChart.csv'))
    df_burnin['date'] = pd.to_datetime(df_burnin['date'])
    df_burnin['year'] = df_burnin['date'].dt.year
    df_burnin = df_burnin.groupby(['year'])[channels_inset_chart].agg(np.mean).reset_index()

    df_pickup = pd.read_csv(os.path.join(working_dir, expt_name_pickup, 'All_Age_InsetChart.csv'))
    df_pickup['date'] = pd.to_datetime(df_pickup['date'])
    df_pickup['year'] = df_pickup['date'].dt.year
    df_pickup = df_pickup.groupby(['year'] + sweep_variables)[channels_inset_chart].agg(np.mean).reset_index()

    # make InsetChart plot
    fig2 = plt.figure('InsetChart', figsize=(12, 6))
    fig2.subplots_adjust(hspace=0.5, left=0.08, right=0.97)
    fig2.suptitle(f'Annual time-series with {serialize_years} years of burnin')
    axes = [fig2.add_subplot(2, 2, x + 1) for x in range(4)]
    for ch, channel in enumerate(channels_inset_chart):
        ax = axes[ch]

        if channel == 'PfHRP2 Prevalence':
            ax.set_ylim(0, 1)
        else:
            ax.set_ylim(0, 1.1 * np.max(df_burnin[channel]))

        ax.plot(df_burnin['year'], df_burnin[channel], '-', linewidth=0.8, color='#5c5859')

        for p, pdf in df_pickup.groupby(sweep_variables):
            pdf = pd.concat([df_burnin[df_burnin['year'] == np.max(df_burnin['year'])], pdf], sort=True)
            ax.plot(pdf['year'], pdf[channel], '-', linewidth=0.8, label=p)
        ax.set_title(channel)
        ax.set_ylabel(channel)
    axes[-1].legend(title=sweep_variables)
    fig2.savefig(os.path.join(working_dir, expt_name_pickup, f'Annual_InsetChart_withBurnin{serialize_years}.png'))


if __name__ == "__main__":
    user = os.getlogin()  # user initials
    expt_name_burnin = f'{user}_example_sim_burnin10'
    expt_name_pickup = f'{user}_example_sim_pickup'
    
    working_dir=os.path.join(manifest.job_directory, 'my_outputs')

    """Set sweep_variables and event_list as required depending on experiment"""
    sweep_variables = ['Run_Number']
    channels_inset_chart = ['Statistical Population', 'New Clinical Cases', 'Adult Vectors', 'Infected']

    """Generate plots"""
    serialize_years = 10  ## Update number of years burnin experiment was run, this number is added to the figure filename
    plot_inset_chart_annual(expt_name_burnin, expt_name_pickup, channels_inset_chart, sweep_variables, serialize_years)
    plt.clf()
    plot_inset_chart(expt_name_burnin, expt_name_pickup, channels_inset_chart, sweep_variables, serialize_years)