from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

import pandas as pd
import numpy as np
import datetime
import pickle
import pandas_datareader.data as web
from pandas_datareader import data as pdr
from random import randint

import instvol.myplotly
import pickle
import csv

from instvol.ivol import ivol
from instvol.hvol import hvol
from instvol.hisrho import hisrho
from instvol.insrho import insrho
from instvol.getcorr import getcorr
from instvol.models import *
#from instvol.VIXmap import tickers
from instvol.VIXmap import *
from instvol.EWMA import ewma
from instvol.garch11 import garch11 

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    if request.GET.get('userlang', 'None') == 'ch':
        request.session['userlang'] = 'ch'
        request.session.set_expiry(4838400)

    if not request.GET.get('userlang', ''):
        if request.session.get('userlang', ''):
            if request.session.get('userlang') == 'en':
                return redirect('/vip/en/')
            
        elif request.LANGUAGE_CODE:
            try:
                if request.LANGUAGE_CODE[:2] != 'zh':
                    return redirect('/vip/en/')
            except:
                pass

    template = loader.get_template('instvol/index.html')

    div0315 = pickle.load(open( BASE_DIR + "/instvol/specialEvents/div0315.p", "rb" ))
    div0824 = pickle.load(open( BASE_DIR + "/instvol/specialEvents/div0824.p", "rb" ))
    div0805 = pickle.load(open( BASE_DIR + "/instvol/specialEvents/div0805.p", "rb" ))
    div0808 = pickle.load(open( BASE_DIR + "/instvol/specialEvents/div0808.p", "rb" ))

    context = {'plot_div_0315': div0315, 'plot_div_0824': div0824,
               'plot_div_0805': div0805, 'plot_div_0808': div0808}

    response = HttpResponse(template.render(context, request))
    return response

def aboutvol(request):
    template = loader.get_template('instvol/introvol.html')
    return HttpResponse(template.render({}, request))

def aboutcorr(request):
    template = loader.get_template('instvol/introcorr.html')
    return HttpResponse(template.render({}, request))

