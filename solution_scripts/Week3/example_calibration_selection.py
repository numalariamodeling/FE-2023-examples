import os

import pandas as pd
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from idmtools_calibra.utilities.ll_calculators import beta_binomial
import manifest

user = os.getlogin()  # user initials
expt_name = 'week3_calib'

jdir = manifest.job_directory
output_dir=os.path.join(jdir, 'my_outputs')

input_dir = manifest.input_dir
data_dir = os.path.join('data')

sim_pfpr_df = pd.read_csv(os.path.join(output_dir, expt_name, 'U5_PfPR_ClinicalIncidence.csv'))
sim_pfpr_df.columns = [col.replace(' U5', '') for col in sim_pfpr_df.columns]
sim_pfpr_df['npos'] = sim_pfpr_df['PfPR'] * sim_pfpr_df['Pop']
sim_pfpr_df['npos'] = sim_pfpr_df.npos.round(0)
dhs_pfpr_df = pd.read_csv(os.path.join(input_dir, 'fake_DHS_calib.csv'))
sweep_variables = ['x_Temporary_Larval_Habitat', 'Run_Number']


def score(sim_df, data_df, sweep_variables):
    uniq_df = sim_df.groupby(sweep_variables).size().reset_index(name='Freq')
    ll = []
    for r, row in uniq_df.iterrows():
        mask1 = sim_df[sweep_variables[0]] == row[sweep_variables[0]]
        mask2 = sim_df[sweep_variables[1]] == row[sweep_variables[1]]
        mask = mask1 & mask2
        sim_subset_df = sim_df[mask]

        comb_df = data_df.merge(sim_subset_df, on=['year', 'month'], how='left')
        ll = ll + [beta_binomial(comb_df.DHS_n, comb_df.Pop, comb_df.DHS_pos, comb_df.npos)]

    uniq_df['ll'] = ll

    score_df = uniq_df.groupby(['x_Temporary_Larval_Habitat'])['ll'].mean().reset_index(name='ll')
    return score_df


def plot_output(sim_df, data_df, score_df, variable):
    sim_df['date'] = pd.to_datetime([f'{y}-{m}-01' for y, m in zip(sim_df.year, sim_df.month)])
    data_df['date'] = pd.to_datetime([f'{y}-{m}-01' for y, m in zip(data_df.year, data_df.month)])
    data_df['PfPR'] = data_df['DHS_pos'] / data_df['DHS_n']
    sns.set_style('whitegrid', {'axes.linewidth': 0.5})
    fig = plt.figure(figsize=(12, 5))
    axes = [fig.add_subplot(1, 2, x + 1) for x in range(2)]

    candidate_val = score_df[variable]
    score_df1 = score_df[score_df.ll == max(score_df.ll)]
    print(score_df1)
    for cand in candidate_val:
        plot_df = sim_df[sim_df[variable] == cand]
        a = 1 if cand == score_df1[variable].max() else 0.15
        axes[0].plot(plot_df['date'], plot_df['PfPR'], color='#FF0000', alpha=a)

    axes[0].scatter(data_df['date'].values, data_df['PfPR'], data_df['DHS_n'], 'k')
    axes[0].set_ylabel('PfPR')
    axes[0].set_title('Observed vs Simulated (Dark red is the best fit)')

    
    axes[1].plot(score_df[variable], score_df['ll'], '-o', color='#FF0000', markersize=5)
    axes[1].scatter(score_df1[variable], score_df1.ll, s=90, color='red')
    axes[1].set_ylabel('log-likelihood')
    axes[1].set_xlabel('x_Temporary_Larval_Habitat')
    axes[1].set_title('Mean log-likelihood. Larger value = better fit')

    fig.savefig(os.path.join(output_dir, expt_name, 'selection.png'))


if __name__ == "__main__":
    scores = score(sim_pfpr_df, dhs_pfpr_df, sweep_variables)
    print(scores)

    sim_pfpr_agg = sim_pfpr_df.groupby(['year', 'month', 'x_Temporary_Larval_Habitat'])['PfPR'].mean().reset_index(name='PfPR')
    plot_output(sim_pfpr_agg, dhs_pfpr_df, scores, 'x_Temporary_Larval_Habitat')