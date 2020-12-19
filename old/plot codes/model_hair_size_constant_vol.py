import seaborn as sns
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib import rc
from datetime import datetime

matplotlib.use('Qt5Agg')

##sns.set(rc={'figure.figsize':(15,7)})
sns.set_theme(context = 'talk',
              style="ticks")
fig_size = (11,6) #figure size
plot_name = "Figure10-Effect_of_hair_size_constant_volume"
save = False #change to False if dont want to save
zero_line = True #set True for dashed zero line in plot
folderPath = 'E:/Work/Surface Evolver/Data/Bubble_Bridge/20201123 constant total fluid volume/'
dataPath = folderPath + 'summary_data_constant_vol.xlsx'

modelData = pd.read_excel(dataPath) # Load dataset

column_list = list(modelData.columns)
##['Distance', 'Force_hair_air', 'Force_hair_water', 'Force (hair)',
##       'Bubble', 'Underwater: Bubble', 'Air', 'Underwater: Wet',
##       'Bubble Contact Area', 'Pad  area', 'Hair Area', 'Contact Angle',
##       'θ-fa', 'θ-fw', 'D_p/D_h', 'a_b', 'a_f', 'Packing fraction',
##       'Aspect Ratio', 'Hair dia', 'Pad dia', 'Number of hairs', 'Hair length',
##       'γ-fa', 'γ-wa', 'γ-fw', 's-f', 's-b', 'Vf', 'Vb', 'Fluid data file',
##       'Bubble data file']

#force variables in data (used to convert data to long form)
force_vars = ['Force_hair_air', 'Force_hair_water', 'Force (hair)',
              'Bubble only', 'Underwater: Bubble', 'Air', 'Underwater: Wet']
#forces to include in plot
force_order = ['Air','Underwater: Wet','Underwater: Bubble', 'Bubble only']#['Air','Underwater: Wet','Underwater: Bubble','Bubble only']
color_list = ['g', 'b', 'r', 'r']#['g', 'b', 'r', 'c'] #corresponding colors
fix_marker = None #set to 'o' if style_param is None else set as None
line_styles = [(1, 0), (1, 0), (1, 0), (1, 1)]#[(1, 0), (1, 1)] #set True if line style needs to be changed by default. or include style as list of tuples {on, off) eg. (1,0): solid, (1,1):dotted

x_param = "Hair dia"
x_label = r'Hair diameter, $D_h/D_p$'
y_param = "Force"
y_label = r"Force, $F/\gamma D_p$"
hue_param = "Model" #"Model"
hue_param_order = force_order #set to force_order to show multiple forces in color, else set to None for single force
style_param = 'Model'
style_param_order = force_order
col_param = "Contact Angle"
col_param_order = ['24°','120°']
#set to None if dont want to group and find Max
##group_param = None
group_param = ['Model', 'Contact Angle', 'θ-fa', 'θ-fw',
               'D_p/D_h', 'a_b', 'a_f', 'Fluid data file',
               'Bubble data file'] 
fixed_param = {'a_b' : [1.5]} #fixed parameters in order of textbox display
#create latex formatted mapping for relevant column names for plot display
#change this to alter displayed parameter text
latex_map = {'D_p/D_h' : r'D_p/D_h',
             'a_b' : r'\phi_b',
             'Pad dia': r'D_p'}
##latex_map = {'D_p/D_h' : r'\frac{D_p}{D_h}',
##             'a_b' : r'\phi_b'} 


#textbox text in latex format
fixed_param_text = r' \\ '.join([latex_map[x] + '&=&' +
                                 ','.join(map(str,fixed_param[x]))
                              for x in fixed_param.keys()])


#include degree sign to contact angle
modelData['Contact Angle'] = modelData['Contact Angle'].astype(str) + '°'

#filter data based on fixed parameters
for param in fixed_param.keys():
    modelData = modelData[modelData[param].isin(fixed_param[param])]

