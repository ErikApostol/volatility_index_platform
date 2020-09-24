import pandas as pd
import numpy as np
import cufflinks as cf
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Bar, Scatter, Figure, Layout

colors = {
    'Black': '#000000',
    'Red':   '#FF0000',
    'Green': '#00FF00',
    'Blue':  '#0000FF',
}

def getdiv(idx, close, inst, hvol, ewma, garch, vix, symbolName, isLegend, hisWindow=22):
    trace_index = go.Scatter(
        x=idx,
        y=close,
        name=symbolName
    )
    trace2 = go.Scatter(
        x=idx,
        y=inst,
        name='Instant Vol',
        yaxis='y2'
    )
    trace3 = go.Scatter(
        x=idx[hisWindow:],
        y=hvol,
        name='Historical Vol',
        yaxis='y2'
    )
    trace3_1 = go.Scatter(
        x=idx[-len(ewma):],
        y=ewma,
        name='EWMA Vol',
        yaxis='y2'
    )
    trace3_2 = go.Scatter(
        x=idx[-len(garch):],
        y=garch,
        name='GARCH(1,1) Vol',
        yaxis='y2'
    )
    data = [trace_index,    #left y-axis
            trace2, trace3, trace3_1, trace3_2] #fight y-axis
    if vix is not None:
        trace4 = go.Scatter(
            x=vix.index,
            y=vix['price'].astype('double'),
            name='VIX',
            yaxis='y2'
        )
        data.append(trace4)
    layout = go.Layout(
        # title=fig_title,
        margin=go.layout.Margin(
            #l=50,
            #r=50,
            b=50,
            t=25,
            pad=4
        ),
        yaxis=dict(
            title='Index'
        ),
        yaxis2=dict(
            title='Volatility',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        ),
        showlegend=isLegend,
    )

    fig = go.Figure(data=data, layout=layout)
    div = plotly.offline.plot(fig,
                              output_type='div',
                              auto_open=False,
                              show_link=False)

    return div

def getcorrdiv(rhodata, hisWindow=22, isHis=0):
    data = []
    for rho in rhodata:
        if isHis:
            idx = rho[0][-len(rho[2]):]
        else:
            idx = rho[0][-len(rho[1]):]
        trace = go.Scatter(
            x=idx,
            y=rho[2] if isHis else rho[1],
            name=rho[3],
        )
        data.append(trace)

    layout = go.Layout(
        margin=go.layout.Margin(
            b=50,
            t=25,
            pad=4
        ),
        yaxis=dict(
            title='Correlation'
        ),
        showlegend=True,
    )

    fig = go.Figure(data=data, layout=layout)
    div = plotly.offline.plot(fig,
                              output_type='div',
                              auto_open=False,
                              show_link=False)

    return div

def getspotdiv(spotdata):
    data = []
    for spot in spotdata:
        idx = spot[0].index
        trace = go.Scatter(
            x=idx,
            y=spot[0]['price'],
            name=spot[1],
        )
        data.append(trace)

    layout = go.Layout(
        margin=go.layout.Margin(
            b=50,
            t=25,
            pad=4
        ),
        yaxis=dict(
            title='Spot Price',
            type='log',
            tickformat=",.2r"
        ),
        showlegend=True,
    )

    fig = go.Figure(data=data, layout=layout)
    div = plotly.offline.plot(fig,
                              output_type='div',
                              auto_open=False,
                              show_link=False)

    return div
