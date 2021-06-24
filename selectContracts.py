import pathlib
import requests
from requests.api import request
from requestAccessToken import *
import time

def requestContracts(id: list, accTkn: str):
    '''This function will return the data of a contract given its id '''

    urlbase = f'https://www.contrataciones.gov.py/datos/api/v3/doc/contracts/{id}'
    headers = {'accept':'application/json', 'Authorization':f'Bearer {accTkn}'}
    data = requests.get(urlbase, headers = headers)
    
    if data.ok == True:
        data = data.json()
        res = {}
        for el in data['contracts']:
            res[el['id']] = el
    elif data.reason == "TOO MANY REQUESTS":

        with open(pathlib.Path(__file__).parent / "CK.txt", 'r') as file:
            CK = file.read()
        with open(pathlib.Path(__file__).parent / "CS.txt", "r") as file:
            CS = file.read()
        accTkn = requestAccessToken(CK, CS)
        return requestContracts(id, accTkn)
    else:

        raise Exception(data.reason)
    return res


if __name__ == "__main__":
    import requests
    import pathlib
    from requestAccessToken import *   

    mypath = pathlib.Path(__file__).parent
    #First, we obtain the access token
    with open(mypath / "CK.txt", 'r') as file:
        CK = file.read()
    with open(mypath / "CS.txt", "r") as file:
        CS = file.read()
    accTkn = requestAccessToken(CK, CS)
    requestContracts("LP-30001-19-171139", accTkn)
