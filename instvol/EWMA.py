#!/home/spock/anaconda3/envs/VIP2018/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:33:18 2019

@author: kunwa
"""

import pandas as pd
import numpy as np
import pandas_datareader as pdr
from datetime import datetime

# Declare variables
#data = pdr.get_data_yahoo(symbols='ibm', start=datetime(2019, 1, 1), end=datetime(2019, 9, 28)).reset_index(drop=True)['Adj Close']

def ewma(data):
    p=data
    y = np.diff(np.log(p), n=1, axis=0)            # calculate returns
    y[:] = y[:]-np.mean(y[:])                      # subtract mean
    T = len(y[:])
    EWMA = np.full([T], np.nan)
    lmbda = 0.94
    S = np.cov(y, rowvar = False)
    EWMA[0] = S.flatten()
    for i in range(1,T):
        S = lmbda * S + (1-lmbda) * np.transpose(np.asmatrix(y[i-1]))* np.asmatrix(y[i-1])
        EWMA[i] = np.sqrt(S)*np.sqrt(252)
    return EWMA

#ewma(data)
