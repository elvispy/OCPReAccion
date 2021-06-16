import requests
import json
import pathlib
from requestAccessToken import *



def requestDNCP(configs: dict, accTkn: str):
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
        aux = configs['tender.procuringEntity.name']
        with open(pathlib.Path(__file__).parent / f'{aux}.json', 'w') as file:
            json.dump(data.json()['records'], file, indent=4)
        print("Done!")
        return data.json()['records']
    else:
        raise Exception("Smth went wrong. Contact Elvis for help")


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

    requestDNCP(configs, accTkn)