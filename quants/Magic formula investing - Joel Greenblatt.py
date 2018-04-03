def introducecompanies():
    '''We introduce the data of the companies and create several dictionaries inside a list'''
    i = int(input("How many companies do you want to analyse?"))
    x=0
    name = []
    while x<i:
        company = input('Please introduce the name of the company: ')
        PE = int(input('Introduce the Earnings yield (1/PER) ratio: '))
        ROCE = int(input("Introduce the ROCE(EBIT/(TotalAssets + WCR)) ratio: "))
        company = {'Company name:' : company.title(),
                'Earnings yield:' : PE,
                'ROCE:': ROCE,
                }
        name.append(company)
        x+=1
    print("These are the companies you have introduced in the program:")
    return name

def workwithdata(name):
    '''We use the data previously introduced to generate the rankings'''
    PE = []
    for item in name:
        PE.append(int(item['Earnings yield:']))
    PE = sorted(PE)
    for item in name:
        x = 0
        for p in PE:
            if item['Earnings yield:'] == p:
                item['PE ranking:'] = int(x +1)
            else:
                x += 1
    ROCE = []
    for item in name:
        ROCE.append(int(item['ROCE:']))
    ROCE = sorted(ROCE)
    for item in name:
        x = 0
        for p in ROCE:
            if item['ROCE:'] == p:
                item['ROCE ranking:'] = int(x + 1)
            else:
                x += 1
    return name

def datapresentation(name):
    '''Finnaly, we present our data ranked from best to worst'''
    for item in name:
        item["Total score:"] = item["ROCE ranking:"] + item["PE ranking:"]
    Ranking = []
    for item in name:
        Ranking.append(int(item["Total score:"]))
    Ranking = sorted(Ranking)
    for rank in Ranking:
        for item in name:
            if item["Total score:"] == rank:
                print(item)
                item["Total score:"] = int(0)
            else:
                continue

name = introducecompanies()
name = workwithdata(name)
datapresentation(name)


