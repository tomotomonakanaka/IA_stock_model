import datetime
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf

# topix銘柄を東証のファイルから取得
df_company = pd.read_excel('data/data_j.xls', sheet_name=0, index_col=0)
df_company = df_company.reset_index()
df_company = df_company.rename(columns={'コード':'code', '銘柄名':'name', '市場・商品区分':'market', '33業種区分':'cat33', '17業種区分':'cat17', '規模区分':'scale'})
df_company = df_company[['code','name', 'market', 'cat33', 'cat17', 'scale']]
df_company = df_company[df_company['scale'].str.contains('TOPIX')]
df_company = df_company[~df_company['scale'].str.contains('TOPIX Small ')]

# for loop
code_ids = df_company.code.to_numpy()
df_fs = pd.DataFrame()
for code_id in code_ids:
    print(code_id)
    ticker = yf.Ticker(str(code_id)+".T")
    pnl = ticker.financials
    pnl.index = pnl.index + ' pnl'
    bs = ticker.balancesheet
    bs.index = bs.index + ' bs'
    cf = ticker.cashflow
    cf.index = cf.index + ' cf'
    fs = pd.concat([pnl, bs, cf])
    fs = fs.T.rename_axis('year').reset_index()
    fs['code'] = str(code_id)

    # for concatenation
    fs = fs.set_index(['year', 'code'])

    # concat
    df_fs = pd.concat([df_fs, fs], axis=0)


df_fs.to_pickle('data/df_fs.pickle')