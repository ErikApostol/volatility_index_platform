import numpy as np

def historical_volatility(quotes, annParam):
    logreturns = np.log(quotes / quotes.shift(1))
    return np.sqrt(252*annParam*logreturns.var())

def hvol(quotes, windowSize=22, annParam=1): #volitility series
    return [100 * historical_volatility(quotes[i-windowSize:i], annParam) for i in range(windowSize, len(quotes)+1)]