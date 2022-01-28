# OCP ReAcción

Este repositorio tiene como finalidad descargar datos de una municipalidad de Paraguay del sitio de la
Dirección Nacional de Contrataciones Públicas, mediante la APIv3, disponible en 

> https://www.contrataciones.gov.py/datos/

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

    hola
    bb
    234

**probando**