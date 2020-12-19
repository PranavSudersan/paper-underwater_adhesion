import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib import rc
from datetime import datetime

matplotlib.use('Qt5Agg')

##sns.set(rc={'figure.figsize':(15,7)})
sns.set_theme(context = 'talk',
              style="ticks",
              palette = sns.color_palette("hls", 4))
fig_size = (6,6) #figure size
plot_name = "Figure11-Effect of fluid volume"
save = False #change to False if dont want to save
zero_line = True #set True for dashed zero line in plot
folderPath = 'E:/Work/Surface Evolver/Data/Bubble_Bridge/20201123 constant total fluid volume/'
dataPath = folderPath + 'fluid_data_all.xlsx'

modelData = pd.read_excel(dataPath) # Load dataset

modelData.rename(columns={'Force': 'Force Deriv'}, inplace = True) #force from energy derivative
modelData.rename(columns={'Force_Calc': 'Total'}, inplace = True) #force from energy derivative
#include degree sign to contact angle
##modelData['Contact Angle'] = modelData['Bottom_Angle'].astype(str) + '°'

modelData['Contact Angle'] = (180-modelData['Bottom_Angle']).astype(str) + '°'
#non dimensionalize volume, length scale relative to pinned DIAMETER (factor of 2)
modelData['Fluid Volume'] = (4*np.pi/3)*((modelData['Pin_Radius']*2)**(-3))

#forces scale
modelData['Force Deriv'] *= 2*np.pi*modelData['Pin_Radius']*2
modelData['Total'] *= 2*np.pi*modelData['Pin_Radius']*2
modelData['Laplace'] = (modelData['Pressure'] - modelData['Ambient_Pressure']) * modelData['Bottom_Area']*modelData['Pin_Radius']*2
modelData['Surface Tension'] = -1 * modelData['Bottom_Length'] * np.sin(modelData['Bottom_Angle']*np.pi/180)*modelData['Pin_Radius']*2
##modelData['Force_Total'] = modelData['Force_Laplace'] + modelData['Force_Surface_Tension']

column_list = list(modelData.columns)
##['Bottom_Angle', 'Pin_Radius', 'Elastic_Modulus', 'Aspect_Ratio',
## 'Ambient_Pressure', 'Height', 'Base_Height', 'Height_Final',
## 'Strain', 'Force', 'Force_Calc', 'Energy', 'Area', 'Scale',
## 'Volume', 'Pressure', 'Bottom_Length', 'Top_Length', 'Bottom_Area',
## 'Top_Area', 'Mean_Curvature', 'Min_Radius', 'Max_Radius',
## 'Pinning_Angle', 'Iterations', 'Contact Angle', 'Force_Laplace',
## 'Force_Surface_Tension', 'Force_Total']
#group data based on these columns
group_vars = ['Bottom_Angle', 'Pin_Radius', 'Elastic_Modulus', 'Aspect_Ratio',
              'Ambient_Pressure']
#force variables in data (used to convert data to long form)
force_vars = ['Force Deriv', 'Total', 'Laplace',
              'Surface Tension']
#forces to include in plot
force_order = None#['Total', 'Laplace', 'Surface Tension']
color_list = None#['g', 'b', 'r', 'c'] #corresponding colors
fix_marker = None #set to 'o' if style_param is None else set as None
line_styles = False#[(1, 0), (1, 1)] #set True if line style needs to be changed by default. or include style as list of tuples {on, off) eg. (1,0): solid, (1,1):dotted
angle_order = ['1°','6°','50°','150°']

x_param = "Fluid Volume"
x_label = "Fluid Volume, $V_f/D^3$"
y_param = "Total"
y_label = r"Force, $F_{min}/\gamma D$"
hue_param = "Contact Angle" #"Model"
hue_param_order = angle_order #set to force_order to show multiple forces in color, else set to None for single force
style_param = 'Contact Angle'
style_param_order = angle_order
col_param = None
col_param_order = None
#set to None if dont want to group and find Max
group_param = None
##group_param = ['Model', 'Contact Angle', 'θ-fa', 'θ-fw',
##               'D_p/D_h', 'a_b', 'a_f', 'Fluid data file',
##               'Bubble data file'] 
##fixed_param = {'D_p/D_h' : [50],
##               'a_b' : [1.5]} #fixed parameters in order of textbox display
#create latex formatted mapping for relevant column names for plot display
#change this to alter displayed parameter text
##latex_map = {'D_p/D_h' : r'D_p/D_h',
##             'a_b' : r'\phi_b'}
##latex_map = {'D_p/D_h' : r'\frac{D_p}{D_h}',
##             'a_b' : r'\phi_b'} 


