#GraphData_Jan24.py
import pandas as pd
import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.environ.get('FTOF_OUTPUT_DIR', os.path.join(BASE_DIR, 'output'))
PDF_DIR = os.environ.get('FTOF_PDF_DIR', os.path.join(BASE_DIR, 'PDFs'))


def main():
   run_number = sys.argv[1]
   # Expects the wide file written by MakeData_Jan24.py for this run
   df_filepath = os.path.join(OUTPUT_DIR, f'ftof_eff_{run_number}_wide.csv')
   if not os.path.exists(df_filepath):
       sys.exit(f'{df_filepath} not found; run MakeData_Jan24.py {run_number} first')
   df_all = pd.read_csv(df_filepath)
   ser_sectors = sys.argv[2]
   ser_layers = sys.argv[3]
   ser_topologies = sys.argv[4]
   sectors = json.loads(ser_sectors)
   layers = json.loads(ser_layers)
   topologies = json.loads(ser_topologies)

   if sys.argv[5] == "True":
       overlay_sectors = True
   else:
       overlay_sectors = False
   if sys.argv[6] == "True":
       overlay_layers = True
   else:
       overlay_layers = False
   if sys.argv[7] == "True":
       overlay_topologies = True
   else:
       overlay_topologies = False
   sectors = json.loads(ser_sectors)
   layers = json.loads(ser_layers)
   topologies = json.loads(ser_topologies)


   def make_graphs(sectors, topologies, layers):
       color_list = ['blue', 'red', 'green', 'black', 'magenta', 'yellow']
       color_num = 0


       if overlay_sectors:
           sector_groups = [sectors]
       else:
           sector_groups = [[sector] for sector in sectors]


       if overlay_topologies:
           topology_groups = [topologies]
       else:
           topology_groups = [[topology] for topology in topologies]


       if overlay_layers:
           layer_groups = [layers]
       else:
           layer_groups = [[layer] for layer in layers]

       os.makedirs(PDF_DIR, exist_ok=True)

       for sector_group in sector_groups:
           for topology_group in topology_groups:
               for layer_group in layer_groups:
                   plt.figure()
                   color_num = 0


                   for sector in sector_group:
                       for topology in topology_group:
                           for layer in layer_group:
                               df_filtered = df_all[
                                   (df_all['sector'] == sector) &
                                   (df_all['layer'] == layer)
                                   ]


                               #Creating scatterplot
                               plt.scatter(
                                   df_filtered['paddle'],
                                   df_filtered[f'ef_{topology}'],
                                   color=color_list[color_num % len(color_list)],
                                   label=f"Sector {sector}, Layer {layer}, Topology {topology}",
                                   s=25
                               )
                               #Creating error bars with variance in dataframe
                               plt.errorbar(
                                   df_filtered['paddle'],
                                   df_filtered[f'ef_{topology}'],
                                   yerr=df_filtered[f'variance_{topology}'],
                                   fmt='None',
                                   ecolor=color_list[color_num % len(color_list)],
                                   elinewidth=2,
                                   capsize=3,
                                   capthick=2
                               )
                               color_num += 1


                   #Adding labels & legend
                   plt.xlabel('Paddle #')
                   plt.ylabel('Efficiency')
                   title = f"Sectors {sector_group}; Layers {layer_group}; Topologies {topology_group}; Run Number {run_number}"
                   plt.title(title)
                   plt.legend(loc='best')


                   #Saving & naming plot
                   sector_str = f"Sectors [{','.join(map(str, sector_group))}]"
                   layer_str = f"Layers [{','.join(map(str, layer_group))}]"
                   topology_str = f"Topologies [{','.join(map(str, topology_group))}]"
                   pdf_filename = f"{sector_str}; {layer_str}; {topology_str}; Run Number {run_number}.pdf"


                   file_path = os.path.join(PDF_DIR, pdf_filename)
                   plt.savefig(file_path, format='pdf')
                   plt.close()
                   print(file_path + " created")


   make_graphs(sectors, topologies, layers)


if __name__ == "__main__":
   main()