#reshape force data into long form based on force_vars
id_vars_list = [x for x in column_list if x not in force_vars]
data_reshaped = pd.melt(modelData,
                        id_vars = id_vars_list,
                        var_name="Model",
                        value_name="Force")

#filter data
data_filtered = data_reshaped[data_reshaped['Model'].
                              isin(force_order)]


#group data (find maxima)
if group_param != None:
##    group_list = list(data_filtered.columns)
##    group_list.remove(group_param)
##    group_list.remove(y_param)
    data_grouped = data_filtered.groupby(group_param).min().reset_index()
##    data_grouped['Force'] *= -1 #inverse sign for plotting max force
else:
    data_grouped = data_filtered

#normalize w.r.t pad dia
data_grouped['Force'] = data_grouped['Force']/data_grouped['Pad dia']
data_grouped['Hair dia'] = data_grouped['Hair dia']/data_grouped['Pad dia']

# Draw a nested boxplot to show bills by day and time
ax = sns.relplot(data=data_grouped,
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
                 alpha = 0.8,
                 facet_kws={"legend_out": True})

(ax.map(plt.axhline, y=0, color=".7", dashes=(2, 1), zorder=0)
     .set_axis_labels(x_label, y_label)
  .tight_layout(w_pad=0))

fig = ax.fig

#legend adjust
col_num = 2 #number of legend columns SET
handles, labels = ax.axes[0][0].get_legend_handles_labels()
leg = ax._legend
##leg_bbox = leg.get_tightbbox(fig.canvas.get_renderer())
##x0, y0, w, h = leg_bbox.inverse_transformed(fig.transFigure).bounds
##w = w/col_num
##h = h/col_num

leg.remove()
fig.tight_layout()

leg = plt.legend(handles, labels, ncol = col_num,
                 framealpha = 0)
#rename legend text based on latex_map 
##for text in leg.texts:
##    if text.get_text() in latex_map.keys():
##        text.set_text('$' + latex_map[text.get_text()] + '$')
        
leg_bbox = leg.get_tightbbox(fig.canvas.get_renderer())
x0, y0, w, h = leg_bbox.inverse_transformed(fig.transFigure).bounds
##w = w/col_num
##h = h/col_num
bbox = (-w, -h, 1 + 2 * w, 1 +  2 * h)
leg.set_bbox_to_anchor(bbox, transform = fig.transFigure)
leg._loc = 8 #legend location SET

##'best'    0
##'upper right' 1
##'upper left' 	2
##'lower left' 	3
##'lower right' 4
##'right'   5
##'center left' 6
##'center right'    7
##'lower center'    8
##'upper center'    9
##'center'  10

#draw textbox of fixed parameters
rc('font',**{'serif':['Times']})
rc('text', usetex=True)

##r"\frac{D}{d}&=&50\\ \phi_b&=&0.5"
text = r"\begin{eqnarray*}" + fixed_param_text + r"\end{eqnarray*}"
anc = AnchoredText(text, loc="lower left", frameon=True,
                   bbox_to_anchor= (0,-h),
                   bbox_transform=ax.fig.transFigure)
##anc.patch.set_alpha(0)
##anc.patch.set_edgecolor('k')
ax.fig.add_artist(anc)
#SET bbox_to_anchor accordingly!

#format plot
ax.fig.set_size_inches(*fig_size)
##(ax.map(plt.axhline, y=0, color=".7", dashes=(2, 1), zorder=0)
##     .set_axis_labels(x_label, y_label)
##  .tight_layout(w_pad=0))
##if zero_line == True:
##    ax.map(plt.axhline, y=0, color=".7", dashes=(2, 1), zorder=0)


##ax.set_axis_labels(x_label, y_label)
##leg = ax._legend
##leg.set_bbox_to_anchor([0.95,0.5])
##
##ax.tight_layout(w_pad=0)
##ax.fig.tight_layout()

##sns.despine(offset=10, trim=True)

plt.show()

if save == True:
    timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
    fig = ax.fig
    fig.savefig(plot_name + "-" + timestamp + ".svg",
                bbox_inches='tight', transparent = True)
