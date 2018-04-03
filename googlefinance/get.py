# based on : https://github.com/pdevty/googlefinance-client-python
# get  url : https://finance.google.com/finance/getprices?q=LHA&p=10Y&f=d,c,h,l,o,v
# https://gist.github.com/lebedov/f09030b865c4cb142af1


def get(code):
    print(code)


# Yahoo finance 모듈 활용하기
def get_data_yahoo(code, start_date=False, end_date=False):

    if end_date == False:
        from datetime import datetime
        end_date = str(datetime.now().date())

    if start_date == False:
        start_date = '2010-01-01'

    from pandas_datareader import data
    import fix_yahoo_finance as yf
    yf.pdr_override()
    stock = data.get_data_yahoo(code, start_date, end_date)
    return stock



# single code, [codes] both possible
def get_data(codes, period='30d', interval="86400"):

    # single code to DataFrame
    def code_to_dataframe(code, period = "30d", interval="86400"):

        if period[-1] not in ['d','M','Y']:
            print('Option Error : period option is Not in { d :day, M : month, Y : year }')
            return

        if type(code) != str:
            print('''Input Error : please use the .get() function, this is for only single code..''')

        import requests
        from datetime import datetime
        import pandas as pd

        # input the 'codes' by KRX:005930

        split_code = code.split(':')

        # build the Query
        query = { 'x' : split_code[0],   # exchange     ex) "NASD", "KRX", "KOSDAQ"
                  'q' : split_code[1],   # company code ex) "gogl", "MSFT"
                  'i' : interval,        # interval time : 60 sec X n
                  'p' : period }         # Total period  : {"1Y" : 1 year, "30d" : 30 days}  cf) 30D is error
        response = requests.get("https://finance.google.com/finance/getprices", params=query)
        lines    = response.text.splitlines()  # json data split to [list]

        data, index, basetime     = [], [], 0
        for price in lines:
            cols = price.split(",")
            if cols[0][0] == 'a':
                basetime = int(cols[0][1:])
                index.append(datetime.fromtimestamp(basetime))
                data.append([float(cols[4]), float(cols[2]), float(cols[3]), float(cols[1]), int(cols[5])])
            elif cols[0][0].isdigit():
                date = basetime + (int(cols[0])*int(query['i']))
                index.append(datetime.fromtimestamp(date))
                data.append([float(cols[4]), float(cols[2]), float(cols[3]), float(cols[1]), int(cols[5])])
        df = pd.DataFrame(data, index = index, columns = ['Open', 'High', 'Low', 'Close', 'Volume'])
        df.insert(0,'Code',code)

        # If you set the 'interval' by day..
        # just printed the Date infomation
        if int(interval) >= 86400:
            df          = df.reset_index()                          # datetimeindex to columns data
            df['index'] = df['index'].apply(lambda x : x.date())    # index is'n using the .apply()
            df          = df.set_index('index')                     # set back to index
            df.index    = pd.to_datetime(df.index)              # set the attribute to datatimeindex
            df.index.name  = 'Date'
        return df


    # checking the "codes" is 'single code'
    if type(codes) == str:
        return code_to_dataframe(codes, period)

    # checking the "codes" is [list] type
    if type(codes) != list  or  type(codes[0]) != str:
        print("Input Error : 'code' is not a [list] or 'single code' ")
        return

    import pandas as pd
    prices_data = pd.DataFrame()
    for code in codes:
        df = code_to_dataframe(code, period)
        prices_data = pd.concat([prices_data, df[~df.index.duplicated(keep='last')]], axis=0)
    return prices_data



if __name__ == '__main__':

    # <Parmetor's>
    #
    # codelist download : http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download
    #
    # 1. code = 'NASDAQ: code list'
    #
    # 2. period = '30d': 30 days (default)
    #             '1M' : Month
    #             '1Y' : year
    #
    # 3. interval = 86400 : 1 day (default)
    #               60 * integer (seconds)


    # based on : https://github.com/pdevty/googlefinance-client-python
    # edited merged on sigle function
    # and covert to the simple text input query  (same as Google finance site's format)
    #


    # 1. Import googlefinance.get
    # input the Codes by [list]
    from googlefinance.get import get_data

    df = get_data(['KRX:005930',
                   'KOSDAQ:091990',
                   'NASDAQ:TSLA',
                   'NASDAQ:AMZN'], period='2M')
    print(df.shape)
    df.head()

    # (154, 6)
    #     Code    Open    High    Low     Close   Volume
    # Date
    # 2018-02-05  KRX:005930  2325000.0   2416000.0   2300000.0   2396000.0   516513
    # 2018-02-06  KRX:005930  2330000.0   2396000.0   2329000.0   2371000.0   364291
    # 2018-02-07  KRX:005930  2412000.0   2413000.0   2290000.0   2290000.0   465246
    # 2018-02-08  KRX:005930  2306000.0   2331000.0   2299000.0   2300000.0   448981
    # 2018-02-09  KRX:005930  2222000.0   2259000.0   2221000.0   2235000.0   339916


    # 2. filtering by Code
    df[df.Code == 'NASDAQ:TSLA'].head()

    #     Code    Open    High    Low     Close   Volume
    # Date
    # 2017-04-04  NASDAQ:AMZN     888.00  893.4900    885.4200    891.51  3422328
    # 2017-04-05  NASDAQ:AMZN     891.50  908.5384    890.2800    906.83  4984656
    # 2017-04-06  NASDAQ:AMZN     910.82  923.7200    905.6200    909.28  7508370
    # 2017-04-07  NASDAQ:AMZN     913.80  917.1899    894.4927    898.28  6344065
    # 2017-04-08  NASDAQ:AMZN     899.65  900.0900    889.3100    894.88  3710922


    # 3. googlefinance.get
    # input the Single Code

    df = get_data('NASDAQ:AMZN',
                   period='1Y')
    df.head()
    #     Code    Open    High    Low     Close   Volume
    # Date
    # 2017-04-04  NASDAQ:AMZN     888.00  893.4900    885.4200    891.51  3422328
    # 2017-04-05  NASDAQ:AMZN     891.50  908.5384    890.2800    906.83  4984656
    # 2017-04-06  NASDAQ:AMZN     910.82  923.7200    905.6200    909.28  7508370
    # 2017-04-07  NASDAQ:AMZN     913.80  917.1899    894.4927    898.28  6344065
    # 2017-04-08  NASDAQ:AMZN     899.65  900.0900    889.3100    894.88  3710922


    # 4. googlefinance.get
    # Using Yahoo finance history data API


    # © 2018 GitHub : https://github.com/YongBeomKim