#First, let create creds
#First, we obtain the access token
import pathlib
import json
from requestAccessToken import *
from selectAwards import *
from selectContracts import *
from selectTenders import *

with open(pathlib.Path(__file__).parent / "CK.txt", 'r') as file:
    CK = file.read()
with open(pathlib.Path(__file__).parent / "CS.txt", "r") as file:
    CS = file.read()
accTkn = requestAccessToken(CK, CS)

def create_data(entity: str = "Municipalidad de Asunción", accTkn:str = accTkn)-> None:
    
    configs = {
        'items_per_page':1000,
        'fecha_desde':'2013-01-01',
        'tipo_fecha':'fecha_release',
        'tender.procuringEntity.name':entity,
        'contracts.implementation.financialProgress.breakdown.classifications.financiador':3
    }
    
    final_data = []
    #First we request for tenders
    data = requestTenders(configs, accTkn)

    for record in data:
        record = record['compiledRelease']
        for contract in record['contracts']:
            contract_info = requestContracts(contract['id'], accTkn)
            contract_info['tender'] = record['tender']
            aw_ID = contract_info[contract['id']]['awardID']
            award_info = requestAwards(aw_ID, accTkn)
            contract_info['suppliers'] = award_info[aw_ID]['suppliers']

            final_data.append(contract_info)
    
    with open(pathlib.Path(__file__).parent / f'{entity}.json', 'w') as file:
        json.dump(final_data, file, indent = 4)
    
    return final_data


if __name__ == "__main__":
    create_data("Municipalidad de Asunción", accTkn)
    create_data("Municipalidad de Encarnación", accTkn)

