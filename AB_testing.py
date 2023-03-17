##############################################################
# Hypothesis Test Steps
##############################################################
# Two-Sample Hypothesis Test

##############################################################
# Step 1: Defining The Hypothesis
##############################################################
# * H0: There is no significant difference between the two samples.
# * H1: There is a significant difference between the two samples.

##############################################################
# Step 2: Assumption Check
##############################################################
# 1. Normality assumption: Use Shapiro-Wilk test to check normality assumption of the sample distributions.
# 2. Homogeneity of variance: Use Levene's test to check if variances of the samples are equal.

##############################################################
# # Step 3: Implementation of the Hypothesis Test
##############################################################
# 1. If normality assumption are met, use the independent two-sample t-test.
# 2. If normality assumption are not met, use the Mann-Whitney U test.

##############################################################
# Step 4: Interpret the Results Based on the p-value
##############################################################
# If the p-value is greater than the significance value (0.05),
# it cannot reject the null hypothesis and it is concluded that there is no significant difference between the two samples.

# If the p value is less than the significance value (0.05),
# reject the null hypothesis and it is concluded that there is a significant difference between the two samples.

##############################################################
# Data Preparation
##############################################################

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel('datasets/ab_testing.xlsx', sheet_name='Control Group')
df_test = pd.read_excel('datasets/ab_testing.xlsx', sheet_name='Test Group')

df_control.columns = ['control_Impression', 'control_Click', 'control_Purchase', 'control_Earning']
df_test.columns = ['test_Impression', 'test_Click', 'test_Purchase', 'test_Earning']

# plotting
for col in df_test.columns:
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(data=df_control, x=col, kde=True)
    plt.title('Maximum Bidding')
    plt.xlabel(col)
    plt.xticks(rotation = 90)
    plt.ylabel('Count')

    plt.subplot(1, 2, 2)
    sns.histplot(data=df_test, x=col, kde=True)
    plt.title('Average Bidding')
    plt.xlabel(col)
    plt.xticks(rotation = 90)
    plt.ylabel('Count')
    plt.show(block=True)

def check_df(dataframe, head=5):
    print('##################### Shape #####################')
    print(dataframe.shape)
    print('##################### Types #####################')
    print(dataframe.dtypes)
    print('##################### Head #####################')
    print(dataframe.head(head))
    print('##################### Tail #####################')
    print(dataframe.tail(head))
    print('##################### NA #####################')
    print(dataframe.isnull().sum())
    print('##################### Quantiles #####################')
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)

df_control.corr()
df_test.corr()

# corr
df.corr()

df_control['control_Impression'].corr(df_control['control_Purchase']) # 0.21457493332510497
df_control['control_Click'].corr(df_control['control_Purchase']) # 0.057397460002540576
df_control['control_Earning'].corr(df_control['control_Purchase']) # 0.06172845453279909

df_test['test_Impression'].corr(df_test['test_Purchase']) # 0.13779572364901418
df_test['test_Click'].corr(df_test['test_Purchase']) # -0.0744144378715168
df_test['test_Earning'].corr(df_test['test_Purchase']) # 0.1024809526296904

df = pd.concat([df_test, df_control], axis=1)

#####################################################
# Defining The Hypothesis
#####################################################
# H0: There is no statistically significant difference between the purchase averages of Maximum Bidding and Average Bidding.
# H1:There is a statistically significant difference between the purchase averages of Maximum Bidding and Average Bidding.

######################################################
# Assumption Control
######################################################
# 1. Normality assumption: Use Shapiro-Wilk test to check normality assumption of the sample distributions.

test_stat, pvalue = shapiro(df['test_Purchase'])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # Test Stat = 0.9589, p-value = 0.1541 // p > .05

test_stat, pvalue = shapiro(df['control_Purchase'])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # Test Stat = 0.9773, p-value = 0.5891 // p > .05

# p-value is greater than .05, so we can say that the sample is normally distributed

# 2. Homogeneity of variance: Use Levene's test to check if variances of the samples are equal.

test_stat, pvalue = levene(df['control_Purchase'],
                           df['test_Purchase'])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # Test Stat = 2.6393, p-value = 0.1083 // p > .05

# p-value is greater than .05 that's why we can say the variance is homogeneous.

##############################################################
# Implementation of the Hypothesis Test
##############################################################
# 1. If normality assumption are met, use the independent two-sample t-test. - USED
# 2. If normality assumption are not met, use the Mann-Whitney U test. - NOT USED

test_stat, pvalue = ttest_ind(df['control_Purchase'],
                              df['test_Purchase'],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # Test Stat = -0.9416, p-value = 0.3493 // p > .05

# The H0 hypothesis cannot be rejected because its p-value is greater than .05
# It means that there is no statistically significant difference between the purchasing averages of these Bidding methods.