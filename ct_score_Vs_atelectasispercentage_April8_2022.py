#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sys,os,glob,subprocess
import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import pointbiserialr
from statsmodels.miscmodels.ordinal_model import OrderedModel
from IPython.display import Markdown, display
sys.path.append("/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/SOFTWARE/")
from utilities_simple_latex import * 
# get_ipython().run_line_magic('matplotlib', 'inline')
sns.set(rc={"figure.figsize":(20, 20)})


# In[27]:
def printmd(string, color=None):
    colorstr = "<span style='color:{}'>{}</span>".format(color, string)
    display(Markdown(colorstr))

grayscale_dir="/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA/Lungs/RENAMEDUNIQUE"
calculation_output_directory='calculatedNscore'
input_directory=os.path.join(grayscale_dir,calculation_output_directory) #'RESULTS_bothfilter') #'calculation_output_directory')
atelectatsis_perc_df_all=glob.glob(os.path.join(input_directory,"*.csv"))
atelectatsis_perc_df_file='/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA/Lungs/RENAMEDUNIQUE/calculatedNscore/scoreVscalculatedvals.csv'

# count=0
# for atelectatsis_perc_df_file in atelectatsis_perc_df_all:
#     if count <1:
atelectatsis_perc_df=pd.read_csv(atelectatsis_perc_df_file) 
# atelectatsis_perc_df=atelectatsis_perc_df.loc[:, ~atelectatsis_perc_df.columns.str.contains('^Unnamed')]
#os.path.join(input_directory,'CT_ID_and_ateleactasis_volume_ct_score.csv'))
latexfilename=atelectatsis_perc_df_file.split('.csv')[0]+'.tex' #os.path.join(input_directory,'CT_ID_and_ateleactasis_volume_ct_score')+".tex"
latex_start(latexfilename)
latex_begin_document(latexfilename)
## plot correlation graph.
from IPython.display import display


