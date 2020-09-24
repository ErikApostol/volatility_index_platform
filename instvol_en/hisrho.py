import numpy as np

def hisrho(stock1,stock2,window):
    rho=[]
    for i in range(len(stock1)-window):
        N = window
        log_change_1=np.log(stock1[i+1:i+N+1]/stock1[i:i+N]) #報酬率取對數
        log_change_2=np.log(stock2[i+1:i+N+1]/stock2[i:i+N])
        matrix =  np.corrcoef(log_change_1,log_change_2) #算corrcoef
        dia= matrix[1,0] #取rho
        rho.append(dia)
    return rho

