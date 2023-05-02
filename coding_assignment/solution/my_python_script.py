import pandas as pd
import numpy as np
import os

data_path = 'project_dir/example_data/'
datasets = os.listdir(data_path)
output_path = 'project_dir/output_cleaned.csv'
output_df = pd.DataFrame()

for ds in datasets:
  #print((os.path.join(data_path,ds,'output.csv')))
  df= pd.read_csv((os.path.join(data_path,ds,'output.csv')))
  
  max_day = np.max(df['Day'])
  df = df[df['Day']> max_day-365]
  df = df[['Day','Site','Trial_Number','Arm','Var1','Var3']]
  output_df = pd.concat([output_df,df])
  
output_df.to_csv(output_path)
