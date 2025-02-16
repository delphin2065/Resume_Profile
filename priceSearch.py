import yfinance as yf
import pandas as pd
import datetime as dt



def getPrice(stockID, startDate, endDate):
   
    start = startDate
    end = endDate
    df = yf.Ticker(stockID).history(start=start, end=end, interval='1d', auto_adjust=False)
    df = df.round(decimals=2)
    df.reset_index(inplace=True, drop=False)
    df['Date'] = df['Date'].apply(lambda x: dt.date.strftime(x, '%Y-%m-%d'))
    list_vol = df['Volume'].apply(lambda x:(x/1000000)).round(decimals=2)
    df.insert(1, "Symbol", stockID)
    try:
        del df['Stock Splits']
        try:
            del df['Capital Gains']
        except:
            pass   
    except:
        del df['Capital Gains']
        try:
            del df['Stock Splits']
        except:
            pass
    finally:
        del df['Volume']
        df.insert(6, 'Volume(Million)', list_vol)
        return df





def portfolioInfo(initCapital,  startDate, endDate, stockID, stockWeightList):
    startDate = dt.datetime.strptime(startDate,'%Y-%m-%d').date()
    endDate = dt.datetime.strptime(endDate,'%Y-%m-%d').date()
    
    i = stockID[0]
    dfn = yf.Ticker(i).history(start=startDate, end=endDate, interval='1d' ,auto_adjust=False)
    dfn.insert(0, "stockID", i)
    dfn[i] = dfn['Adj Close']
    w = stockWeightList[stockID.index(i)]
    dfn[i + '%' + str(w)] = (dfn['Adj Close']/dfn.loc[dfn.index[0],'Adj Close'])*w 
    dfn.index = dfn.index.date
    dfn.insert(0, 'Date', dfn.index)
    dfn = dfn[['Date', i + '%' + str(w)] ]
    dfn.reset_index(inplace=True, drop=True)


    for i in stockID[1:]:
        df = yf.Ticker(i).history(start=startDate, end=endDate, interval='1d' ,auto_adjust=False)
        df.insert(0, "stockID", i)
        df[i] = df['Adj Close']
        w = stockWeightList[stockID.index(i)]
        df[i + '%' + str(w)] = (df['Adj Close']/df.loc[df.index[0],'Adj Close'])*w 
        df.index = df.index.date
        df.insert(0, 'Date', df.index)
        df = df[['Date', i + '%' + str(w)]]
        df.reset_index(inplace=True, drop=True)
        
        dfn = pd.merge(dfn, df, on='Date', how='outer')



    dfn.fillna(method='ffill', inplace=True)
    dfn.dropna(inplace=True, axis=0)
    dfn['portfolio'] = dfn.iloc[:, 1:].sum(axis=1)

    dfn['capital'] = (dfn['portfolio']*float(initCapital))
    dfn['cash'] = float(initCapital)*(1 - sum(stockWeightList))
    dfn['net%'] = (dfn['capital'] + dfn['cash'])/float(initCapital)
    dfn['dd%'] = 0
    for i in range(dfn.shape[0]):
        m = max(dfn.loc[:i, 'net%'])
        dfn.loc[i, 'dd%'] = dfn.loc[i, 'net%'] - m

    
    
    dfn = dfn.round(decimals=4) 
    # dfn.iloc[:,5:] = dfn.iloc[:,5:].round(decimals=1)
    dfn.sort_values(by='Date', ascending=True, inplace=True)
    dfn.reset_index(inplace=True, drop=True)    
    return dfn