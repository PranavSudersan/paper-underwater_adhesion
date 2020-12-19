import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

plot_name = 'Figure-9-Gecko_comparison'
save = False

##sns.set(rc={'figure.figsize':(30,25)})
sns.set_theme(context = 'paper',style="ticks",
              palette="pastel", font_scale = 2)

#only 2 colors chosen
color_list = sns.color_palette('pastel')[:2] #['lightgreen', 'b']
color_list.reverse() #reversed so blue is for Wet

# Load experiment data
geckoData = pd.read_excel('E:/Work/Documents/paper-underwater_adhesion/Data/gecko_comparison.xlsx')

#filter based on substrates
geckoData = geckoData[(geckoData['Substrate'] == 'Glass') | True]#(geckoData['Substrate'] == 'PTFE')]


# Draw a nested boxplot to show bills by day and time
ax = sns.catplot(x='Substrate', y='Force',
                hue='Contact type', col = 'Source',
                kind = 'bar', data=geckoData,
                 palette = color_list)

ax.set(xlabel=None, ylabel='Force $[N]$')

#replace 'Source = ' from titles
axes = ax.axes.flatten()
for ax in axes:
    ax.set_title(ax.get_title().replace('Source = ', ''))

##ax.set_xticklabels(rotation=45,
##                   horizontalalignment='right')
##ax.tight_layout(w_pad=0)
##sns.despine(offset=10, trim=True)
##plt.tight_layout()
##plt.show()


#save data and plot
if save == True:
    fig = ax.figure
    timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
    fig.savefig(plot_name + "-" + timestamp + ".svg",
                bbox_inches = 'tight', transparent = True)

plt.show()

