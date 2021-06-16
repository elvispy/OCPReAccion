import requests
from base64 import b64encode
import pathlib
def requestAccessToken(CK, CS) -> str:
    '''This function will return an access token to be used '''

    file_path = pathlib.Path(__file__).parent / "access.bin"
    if pathlib.Path.exists(file_path):
        with open(file_path, "r") as f:
            accTkn = f.read()
        
        if accTkn and testAccessToken(accTkn):
            return accTkn
        else:
            pathlib.Path.unlink(file_path)

    request_token_bytes = f'{CK}:{CS}'.encode('ascii')
    request_token = b64encode(request_token_bytes).decode('ascii')
    oauth_url = 'https://www.contrataciones.gov.py/datos/api/v3/doc/oauth/token' #For requests
    payload = { 'request_token': request_token}

    response = requests.post(oauth_url, json = payload)

    if response.status_code == 200:
        accTkn = response.json()['access_token']
        with open(file_path, 'w') as file:
            file.write(accTkn)
        return accTkn
    else:
        raise Exception("Still smth wrong!")


def testAccessToken(accTkn:str) -> bool:
    '''This function will test whether the accessToken is still valid'''

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
    CK = '835c2f20-8979-461c-a1b7-6bca4e71770a'
    CS = '388e7611-0ccd-4025-a9a4-22f0afb87fec'
    requestAccessToken(CK, CS)
