"""
Author: Elvis Agüero <elvisavfc65@gmail.com>

Created: 27th January, 2022
"""

# Built in imports
import requests
import re
from pathlib import Path
import logging
logging.basicConfig(filename = 'debug.log', filemode = 'a', level = logging.INFO, \
    format='%(asctime)s %(message)s')

# Local imports
from requestAccessToken import requestAccessToken

# Modules
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
    headers = {'accept':'application/json', 'Authorization':f'{accTkn}'} # XXXX

    data = requests.get(urlbase, headers = headers)
    if data.ok == True:
        res = data.json()['records']
        c = 0
        for rec in res:
            urlbase2 =  f"https://www.contrataciones.gov.py/datos/api/v3/doc/tender/{rec['compiledRelease']['planning']['identifier']}?sections=datePublished,documents,procuringEntity"
            myreq = requests.get(urlbase2, headers = headers)
            print(rec['compiledRelease']['planning']['identifier'])
            print(c)
            c+=1
                
            if myreq.reason == 'TOO MANY REQUESTS':
                print(accTkn)
                accTkn = requestAccessToken()
                print(accTkn)
                headers = {'accept':'application/json', 'Authorization':f'{accTkn}'} # XXXX
                myreq = requests.get(urlbase2, headers = headers).json()
            elif myreq.ok == False:
                raise Exception(myreq.reason)

            myreq = myreq.json()
            rec['compiledRelease']['tenderDatePublished'] = myreq['tender']['datePublished']
            anho = myreq['tender']['datePublished'][:4]
            rec['compiledRelease']['anho'] = anho
            entidad = myreq['tender']['procuringEntity']['name']
            folderpath = Path(__file__).parent / "Documentos" / entidad / anho
            if not Path.is_dir(folderpath): Path.mkdir(folderpath, parents = True, exist_ok=True)
            PBC_url = f'https://www.contrataciones.gov.py/documentos/download/pliego/{myreq["tender"]["id"]}/2'
            try:
                path =  folderpath / f"{myreq['tender']['id']}.zip"
                if Path.is_file(path): continue
                PBC_data = requests.get(PBC_url, allow_redirects=True)                    
                if PBC_data.status_code == 200:
                    if Path.is_file(path):
                        continue
                    with open(path, 'wb') as f:
                        f.write(PBC_data.content)
                elif PBC_data.status_code == 404:
                    # We need to look in documents
                    for doc in myreq['tender']['documents']:
                        if test_pbc(doc['documentTypeDetails'], doc['title']):
                            PBC_path = folderpath / f'PBC {myreq["tender"]["id"]} {doc["title"]}'
                            if Path.is_file(PBC_path): continue
                            PBC_data = requests.get(doc['url'], allow_redirects=True)
                            if not Path.is_file(PBC_path):
                                with open(PBC_path, 'wb') as file:
                                    file.write(PBC_data.content)

                    pass
                else:
                    raise Exception("Not coded yet")
                    # We look for PBC on documents
            except Exception as e:
                print(f"Couldnt download PBC of \n {myreq['tender']['id']}")
                print(e)

        return res
    elif data.reason == "TOO MANY REQUESTS":
        accTkn = requestAccessToken()
        return requestTenders(configs, accTkn)
    else:
        raise Exception(data.reason)

def test_pbc(*args)-> bool:
    """
    This function will test whether the arguments are a valid 
    Pliego de Bases y Condiciones format

    >>> test_pbc()
    False
    >>> test_pbc('pbc.pdf', 'hahaha')
    True
    >>> test_pbc('Hey', 'bro')
    False
    >>> test_pbc('Hey', 'bro', 'Pliego de Bases y Condiciones.pdf')
    True
    """

    testpbc = re.compile(f'pbc|pliego|bases|condiciones', re.IGNORECASE)

    for string in args:
        if testpbc.search(string):
            return True
    return False
if __name__ == "__main__":
    configs = {
        'items_per_page':100,
        'fecha_desde':'2013-01-01',
        'tipo_fecha':'fecha_release',
        'tender.procuringEntity.name':"Municipalidad de Encarnación",
        'contracts.implementation.financialProgress.breakdown.classifications.financiador':3
    }
    #First, we obtain the access token
    accTkn = requestAccessToken()
    requestTenders(configs, accTkn)