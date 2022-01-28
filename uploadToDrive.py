"""
This script uploads the data of awards in a json file to a spreadsheet

Author: Elvis Agüero <elvisavfc65@gmail.com>

Created: 27th January, 2022
"""

# Standard Library Imports
import json
from pathlib import Path
import logging
logging.basicConfig(filename = 'debug.log', filemode = 'a', level = logging.INFO, \
    format='%(asctime)s %(message)s')

# Thirds Party Imports
import gspread

# Modules
def upload_data(fileName: str, key: str):
    """
    This script will upload data stored in fileNames list and upload it to drive
    in respective keys
    Inputs:
        - filenames: str
            * File Name of of json to be uploaded
        - keys: str
            * spreadsheet key to open on google drive
    """
    # Open JSON data with the awards data
    path = Path(__file__).parent / fileName
    with open(path, 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    
    values = list()
    for num, award in enumerate(data, start = 1):
        # Now we extract the data out of the json

        rescindido = "-"
        convocante = award["tender"]["procuringEntity"]["name"] 
        id_ocds = award['id_ocds']
        nro_contrato = '-'
        id_licitacion = award['planning']['identifier'] #award[list(award.keys())[0]]["implementation"]["financialProgress"]["breakdown"][0]["classifications"]["cdp"]
        tipo_licitacion = award["tender"]["procurementMethodDetails"]
        fecha_publicacion_licitation = award["tenderDatePublished"][:10] #Fecha de publicacion de la licitacion
        fecha_firma_contrato = award[id_ocds]["dateSigned"][:10]
        anho= fecha_publicacion_licitation[:4]           
        titulo_contrato = award["tender"]['title']
        url = f"https://www.contrataciones.gov.py/licitaciones/adjudicacion/contrato/{award[id_ocds]['awardID']}.html"
        categoria = '-'
        # cr = award["tenderDatePublished"][:10]     #compiledRelease maembo
        # Vemos cuantos proveedores hay
        if len(award["suppliers"]) == 1:
            proveedor = award["suppliers"][0]["name"]
            if award["suppliers"][0]["id"][:7] == "PY-RUC-":
                ruc = award["suppliers"][0]["id"][7:]
            else:    
                ruc ='-1'
        else: 
            proveedor ='-1'
            ruc ='-1'

        # Calculamos monto total, y lo que viene de fonacide
        monto_contrato = award[id_ocds]["value"]["amount"]#monto total 
        monto_fonacide = 0   #monto fonacide
        monto_otras_fuentes = 0   #otras fuentes
        years = set()    #stores years of budgets contract is using 
        # Sumamos los anhos 
        for fuente in award[id_ocds]["implementation"]["financialProgress"]["breakdown"]:
            years.add(fuente['classifications']["anio"])
            if str(fuente['classifications']['financiador']) == '3':
                monto_fonacide += int(fuente["measures"]["monto_a_utilizar"])
            else: 
                monto_otras_fuentes += int(fuente["measures"]["monto_a_utilizar"])
        
        plurianual = "Si" if len(years) > 1 else "No"
        if monto_fonacide+monto_otras_fuentes != monto_contrato:
            logging.info('Para el contrato %s, el monto no concuerda con fonacide y otras fuentes', id_ocds)
            logging.info('Monto total: %s', monto_contrato)
            logging.info('\n%s\n', json.dumps(award[id_ocds]["implementation"]["financialProgress"]["breakdown"], indent = 4))
            monto_otras_fuentes = str(monto_otras_fuentes) + " (?)"
            monto_fonacide = str(monto_fonacide) + " (?)"
            monto_contrato = str(monto_contrato) + " (?)"
        # tp = award["tender"]['tenderPeriod']["durationInDays"]    #tender period in days
        # tpsd = award["tender"]['tenderPeriod']["startDate"][:10]  #tender period start date
        values.append([
            num, rescindido, convocante,
            id_ocds, nro_contrato, fecha_firma_contrato, 
            id_licitacion, tipo_licitacion, fecha_publicacion_licitation, 
            proveedor, ruc, titulo_contrato, monto_contrato, 
            monto_fonacide, monto_otras_fuentes, anho,
            categoria, url, plurianual
            ])

    # We begin authentication via OAuth2. 
    # For more information on this proccess please refer to    
    # https://docs.gspread.org/en/latest/oauth2.html 
    gc = gspread.oauth(
        credentials_filename='.config/gspread/credentials.json',
        authorized_user_filename='.config/gspread/authorized_user.json'
    )
 
    # Open Spreadheet by Key
    sh = gc.open_by_key(key)
    worksheet = sh.get_worksheet(0)

    # Get header 
    ii = 1
    while not worksheet.cell(ii, ii).value:
        ii+=1
    jj = ii
    while jj > 1 and worksheet.cell(ii, jj-1).value:
        jj -= 1
    # There are about 20 columns, and we expect no more than 300 tenders
    myrange = f'{chr(jj+64)}{ii+1}:V300' 

    # Update on drive
    print("BEFORE CHANGING SOMETHING, ADD PASSWORD")
    if input("") == "confirm":
        worksheet.update(myrange, values)
        worksheet.format(myrange, {'horizontalAlignment': "CENTER"})
    else:
        print("Wrong password, action cancelled :)")
        
if __name__ == '__main__':
    upload_data("Municipalidad de Minga Guazú.json", "1VIk3HffKsIG9X1igF8B8mD1cTU9TO5C0efZ2gAlPnk0")