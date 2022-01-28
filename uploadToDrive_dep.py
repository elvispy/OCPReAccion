import json
from pathlib import Path
from httplib2 import Http
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\junio\OneDrive\Escritorio\rproject\creds.json"


scopes="https://www.googleapis.com/auth/spreadsheets"
ssid= "1naVvZMOiMEmxOYI1pHyl7hgLD_IjaR6rHYRwM5d0z_Q" #test spreadsheet id
creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\junio\\OneDrive\\Escritorio\\rproject\\creds.json', scopes)

sserv=build('sheets','v4', http=creds.authorize(Http())) #sheets service
#def parser(f):
    #fields to look for: [Id de licitacion, Tipo de licitacion, Fecha de publicacion de convocatoria de licitacion
    # , Compiledrelease, , Fecha firma de contrato, proveedor segun dncp, ruc, Titulo de contrato, Monto Total de contrato, Monto F, Monto Otras fuentes
    # ,Ano,  , url, Contrato Plurianual]
#    values=[f[]]

with open("C:\\Users\\junio\OneDrive\\Escritorio\\rproject\\Municipalidad de Encarnacion.json",'r') as file:
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
        values.append(tuple((conv,
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
    #print(values)
    bodyy={
        'values':values
    }
cd=dict()
for i in values:
    cd[i[1]]=i[3]  
#    sserv.spreadsheets().values().append(
#    spreadsheetId="1orpsKa2904Uprmk26yOTr7rbh_br3pLLL4Bynk6ds5c", range="C3:U4",
#    valueInputOption="RAW", body=bodyy).execute()
print(cd)
nf=list([[],[]])

print(Path.cwd())
with open("C:\\Users\\junio\OneDrive\\Escritorio\\rproject\\Municipalidad de Encarnacion_old.json","r") as file:
    f=json.loads(file.read())
    for i in f:
        nurl=str("https://www.contrataciones.gov.py/licitaciones/adjudicacion/contrato/" + i[list(i.keys())[0]]["awardID"]+ ".html")
        fpkey=i[list(i.keys())[0]]["implementation"]["financialProgress"]["breakdown"][0]["classifications"]["cdp"]
        nf[1].append([nurl])
        nf[0].append([cd[fpkey]])
nbody= {
    "valueInputOption":"RAW",
    "data" :  [{"range": "'Solo contratos 2013 -2021'!I2:I99",
    "values": list(nf[0])},
    {"range": "'Solo contratos 2013 -2021'!R2:R99",
    "values": list(nf[1] ) }]
}

sserv.spreadsheets().values().batchUpdate(
spreadsheetId="1445q8t5gvYRTZwozHExdcfqS-TDwLjgVZ_r-UZws7eQ", body=nbody).execute()
