#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd #for manipulating data
import numpy as np #for manipulating data
import sklearn #for building models
import xgboost as xgb #for building models
import sklearn.ensemble #for building models
from sklearn.model_selection import train_test_split #for creating a hold-out sample
import lime #LIME package
import lime.lime_tabular #the type of LIIME analysis we’ll do
import shap #SHAP package
import time #some of the routines take a while so we monitor the time
import os #needed to use Environment Variables in Domino
import matplotlib.pyplot as plt #for custom graphs at the end
import seaborn as sns #for custom graphs at the end
from shap import TreeExplainer
from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

X,y = shap.datasets.boston()
#print(X)
#print(y)
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=0.2, random_state=0)
X.head()
#print(X.head())
#pd.Series(y).head()
#print(pd.Series(y).head())
#print(sklearn.datasets.load_boston().DESCR)

 
# Random Forest
rf = sklearn.ensemble.RandomForestRegressor()
rf.fit(X_train, y_train)
 

# Tree on Random Forestexplainer
explainerRF = shap.TreeExplainer(rf)
shap_values_RF_test = explainerRF.shap_values(X_test)
shap_values_RF_train = explainerRF.shap_values(X_train)

# Random Forest
df_shap_RF_test = pd.DataFrame(shap_values_RF_test, columns=X_test.columns.values)
df_shap_RF_train = pd.DataFrame(shap_values_RF_train, columns=X_train.columns.values)


# j will be the record we explain
j = 0
# initialize js for SHAP
shap.initjs()

shap.force_plot(explainerRF.expected_value, shap_values_RF_test[j], X_test.iloc[[j]])



#Random Forest SHAP
shap.force_plot(explainerRF.expected_value, shap_values_RF_test[j], X_test.iloc[[j]])

#Random Forest LIME
explainer = lime.lime_tabular.LimeTabularExplainer(X_train.values, feature_names=X_train.columns.values.tolist(),class_names=['price'], verbose=True, mode='regression')

exp = explainer.explain_instance(X_test.values[j], rf.predict, num_features=5)
exp.show_in_notebook(show_table=True)


shap.summary_plot(shap_values_RF_train, X_train, plot_type="bar")

shap.summary_plot(shap_values_RF_train, X_train)


shp_plt = shap.dependence_plot("LSTAT", shap_values_RF_train, X_train)