#textbox text in latex format
##fixed_param_text = r' \\ '.join([latex_map[x] + '&=&' +
##                                 ','.join(map(str,fixed_param[x]))
##                              for x in fixed_param.keys()])


###include degree sign to contact angle
##modelData['Contact Angle'] = modelData['Contact Angle'].astype(str) + '°'

###filter data based on fixed parameters
##for param in fixed_param.keys():
##    modelData = modelData[modelData[param].isin(fixed_param[param])]
##
#find minimum force based on Force_Calce and its corresponding values
modelData = modelData.loc[modelData.groupby(group_vars)["Total"].idxmin()]

###reshape force data into long form based on force_vars
##id_vars_list = [x for x in column_list if x not in force_vars]
##data_reshaped = pd.melt(modelData,
##                        id_vars = id_vars_list,
##                        var_name="Force",
##                        value_name="Force value")
##
###filter data
##data_filtered = data_reshaped[data_reshaped['Force'].
##                              isin(force_order)]
##
##
###group data (find maxima)
##if group_param != None:
####    group_list = list(data_filtered.columns)
####    group_list.remove(group_param)
####    group_list.remove(y_param)
##    data_grouped = data_filtered.groupby(group_param).min().reset_index()
####    data_grouped['Force'] *= -1 #inverse sign for plotting max force
##else:
##    data_grouped = data_filtered

# Draw a nested boxplot to show bills by day and time
ax = sns.relplot(data=modelData,
                 x = x_param,
                 y = y_param,
                 hue = hue_param,
                 hue_order = hue_param_order,
                 style = style_param,
                 style_order = style_param_order,
                 col = col_param,
                 col_order = col_param_order,
                 palette= color_list,
                 kind = 'line',
                 markers = True,
                 dashes = line_styles,
                 marker = fix_marker,
                 alpha = 0.8)

##if zero_line == True:
##    ax.map(plt.axhline, y=0, color=".7", dashes=(2, 1), zorder=0)

(ax.map(plt.axhline, y=0, color=".7", dashes=(2, 1), zorder=0)
     .set_axis_labels(x_label, y_label)
  .tight_layout(w_pad=0))

fig = ax.fig

#legend adjust
##col_num = 1
##handles, labels = ax.axes[0][0].get_legend_handles_labels()
##leg = ax._legend
##leg_bbox = leg.get_tightbbox(fig.canvas.get_renderer())
##x0, y0, w, h = leg_bbox.inverse_transformed(fig.transFigure).bounds
##w = w/col_num
##h = h/col_num
##
##leg.remove()
fig.tight_layout()
##
##plt.legend(handles, labels, bbox_to_anchor=(-w, -h, 1 + 2 * w, 1 +  2 * h),
##           loc='lower right', bbox_transform = fig.transFigure,
##           ncol = col_num)

#draw textbox of fixed parameters facet_kws={"legend_out": True} 
rc('font',**{'serif':['Times']})
##rc('text', usetex=True)

##r"\frac{D}{d}&=&50\\ \phi_b&=&0.5"
##text = r"\begin{eqnarray*}" + fixed_param_text + r"\end{eqnarray*}"
##anc = AnchoredText(text, loc="upper right", frameon=True,
##                   bbox_to_anchor=(0.9, 1.),
##                   bbox_transform=ax.fig.transFigure)
##ax.fig.add_artist(anc)

#format plot
ax.fig.set_size_inches(*fig_size)
##(ax.map(plt.axhline, y=0, color=".7", dashes=(2, 1), zorder=0)
##     .set_axis_labels(x_label, y_label)
##  .tight_layout(w_pad=0))


#rename legend text based on latex_map 
##for text in ax._legend.texts:
##    if text.get_text() in latex_map.keys():
##        text.set_text('$' + latex_map[text.get_text()] + '$')

##ax.set_axis_labels(x_label, y_label)
##leg = ax._legend
##leg.set_bbox_to_anchor([1,0.75])
##leg._loc = 8

##ax.tight_layout(w_pad=0)
##ax.fig.tight_layout()

##sns.despine(offset=10, trim=True)

plt.show()

if save == True:
    timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
    fig = ax.fig
    fig.savefig("Figure1-Force contribution-" + timestamp + ".svg",
                bbox_inches='tight', transparent = True)
