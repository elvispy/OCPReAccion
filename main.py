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
    
    # Configuraciones
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
            contract_info['planning'] = record['planning']
            contract_info['tenderDatePublished'] = record['tenderDatePublished']
            aw_ID = contract_info[contract['id']]['awardID']
            award_info = requestAwards(aw_ID, accTkn)
            contract_info['suppliers'] = award_info[aw_ID]['suppliers']

            final_data.append(contract_info)
    
    with open(pathlib.Path(__file__).parent / f'{entity}.json', 'w') as file:
        json.dump(final_data, file, indent = 4)
    
    return final_data


#connecting to google sheets api
from httplib2 import Http
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
scopes="https://www.googleapis.com/auth/spreadsheets"
ssid= "" #spreadsheet id
creds = ServiceAccountCredentials.from_json_keyfile_name('json file with credentials', scopes)
sserv=build('sheets','v4', http=creds.authorize(Http())) #sheets service


def data_filler(jpath)-> None:
    with open(jpath,'r') as file:
    f=json.loads(file.read())
    print(f[0][list(f[0].keys())[0]].keys())
  

    values=list()

    for i in f:
        conv= i["tender"]["procuringEntity"]["name"]    #Convocante
        id_de_lic=i[list(i.keys())[0]]["implementation"]["financialProgress"]["breakdown"][0]["classifications"]["cdp"]
        Tipo_lic= i["tender"]["procurementMethodDetails"]
        pub_lic=i["tenderDatePublished"][:10] #Fecha de publicacion de la licitacion
        fecha_firma=i[list(i.keys())[0]]["dateSigned"][:10]
        cr= i["tenderDatePublished"][:10]     #compilerelEase maembo
        if len(i["suppliers"])==1:
            prov=i["suppliers"][0]["name"]
            if i["suppliers"][0]["id"][:7]=="PY-RUC-":
                ruc=i["suppliers"][0]["id"][7:]
            else:    
                ruc='-1'
        else: 
            prov='-1'
            ruc='-1' 
        titulo= i["tender"]['title']
        mtotal= i[list(i.keys())[0]]["value"]["amount"]#monto total    
        monto_f=int()   #monto fonacide
        monto_o=int()   #otras fuentes
        years= set()    #stores years of budgets contract is using
        for ii in i[list(i.keys())[0]]["implementation"]["financialProgress"]["breakdown"]:
            years.add(ii['classifications']["anio"])
            if ii['classifications']['financiador']== '3':
                monto_f+= int(ii["measures"]["monto_a_utilizar"])
            else: 
                monto_o+= int(ii["measures"]["monto_a_utilizar"]     )
        if monto_f+monto_o!=mtotal:
            monto_o="-1"
            monto_f="-1"
            mtotal="-1"
        ano= fecha_firma[:4]           
        url = str("https://www.contrataciones.gov.py/licitaciones/adjudicacion/contrato/" + i[list(i.keys())[0]]["awardID"]+ ".html")
        plr="No" #plurianual
        if len(years)>1:
            plr= "Si" 
        tp= i["tender"]['tenderPeriod']["durationInDays"]    #tender period in days
        tpsd= i["tender"]['tenderPeriod']["startDate"][:10]  #tender period start date
        values.append(list((conv,
         id_de_lic, 
          Tipo_lic,
          pub_lic
          ,cr
          ,' '
          , 
          fecha_firma,
           prov,
            ruc, 
            titulo, 
            mtotal,
            monto_f, 
            monto_o, 
            ano,
            '',
            url,
            plr,
            tp,
            tpsd)))      
    print(values)
    bodyy={
        'values':values
    }
    
    sserv.spreadsheets().values().append(spreadsheetId="spreadsheetId", range="range in A notation", valueInputOption="RAW", body=bodyy).execute()
    return None

if __name__ == "__main__":
    create_data("Municipalidad de Asunción", accTkn)
    create_data("Municipalidad de Encarnación", accTkn)

    
