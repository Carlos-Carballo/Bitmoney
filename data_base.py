import datetime as dt
from datetime import datetime, timedelta
import pandas as pd 
import numpy as np
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
import chart_studio.plotly as py
import plotly.graph_objs as go
import chart_studio
import pickle
import quandl
from datetime import datetime
from pandas_datareader import DataReader
chart_studio.tools.set_credentials_file(username='sacbe', api_key='YyuW1xjKew2FpqsOUAvr')


def get_quandl_data(quandl_id):
    '''Download and cache Quandl dataseries'''
    cache_path = '{}.pkl'.format(quandl_id).replace('/','-')
    try:
        f = open(cache_path, 'rb')
        df = pickle.load(f)   
        print('Loaded {} from cache'.format(quandl_id))
    except (OSError, IOError) as e:
        print('Downloading {} from Quandl'.format(quandl_id))
        df = quandl.get(quandl_id, returns="pandas")
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(quandl_id, cache_path))
    return df

exchanges = ['KRAKEN','BITSTAMP']
exchange_data = {}
exchange_data['YAHOO'] = DataReader("BTC-USD", "yahoo", datetime(2014,9,16))
exchange_data['YAHOO'] = exchange_data['YAHOO'][['Open', 'High', 'Low', 'Close', 'Volume','Adj Close']]
exchange_data['YAHOO'] = exchange_data['YAHOO'].rename(columns={'Volume': 'Volume (Currency)'})

for exchange in exchanges:
    exchange_code = 'BCHARTS/{}USD'.format(exchange)
    btc_exchange_df = get_quandl_data(exchange_code)
    exchange_data[exchange] = btc_exchange_df

exchange_data['YAHOO'] = exchange_data['YAHOO'][~exchange_data['YAHOO'].index.duplicated()]

def merge_dfs_on_column(dataframes, labels, col):
    series_dict = {}
    for index in range(len(dataframes)):
        series_dict[labels[index]] = dataframes[index][col]
    return pd.DataFrame(series_dict)

btc = {'Open':  merge_dfs_on_column(list(exchange_data.values()), list(exchange_data.keys()), 'Open').mean(axis=1),
       'High':  merge_dfs_on_column(list(exchange_data.values()), list(exchange_data.keys()), 'High').mean(axis=1),
       'Low':  merge_dfs_on_column(list(exchange_data.values()), list(exchange_data.keys()), 'Low').mean(axis=1),
       'Close':  merge_dfs_on_column(list(exchange_data.values()), list(exchange_data.keys()), 'Close').mean(axis=1),
       'Volume_Currency':  merge_dfs_on_column(list(exchange_data.values()), list(exchange_data.keys()), 'Volume (Currency)').mean(axis=1), 
      }

#btc.to_csv('BTC-USD.csv', encoding='utf-8', index=True)


nombreBolsa='BTC-USD'

