#MakeData_Jan24.py
import pandas as pd
import sys
import numpy as np
import os
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get('FTOF_DATA_DIR', os.path.join(BASE_DIR, 'CSV'))
OUTPUT_DIR = os.environ.get('FTOF_OUTPUT_DIR', os.path.join(BASE_DIR, 'output'))


def find_run_file(run_number):
   # Per-run inputs live two levels down, e.g. CSV/RGA/Inbending/ftof_eff_5032.csv
   matches = sorted(glob.glob(os.path.join(DATA_DIR, '*', '*', f'ftof_eff_{run_number}.csv')))
   if not matches:
       sys.exit(f'No input file ftof_eff_{run_number}.csv found under {DATA_DIR}')
   return matches[0]


def main():
   run_number = sys.argv[1]
   input_path = find_run_file(run_number)
   print(f'Reading {input_path}')
   df = pd.read_csv(input_path)



   dfs = []
   for i in range(1, 6):
       df1 = df[df['topology'] == i]
       df1 = df1.copy(deep=True)
       df1 = df1.drop(['topology'], axis=1)
       dfs.append(df1)


   # now we have a list with 5 dfs.
   # merge them
   df_all = dfs[0].copy(deep=True)
   merge_cols = df_all.columns
   merge_cols = merge_cols.drop('should')
   merge_cols = list(merge_cols.drop('did'))
   for index, adf in enumerate(dfs[1:]):
       df_all = pd.merge(left=df_all, right=adf,
                         left_on=merge_cols, right_on=merge_cols,
                         suffixes=[None, f'_{index + 2}'])


   df_all['should_1'] = df_all['should']
   df_all['did_1'] = df_all['did']
   df_all = df_all.drop(['should', 'did'], axis=1)


   for num in range(1, 6):
       #creating efficiency columns
       df_all['ef_' + str(num)] = np.where(df_all[f'should_{num}'] != 0,
                                               df_all[f'did_{num}'] / df_all[f'should_{num}'],
                                               0)


   def calculate_variance(row, num):
       should = row[f'should_{num}']
       did = row[f'did_{num}']
       ef = row[f'ef_{num}']


       if should == did and should != 0 and did != 0:
           return ((did - 1) / should) * (1 - ((did - 1) / should)) / should
       elif did == 0 and should != 0:
           return ((did + 1) / should) * (1 - ((did + 1) / should)) / should
       elif should != 0:
           return ef * (1 - ef) / should
       else:
           return


   for num in range(1, 6):
       df_all[f'variance_{num}'] = df_all.apply(calculate_variance, axis=1, num=num)


   df_all = df_all[['run', 'sector', 'layer', 'paddle', 'distance', 'should_1', 'did_1', 'ef_1', 'variance_1',
                    'should_2','did_2', 'ef_2', 'variance_2', 'should_3', 'did_3', 'ef_3', 'variance_3',
                    'should_4', 'did_4', 'ef_4', 'variance_4', 'should_5', 'did_5', 'ef_5', 'variance_5']]


   os.makedirs(OUTPUT_DIR, exist_ok=True)
   df_filepath = os.path.join(OUTPUT_DIR, f'ftof_eff_{run_number}_wide.csv')
   df_all.to_csv(df_filepath, index=False)
   print(f'Wrote {df_filepath}')


if __name__ == "__main__":
   main()
