from time import sleep
import requests
from base64 import b64encode
from pathlib import Path


def requestAccessToken(CK: str = '', CS: str = '') -> str:
    '''This function will return an access token to be used '''
    # If there are not Consumer Keys or consumer Secrets, lets open them. 
    mypath = Path(__file__).parent

    if False and Path.is_file(mypath / "access.bin"):
        with open(mypath / "access.bin", "r", encoding = 'utf-8') as f:
            accTkn = f.read()
            if testAccessToken(accTkn):
                return accTkn
    elif not CK or not CS:
        #First, we obtain the access token
        with open(mypath / "CK.txt", 'r') as file:
            CK = file.read()
        with open(mypath / "CS.txt", "r") as file:
            CS = file.read()
    elif CK and CS:
        # Write consumer secret and key if needed.
        if Path.is_file(mypath / "CK.txt"):
            raise Exception("Duplicating Consumer Key")
        if Path.is_file(mypath / "CS.txt"):
            raise Exception("Duplicating Consumer Secret")
        
        with open(mypath / "CK.txt", "w", encoding = 'utf-8') as f:
            f.write(CK)
        with open(mypath / "CS.txt", "w", encoding = 'utf-8') as f:
            f.write(CS)

    # We need to decode them
    request_token_bytes = f'{CK}:{CS}'.encode('ascii')
    request_token = b64encode(request_token_bytes).decode('ascii')

    oauth_url = 'https://www.contrataciones.gov.py/datos/api/v3/doc/oauth/token' #For requests
    payload = { 'request_token': request_token}
    response = requests.post(oauth_url, json = payload)
    if response.status_code == 200:
        accTkn = response.json()['access_token']
        with open(mypath / "access.bin", 'w') as file:
            file.write(accTkn)
        return accTkn
    else:
        raise Exception(response.reason)

def testAccessToken(accTkn:str) -> bool:
    '''This function will test whether the accessToken is still valid'''
    # accTkn = ' ' + accTkn
    #Just an example
    urlbase = 'https://www.contrataciones.gov.py/datos/api/v3/doc/tender/383062-contratacion-servicios-alquiler-software-institucion-municipal-1'
    
    headers = {'accept':'application/json',
               'Authorization':accTkn}
    try:
        y = requests.get(urlbase, headers = headers)
    except Exception as e:
        print(e)
        return False
    try:
        return y.ok
    except KeyError:
        return False

if __name__ == "__main__":
    print(requestAccessToken())
    sleep(1)
    print(requestAccessToken())


