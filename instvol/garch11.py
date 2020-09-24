import pandas as pd
import numpy as np
import pandas_datareader as pdr
from datetime import datetime

# Declare variables
# data = pdr.get_data_yahoo(symbols='ibm', start=datetime(2010, 1, 1), 
#                           end=datetime(2019,11,19)).reset_index(drop=True)['Adj Close']

def garch11(data):
    # Return
    returns = np.diff(np.log(data))
    
    from arch import arch_model
    garch11 = arch_model(returns, p=1, q=1, rescale=False)
    return np.sqrt(252) * garch11.fit(update_freq=5).conditional_volatility
