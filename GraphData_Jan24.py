#GraphData_Jan24.py
import pandas as pd
import sys
import numpy as np
from matplotlib import pyplot as plt
import os
import json


def main():
   print("Hello from GraphData_Jan24.py")
   df_directory = 'CSVs'
   df_filename = 'ftof.csv'
   df_filepath = os.path.join(r'C:\Users\zisha\SynologyDrive\Drive\Tkinter_GUI', df_filename)
   #df_filepath = os.path.join(df_directory, df_filename)
   #df_filepath = r'C:\Users\zisha\SynologyDrive\Drive\Tkinter_GUI'
   #df_all = pd.read_csv(df_filepath)

    #test
   df_filename = 'rga_all.csv'
   df_filepath = (r'C:\Users\zisha\SynologyDrive\Drive\Tkinter_GUI', df_filename)


   df_all = pd.read_csv(df_filepath)
   run_number = sys.argv[1]
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


    #    if overlay_sectors:
    #        sector_groups = [sectors]
    #    else:
    #        sector_groups = [[sector] for sector in sectors]


    #    if overlay_topologies:
    #        topology_groups = [topologies]
    #    else:
    #        topology_groups = [[topology] for topology in topologies]


    #    if overlay_layers:
    #        layer_groups = [layers]
    #    else:
    #        layer_groups = [[layer] for layer in layers]


       sector_groups = [[sector] for sector in sectors]
       topology_groups = [[topology] for topology in topologies]
       layer_groups = [[layer] for layer in layers]



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
                   pdf_directory = 'PDFs'
                   sector_str = f"Sectors [{','.join(map(str, sector_group))}]"
                   layer_str = f"Layers [{','.join(map(str, layer_group))}]"
                   topology_str = f"Topologies [{','.join(map(str, topology_group))}]"
                   pdf_filename = f"{sector_str}; {layer_str}; {topology_str}; Run Number {run_number}.pdf"


                   file_path = os.path.join(pdf_directory, pdf_filename)
                   print(file_path + " created")
                   plt.savefig(file_path, format='pdf')


   make_graphs(sectors, topologies, layers)


if __name__ == "__main__":
   main()

#    def make_graphs(sectors, topologies, layers):
#        color_num = 0
#        color_list = ['blue', 'red', 'green', 'black', 'magenta', 'yellow']
#        for sector in sectors:
#            for topology in topologies:
#                for layer in layers:
#                    # creating plot
#                    df_sector_filtered = df_all[df_all['sector'] == sector]
#                    df_filtered = df_sector_filtered[df_sector_filtered['layer'] == layer]
#                    plt.scatter(
#                        df_filtered['paddle'],
#                        df_filtered[f'ef_{topology}'],
#                        color=color_list[color_num % len(color_list)],
#                        label=f'Sector {sector}',
#                        s=25
#                    )
#                    # y error bar
#                    plt.errorbar(
#                        df_filtered['paddle'],
#                        df_filtered[f'ef_{topology}'],
#                        yerr=df_filtered[f'variance_{topology}'],
#                        fmt='None',
#                        ecolor=color_list[color_num],
#                        elinewidth=2,
#                        capsize=3,
#                        capthick=2
#                    )
#                    color_num += 1


#        # plt.show()
#        plt.xlabel('Paddle #')
#        plt.ylabel('Efficiency')
#        plt.title(f'Sectors {sectors}; Layers {layers}; Topologies {topologies}; Run Number {run_number}')
#        plt.legend(loc='best')
#        pdf_directory = r'C:\Users\zisha\SynologyDrive\Drive\Tkinter_GUI\PDFs'
#        pdf_filename = f'Sectors {sectors}; Layers {layers}; Topologies {topologies}; Run Number {run_number}.pdf'
#        file_path = os.path.join(pdf_directory, pdf_filename)
#     #    os.makedirs(pdf_directory, exist_ok=True)
#     #    try:
#     #        plt.savefig(file_path, format='pdf')
#     #    except Exception as e:
#     #        print("Error saving PDF:", e)
#        plt.savefig(file_path, format='pdf')



#    make_graphs(sectors, topologies, layers)


# if __name__ == "__main__":
#    main()