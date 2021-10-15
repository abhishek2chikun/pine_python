from textwrap import indent
import pandas as pd
import streamlit as st
import glob
import matplotlib.pyplot as plt 
import base64
import os
import datetime
import time
import talib 
import numpy as np
#from fun_st import *
import mplfinance as mpf

src = pd.DataFrame()
color = 'Default'
color_lime = 'lime'
color_red = 'red'
shape_circle = 'o'
shape_square = 's'
location_bottom = 'bottom'
size_tiny = 'tiny'

fig,ax = plt.subplots()
indicator = []
def Input(value,title=None,minval=None): 
    return {'key':title,'value':value,'minval':minval}


def rsi(close,window_length):
   
    return talib.RSI(close['value'],window_length['value'])

def stoch(rsi1,rsi2,rsi3,window_length):
   
    return talib.STOCH(rsi1,rsi2,rsi3,window_length['value'])
   
       
def sma(close,window_length): 
    if window_length['key'] == 'K': 
        return talib.SMA(close[0],window_length['value'])
    # elif window_length['key'] == 'D': return talib.SMA(close
    # [0],window_length['value'])
    else: 
        return talib.SMA(close,window_length['value'])

def plot(value, title, color):
    #return ax.plot(value)
    #return indicator.append(mpf.make_addplot(value,type='line',panel=1))
    pass
def hline(value, title, color):
    #ax.axhline(y=value)
    return {'title':title,'value':value,'color':color}

def fill(h0, h1, color='blue', transp=85, title="Background"):
    

    #return ax.axhspan(h0['value'], h1['value'],color='red',alpha=0.1)
    pass


def plotshape(value,title,  color, style, location, transp, size, text):
    x=np.where(value)[0]
    y=np.zeros(len(np.where(value)[0]),dtype='int')
    global indicator
    
    #mpf.make_addplot(signal,type='scatter',markersize=200,marker='^')

    #return ax.scatter(x,y,color=color,marker=style)
    indicator.append(mpf.make_addplot(x,type='scatter',markersize=200,marker=style,panel=1))
def alertcondition(value,title="Compra", message='Compra'):
    for i,j in zip(value.index,value):
        if j == True and i > (datetime.datetime.now().date()-datetime.timedelta(30)):
            print(message,i)
        else:
            continue
        
def highest(src,length=None):
    if length!= None:
        return min(src[:length])
    return src['high'][:length]

def atr(timeperiod,src=src):
    return talib.ATR(src.high, src.low, src.close, timeperiod)

def ema(src,length):
    return talib.EMA(src,length)



st.set_option('deprecation.showPyplotGlobalUse', False)


import streamlit.components.v1 as components
st.set_page_config(layout="wide")


Data = pd.read_pickle('~/python_venv/Dev/spain/pine_python/Yahoo_data/NCPL.pkl')

#fig,ax = plt.subplots()


close=Data.Close

high=Data.High

low=Data.Low

open=Data.Open

#print(Symbol,":")

st.text("Hello")
# //@version=4
# study(title="Stochastic RSI", format=format_price, precision=2, resolution="")
smoothK = Input(3, "K", minval=1)
smoothD = Input(3, "D", minval=1)
lengthRSI = Input(10, "RSI Length", minval=1)
lengthStoch = Input(10, "Stochastic Length", minval=1)
src = Input(close, title="RSI Source")
rsi1 = rsi(src, lengthRSI)
k = sma(stoch(rsi1, rsi1, rsi1, lengthStoch), smoothK)
d = sma(k, smoothD)
plot(k, "K", color=color)
plot(d, "D", color=color)
h0 = hline(80, "Upper Band", color=color)
h1 = hline(20, "Lower Band", color=color)
fill(h0, h1, color=color, transp=85, title="Background")
hline(0, "Lower Band", color=color)
hline(100, "Lower Band", color=color)
hline(50, "Lower Band", color=color)

a7 = k == 0
plotshape(a7,title="blanco 1", color = color_lime, style=shape_circle, location=location_bottom, transp=0, size=size_tiny, text="0")
a8 = k == 100
plotshape(a8,title="blanco 1", color = color_red, style=shape_circle, location=location_bottom, transp=0, size=size_tiny, text="100")

alertcondition(a7,title="Compra", message='Compra')
alertcondition(a8,title="Venta", message='Venta')
#print(indicator)
ax= mpf.plot(Data,addplot=indicator)
plt.show(fig)