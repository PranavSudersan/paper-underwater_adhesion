import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


get_stats = False #calculate statistics
save = False #save plot and statistics
plot_name = 'Figure5-Expt_Effect_of_contact'
contact_order = ['Air', 'Underwater: Bubble', 'Underwater: Wet', 'Bad Contact']

sns.set(rc={'figure.figsize':(14,10)})
sns.set_theme(context = 'paper',style="ticks",
              palette="pastel", font_scale = 2)

# Load experiment data
exptData = pd.read_excel('E:/Work/Documents/paper-underwater_adhesion/Data/summary_data_Effect of contact-201112145030.xlsx', index_col=0)
exptData.rename(columns = {'Pulloff Force': 'Adhesion_Force'}, inplace = True)
exptData.rename(columns = {'Contact Type': 'Contact_type'}, inplace = True)
##exptData = exptData[exptData["Contact type"] != "Ambiguous"] #filter out ambiguous data
exptData.replace({'Contact_type': {'Dry': 'Air',
                                   'Bubble': 'Underwater: Bubble',
                                   'Wet': 'Underwater: Wet',
                                   'Ambiguous': 'Bad Contact'}},
                 inplace = True)
exptData['Data'] = 'Experiment'
exptData_relevant = exptData[['Contact_type',
                              'Adhesion_Force',
                              'Substrate',
                              'Data']].copy()

# Model data
folderPath = 'E:/Work/Surface Evolver/Data/Bubble_Bridge/20201020 ladybug data final/'
dataPath = folderPath + 'summary_data_final.xlsx'
modelData = pd.read_excel(dataPath)
modelData.rename(columns = {'Model': 'Contact_type'}, inplace = True)
column_list = list(modelData.columns)
modelData = modelData[modelData['Hair dia'] == 4e-6] #filter hair diameter (4um)
#force variables in data (used to convert data to long form)
force_vars = ['Force_hair_air', 'Force_hair_water', 'Force (hair)',
              'Bubble only', 'Underwater: Bubble', 'Air', 'Underwater: Wet']
#forces to include in plot
force_order = ['Air','Underwater: Wet','Underwater: Bubble']
group_param = ['Contact_type', 'Contact Angle', 'θ-fa', 'θ-fw',
               'D_p/D_h', 'a_b', 'a_f', 'Fluid data file',
               'Bubble data file']

#reshape force data into long form based on force_vars
id_vars_list = [x for x in column_list if x not in force_vars]
data_reshaped = pd.melt(modelData,
                        id_vars = id_vars_list,
                        var_name="Contact_type",
                        value_name="Adhesion_Force")

