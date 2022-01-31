# OCP ReAcción

Este repositorio tiene como finalidad descargar datos de una municipalidad de Paraguay del sitio de la
Dirección Nacional de Contrataciones Públicas, mediante la APIv3, disponible en 

> https://www.contrataciones.gov.py/datos/


## Descargando los datos para análisis: fetch_data_from_dncp()
El script que se encarga de descargar los datos es <code> fetch_data_from _dncp </code>, que recibe dos argumentos: el nombre del convocante y, opcionalmente el access token de la API de la DNCP. Si el access token no es proveido, el script espera dos archivos "CK.txt" y "CS.txt", dos archivos con el consumer key y el consumer secret de la aplicación. Para más información, léase la documentación proveída por la DNCP:

> https://www.contrataciones.gov.py/datos/manual

El output de este script son archivos guardados en el directorio <code> Documentos / Nombre del Convocante </code>. Este consiste de los contratos, códigos de contratación y Pliego de bases y condiciones de cada adjudicación. El diccionario de configuraciones, al dia de 28/01/2022 es el siguiente

```yaml
configs = { 
    'items_per_page':1000,
    'fecha_desde':'2013-01-01',
    'tipo_fecha':'fecha_release',
    'tender.procuringEntity.name':entity,
    'contracts.implementation.financialProgress.breakdown.classifications.financiador':3
}
```

Además, un resumen de los datos obtenidos se guardarán en un archivo JSON, que posee entradas con el siguiente formato:

```yaml
{
        "CO-30162-22-210715": {
            "awardID": "401060-prismapar-s-a-2",
            "period": {
                "endDate": "2022-03-21T00:00:00-04:00",
                "startDate": "2021-12-17T00:00:00-04:00"
            },
            "documents": [
                {
                    "datePublished": "2022-01-24T11:15:48-04:00",
                    "documentTypeDetails": "Nota de Aclaraci\u00f3n",
                    "language": "es",
                    "id": "z6FMmGkoRA4=",
                    "title": "acuerdo_y_sentencia_n__37_1643032855960.pdf",
                    "url": "https://www.contrataciones.gov.py/documentos/download/contrato/z6FMmGkoRA4%253D"
                },
                {
                    "datePublished": "2022-01-24T11:15:48-04:00",
                    "documentTypeDetails": "Nota de Aclaraci\u00f3n",
                    "language": "es",
                    "id": "4CU9gHYL1Zs=",
                    "title": "nota_de_aclaracion_24_1639658812599.pdf",
                    "url": "https://www.contrataciones.gov.py/documentos/download/contrato/4CU9gHYL1Zs%253D"
                }
            ],
            "implementation": {
                "financialProgress": {
                    "breakdown": [
                        {
                            "classifications": {
                                "tipo_programa": "2",
                                "objeto_gasto": "520",
                                "sub_programa": "1",
                                "fuente_financiamiento": "30",
                                "entidad": "162",
                                "programa": "3",
                                "proyecto": "0",
                                "departamento": "10",
                                "nivel": "30",
                                "anio": "2022",
                                "financiador": "3",
                                "cdp": "401060"
                            },
                            "period": {
                                "endDate": "2022-12-31T00:00:00Z",
                                "startDate": "2022-01-01T00:00:00Z"
                            },
                            "measures": {
                                "monto_a_utilizar": "400496538"
                            },
                            "financialCode": "CO-30162-22-210715",
                            "id": "2022/30/162/2/3/1/0/3/10/520/30/CO-30162-22-210715"
                        }
                    ]
                }
            },
            "statusDetails": "Adjudicado",
            "id": "CO-30162-22-210715",
            "dateSigned": "2021-12-22T12:00:00-04:00",
            "value": {
                "amount": 400496538,
                "currency": "PYG"
            },
            "status": "active"
        },
        "id_ocds": "CO-30162-22-210715",
        "tender": {
            "procuringEntity": {
                "name": "Municipalidad de Minga Guaz\u00fa",
                "id": "DNCP-SICP-CODE-233"
            },
            "coveredBy": [
                "fonacide"
            ],
            "mainProcurementCategoryDetails": "Alimentación Escolar",
            "statusDetails": "Adjudicada",
            "id": "ejemplo_de_id",
            "title": "Ejemplo de Titulo",
            "procurementMethodDetails": "Concurso de Ofertas",
            "tenderPeriod": {
                "durationInDays": 9,
                "endDate": "2021-10-29T08:00:00-04:00",
                "startDate": "2021-10-19T16:20:46-04:00"
            }
        },
        "planning": {
            "identifier": "401060"
        },
        "tenderDatePublished": "2021-10-19T16:20:46-04:00",
        "suppliers": [
            {
                "name": "PRISMAPAR S.A",
                "id": "PY-RUC-80075157-4"
            }
        ]
    }
```

## Subiendo los datos a una planilla de google para análisis: uploadToDrive()

Este script tiene como finalidad subir los datos del json al Google Drive. Espera como argumentos dos strings, uno con el nombre del json a ser analizado, y otro con el código de
la hoja de cálculo de Google donde deben cargarse los datos. 

Se debe realizar una autenticación previa del servicio de consumo de APIS de google, cuya documentación está disponible en 

> https://docs.gspread.org/en/latest/oauth2.html 


## Siguientes pasos:

- Hacer que el script suba al drive solo los datos que faltan (Para facilitar actualizacion de datos)
- Hacer que el script induzca que Instituciones pudieron haber sido beneficiadas en un contrato. 