#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 01:08:24 2021

@author: abhishek
"""

#from talib import *
import talib 
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd
#Read Data
color = 'Default'
color_lime = 'lime'
color_red = 'red'
shape_circle = 'o'
shape_square = 's'
location_bottom = 'bottom'
size_tiny = 'tiny'




# def Input(value,title=None,minval=None): 
#     return {'key':title,'value':value,'minval':minval}


# def rsi(close,window_length):
   
#     return talib.RSI(close['value'],window_length['value'])

# def stoch(rsi1,rsi2,rsi3,window_length):
   
#     return talib.STOCH(rsi1,rsi2,rsi3,window_length['value'])
   
       
# def sma(close,window_length): 
#     if window_length['key'] == 'K': 
#         return talib.SMA(close[0],window_length['value'])
#     # elif window_length['key'] == 'D': return talib.SMA(close
#     # [0],window_length['value'])
#     else: 
#         return talib.SMA(close,window_length['value'])

# def plot(value, title, color):
#     return plt.plot(value)

# def hline(value, title, color):
#     plt.axhline(y=value)
#     return {'title':title,'value':value,'color':color}

# def fill(h0, h1, color='blue', transp=85, title="Background"):
    

#     return plt.axhspan(h0['value'], h1['value'],color='red',alpha=0.1)



# def plotshape(value,title,  color, style, location, transp, size, text):
#     x=np.where(value)[0]
#     y=np.zeros(len(np.where(value)[0]),dtype='int')
    
    
    
#     return plt.scatter(x,y,color=color,marker=style)
# def alertcondition(value,title="Compra", message='Compra'):
#     for i,j in zip(value.index,value):
#         if j == True and i > (datetime.datetime.now().date()-datetime.timedelta(30)):
#             print(message,i)
#         else:
#             continue
        
# def highest(src,length=None):
#     if length!= None:
#         return min(src[:length])
#     return src['high'][:length]

# def atr(timeperiod,src=src):
#     return talib.ATR(src.high, src.low, src.close, timeperiod)

# def ema(src,length):
#     return talib.EMA(src,length)


class Function:
    def __init__(self):
        self.Indicator = []
        self.Message = []


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
        #return plt.plot(value)
        self.indicator.append(mpf.make_addplot(value,type='line',panel=1))
        #pass
    def hline(value, title, color):
        self.indicator.append(mpf.make_addplot([value for i in range(Data.shape[0])],panel='lower',secondary_y=False))
        return {'title':title,'value':value,'color':color}

    def fill(h0, h1, color='blue', transp=85, title="Background"):
        

        #return plt.axhspan(h0['value'], h1['value'],color='red',alpha=0.1)
        pass

    #a=None
    def plotshape(value:list,title,  color, style, location, transp, size, text):
        
        x = []
        c =0
        for i,j in value.iteritems():
            print("i:",j)
            if j == True:
                x.append(1)
                c+=1
            else:
                x.append(np.nan)
        #y=np.zeros(len(np.where(value)[0]),dtype='int')
        #print("x:",x)
        #if len(x) > 0:

        if c!=0:
            self.indicator.append(mpf.make_addplot(x,type='scatter',markersize=60,marker=style,panel=1))
        
        #return plt.scatter(x,y,color=color,marker=style)
    def alertcondition(value,title="Compra", message='Compra'):
        for i,j in zip(value.index,value):
            if j == True and i > (datetime.datetime.now().date()-datetime.timedelta(300)):
                print(message,i)
                self.Message.append({message:i})
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








"""
The most important, apart from the standard:pivothigh, pivotlow, barssince, offset, line.new, nz, input, ema, atan, highest, lowest, abs, plotshape, plot, atr, hline, label.new, valuewhen, sar, max, min, na, barcolor

float, if, and, or, var, var line, var label, not, var bool, bool

high, close, open, low,

<, >, =, ==, >=, <=, !=, ?, [], :, :=
"""