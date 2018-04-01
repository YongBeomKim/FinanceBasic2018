# based on : https://github.com/pdevty/googlefinance-client-python
# get  url : https://finance.google.com/finance/getprices?q=LHA&p=10Y&f=d,c,h,l,o,v
# https://gist.github.com/lebedov/f09030b865c4cb142af1


# single code, [codes] both possible
def get_finance(codes, period='30d', interval="86400"):

    # single code to DataFrame
    def code_to_dataframe(code, period = "30d", interval="86400"):

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

    # based on : https://github.com/pdevty/googlefinance-client-python
    # edited merged on sigle function
    # and covert to the simple text input query  (same as Google finance site's format)
    #
    # Default setting is...
    # period : 30 day's,
    # invertal : 1 day (closed time)


    # 1. single code's DataFrame

    df = get_finance("KRX:005930",
                     period='1Y',     # total period
                     interval='300')  # data interval (step by : 60 sec * n)
    print(df)

    #                            Code       Open       High        Low      Close  \
    # 2018-02-12 09:05:00  KRX:005930  2255000.0  2258000.0  2252000.0  2254000.0
    # 2018-02-12 09:10:00  KRX:005930  2254000.0  2260000.0  2253000.0  2259000.0
    # 2018-02-12 09:15:00  KRX:005930  2259000.0  2271000.0  2259000.0  2263000.0

    #                      Volume
    # 2018-02-12 09:05:00   35993
    # 2018-02-12 09:10:00   11044
    # 2018-02-12 09:15:00    9902


    # 2. Codes DataFrame (.get is Both usable)

    df = get_finance(["INDEXDJX:.DJI",
                      "INDEXNYSEGIS:NYA",
                      "KRX:005930",
                      "KOSDAQ:053800"], period='30d', inverval='300')
    print(df)

    #                               Code      Open      High       Low     Close  \
    # 2016-03-29 05:00:00  INDEXDJX:.DJI  17526.08  17583.81  17493.03  17535.39
    # 2016-03-30 05:00:00  INDEXDJX:.DJI  17512.58  17642.81  17434.27  17633.11
    # 2016-03-31 05:00:00  INDEXDJX:.DJI  17652.36  17790.11  17652.36  17716.66

    #                         Volume
    # 2016-03-29 05:00:00   70452434
    # 2016-03-30 05:00:00   86159775
    # 2016-03-31 05:00:00   79326225

    # © 2018 GitHub : https://github.com/YongBeomKim