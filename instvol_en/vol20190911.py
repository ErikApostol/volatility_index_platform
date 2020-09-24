import numpy as np
import pandas as pd
import ivol
import hvol

agg = pd.read_csv('AGG.csv')
#evz = pd.read_csv('EVZ.csv')
#fxe = pd.read_csv('FXE.csv')
#gld = pd.read_csv('GLD.csv')
#gvz = pd.read_csv('GVZ.csv')
#spy = pd.read_csv('SPY .csv')
#tyv = pd.read_csv('tyvixdailyprices .csv')
#vix = pd.read_csv('VIX .csv')
#btc = pd.read_csv('BTC-USD.csv')
#eth = pd.read_csv('ETH-USD.csv')

his_agg = hvol.hvol(agg.Adj_Close)
#his_evz = hvol.hvol(evz.Adj_Close)
#his_fxe = hvol.hvol(fxe.Adj_Close)
#his_gld = hvol.hvol(gld.Adj_Close)
#his_gvz = hvol.hvol(gvz.Adj_Close)
#his_spy = hvol.hvol(spy.Adj_Close)
#his_tyv = hvol.hvol(tyv.Close)
#his_vix = hvol.hvol(vix.Adj_Close)
#his_btc = hvol.hvol(btc.Adj_Close)
#his_eth = hvol.hvol(eth.Adj_Close)

ins_agg = np.sqrt(ivol.ivol(np.log(agg.Adj_Close.values), len(agg)/252, len(agg)//2-1, (len(agg)-1)//2))
#ins_evz = ivol.ivol(np.log(evz.Adj_Close.values), len(evz)/252, len(evz)//2-1, (len(evz)-1)//2)
#ins_fxe = ivol.ivol(np.log(fxe.Adj_Close.values), len(fxe)/252, len(fxe)//2-1, (len(fxe)-1)//2)
#ins_gld = ivol.ivol(np.log(gld.Adj_Close.values), len(gld)/252, len(gld)//2-1, (len(gld)-1)//2)
#ins_gvz = ivol.ivol(np.log(gvz.Adj_Close.values), len(gvz)/252, len(gvz)//2-1, (len(gvz)-1)//2)
#ins_spy = ivol.ivol(np.log(spy.Adj_Close.values), len(spy)/252, len(spy)//2-1, (len(spy)-1)//2)
#ins_tyv = ivol.ivol(np.log(tyv.Close.values), len(tyv)/252, len(tyv)//2-1, (len(tyv)-1)//2)
#ins_vix = ivol.ivol(np.log(vix.Adj_Close.values), len(vix)/252, len(vix)//2-1, (len(vix)-1)//2)
#ins_btc = ivol.ivol(np.log(btc.Adj_Close.values), len(btc)/252, len(btc)//2-1, (len(btc)-1)//2)
#ins_eth = ivol.ivol(np.log(eth.Adj_Close.values), len(eth)/252, len(eth)//2-1, (len(eth)-1)//2)

result_agg = pd.DataFrame(columns=['Date', 'AGG', 'his_vol', 'ins_vol'])
#result_evz = pd.DataFrame(columns=['Date', 'his_vol', 'ins_vol'])
#result_fxe = pd.DataFrame(columns=['Date', 'his_vol', 'ins_vol'])
#result_gld = pd.DataFrame(columns=['Date', 'his_vol', 'ins_vol'])
#result_gvz = pd.DataFrame(columns=['Date', 'his_vol', 'ins_vol'])
#result_spy = pd.DataFrame(columns=['Date', 'his_vol', 'ins_vol'])
#result_tyv = pd.DataFrame(columns=['Date', 'his_vol', 'ins_vol'])
#result_vix = pd.DataFrame(columns=['Date', 'his_vol', 'ins_vol'])
#result_btc = pd.DataFrame(columns=['Date', 'his_vol', 'ins_vol'])
#result_eth = pd.DataFrame(columns=['Date', 'his_vol', 'ins_vol'])

result_agg.Date = agg.Date
#result_evz.Date = evz.Date
#result_fxe.Date = fxe.Date
#result_gld.Date = gld.Date
#result_gvz.Date = gvz.Date
#result_spy.Date = spy.Date
#result_tyv.Date = tyv.Date
#result_vix.Date = vix.Date
#result_btc.Date = btc.Date
#result_eth.Date = eth.Date

result_agg.AGG = agg.Adj_Close

result_agg.his_vol.iloc[-len(his_agg):] = his_agg
#result_evz.his_vol[-len(his_evz):] = his_evz
#result_fxe.his_vol[-len(his_fxe):] = his_fxe
#result_gld.his_vol[-len(his_gld):] = his_gld
#result_gvz.his_vol[-len(his_gvz):] = his_gvz
#result_spy.his_vol[-len(his_spy):] = his_spy
#result_tyv.his_vol[-len(his_tyv):] = his_tyv
#result_vix.his_vol[-len(his_vix):] = his_vix
#result_btc.his_vol[-len(his_btc):] = his_btc
#result_eth.his_vol[-len(his_eth):] = his_eth

result_agg.ins_vol.iloc[-len(ins_agg):] = ins_agg
#result_evz.ins_vol[-len(ins_evz):] = ins_evz
#result_fxe.ins_vol[-len(ins_fxe):] = ins_fxe
#result_gld.ins_vol[-len(ins_gld):] = ins_gld
#result_gvz.ins_vol[-len(ins_gvz):] = ins_gvz
#result_spy.ins_vol[-len(ins_spy):] = ins_spy
#result_tyv.ins_vol[-len(ins_tyv):] = ins_tyv
#result_vix.ins_vol[-len(ins_vix):] = ins_vix
#result_btc.ins_vol[-len(ins_btc):] = ins_btc
#result_eth.ins_vol[-len(ins_eth):] = ins_eth

result_agg.to_csv('result_agg20190914.csv')
#result_evz.to_csv('result_evz20190911.csv')
#result_fxe.to_csv('result_fxe20190911.csv')
#result_gld.to_csv('result_gld20190911.csv')
#result_gvz.to_csv('result_gvz20190911.csv')
#result_spy.to_csv('result_spy20190911.csv')
#result_tyv.to_csv('result_tyv20190911.csv')
#result_vix.to_csv('result_vix20190911.csv')
#result_btc.to_csv('result_btc20190912.csv')
#result_eth.to_csv('result_eth20190912.csv')