#filter data
data_filtered = data_reshaped[data_reshaped['Contact_type'].
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

modelData_relevant = data_grouped[['Contact_type',
                                  'Adhesion_Force',
                                  'Substrate',
                                   'Data']].copy()

#append model and experiment data
dataCombined = exptData_relevant.append(modelData_relevant)

#Draw model prediction as stars
ax1 = sns.swarmplot(x='Contact_type', y='Adhesion_Force',
                hue='Substrate', order= contact_order,
                    dodge = True, marker = '*', edgecolor = 'k',linewidth=0.5,
                    size = 20, alpha = 0.8,
                data=dataCombined[dataCombined['Data'] == 'Model'])
##ax2.get_legend().remove()
legs1 = ax1.get_legend().texts
##print(legs1)

#Experimental data plot overlayed
ax2 = sns.boxplot(x='Contact_type', y='Adhesion_Force',
                hue='Substrate', order = contact_order,
                data=dataCombined[dataCombined['Data'] == 'Experiment'])

#clean up legend
handles, labels = ax2.get_legend_handles_labels()
l = plt.legend(handles[0:2], labels[0:2])

ax2.set(xlabel='Contact Type', ylabel='Adhesion Force $[μN]$')
##
##ax.set_xticklabels(rotation=45,
##                   horizontalalignment='right')
##ax.tight_layout(w_pad=0)
sns.despine(offset=10, trim=True)
##plt.tight_layout()
##plt.show()


#save data and plot
if save == True:
    timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
    fig = ax2.get_figure()
    fig.savefig(plot_name + "-" + timestamp + ".svg",
                bbox_inches = 'tight', transparent = True)

plt.show()

#########Statistical Analysis####################
##reference: https://reneshbedre.github.io/blog/anova.html
#IMPORTANT! requirements XlsxWriter==1.3.7, statsmodels==0.12.0

if get_stats == True:
    from pingouin import anova, normality, homoscedasticity, pairwise_tukey
##    import statsmodels.api as sm
##    from statsmodels.formula.api import ols
##    # Ordinary Least Squares (OLS) model
##    # C(Label):C(Substrate) represent interaction term
##    model = ols('Adhesion_Force ~ C(Contact_type) + C(Substrate) + C(Contact_type):C(Substrate)',
##                data=exptData).fit()
##    anova_table = sm.stats.anova_lm(model, typ=2)
##    print('ANOVA:\n', anova_table)

    #Two-way ANOVA test
    
##    from pingouin import anova
    aov = anova(data = exptData,
                dv="Adhesion_Force",
                between=["Contact_type", "Substrate"]).round(3)
    print('ANOVA:\n', aov)

    # Shapiro-Wilk test used to check the normal distribution of residuals

##    import scipy.stats as stats
##    w, pvalue = stats.shapiro(model.resid)
##    print('Shapiro-Wilk test:\n', w, pvalue)

##    from pingouin import normality
    norm_glass = normality(exptData[exptData['Substrate'] == 'Glass'],
                           dv='Adhesion_Force',
                           group='Contact_type',
                           method = 'shapiro').round(3)
    norm_glass['Substrate'] = 'Glass'
    print('Shapiro-Wilk test (glass):\n', norm_glass)
    norm_pfots = normality(exptData[exptData['Substrate'] == 'PFOTS'],
                           dv='Adhesion_Force',
                           group='Contact_type',
                           method = 'shapiro').round(3)
    norm_pfots['Substrate'] = 'PFOTS'
    print('Shapiro-Wilk test (PFOTS):\n', norm_pfots)

    norm_test = norm_glass.append(norm_pfots)
    
    #Bartlett’s test to check the Homogeneity of variances
    ##import scipy.stats as stats
    ##w, pvalue = stats.bartlett(d['A'], d['B'], d['C'], d['D'])
    ##print(w, pvalue)

    #Levene's/Bartlett’s Test to check equality of variance (levene or bartlett)
##    from pingouin import homoscedasticity
    lev_glass = homoscedasticity(exptData[exptData['Substrate'] == 'Glass'],
                           dv='Adhesion_Force',
                           group='Contact_type',
                           method = 'levene').round(3)
    lev_glass['Substrate'] = 'Glass'
    print('Levene Test (glass):\n', lev_glass)
    lev_pfots = homoscedasticity(exptData[exptData['Substrate'] == 'PFOTS'],
                           dv='Adhesion_Force',
                           group='Contact_type',
                           method = 'levene').round(3)
    lev_pfots['Substrate'] = 'PFOTS'
    print('Levene Test (PFOTS):\n', lev_pfots)

    var_eq_test = lev_glass.append(lev_pfots)

    # perform multiple pairwise comparison (Tukey HSD)
    # for unbalanced (unequal sample size) data, pairwise_tukey uses Tukey-Kramer test
##    from pingouin import pairwise_tukey
    
    statDf = pd.DataFrame()

    fixed_params = ["Substrate", "Contact_type"]
    i = 0
    for fixed in fixed_params:
        for val in exptData[fixed].unique():
            m_comp = pairwise_tukey(data=exptData[exptData[fixed] == val],
                                    dv= 'Adhesion_Force',
                                    between= fixed_params[i-1],
                                    effsize = 'r')
            m_comp['Fixed_Parameter'] = val
            statDf = statDf.append(m_comp).round(3)
    ##        print(m_comp)
        i += 1

    print(statDf[["Fixed_Parameter","A","B","T","p-tukey", "r"]])

    #save statistics
    if save == True:
        writer = pd.ExcelWriter("summary_statistics-" + timestamp + ".xlsx",
                                engine='xlsxwriter')
        statDf.to_excel(writer, sheet_name='pairwise_t-test')
        aov.to_excel(writer, sheet_name='anova')
        norm_test.to_excel(writer, sheet_name='norm_test')
        var_eq_test.to_excel(writer, sheet_name='variance_eq_test')
        writer.save()