def engine(request):
    if request.method == 'POST': #custom upload
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            cusdata = pd.read_csv(request.FILES['file'], header=None)

            # Instantaneeous Vol
            inst_vol = np.sqrt(ivol(np.log(cusdata.iloc[:,0].astype('double')),
                            len(cusdata)/252,\
                            len(cusdata)//2-1,\
                            (len(cusdata)-1)//2))

            # Historical Vol
            hist_vol = hvol(cusdata.iloc[:,0].astype('double'))

            # volatility using EWMA
            ewma_vol = 100 * ewma(cusdata.iloc[:,0].astype('double'))

            # volatility using GARCH(1,1)
            garch_vol = 100 * garch11(cusdata.iloc[:,0].astype('double'))

            div = instvol.myplotly.getdiv(cusdata.index, cusdata.iloc[:,0].astype('double'),
                                          100*inst_vol, hist_vol, ewma_vol, garch_vol, None, 'Custom', True)

            df = pd.DataFrame({'inst_vol':[None,]*(len(cusdata)-len(inst_vol)) + list(inst_vol),
                               'hist_vol':[None,]*(len(cusdata)-len(hist_vol)) + list(hist_vol),
                               'ewma_vol':[None,]*(len(cusdata)-len(ewma_vol)) + list(ewma_vol),
                               'garch_vol':[None,]*(len(cusdata)-len(garch_vol)) + list(garch_vol) })
    

    else:
        getSymbol = request.GET.get('symbol', 'None')
        if getSymbol == 'None':
            symbol = 'SPX'
        else:
            symbol = getSymbol
        print(symbol)

        daterange = request.GET.get('daterange', 'None')
        if daterange == 'None':
            today = datetime.datetime(2018, 11, 30)
            daterange = (today - datetime.timedelta(days=365)).strftime('%Y%m%d') + ' - ' + today.strftime('%Y%m%d')

        if request.GET.get('symbol', 'None') == 'None' and request.GET.get('daterange', 'None') == 'None':
            context = pickle.load(open( "defaultvol_context.p", "rb" ))
            #context['ticker_list'] = tickers
            context['stock_index_tickers'] = stock_index_tickers
            context['volatility_index_tickers'] = volatility_index_tickers
            context['equity_ETF_tickers'] = equity_ETF_tickers
            context['bond_ETF_index_tickers'] = bond_ETF_index_tickers
            context['commodity_ETF_tickers'] = commodity_ETF_tickers
            context['sustainable_ETF_tickers'] = sustainable_ETF_tickers
            context['other_tickers'] = other_tickers
            template = loader.get_template('instvol/calculator.html')
            return HttpResponse(template.render(context, request))

        daterange = daterange.replace(' ','').split('-')
        start = datetime.datetime.strptime(daterange[0], '%Y%m%d')
        end = datetime.datetime.strptime(daterange[1], '%Y%m%d')

        # Symbol data
        f = Stock.objects.get(ticker=symbol).stockprice_set.filter(ts__gte=start.date(), ts__lte=end.date())
        fdata = pd.DataFrame(list(f.values()))
        fdata = fdata.set_index('ts').astype('float').dropna()

        # Instantaneeous Vol
        inst_vol = np.sqrt(ivol(np.log(fdata['price'].astype('double')),\
                           (end-start).days/252,\
                           len(fdata['price'])//2-1,\
                           (len(fdata['price'])-1)//2))

        # Historical Vol
        hist_vol = hvol(fdata['price'])

        # volatility using EWMA
        ewma_vol = 100 * ewma(fdata['price'])

        # volatility using GARCH(1,1)
        garch_vol = 100 * garch11(fdata['price'])

        df = pd.DataFrame({'inst_vol':[None,]*(len(fdata)-len(inst_vol)) + list(inst_vol),
                           'hist_vol':[None,]*(len(fdata)-len(hist_vol)) + list(hist_vol),
                           'ewma_vol':[None,]*(len(fdata)-len(ewma_vol)) + list(ewma_vol),
                           'garch_vol':[None,]*(len(fdata)-len(garch_vol)) + list(garch_vol) })

        # VIX
        if symbol == 'SPX':
            v = Stock.objects.get(ticker='VIX').stockprice_set.filter(ts__gte=start.date(), ts__lte=end.date())
            vdata = pd.DataFrame(list(v.values()))
            vdata = vdata.set_index('ts').astype('float').dropna()
            df['vix'] = [None,]*(len(fdata)-len(v.values())) + list(v.values())
        else:
            vdata = None

        div = instvol.myplotly.getdiv(fdata.index, fdata['price'].astype('double'), 100*inst_vol, hist_vol, ewma_vol, garch_vol, vdata, symbol, True)

        form = UploadFileForm()

        #if symbol and symbol != 'None':
        #    context['symbolName'] = symbol

    rnd_str = str(randint(1000000000,10000000000))
    csv_filename = 'instvol/results_csv/' + rnd_str + '.csv'
    df.to_csv('instvol/static/' + csv_filename)

    template = loader.get_template('instvol/calculator.html')

    context = {'plot_div': div,
               #'ticker_list': tickers,
               'stock_index_tickers': stock_index_tickers,
               'volatility_index_tickers': volatility_index_tickers,
               'equity_ETF_tickers': equity_ETF_tickers,
               'bond_ETF_index_tickers': bond_ETF_index_tickers,
               'commodity_ETF_tickers': commodity_ETF_tickers,
               'sustainable_ETF_tickers': sustainable_ETF_tickers,
               'other_tickers': other_tickers,
               'form': form,
               'csv_filename':csv_filename}

    if (('symbol' in locals()) or ('symbol' in globals())) and symbol and symbol != 'None':
        context['symbolName'] = symbol

    return HttpResponse(template.render(context, request))

def correlation(request):
    if request.method == 'POST': #custom upload
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            cusdata = pd.read_csv(request.FILES['file'], header=None)

        spot1 = ['Asset 1', ]
        spot2 = ['Asset 2', ]
        symbolPair = list(zip(spot1, spot2))

        start = 1
        end = len(cusdata)

        rhodata = []
        df = pd.DataFrame()
        for pair in symbolPair:
            f1 = pd.DataFrame({'price':cusdata.iloc[:,0].astype('double')})
            f2 = pd.DataFrame({'price':cusdata.iloc[:,1].astype('double')})

            T = (end-start) / 252

            corr = getcorr(f1, f2, T)
            corr.append(' / '.join(list(pair)))
            rhodata.append(corr)

            df[pair[0]+'/'+pair[1]+' inst_corr'] = [None,]*(len(cusdata)-len(corr[1])) + list(corr[1])
            df[pair[0]+'/'+pair[1]+' hist_corr'] = [None,]*(len(cusdata)-len(corr[2])) + list(corr[2])

        spotdata = []
        spots = list(set(spot1+spot2))
        for i in range(len(spots)):
            spotval = pd.DataFrame({'price':cusdata.iloc[:,i].astype('double')})
            spotdata.append([spotval, spots[i]])

        instcorrdiv = instvol.myplotly.getcorrdiv(rhodata)
        hiscorrdiv = instvol.myplotly.getcorrdiv(rhodata, isHis=1)
        spotdiv = instvol.myplotly.getspotdiv(spotdata)


    elif request.method == 'GET' and request.GET.getlist('field-a'): # built-in data
        spot1 = request.GET.getlist('field-a')
        spot2 = request.GET.getlist('field-b')
        symbolPair = list(zip(spot1, spot2))
        daterange = request.GET.get('daterange', 'None')

        if len(symbolPair) == 0:
            symbolPair = [['SPX','NDWLIT'], ['SPX', 'FTMIGMI'], ['SPX','GBIEMDCW']]
            spot1 = list(zip(*symbolPair))[0]
            spot2 = list(zip(*symbolPair))[1]
            if daterange == 'None':
                context = pickle.load(open( "defaultcorr_context.p", "rb" ))
                template = loader.get_template('instvol/correlation.html')
                return HttpResponse(template.render(context, request))

        daterange = daterange.replace(' ','').split('-')
        start = datetime.datetime.strptime(daterange[0], '%Y%m%d')
        end = datetime.datetime.strptime(daterange[1], '%Y%m%d')

        rhodata = []
        df = pd.DataFrame()
        for pair in symbolPair:
            f1 = Stock.objects.get(ticker=pair[0]).stockprice_set.filter(ts__gte=start.date(), ts__lte=end.date())
            f1 = pd.DataFrame(list(f1.values())).set_index('ts').astype('float').dropna()
            f1.index = pd.to_datetime(f1.index.date)
            f2 = Stock.objects.get(ticker=pair[1]).stockprice_set.filter(ts__gte=start.date(), ts__lte=end.date())
            f2 = pd.DataFrame(list(f2.values())).set_index('ts').astype('float').dropna()
            f2.index = pd.to_datetime(f2.index.date)
            commonidx = f1.index.intersection(f2.index)
            f1 = f1.loc[commonidx]
            f2 = f2.loc[commonidx]

            T = (end-start).days / 252

            corr = getcorr(f1, f2, T)
            corr.append(' / '.join(list(pair)))
            rhodata.append(corr)

            df[pair[0]+'/'+pair[1]+' inst_corr'] = [None,]*((end-start).days-len(corr[1])) + list(corr[1])
            df[pair[0]+'/'+pair[1]+' hist_corr'] = [None,]*((end-start).days-len(corr[2])) + list(corr[2])

        spotdata = []
        for spot in list(set(spot1+spot2)):
            spotval = Stock.objects.get(ticker=spot).stockprice_set.filter(ts__gte=start.date(), ts__lte=end.date())
            spotval = pd.DataFrame(list(spotval.values()))
            spotval = spotval.set_index('ts').astype('float').dropna()
            spotval.index = pd.to_datetime(spotval.index.date)
            spotdata.append([spotval, spot])

        instcorrdiv = instvol.myplotly.getcorrdiv(rhodata)
        hiscorrdiv = instvol.myplotly.getcorrdiv(rhodata, isHis=1)
        spotdiv = instvol.myplotly.getspotdiv(spotdata)

        form = UploadFileForm()
    
    else: # Loading the page in the first place without passing parameters
        instcorrdiv = None
        hiscorrdiv = None
        spotdiv = None
        form = UploadFileForm()
        df = pd.DataFrame()

    rnd_str = str(randint(1000000000,10000000000))
    csv_filename = 'instvol/results_csv/' + rnd_str + '.csv'
    df.to_csv('instvol/static/' + csv_filename)

    template = loader.get_template('instvol/correlation.html')

    context = {'plot_div_inst': instcorrdiv,
               'plot_div_his': hiscorrdiv,
               'plot_div_spot': spotdiv,  
               #'ticker_list': tickers,
               'stock_index_tickers': stock_index_tickers,
               'volatility_index_tickers': volatility_index_tickers,
               'equity_ETF_tickers': equity_ETF_tickers,
               'bond_ETF_index_tickers': bond_ETF_index_tickers,
               'commodity_ETF_tickers': commodity_ETF_tickers,
               'sustainable_ETF_tickers': sustainable_ETF_tickers,
               'other_tickers': other_tickers,
               'form': form,
               'csv_filename':csv_filename}

    return HttpResponse(template.render(context, request))
