from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from priceSearch import getPrice, portfolioInfo


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/file')
def file():
    return render_template('file.html')

@app.route('/record')
def record():
    return render_template('record.html')

@app.route('/resume')
def record():
    return render_template('resume.html')

@app.route('/priceSearch', methods=['POST', 'GET'])
def priceSearch():
    stockID = request.form.get('uSymb')
    startDate = request.form.get('startDate')
    endDate = request.form.get('endDate')



    if stockID:
        k = stockID
        s = dt.datetime.strptime(startDate, '%Y-%m-%d')
        d = dt.datetime.strptime(endDate, "%Y-%m-%d")
        df = getPrice(k, s, d)
        tables = df.to_html(index=False, classes='table table-success table-striped table-bordered table-responsive')
        return render_template('priceSearch.html', stockPrice = tables)
    else:
        
        return render_template('priceSearch.html', stockPrice = None)

@app.route('/portfolioBackTest', methods=['POST', 'GET'])
def portfolioBackTest():
    initCapital = request.form.get('initCapital')
    startDate = request.form.get('startDate')
    endDate = request.form.get('endDate')
    stockID = request.form.getlist('stockID')
    stockWeight = request.form.getlist('stockWeight')
    stockWeightList = [float(i) for i in stockWeight]
    try:
        if sum(stockWeightList) > 1.0:
            return render_template('portfolioBackTest.html', info = "權重加總大於1.0", list_date = "", list_net = "", list_dd ="")

        dfn = portfolioInfo(initCapital,  startDate, endDate, stockID, stockWeightList)
        

        dfnH = dfn.to_html(index=False, classes='table table-success table-striped table-bordered')
        return render_template('portfolioBackTest.html', info = dfnH, list_date = [i.strftime('%Y-%m-%d') for i in dfn['Date']], list_net = [i for i in dfn['net%']], list_dd = [i for i in dfn['dd%']])
    except:
        pass
    return render_template('portfolioBackTest.html', info="", list_date = "", list_net = "", list_dd ="")

if __name__ == '__main__':
    app.run(debug=True)