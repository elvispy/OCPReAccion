import pathlib
import requests
from requests.api import request
from requestAccessToken import *

def requestTenders(configs: dict, accTkn: str):
    '''This functions will make a request to search for all tenders in a given range'''

    

    #Now lets build the base URL with the configurations
    urlbase = 'https://www.contrataciones.gov.py/datos/api/v3/doc/search/processes?'
    for con in configs.keys():
        if type(configs[con]) == type([]):
            res = ''
            for el in configs[con]:
                res = res + f'{el},'
            res = res[:-1] #Take out last comma
        else:
            res = configs[con]
        
        urlbase = urlbase + f'{con}={res}&'
    urlbase = urlbase[:-1]
    
    #BUilding header
    headers = {'accept':'application/json', 'Authorization':f'Bearer {accTkn}'}

    data = requests.get(urlbase, headers = headers)
    if data.ok == True:
        res = data.json()['records']
        
        for rec in res:
            urlbase2 =  f"https://www.contrataciones.gov.py/datos/api/v3/doc/tender/{rec['compiledRelease']['planning']['identifier']}?sections=datePublished"
            myreq = requests.get(urlbase2, headers = headers)
            if myreq.ok == True:
                rec['compiledRelease']['tenderDatePublished'] = myreq.json()['tender']['datePublished']
            elif myreq.reason == 'TOO MANY REQUESTS':

                with open(pathlib.Path(__file__).parent / "CK.txt", 'r') as file:
                    CK = file.read()
                with open(pathlib.Path(__file__).parent / "CS.txt", "r") as file:
                    CS = file.read()
                accTkn = requestAccessToken(CK, CS)
                urlbase2 =  f"https://www.contrataciones.gov.py/datos/api/v3/doc/tender/{rec['compiledRelease']['planning']['identifier']}?sections=datePublished"
                myreq = requests.get(urlbase2, headers = headers)
                rec['compiledRelease']['tenderDatePublished'] = myreq['tender']['datePublished']
            else:
                raise Exception(myreq.reason)
        return res
    elif data.reason == "TOO MANY REQUESTS":
        with open(pathlib.Path(__file__).parent / "CK.txt", 'r') as file:
            CK = file.read()
        with open(pathlib.Path(__file__).parent / "CS.txt", "r") as file:
            CS = file.read()
        accTkn = requestAccessToken(CK, CS)
        return requestTenders(configs, accTkn)
    else:
        raise Exception(data.reason)


if __name__ == "__main__":
    
    configs = {
        'items_per_page':100,
        'fecha_desde':'2013-01-01',
        'tipo_fecha':'fecha_release',
        'tender.procuringEntity.name':"Municipalidad de Encarnación",
        'contracts.implementation.financialProgress.breakdown.classifications.financiador':3
    }

    #First, we obtain the access token
    with open(pathlib.Path(__file__).parent / "CK.txt", 'r') as file:
        CK = file.read()
    with open(pathlib.Path(__file__).parent / "CS.txt", "r") as file:
        CS = file.read()
    accTkn = requestAccessToken(CK, CS)

    requestTenders(configs, accTkn)