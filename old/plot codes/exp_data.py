import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

sns.set(rc={'figure.figsize':(14,10)})
sns.set_theme(context = 'paper', style="ticks",
              palette="pastel", font_scale = 2)


# Load the example tips dataset
summaryData = pd.read_excel('E:/Work/Documents/paper-underwater_adhesion/Data/summary_20200911.xlsx', index_col=0)
summaryData.rename(columns = {'Label': 'Contact_type'}, inplace = True)
##summaryData = summaryData[summaryData["Label"] != "Ambiguous"]
summaryData.replace({'Contact_type': {'Dry': 'Air',
                                      'Bubble': 'Underwater: Bubble',
                                      'Wet': 'Underwater: Wet'}},
                    inplace = True)

# Draw a nested boxplot to show bills by day and time
ax = sns.boxplot(x="Contact_type", y="Adhesion_Force",
                hue="Substrate",
                data=summaryData)
ax.set(xlabel=None, ylabel='Adhesion Force $[μN]$')

sns.despine(offset=10, trim=True)
plt.xticks(rotation=0)
plt.tight_layout()
##plt.show()

import statsmodels.api as sm
from statsmodels.formula.api import ols
# Ordinary Least Squares (OLS) model
# C(Label):C(Substrate) represent interaction term
model = ols('Adhesion_Force ~ C(Contact_type) + C(Substrate) + C(Contact_type):C(Substrate)',
            data=summaryData).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

# Shapiro-Wilk test used to check the normal distribution of residuals
import scipy.stats as stats
w, pvalue = stats.shapiro(model.resid)
print(w, pvalue)

#Bartlett’s test to check the Homogeneity of variances
##import scipy.stats as stats
##w, pvalue = stats.bartlett(d['A'], d['B'], d['C'], d['D'])
##print(w, pvalue)

# load packages
from pingouin import pairwise_tukey
# perform multiple pairwise comparison (Tukey HSD)
# for unbalanced (unequal sample size) data, pairwise_tukey uses Tukey-Kramer test

statDf = pd.DataFrame()

fixed_params = ["Substrate", "Contact_type"]
i = 0
for fixed in fixed_params:
    for val in summaryData[fixed].unique():
        m_comp = pairwise_tukey(data=summaryData[summaryData[fixed] == val],
                                dv= 'Adhesion_Force',
                                between= fixed_params[i-1],
                                effsize = 'r')
        m_comp['Fixed_Parameter'] = val
        statDf = statDf.append(m_comp)
        print(m_comp)
    i += 1

print(statDf[["Fixed_Parameter","A","B","T","p-tukey", "r"]])

#save data and plot
##timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
##statDf.to_excel("summary_statistics-" + timestamp + ".xlsx")
##fig = ax.get_figure()
##fig.savefig("exp_plot-" + timestamp + ".png", bbox_size = 'tight',
##            transparent = True)

plt.show()

