import pandas as pd
import numpy as np
from instvol.ivol import ivol
from instvol.hvol import hvol
from instvol.insrho import insrho
from instvol.hisrho import hisrho

def getcorr(f1, f2, T):
    # Instantaneeous Vol
    f1_inst_vol = np.sqrt(ivol(np.log(f1['price'].astype('double')), T, len(f1['price'])//2-1, (len(f1['price'])-1)//2))
    f2_inst_vol = np.sqrt(ivol(np.log(f2['price'].astype('double')), T, len(f2['price'])//2-1, (len(f2['price'])-1)//2))

    # Correlation
    if len(f1) % 2 == 0:
        inst_rho = insrho(np.array(f1['price'][1:]), np.array(f2['price'][1:]), f1_inst_vol, f2_inst_vol)
    else:
        inst_rho = insrho(np.array(f1['price']), np.array(f2['price']), f1_inst_vol, f2_inst_vol)

    his_rho = hisrho(np.array(f1['price']), np.array(f2['price']), 22)

    return [f1.index, inst_rho.flatten(), his_rho]