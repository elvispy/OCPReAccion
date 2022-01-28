"""
Author: Elvis Agüero <elvisavfc65@gmail.com>

Created: 27th January, 2022
"""

import requests
from requestAccessToken import requestAccessToken
from pathlib import Path

def requestContracts(id: list, accTkn: str, anho: str, entidad:str):
    '''This function will return the data of a contract given its id '''


    # Path of the folder to store data
    folderpath = Path(__file__).parent / "Documentos" / entidad / anho
    # Check if folder exists
    if not Path.is_dir(folderpath): Path.mkdir(folderpath, parents = True, exist_ok=True)
    
    # DNCP URL to request contracts data
    urlbase = f'https://www.contrataciones.gov.py/datos/api/v3/doc/contracts/{id}'
    headers = {'accept':'application/json', 'Authorization':f'{accTkn}'}
    tender_info = requests.get(urlbase, headers = headers)
    if tender_info.ok == True:
        tender_info = tender_info.json()
        res = {}
        # Look for contracts in tender
        for contract in tender_info['contracts']:
            res[contract['id']] = contract
            contract_path = folderpath / f"{contract['id']} (Contrato).pdf"
            if not Path.is_file(contract_path): 
                # Check inside contract documents
                for document in contract['documents']:
                    # Check if document its equal to contract
                    if 'documentType' in document.keys() and document['documentType'] == 'contractSigned' and (not Path.is_file(contract_path)):
                        #Download contract
                        contract_pdf = requests.get(document['url'], allow_redirects = True)
                        try:
                            with open(contract_path, 'wb') as f:
                                f.write(contract_pdf.content)
                        except Exception as e:
                            print(f"Couldnt download contract with id {contract['id']}")
                            print(e)
                        break
            # Now we look for codigo de contratacion
            cco_url = f'https://www.contrataciones.gov.py/reporte/codigo-contratacion/{contract["id"]}.pdf'
            cc_path = folderpath / f"{contract['id']} (Codigo Contratacion).pdf"
            if not Path.is_file(cc_path):
                try:
                    cod_contratacion = requests.get(cco_url, allow_redirects = True)
                    with open(cc_path, 'wb') as f:
                        f.write(cod_contratacion.content)
                except Exception as e:
                    print(f"Couldnt download Codigo de Contratacion with id {tender_info['id']}")
                    print(e)
    elif tender_info.reason == "TOO MANY REQUESTS":
        accTkn = requestAccessToken()
        return requestContracts(id, accTkn)
    else:
        raise Exception(tender_info.reason)
    return res


if __name__ == "__main__":
    accTkn = requestAccessToken()
    requestContracts("LP-30001-19-171139", accTkn)
