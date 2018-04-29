## SK 하이닉스를 활용한 BackTesting

<img src="https://github.com/YongBeomKim/FinanceBasic2018/raw/master/data/MMCA.png"/><br>


## PortFolio 최적 분포비율 계산

<img src="https://github.com/YongBeomKim/FinanceBasic2018/raw/master/data/portfolio.png"/><br>


## Tesla 주가 패턴 예측 (Prophet (R))

<img src="https://github.com/YongBeomKim/FinanceBasic2018/raw/master/data/tesla-prophetR.png" width="300"\><br>




# 파이썬을 활용한 금융데이터 다루기


## 강의의 목표

본 강의의 목적은 공개 오픈소스 툴인 파이썬 언어의 기초를 익히고, 이를 활용하여 Pandas 모듈을 활용하여 다양한 금융 기술적 분석 능력을 스스로 갖출 수 있도록 실습과 이론을 통하여 배울 수 있도록 하는 것입니다. 본 강의를 통해 수강생들이 단순한 실습만아니라 실제적으로 각자의 업무에 어떻게 파이썬을 적용해야 할지 실무적 아이디어를 얻어 가시기를 바랍니다.


## 과정 상세

금융데이터 분석을 진행하면서 Pandas, Tensorflow, Scikit-Learn, Keras 등 적용 가능한 모듈의 종류와 수는 상당히 많고, 이들이 새로운 버젼이 제공될때마다 관련 코드의 내용이 달라짐에 따라 유연한 대처를 못함으로써 곤란함을 격는 경우를 많이 봤습니다 

이러한 경험에 비추어 봤을때 다양한 모듈을 맛보기 식으로 진행하기 보다는, 기본 이론을 익힌 뒤 Pandas 모듈을 활용한 금융데이터 다루기(시계열 데이터 다루기)를 집중적으로 진행합니다 

이를 위해 먼저 파이썬의 기본적인 객체와 함수들에 대한 내용을 학습합니다. 이를 바탕으로 **Pandas** 모듈을 활용한 시계열 금융 데이터를 다루는 방식을 학습함으로써 기본개념들이 각각의 모듈에 어떤 방식으로 적용되는지를 익히는 과정을 진행합니다.

Pandas로 생성한 DataFrame을 바탕으로 시각화, BackTesting, Risk관리를 위한 포트폴리오 구성비율 예측 그리고 머신러닝 기본 이론을 적용한 '종가 데이터를 활용한 주가예측'을 진행합니다

종가를 활용한 주가 예측은 'hidden Markov model', 'ARIMA'시계열 패턴 예측, Prophet (R) 모듈의 활용 및 Keran LSTM을 활용하여 미래의 주가 패턴을 예측까지 진행합니다.

대표적인 모듈인 Pandas 내용을 통해서 Python의 기본 철학에 익숙해 지신다면, 다른 어떠한 모듈에 대해서도 두려움 없이 접근하고 학습의 방향을 스스로 잡는 능력을 배양할 기회가 될것입니다.


## 수강 대상
    Pandas 모듈을 활용한 시계열 데이터를 다루기 원하시는 분 

Python을 활용한 시계열 데이터를 다루기 원하시는 금융 업계 종사자

    스스로 금융 분석을 위한 Simulation을 구현하기 원하는 분

독자적 투자 시스템을 구축하기 위한 기술과 이론에 대한 실습을 통해 핵심 내용을 알려드립니다.

    투자 또는 금융 데이터 분석에 기본적인 머신러닝 이론을 적용해 보고 싶은 분

Python 을 통한 금융 투자 분석과 투자 기회에 인사이트를 얻고자 하는 금융 업계 종사자



## 수업내용

### Python 기초 및 객체 다루기

### Pandas 기초 및 시계열 데이터 다루기

### 금융데이터 분석
1. 종목간 상관성 분석
2. Value at Risk
3. 이평선 활용한 수익률 분석
4. 몬테카를로 시뮬레이션을 활용한 최적의 포트폴리오 찾기
5. 다양한 기술적 보조지표 생성
    1. Stochastic Oscillator
    2. RSI(Relative Strength Index : 상대강도지수)
    3. 볼린저 밴드
    4. MACD(moving average convergence/divergence)

