import requests
from base64 import b64encode
import pathlib
import time
def requestAccessToken(CK, CS) -> str:
    '''This function will return an access token to be used '''

    file_path = pathlib.Path(__file__).parent / "access.bin"
    '''
    if pathlib.Path.exists(file_path):
        with open(file_path, "r") as f:
            accTkn = f.read()
        
        if accTkn and testAccessToken(accTkn):
            return accTkn
        else:
            pathlib.Path.unlink(file_path)
    '''
    request_token_bytes = f'{CK}:{CS}'.encode('ascii')
    request_token = b64encode(request_token_bytes).decode('ascii')

    oauth_url = 'https://www.contrataciones.gov.py/datos/api/v3/doc/oauth/token' #For requests
    payload = { 'request_token': request_token}
    response = requests.post(oauth_url, json = payload)
    if response.status_code == 200:
        accTkn = response.json()['access_token']
        #with open(file_path, 'w') as file:
        #    file.write(accTkn)
        return accTkn
    else:
        raise Exception(response.reason)


def testAccessToken(accTkn:str) -> bool:
    '''This function will test whether the accessToken is still valid'''
    return False
    accTkn = 'Bearer ' + accTkn
    #Just an example
    urlbase = 'https://www.contrataciones.gov.py/datos/api/v3/doc/tender/383062-contratacion-servicios-alquiler-software-institucion-municipal-1'
    
    headers = {'accept':'application/json',
               'Authorization':accTkn}
    try:
        y = requests.get(urlbase, headers = headers)
    except Exception as e:
        print(e)
        return False

    return y.ok


if __name__ == "__main__":
    CK = '829fd4c3-7119-4543-8a97-82b9d2311ef4'
    CS = '3f794913-df7c-43de-9170-b8bd4d0d6004'
    print(requestAccessToken(CK, CS))

