
# ========================= Dart 기업정보 수집하기 ============================
# https://datascienceschool.net/view-notebook/adead36729704e7b8660dda3be6a6524/

def get_dart(code):

    import requests, json
    import pandas as pd
    key_name = { "acc_mt" : "결산월(MM)",
                 "bsn_no" : "사업자등록번호",
                 "adr"    : "주소",
                 "crp_cls" : "법인구분",  # : Y(유가), K(코스닥), N(코넥스), E(기타)
                "crp_no"  : "법인등록번호",
                "ceo_nm"  : "대표자명",
                "crp_nm"  : "정식명칭",
                "crp_nm_e" : "영문명칭",
                "crp_nm_i" : "약식명칭",
                "err_code" : "에러코드",
                "err_msg" : "에러메시지",
                "est_dt" : "설립일",
                "fax_no" : "팩스번호",
                "hm_url" : "홈페이지",
                "ind_cd" : "업종코드",
                "ir_url" : "IR홈페이지",
                "stock_cd" : "종목코드",
                "phn_no" : "전화번호"}

    url        = "http://dart.fss.or.kr/api/company.json?auth={0}&crp_cd={1}"
    url        = url.format("8e30368d048361ba865f916c30739160a0e58ddd", code)
    response   = requests.get(url)
    response   = json.loads(response.content)
    df         = pd.DataFrame( list( response.items() ) )
    df[0]      = [ key_name[k]    for  k  in  df[0] ]
    df.columns = ['설명','내용']
    return  df




# ==================   기업의 세부정보 수집하기 =========================
# ================== http://marketdata.krx.co.kr/ =======================
def get_data_info():
    # 기업정보 수집하기 | http://kind.krx.co.kr/corpgeneral/corpList.do
    import requests
    import numpy as np
    import pandas as pd
    from io import BytesIO
    url  = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    data = {'method':'download',
            'orderMode':'1',           # 정렬컬럼
            'orderStat':'D',           # 정렬 내림차순
            'searchType':'13',         # 검색유형: 상장법인
            'fiscalYearEnd':'all',     # 결산월: 전체
            'location':'all',}         # 지역: 전체
    r   = requests.post(url, data = data)
    f   = BytesIO(r.content)           # HTML String을 HTML binary로 변환
    dfs = pd.read_html(f, header = 0, parse_dates = ['상장일'])
    df  = dfs[0].copy()
    # 종목코드를 앞자리가 0인 6자리 문자로 변환
    df['종목코드'] = df['종목코드'].astype(np.str)
    df['종목코드'] = df['종목코드'].str.zfill(6)
    return df


# 기업의 시장정보 수집
# http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx
def get_data_price(date=None, market = 'ALL'):
    import requests
    import pandas as pd
    from io import BytesIO
    from datetime import datetime
    if date == None:
        date = datetime.today().strftime('%Y%m%d')  # 오늘 날짜

    # Post 정보 접속 : OTP Code 정보값  및 header 삽입
    headers               = requests.utils.default_headers()
    headers['User-Agent'] = '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'''
    gen_otp_url  = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
    gen_otp_data = {'name'         : 'fileDown',
                    'filetype'     : 'xls',
                    'market_gubun' : market,     # 'STK':코스피 추출
                    'url'          : 'MKD/04/0404/04040200/mkd04040200_01',
                    'indx_ind_cd'  : '', 'sect_tp_cd'   : '',
                    'schdate'      : date,
                    'pagePath'     : '/contents/MKD/04/0404/04040200/MKD04040200.jsp', }
    r                     = requests.post(gen_otp_url, gen_otp_data, headers=headers)
    OTP_code              = r.content

    # AJAX 분석결과로 xls 다운로드
    down_url  = 'http://file.krx.co.kr/download.jspx'
    down_data = {'code': OTP_code}
    r         = requests.post(down_url, down_data)
    df        = pd.read_excel(BytesIO(r.content), header=0, thousands=',')
    return df


# KRX & KOSDAQ code 확인
def get_data_codes():

    def get_data_price(date=None, market = 'ALL'):
        import requests
        import pandas as pd
        from io import BytesIO
        from datetime import datetime
        if date == None:
            date = datetime.today().strftime('%Y%m%d')  # 오늘 날짜

        # Post 정보 접속 : OTP Code 정보값  및 header 삽입
        headers               = requests.utils.default_headers()
        headers['User-Agent'] = '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'''
        gen_otp_url  = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
        gen_otp_data = {'name'         : 'fileDown',
                        'filetype'     : 'xls',
                        'market_gubun' : market,     # 'STK':코스피 추출
                        'url'          : 'MKD/04/0404/04040200/mkd04040200_01',
                        'indx_ind_cd'  : '', 'sect_tp_cd'   : '',
                        'schdate'      : date,
                        'pagePath'     : '/contents/MKD/04/0404/04040200/MKD04040200.jsp', }
        r                     = requests.post(gen_otp_url, gen_otp_data, headers=headers)
        OTP_code              = r.content

        # AJAX 분석결과로 xls 다운로드
        down_url  = 'http://file.krx.co.kr/download.jspx'
        down_data = {'code': OTP_code}
        r         = requests.post(down_url, down_data)
        df        = pd.read_excel(BytesIO(r.content), header=0, thousands=',')
        return df

    krx   = get_data_price().iloc[:,:2]              # 상장기업 모든목록
    kospi = get_data_price(market='STK').iloc[:,:2]  # 상장사  기업목록

    # Kosdaq 코드만 수집
    import pandas as pd
    kosdaq_code = [ code   for code      in  krx['종목코드']
                           if  code  not in  list(kospi['종목코드']) ]

    kosdaq_ = [krx[krx['종목코드'] == code]  for code in kosdaq_code]
    kosdaq  = pd.concat(kosdaq_, axis = 0)
    kosdaq  = kosdaq.reset_index(drop = True)  # 인덱스 숫자를 재정렬

    # 코스닥 기업목록 생성하기
    kosdaq['google'] = ['KOSDAQ:'+code   for code in kosdaq.종목코드]
    kosdaq['yahoo']  = [code + '.KQ'     for code in kosdaq.종목코드]

    # 상장사 기업목록 생성하기
    kospi['google'] = ['KRX:'+code  for code in kospi.종목코드]
    kospi['yahoo']  = [code+'.KS'   for code in kospi.종목코드]
    krx = pd.concat([kospi, kosdaq], axis=0)
    return krx