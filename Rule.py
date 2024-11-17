#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import mplfinance as mpf


# In[2]:


## drift coefficent
mu = 0.5
## number of steps
n = 10002
## time in years
T = 10
## number of sims
M = 100
# initial stock price
S0 = 100
#volatility
sigma = 0.7


# $$ S_{t} = S_{0}e^{(\mu - \frac{\sigma^2}{2})t + \sigma W_{t}}$$

# In[3]:


## calc ecch time step
dt = T/n

St = np.exp(
    (mu - sigma ** 2 / 2) * dt
    + sigma * np.random.normal(0, np.sqrt(dt), size=(M, n)).T
)

St = np.vstack([np.ones(M), St])

St = S0 * St.cumprod(axis=0)


# In[4]:


time = np.linspace(0, T, n + 1)

tt = np.full(shape=(M, n+1), fill_value=time).T


# In[5]:


plt.plot(tt, St)
plt.show()


# In[6]:


def to_candel(idx, St):
    ts1 = St[:, idx]
    ts1 = ts1.reshape(-1, 7)
    Low = np.min(ts1, axis=1)
    High = np.max(ts1, axis=1)
    Open = ts1[:, 0]
    Close = ts1[:, -1]
    return np.vstack((Open, High, Low, Close))


# In[7]:


def plot(idx, St):
    OHLC = to_candel(idx, St)
    
    # Sample OHLC data without timestamps and volume
    data = {
        'Open':OHLC[0],
        'High':OHLC[1], 
        'Low': OHLC[2], 
        'Close': OHLC[3]
    }
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Create a dummy date range to use as an index
    df.index = pd.date_range(start="2023-01-01", periods=len(df), freq="D")
    
    # Plot the candlestick chart
    # add_plot = mpf.make_addplot(df['Close'], color='blue', linestyle='-')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 5))
    
    mpf.plot(df, type='candle', style='yahoo', ax=ax1)
    ax2.plot(tt, St[:, idx])
    plt.plot()


# In[8]:


plot(1, St)


# In[ ]:





# In[27]:


class STC:
    def __init__(self, mat):
        self.mat = mat
    def get_trend(self, idx):
        if idx > 7:
            return self.mat[3][idx - 8: idx]
        else:
            "pass"
    def get_sub_trend(self, idx, pos):
        x = self.get_trend(idx)[pos: pos + 5]
        return x
    def ap(self, idx, pos):
        return np.mean(self.get_sub_trend(idx, pos))
    def price_trend(self, idx):
        aps = [self.ap(idx, 0),
              self.ap(idx, 1),
              self.ap(idx, 2), 
              self.ap(idx, 3)]
        if (aps[0] < aps[1] < aps[2] < aps[3]):
        # if all(aps[i] < aps[i + 1] for i in range(len(aps) - 1)): 
            return 1
        elif (aps[0] > aps[1] > aps[2] > aps[3]):
            return -1
        else:
            return 0
class S:
    def __init__(self, mat, idx, length):
        self.mat = np.moveaxis(mat, 0, 1)
        self.idx = idx
        self.stc = STC(mat)
        self.length = length
        self.pattern = self.mat[idx:idx + length, :] 
    # def slice(self, length):
    #     return self.mat[self.idx: self.idx + length, :]
    def get_trend(self):
        return self.stc.get_trend(self.idx)
    def values(self, length):
        return self.mat[self.idx - 8: self.idx + length, :]
    def ap(self):
        return self.stc.ap(self.idx)
    def price_trend(self):
        return self.stc.price_trend(self.idx)
    
    def op(self, i):
        return self.pattern[i][0]
    def cp(self, i):
        return self.pattern[i][3]
    def hp(self, i):
        return self.pattern[i][1]
    def lp(self, i):
        return self.pattern[i][2]

    def sli_greater(self, x, y):
        ratio = (x - y) / y
        return 0.003 <= ratio < 0.01
    def ext_near(self, x, y):
        numerator = np.absolute(x - y)
        denominator = np.maximum(x, y)
        return (numerator / denominator) <= 0.003
        
    
    def white_body(self, i):
        return self.pattern[i][0] < self.pattern[i][3]
    def small_body(self, i):
        return self.sli_greater(self.tp_body(i), self.bm_body(i))
    def no_ls(self, i):
        return self.ext_near(self.lp(i), self.bm_body(i))
    
       
    def tp_body(self, i):
        x = np.maximum(self.op(i), self.cp(i))
        return x
    def bm_body(self, i):
        return np.minimum(self.op(i), self.cp(i))
        
    def us(self, i):
        return self.hp(i) - self.tp_body(i)
    def ls(self, i):
        return self.bm_body(i) - self.lp(i)
    def hs(self, i):
        return self.us(i) + self.ls(i)
    def hb(self, i):
        return np.absolute(self.cp(i) - self.op(i))
    

class AdvancedBlock:
    def __init__(self, s):
        self.s = s
    def check(self):
        return (self.s.price_trend() == 1) & self.s.white_body(0) & self.s.white_body(1) & self.s.white_body(2) &\
        (self.s.op(0) < self.s.op(1) < self.s.cp(0)) & \
        (self.s.op(1) < self.s.op(2) < self.s.cp(1)) & \
        (self.s.hs(2) > self.s.hb(2)) & \
        (self.s.hs(1) > self.s.hb(1)) & \
        (self.s.hs(2) > self.s.hs(0)) & \
        (self.s.hs(1) > self.s.hs(0))
        


# In[28]:


class Hammer:
    def __init__(self, s):
        self.s = s
    def check(self):
        return self.s.no_ls()
    


# In[22]:


def print_pattern(temp):
    data = {
            'Open':temp[0],
            'High':temp[1], 
            'Low': temp[2], 
            'Close': temp[3]
        }
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Create a dummy date range to use as an index
    df.index = pd.date_range(start="2023-01-01", periods=len(df), freq="D")
    
    # Plot the candlestick chart
    mpf.plot(df, type='candle', style='yahoo')


# In[26]:


count = 0
for j in range(100):
    mat = to_candel(j, St)
    for i in range(8, mat.shape[1] - 3):
        s = S(mat, idx=i, length=1)
        if s.small_body(0):
            temp = np.moveaxis(s.values(1), 1, 0)
            print_pattern(temp)
        # if AdvancedBlock(s).check() == True:
        #     count = count + 1
        #     temp = np.moveaxis(s.values(3), 1, 0)
        #     print_pattern(temp)
print(count)


# In[ ]:





# In[ ]:





# In[ ]:




