import requests
from requestAccessToken import requestAccessToken

def requestAwards(id: str, accTkn: str):
    '''This function will return the data of an award given its id '''

    urlbase = f'https://www.contrataciones.gov.py/datos/api/v3/doc/awards/{id}'
    headers = {'accept':'application/json', 'Authorization':f'{accTkn}'}
    data = requests.get(urlbase, headers = headers)
    if data.ok == True:
        data = data.json()
        res = {}
        for el in data['awards']:
            res[el['id']] = el
    elif data.reason == "TOO MANY REQUESTS":
        accTkn = requestAccessToken()
        return requestAwards(id, accTkn)
    else:
        raise Exception(data.reason)
    return res


if __name__ == "__main__":

    accTkn = requestAccessToken()
    requestAwards("351815-classic-mobles-sociedad-anonima-3", accTkn)

    
