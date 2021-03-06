"""
This script will export awards' data from DNCP's API. 

Author: Elvis Agüero <elvisavfc65@gmail.com>

TODO: Analizar adendas! (Ej 349475)

Created: 27th January, 2022
"""

# Built in imports
from pathlib import Path
import json

# Local importss
from requestAccessToken import requestAccessToken
from selectAwards import requestAwards
from selectContracts import requestContracts
from selectTenders import requestTenders

# Modules
def create_data(entity: str = "Municipalidad de Asunción", accTkn:str = "")-> None:
    
    # Configuraciones
    configs = {
        'items_per_page':1000,
        'fecha_desde':'2013-01-01',
        'tipo_fecha':'publicacion_llamado',
        'tender.procuringEntity.name':entity,
        'contracts.implementation.financialProgress.breakdown.classifications.financiador':3
    }
    
    final_data = []
    #First we request for tenders
    if accTkn == "":
        accTkn = requestAccessToken()
    data = requestTenders(configs, accTkn)

    for record in data:
        record = record['compiledRelease']

        for contract in record['contracts']:
            contract_info = requestContracts(contract['id'], accTkn, record['anho'], entity)
            contract_info['id_ocds'] = contract['id']
            contract_info['tender'] = record['tender']
            contract_info['planning'] = record['planning']
            contract_info['tenderDatePublished'] = record['tenderDatePublished']
            aw_ID = contract_info[contract['id']]['awardID']
            award_info = requestAwards(aw_ID, accTkn)
            contract_info['suppliers'] = award_info[aw_ID]['suppliers']

            final_data.append(contract_info)
    
    with open(Path(__file__).parent / 'Documentos' / f'{entity}' / f'{entity}.json', 'w') as file:
        json.dump(final_data, file, indent = 4)
    return final_data


if __name__ == "__main__":
    accTkn = requestAccessToken()
    create_data("Municipalidad de San Lorenzo", accTkn)