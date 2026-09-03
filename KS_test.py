# pip install scipy
# KS test is used to compare two samples. It is a non-parametric test
# ks_2samp(data1, data2, alternative='two-sided', method='auto', *, axis=0, nan_policy='propagate', keepdims=False)
# User has option to "run KS test" which will bring them to the KS test page and input preset values based on what they already have. But will also allow them to input their own values and hit "Calculate" to get the results.

from scipy.stats import ks_2samp
import numpy as np
import pandas as pd

def getPValue(result):
    """
    Extracts the p-value from the KS test result.
    
    Parameters:
    result (KstestResult): The result object from the ks_2samp function.
    
    Returns:
    float: The p-value of the KS test.
    str: "Error" if an exception occurs.
    """
    try:
        return result.pvalue
    except:
        return "Error"

#This will be rejected once the KS test is implemented in the GUI and we can use default values for the parameters.
def KS_test1(data1, data2):
    try:
        result = ks_2samp(data1, data2)
        return result
    except Exception as e:
        # Returning "Error" means no functions (.pvalue, .statistic, etc.) can be called on the result
        print(f"An error occurred: {e}")
        return "Error"

def KS_test2(data1, data2, alternative, method, axis, nan_policy, keepdims):
    """
    Performs the KS test on two data samples.
    
    Parameters:
    data1 (list): The first data sample.
    data2 (list): The second data sample.
    alternative (str): The alternative hypothesis. Default is 'two-sided'.
    method (str): The method used to calculate the p-value. Default is 'auto'.
    axis (int): The axis along which the test is applied. Default is 0.
    nan_policy (str): The policy for handling NaN values. Default is 'propagate'.
    keepdims (bool): Whether to keep the dimensions of the result. Default is False.
    
    Returns:
    KstestResult: The result object containing the KS test statistic and p-value.
    str: "Error" if an exception occurs.
    """
    try:
        result = ks_2samp(data1, data2, alternative=alternative, method=method, axis=axis, nan_policy=nan_policy, keepdims=keepdims)
        return result
    except Exception as e:
        # Returning "Error" means no functions (.pvalue, .statistic, etc.) can be called on the result
        print(f"An error occurred: {e}")
        return "Error"
'''
res: KstestResult
An object containing attributes:

statistic
float
KS test statistic.

pvalue
float
One-tailed or two-tailed p-value.

statistic_location
float
Value from data1 or data2 corresponding with the KS statistic; i.e., the distance between the empirical distribution functions is measured at this observation.

statistic_sign
int
+1 if the empirical distribution function of data1 exceeds the empirical distribution function of data2 at statistic_location, otherwise -1.
'''