try:
    df = pd.DataFrame (btc, columns = ['Open','High','Low','Close','Volume_Currency'])
    fechadesde = dt.datetime(2011, 9, 13)
    fechahasta = dt.datetime(2020, 11, 20)
    print("Fechas")
    print(fechadesde)
    print(fechahasta)
    print("-----------")
    diferenciaFechas = fechahasta - fechadesde
    print("¿Cuántos días hay entre fechas?")
    print(diferenciaFechas)
    dr = pd.date_range(start=fechadesde, end=fechahasta)
    dft = pd.DataFrame()
    dft['Date'] = dr
    dftTotal= pd.DataFrame()
    dftTotal['Date'] = dr
    cal = calendar()
    holidays = cal.holidays(start=dr.min(), end=dr.max())
    #Quitar de las fechas totales los dias festivos
    dftTotal['Holiday'] = dftTotal['Date'].isin(holidays)
    dftTotal = dftTotal.drop(dftTotal[dftTotal['Holiday']==True].index)

    dft['Holiday'] = dft['Date'].isin(holidays)
    dft = dft.drop(dft[dft['Holiday']==False].index)

    datesHoliday=dft[dft['Holiday']]
    contadorFestivos=datesHoliday['Date'].count()
    print("¿Cuántos días festivos en total?")
    print(contadorFestivos)

    datesHoliday.replace({'Holiday': {True: "presente", False: "falta"}},  inplace = True)

    datesHoliday = datesHoliday.rename_axis(None)
    datesHoliday.reset_index()
    formato = "%Y-%m-%d" 
    formato2='%Y-%m-%d %H:%M:%S'      
    fechadesde = "2011-9-13"
    fechahasta = "2020-11-20"  
    
    fechadesde = datetime.strptime(fechadesde, formato)
    fechahasta = datetime.strptime(fechahasta, formato)    
        
    contFinesT=0
    listFinesSemanaTotales=[]
    while fechadesde <= fechahasta:
        if datetime.weekday(fechadesde) == 1 or datetime.weekday(fechadesde) == 7 : 
            contFinesT +=1
            fechaactual = fechadesde.strftime(formato2)
            for i in range(contadorFestivos):
                fechaactual2 = datesHoliday.iloc[i,0].strftime(formato2)
                if(fechaactual==fechaactual2):
                    contFinesT -=1
                    print(contFinesT, fechaactual, 'es fin y festivo')
            listFinesSemanaTotales.append(fechaactual)
        fechadesde = fechadesde + timedelta(days=1)

    FinesSemanaTotales=pd.DataFrame(np.array(listFinesSemanaTotales), columns=['Dates'])
    print("¿Cuántos días Fines de semana en total?")
    print(contFinesT)
    registrosEsperados=diferenciaFechas.days-contFinesT
    print("¿Cuántos días DEBE tener el archivo ?")
    print(registrosEsperados)

    cont=0
    contDiasFestivos=0
    diasFestivosLista=[]
    listFinesSemana=[]
    contD=0
    totRegistros=0
    datosFaltantes=0
    for r in df.index:
        try:
            a = r.year
            m = r.month
            d = r.day
            fecha = dt.date(a, m, d)
            dia=fecha.strftime('%A').upper()
            for i in range(contadorFestivos):
                if(r==datesHoliday.iloc[i,0]):
                    contDiasFestivos+=1
                    diasFestivosLista.append(r)
            if(dia=='SATURDAY' or dia=='SUNDAY'):
                cont=cont+1
                listFinesSemana.append(contD)
                selectorFin=fecha
            contD=contD+1
        except:
            print("No hay fecha")
            continue
        totRegistros=totRegistros+1
    datosFaltantes=registrosEsperados-totRegistros
    print("---En el archivo---")
    #Se tienen 2 pandas 1 con los días festivos encontrados
    #Otro con los días fines de semana (Siempre esta vacio porque las bolsas no traen)
    print("¿Cuántos registros hay? "+str(totRegistros))

    print("¿Cuántos fines de semana en el archivo? "+str(cont))
    print("¿Cuántos días festivos hay en el archivo? "+str(contDiasFestivos))
    print("¿Cuántos datos faltantes:? "+str(datosFaltantes))
    score1=0.0
    score1=0.0
    if(registrosEsperados==totRegistros):
        print("No hay datos perdidos")
        exit()
    elif(registrosEsperados!=totRegistros):
        print("---Score--")
        score1=(totRegistros/registrosEsperados)*100
        print(score1, '%')
        score2=((totRegistros-datosFaltantes)/registrosEsperados)*100
        print(score2, '%')
        print("---------")
        festivos=pd.DataFrame(np.array(diasFestivosLista), columns=['columnaFestivos'])
        finesD=pd.DataFrame(np.array(listFinesSemana), columns=['columnaFines'])
        df.reset_index(level=['Date'], inplace=True)
        
        for i in finesD.index:
            selectorIndice=finesD['columnaFines'].loc[i]
            #Borrar Fines de semana encontrados
            df.drop(selectorIndice, inplace=True)

        for i in datesHoliday.index:
            df = df.append({'Date': datesHoliday['Date'].loc[i]}, ignore_index=True)
        FinesSemanaTotales['F']=np.nan
        dftTotal = dftTotal.set_index('Date')
        FinesSemanaTotales.Dates=pd.to_datetime(FinesSemanaTotales.Dates, errors='coerce', format='%Y-%m-%d')
        FinesSemanaTotales = FinesSemanaTotales.set_index('Dates')
        
        for i in dftTotal.index:
            if i in FinesSemanaTotales.index:
                dftTotal.drop(i, inplace=True)

        dfPrueba=df

        dfPrueba.Date=pd.to_datetime(dfPrueba.Date, errors='coerce', format='%Y-%m-%d %H:%M:%S')
        dfPrueba = dfPrueba.set_index('Date')

        for i in dftTotal.index:
            if i in dfPrueba.index:
                dftTotal.drop(i, inplace=True)
                
        #Retomar el index
        dftTotal.reset_index(level=['Date'], inplace=True)
        for i in dftTotal.index:
            df = df.append({'Date': dftTotal['Date'].loc[i]}, ignore_index=True)
        df.Date=pd.to_datetime(df.Date, errors='coerce',format='%Y-%m-%d %H:%M:%S')
        df['Open']= pd.to_numeric(df.Open, errors='coerce')
        df['High']= pd.to_numeric(df.High, errors='coerce')
        df['Low']= pd.to_numeric(df.Low, errors='coerce')
        df['Close']= pd.to_numeric(df.Close, errors='coerce')
        df['Volume_Currency']= pd.to_numeric(df.Volume_Currency, errors='coerce')

        
        #Borrar fechas duplicadas
        df.drop_duplicates(subset=['Date'], inplace=True)
        df=df.sort_values(["Date"])
        df=df.reset_index(drop=True)
        nan_rows = df[df.isnull().T.any().T]
        
        xNa13=[] 
        dfPanInterspline=df
        dfPanInterspline.Date=pd.to_datetime(dfPanInterspline.Date, errors='coerce', format='%Y-%m-%d %H:%M:%S')
        dfPanInterspline=dfPanInterspline.interpolate(method='spline', order=3, axis=0, limit_direction ='both')

        for i in df.index:
            if i in nan_rows.index:
                xNa13.append(dfPanInterspline.iloc[i])  
            else:
                continue
        
        dfNan13=pd.DataFrame(np.array(xNa13),columns=['Date','Open','High','Low','Close','Volume_Currency'])
        print("---Fechas imputadas---")
        
        df.to_csv('cleaning/'+nombreBolsa+'.csv', encoding='utf-8', index=False)
        dfPanInterspline.to_csv('cleaning/'+nombreBolsa+'.csv', encoding='utf-8', index=False)
        dfNan13.to_csv('cleaning/SplineImputados_'+nombreBolsa+'.csv', encoding='utf-8', index=False)
        
        #Grafica Online Plotly
        #trace0 = go.Scatter(
         #   x = df.Date,
          #  y =df.Close,
           # name = 'Close-original',
            #line = dict(
             #   color = '#FFDA8C',
              #  width = 4)
        #)
        #trace13 = go.Scatter(
         #   x = df.Date,
          #  y =dfPanInterspline.Close,
           # name = 'spline',
            #line = dict(
             #   color = '#DC0B81',
              #  width = 2,
               # dash = 'dot')
        #)

        #data = [trace0, trace13]
        # Edit the layout
        #layout = dict(title = 'Close '+nombreBolsa,
         #             xaxis = dict(title = 'Years'),
          #            yaxis = dict(title = 'Close'),
           #           )

        #fig = dict(data=data, layout=layout)
        #py.plot(fig, filename='styled-line2')
        
except FileNotFoundError:
    print("No se encuentra el archivo")