### 금융데이터 예측
1. 은닉마르코프 모델을 활용 (HMM)
1. ARIMA 시계열 분석을 활용한 주가 예측
2. Prophet (R) 활용한 주가예측
3. Keras 의 LSTM 모델을 활용한 주가예측



## Python 기본 내용 및 Pandas 요약 

### **Data & Datum**
1. Datum(숫자, "문자"), Data([list], {dict}, (tuple,))
1. (기본/외부/사용자) 모듈, 함수, 메소드
1. []의 문자에서 활용( [index], [:slicing]), 함수를 활용{for : 반복, if :판단, enumerate() :순번 integer 출력}
1. 재무제표 Web Crawling ==> type 변경 ==> 시각화
1. ndarray, Series, Dataframe

### **Pandas Series**
1. pd.Series( [ data ] , index = [ index ])
1. series 사칙연산
1. series [ Boolean 판단문 ]
1. series.index = [ list ]
1. series.isnull()
1. series.drop()

### **Pandas DataFrame**
1. pd.DataFrame( { columns :  [ data ] , columns :  [ data ] } )
1. pd.to_datetime()
1. df.rename( columns = { 기존 column , 새로운 column } )
1. df.insert( 컬럼순서,  컬럼명 ,  data )
1. df.column이름 &nbsp; | &nbsp; df['column이름']
1. df [ index Slicing ]
1. df.iloc[ index slicing,  column slicing ]
1. df.reset_index()        :  index  -> column
1. df.set_index( '컬럼명' ) :  column -> index
1. df.sort_index()
1. df.sort_value()
1. df[ boolean 함수 ]
1. df[ boolean 함수 ].column이름
1. axis = 0 : index | axis = 1 : column
1. df.drop( 'index이름'  , axis = 0 )
1. df.drop( 'column이름' ,  axis = 1 )
1. df.index.tolist()
1. df.column.tolist()
1. df.apply(lambda x: x ** 2)  
1. pd.pivot_table(df,index = [], values = [], aggfunc = [], margins = True)

### **Pandas DataFrame Static**
1. .count()
1. .describe()
1. .min()     .max()
1. .idxmin()  .idxmax()
1. .quantile()   
1. .sum()
1. .mean()    .median()
1. .var() 분산 .std() 정규분산
1. .cumsum()  .cumprod()  누적 합    누적 곱
1. .cummin()  .cummax()   누적최소값, 누적최대값

### **Pandas Series & DataFrame 결측치 제어하기**
1. df.dropna()
1. df.fillna(method='ffill',  limit=2)  # 결측치 대체
1. df.fillna(df.mean()['컬럼명'])   
1. Series.interpolate(method='time')    # 결측치 보간 (시계열적 특성을 부여가능)
1. Series.interpolate(method='values', limit=1, limit_direction='backward') # 'forward','backward','both'

### **Pandas Series map, reduce, lambda, filter**
1. map & lambda : map(lambda x : str(x), [list])
1. map & lambda : list(map(lambda x : str(x), [list]))
1. map & lambda : <strike>[ map(lambda x : str(x), data) ]</strike>
1. Series & lambda : Series.apply(lambda x : str(x))
1. filter & lambda : list(filter(lambda x : x % 2 == 0,  data))
1. <strike>filter</strike> & DataFrame : DataFrame[ Series % 2 == 0 ]
1. reduce & lambda : reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])      # 데이터 차원축소

### **TimeSeries 시계열 데이터 다루기**
1. from datetime import datetime
1. pandas.date_range(end = '2017-07-01', periods=30, freq='BM')  
1. pandas.date_range('2017/8/8 09:09:09', periods=5, normalize=True)
1. [str(date.date()) &nbsp;&nbsp; for &nbsp;&nbsp; date &nbsp;&nbsp; in &nbsp;&nbsp; pd.date_range('2017/01/01', '2017/01/11')]