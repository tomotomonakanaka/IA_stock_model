import datetime
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
import pickle

start = datetime.date(2000,1,1)
end = datetime.date.today()

# topix銘柄を東証のファイルから取得
df_company = pd.read_excel('data/data_j.xls', sheet_name=0, index_col=0)
df_company = df_company.reset_index()
df_company = df_company.rename(columns={'コード':'code', '銘柄名':'name', '市場・商品区分':'market', '33業種区分':'cat33', '17業種区分':'cat17', '規模区分':'scale'})
df_company = df_company[['code','name', 'market', 'cat33', 'cat17', 'scale']]
df_company = df_company[df_company['scale'].str.contains('TOPIX')]
# df_company = df_company[~df_company['scale'].str.contains('TOPIX Small')]

# 企業の株価時系列
code_ids = df_company.code.unique()
closes_dict = {}
for code_id in code_ids:
    print(code_id)
    try:
        df_id = web.DataReader('{}.T'.format(code_id), 'yahoo', start, end)
    except:
        print(code_id)
    df_id = df_id.reset_index()
    closes = []
    for i in range(0, 23):
        for j in range(1, 12):
            date_1 = '20{:02}-{:02}-01'.format(i, j)
            closes_exist = df_id[df_id.Date<=date_1]['Adj Close'].to_numpy()
            if len(closes_exist) == 0:
                closes.append(None)
            else:
                closes.append(closes_exist[-1])
    closes_dict[code_id] = closes

# マクロ指標
for code_id in ['^N225', 'USDJPY=X', 'CL=F', '^TNX']:
    try:
        df_id = web.DataReader('{}'.format(code_id), 'yahoo', start, end)
    except:
        print(code_id)
    df_id = df_id.reset_index()
    closes = []
    for i in range(0, 23):
        for j in range(1, 12):
            date_1 = '20{:02}-{:02}-01'.format(i, j)
            closes_exist = df_id[df_id.Date<=date_1]['Adj Close'].to_numpy()
            if len(closes_exist) == 0:
                closes.append(None)
            else:
                closes.append(closes_exist[-1])
    closes_dict[code_id] = closes

# closes dictを保存
with open("data/closes_dict.pickle", "wb") as tf:
    pickle.dump(closes_dict,tf)