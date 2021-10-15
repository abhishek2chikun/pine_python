from functions import *

import numpy as np

def Find_signals(Data,Symbol):

	close=Data.Close

	high=Data.High

	low=Data.Low

	open=Data.Open

	print(Symbol,":")

	
	# //@version=4
	# study(title="Stochastic RSI", format=format_price, precision=2, resolution="")
	smoothK = Input(3, "K", minval=1)
	smoothD = Input(3, "D", minval=1)
	lengthRSI = Input(108, "RSI Length", minval=1)
	lengthStoch = Input(108, "Stochastic Length", minval=1)
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
	fig,axs=mpf.plot(Data,addplot=indicator,tight_layout=True,returnfig=True)
	plt.show()
	return 'Done'
Find_signals.Indicator = []