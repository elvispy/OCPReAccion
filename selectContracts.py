import requests
import pathlib
from requestAccessToken import *

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
    else:
        raise Exception("Smth Went Wrong!")
    return res


if __name__ == "__main__":
    mypath = pathlib.Path(__file__).parent
    #First, we obtain the access token
    with open(mypath / "CK.txt", 'r') as file:
        CK = file.read()
    with open(mypath / "CS.txt", "r") as file:
        CS = file.read()
    accTkn = requestAccessToken(CK, CS)
    requestContracts("LP-30001-19-171139", accTkn)