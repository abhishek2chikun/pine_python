import pandas as pd
import mplfinance as mpf
import matplotlib.animation as animation

idf = pd.read_pickle('~/python_venv/Dev/spain/pine_python/Yahoo_data/BVHBB.pkl')
idf.shape
idf.head(3)
idf.tail(3)
#df = idf.loc['2011-07-01':'2011-12-30',:]

fig = mpf.figure(style='charles',figsize=(7,8))
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(3,1,3)

def animate(ival):
    if (20+ival) > len(idf):
        print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            exit()
        return
    data = idf.iloc[0:(20+ival)]
    ax1.clear()
    ax2.clear()
    mpf.plot(data,ax=ax1,volume=ax2,type='candle')

ani = animation.FuncAnimation(fig, animate, interval=250)

mpf.show()