atelectatsis_perc_df.ct_score=pd.to_numeric(atelectatsis_perc_df.loc[:,'ct_score'])
atelectatsis_perc_df.atelectasis_percentage=pd.to_numeric(atelectatsis_perc_df.loc[:,'atelectasis_percentage'])
atelectatsis_perc_df_copy=atelectatsis_perc_df.dropna() #copy()
atelectatsis_perc_df_copy=atelectatsis_perc_df_copy[atelectatsis_perc_df_copy.ct_score!="NaN"]
print(atelectatsis_perc_df.ct_score)
#############################################################
imagename=os.path.join(grayscale_dir,calculation_output_directory,os.path.basename(atelectatsis_perc_df_file).split('.csv')[0] +'datatable.png')
plt.rc('figure', figsize=(12, 7))
#plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 12}) old approach
plt.text(0.01, 0.05, str(atelectatsis_perc_df_copy), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig(imagename)
plt.close()
latex_start_tableNc_noboundary(latexfilename,1)
latex_insertimage_tableNc(latexfilename,[imagename],1, caption="datatable",imagescale=0.5, angle=0,space=1)
latex_end_table2c(latexfilename)
latex_end(latexfilename) 

##################################################
text_to_display="Data table we are analyzing"
printmd("**{}**".format(text_to_display), color="blue")
#     print("#"*50+text_to_display+"#"*50)
display(atelectatsis_perc_df_copy)

atelectatsis_perc_df_copy.shape
correlation =stats.spearmanr(atelectatsis_perc_df_copy.atelectasis_percentage, atelectatsis_perc_df_copy.ct_score) # atelectatsis_perc_df_copy.ct_score.corr(atelectatsis_perc_df_copy.atelectasis_percentage)

pbc = pointbiserialr(atelectatsis_perc_df_copy.atelectasis_percentage, atelectatsis_perc_df_copy.ct_score)

text_to_display="Spearman correlation coefficient between atelectasis_percentage and ct_score"
printmd("**{}**".format(text_to_display), color="blue")
#     print("#"*50+text_to_display+"#"*50)
display(correlation.correlation)
corr_table=[[os.path.basename(atelectatsis_perc_df_file).split('.csv')[0],correlation.correlation,correlation.pvalue]]
corr_table_df=pd.DataFrame(corr_table)
corr_table_df.columns = ['Filename','Spearman correlation','P-value']


#         latex_insert_line_nodate(latexfilename,"\\texttt{\\detokenize{" + text_to_display + "}}  ")
#         latex_insert_line_nodek(latexfilename,text="  ")
#         latex_insert_line_nodek(latexfilename,text=str(correlation.correlation) )
text_to_display="Spearman correlation coefficient pvalue"
print("correlation")
print(type(correlation))
print(correlation)
#     printmd("**{}**".format(text_to_display), color="blue")
#     print("#"*50+text_to_display+"#"*50)
display(correlation.pvalue)
#         latex_insert_line_nodate(latexfilename,"\\texttt{\\detokenize{" + text_to_display + "}}  ")
#         latex_insert_line_nodek(latexfilename,text="  ")
#         latex_insert_line_nodek(latexfilename,text=str(correlation.pvalue))
############################################################################################################
# text_to_display="Point Biserial correlation coefficient between atelectasis_percentage and ct_score"
# printmd("**{}**".format(text_to_display), color="blue")
# #     print("#"*50+text_to_display+"#"*50)
# display(correlation.correlation)
# corr_table=[[os.path.basename(atelectatsis_perc_df_file).split('.csv')[0],correlation.correlation,correlation.pvalue]]
# corr_table_df=pd.DataFrame(corr_table)
# corr_table_df.columns = ['Filename','Point Biserial','P-value']


# #         latex_insert_line_nodate(latexfilename,"\\texttt{\\detokenize{" + text_to_display + "}}  ")
# #         latex_insert_line_nodek(latexfilename,text="  ")
# #         latex_insert_line_nodek(latexfilename,text=str(correlation.correlation) )
# text_to_display="Point Biserial correlation coefficient pvalue"
# print("Point Biserial correlation")
# print(type(pbc))
# print(pbc)
# #     printmd("**{}**".format(text_to_display), color="blue")
# #     print("#"*50+text_to_display+"#"*50)
# display(pbc.pvalue)
# #         latex_insert_line_nodate(latexfilename,"\\texttt{\\detokenize{" + text_to_display + "}}  ")
# #         latex_insert_line_nodek(latexfilename,text="  ")
# #         latex_insert_line_nodek(latexfilename,text=str(correlation.pvalue))
##############################################################################################################

###########################################################################################################################
text_to_display="Histogram of ct_score"
#     printmd("**{}**".format(text_to_display), color="blue")
#     print("#"*50+text_to_display+"#"*50)
# ax = sns.boxplot(x='ct_score', y='atelectasis_percentage', data=atelectatsis_perc_df_copy)
# ax = sns.swarmplot(x='ct_score', y='atelectasis_percentage', data=atelectatsis_perc_df_copy, color="black")
# display(ax)
sns.histplot(data=atelectatsis_perc_df_copy, x="ct_score",bins=np.unique(atelectatsis_perc_df_copy.ct_score),discrete="True")
plt.title("HISTOGRAM")
imagename=os.path.join(grayscale_dir,calculation_output_directory,os.path.basename(atelectatsis_perc_df_file).split('.csv')[0] + 'ct_score_histogram.png')
plt.savefig(imagename)
plt.close()
# In[28]:
latex_start_tableNc_noboundary(latexfilename,1)
latex_insertimage_tableNc(latexfilename,[imagename],1, caption="histogram",imagescale=0.9, angle=0,space=1)
latex_end_table2c(latexfilename)
###########################################################################################################################################
# plot a bar chart


# In[29]:


text_to_display="BOXPLOT with jitter of ct_score"
#     printmd("**{}**".format(text_to_display), color="blue")
#     print("#"*50+text_to_display+"#"*50)
ax = sns.boxplot(x='ct_score', y='atelectasis_percentage', data=atelectatsis_perc_df_copy)
ax = sns.swarmplot(x='ct_score', y='atelectasis_percentage', data=atelectatsis_perc_df_copy, color="black")
imagename=os.path.join(grayscale_dir,calculation_output_directory,os.path.basename(atelectatsis_perc_df_file).split('.csv')[0] +'boxplotwithjitter.png')
plt.title("BOXPLOT")
#     display(ax)
plt.savefig(imagename)
plt.close()
# In[30]:
latex_start_tableNc_noboundary(latexfilename,1)
latex_insertimage_tableNc(latexfilename,[imagename],1, caption="BOXPLOT",imagescale=0.9, angle=0,space=1)
latex_end_table2c(latexfilename)

latex_start_tableNc_noboundary(latexfilename,1)
latex_insert_line_nodek(latexfilename,text=corr_table_df.to_latex(index=False))
latex_end_table2c(latexfilename)
############################################################################################################################################        
text_to_display="plot of Ordinary Least Square regression model"
imagename=os.path.join(grayscale_dir,calculation_output_directory,os.path.basename(atelectatsis_perc_df_file).split('.csv')[0] +'OrdinaryLSReg.png')

#     printmd("**{}**".format(text_to_display), color="blue")
#     print("#"*50+text_to_display+"#"*50)
sns.regplot(atelectatsis_perc_df_copy.atelectasis_percentage,atelectatsis_perc_df_copy.ct_score)
plt.title("Ordinary Least Square regression model")
plt.savefig(imagename)
plt.close()
# In[31]:

latex_start_tableNc_noboundary(latexfilename,1)
latex_insertimage_tableNc(latexfilename,[imagename],1, caption="Ordinary Least Square regression model",imagescale=0.9, angle=0,space=1)
latex_end_table2c(latexfilename)
##########################################################################################################################################



text_to_display="Summary of Ordinary Least Square regression model"

#     printmd("**{}**".format(text_to_display), color="blue")
#     print("#"*50+text_to_display+"#"*50)
model = sm.OLS(atelectatsis_perc_df_copy['ct_score'],atelectatsis_perc_df_copy['atelectasis_percentage'])
results = model.fit()
print(results.summary().as_latex())
imagename=os.path.join(grayscale_dir,calculation_output_directory,os.path.basename(atelectatsis_perc_df_file).split('.csv')[0] +'OrdinaryLSRegSummary.png')
plt.rc('figure', figsize=(12, 7))
#plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 12}) old approach
plt.text(0.01, 0.05, str(results.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig(imagename)
plt.close()

latex_start_tableNc_noboundary(latexfilename,1)
latex_insertimage_tableNc(latexfilename,[imagename],1, caption="OrdinaryLSRegSummary",imagescale=0.9, angle=0,space=1)
latex_end_table2c(latexfilename)

###############################################################################################################################################
#     latex_insert_line_nodate(latexfilename,"\\texttt{\\detokenize{" + text_to_display + "}}  ")
#     latex_insert_line_nodek(latexfilename,text="  ")
#     latex_insert_line_nodek(latexfilename,text=results.summary().as_latex())
# latex_insert_line_nodate(latexfilename,"\\texttt{\\detokenize{" + str(correlation.pvalue) + "}}")

# In[32]:


# In[33]:


text_to_display="Summary of Ordinal regression model"
#     printmd("**{}**".format(text_to_display), color="blue")
print("#"*50+text_to_display+"#"*50)
mod_log = OrderedModel(atelectatsis_perc_df_copy['ct_score'],
                        atelectatsis_perc_df_copy[['atelectasis_percentage']],
                        distr='logit',dropna=True)
res_log = mod_log.fit(method='bfgs', disp=True)
print(res_log.summary().as_latex())
#     latex_insert_line_nodate(latexfilename,"\\texttt{\\detokenize{" + text_to_display + "}}  ")
#     latex_insert_line_nodek(latexfilename,text="  ")
#     latex_insert_line_nodek(latexfilename,text=res_log.summary().as_latex())
# latex_insert_line_nodate(latexfilename,"\\texttt{\\detokenize{" + str(correlation.pvalue) + "}}")
imagename=os.path.join(grayscale_dir,calculation_output_directory,os.path.basename(atelectatsis_perc_df_file).split('.csv')[0] +'OrdinalRegSummary.png')
plt.rc('figure', figsize=(12, 7))
#plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 12}) old approach
plt.text(0.01, 0.05, str(res_log.summary()), {'fontsize': 10}, fontproperties = 'monospace') # approach improved by OP -> monospace!
plt.axis('off')
plt.tight_layout()
plt.savefig(imagename)
plt.close()
latex_start_tableNc_noboundary(latexfilename,1)
latex_insertimage_tableNc(latexfilename,[imagename],1, caption="OrdinalRegSummary",imagescale=0.9, angle=0,space=1)
latex_end_table2c(latexfilename)
latex_end(latexfilename) 

#################################################################################################################################
#         count+=1
