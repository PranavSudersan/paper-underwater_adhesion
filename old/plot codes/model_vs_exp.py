import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

sns.set(rc={'figure.figsize':(30,25)})
sns.set_theme(context = 'paper',style="ticks",
              palette="pastel", font_scale = 2)


# Load experiment data
exptData = pd.read_excel('E:/Work/Documents/paper-underwater_adhesion/Data/summary_20200911.xlsx', index_col=0)
exptData.rename(columns = {'Label': 'Contact type'}, inplace = True)
exptData = exptData[exptData["Contact type"] != "Ambiguous"]
exptData.replace({'Contact type': {'Dry': 'Air',
                                   'Bubble': 'Underwater: Bubble',
                                   'Wet': 'Underwater: Wet'}},
                 inplace = True)
exptData['Data'] = 'Experiment'
exptData_relevant = exptData[['Contact type',
                              'Adhesion_Force',
                              'Substrate',
                              'Data']].copy()

# Model data
folderPath = 'E:/Work/Surface Evolver/Data/Bubble_Bridge/20201020 ladybug data final/'
dataPath = folderPath + 'summary_data_final.xlsx'
modelData = pd.read_excel(dataPath)
modelData.rename(columns = {'Model': 'Contact type'}, inplace = True)
column_list = list(modelData.columns)
#force variables in data (used to convert data to long form)
force_vars = ['Force_hair_air', 'Force_hair_water', 'Force (hair)',
              'Bubble only', 'Underwater: Bubble', 'Air', 'Underwater: Wet']
#forces to include in plot
force_order = ['Air','Underwater: Wet','Underwater: Bubble']
group_param = ['Contact type', 'Contact Angle', 'θ-fa', 'θ-fw',
               'D_p/D_h', 'a_b', 'a_f', 'Fluid data file',
               'Bubble data file']

#reshape force data into long form based on force_vars
id_vars_list = [x for x in column_list if x not in force_vars]
data_reshaped = pd.melt(modelData,
                        id_vars = id_vars_list,
                        var_name="Contact type",
                        value_name="Adhesion_Force")

#filter data
data_filtered = data_reshaped[data_reshaped['Contact type'].
                              isin(force_order)]
#group data (find maxima)
data_grouped = data_filtered.groupby(group_param).min().reset_index()
data_grouped['Adhesion_Force'] *= -1000 #mN to uN convert (+ve convention)
#normalized adhesion calculation
data_grouped['Normalized_Adhesion_Force'] = data_grouped['Adhesion_Force']/\
                                            data_grouped['Hair Area']*1e-12

data_grouped['Substrate'] = np.where(data_grouped['Contact Angle']== 24,
                                     'Glass', 'PFOTS')
data_grouped['Data'] = 'Model'

modelData_relevant = data_grouped[['Contact type',
                                  'Adhesion_Force',
                                  'Substrate',
                                   'Data']].copy()

#append model and experiment data
dataCombined = exptData_relevant.append(modelData_relevant)


# Draw a nested boxplot to show bills by day and time
ax = sns.catplot(x='Contact type', y='Adhesion_Force',
                hue='Data', col = 'Substrate',
                kind = 'bar', data=dataCombined)

ax.set(xlabel=None, ylabel='Adhesion Force $[μN]$')

ax.set_xticklabels(rotation=45,
                   horizontalalignment='right')
##ax.tight_layout(w_pad=0)
##sns.despine(offset=10, trim=True)
##plt.tight_layout()
##plt.show()


#save data and plot
##timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
####dataCombined.to_excel("summary_statistics-" + timestamp + ".xlsx")
##fig = ax.fig
##fig.savefig("comparison_plot-" + timestamp + ".png", bbox_inches = 'tight',
##            transparent = True)

plt.show()

