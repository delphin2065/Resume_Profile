from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import openpyxl

# 獲利能力分析 profitAbility
def profitAbility(p):
    stockID = p
    url =  "https://fubon-ebrokerdj.fbs.com.tw/z/zc/zce/zce_" + str(stockID) + ".djhtm"
    params = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    res = requests.get(url, headers = params)
    soup = BeautifulSoup(res.text, 'lxml')

    tr = soup.find_all('tr')
    dfn = pd.DataFrame()
    for k in range(11):
        list_data = []
        for i in tr[5:-2]:
            td = i.find_all('td')  
            list_data.append(td[k].text)
        df = pd.DataFrame(list_data[1:], columns=[list_data[0]])            
        dfn = pd.concat([dfn, df], axis=1)

    stockName = soup.find('td', attrs={"class": "t10"}).text
    stockName = stockName.split('獲利能力分析')[0]
    dfn.insert(1, '個股名稱', stockName)
    return dfn.to_excel(stockName + '獲利能力分析.xlsx', index=False)
    

# 經營績效 operationPerform
def operationPerform(p):
    stockID = p
    url = "https://fubon-ebrokerdj.fbs.com.tw/z/zc/zcd_" + str(stockID) + ".djhtm"
    params = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    res = requests.get(url, headers = params)
    soup = BeautifulSoup(res.text, 'lxml')

    tr = soup.find_all('tr')
    dfn = pd.DataFrame()
    for k in range(8):
        list_data = []
        for i in tr[4:-2]:
            td = i.find_all('td')
            list_data.append(td[k].text)
        df = pd.DataFrame(list_data[1:], columns=[list_data[0]])            
        dfn = pd.concat([dfn, df], axis=1)

    stockName = soup.find('td', attrs={"class": "t10"}).text
    stockName = stockName.split('之經營績效')[0]
    dfn.insert(1, '個股名稱', stockName)
    return dfn.to_excel(stockName + '之經營績效_季報.xlsx', index=False)


# 財務比率_季度_獲利能力指標
def profitAbilityIndicator(p):
    stockID = p
    url = "https://fubon-ebrokerdj.fbs.com.tw/z/zc/zcr/zcr0.djhtm?b=Q&a=" + str(stockID) 
    params = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    res = requests.get(url, headers = params)
    soup = BeautifulSoup(res.text, 'lxml')

    tr = soup.find_all('div', attrs={"class":"table-row"})
    dfn = pd.DataFrame()
    for k in range(9):
        list_data = []
        for i in tr[:14]:
            td = i.find_all('span', attrs={"class":"table-cell"})
            list_data.append(td[k].text)
        df = pd.DataFrame(list_data[1:], columns=[list_data[0]])            
        dfn = pd.concat([dfn, df], axis=1)

    dfn.drop(df.index[0], inplace=True)
    dfn.reset_index(drop=True, inplace=True)
    stockName = soup.find('div', attrs={"id": "oScrollHead"}).text
    stockName = stockName.split('財務比率')[0]
    stockName = stockName.replace('\r\n', '')

    dfn.insert(1, '個股名稱', stockName)
    return dfn.to_excel(stockName + '獲利能力指標_季報.xlsx', index=False)

