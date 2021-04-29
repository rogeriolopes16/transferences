import urllib3
import csv
from datetime import datetime
from modules.getDataBase import *
from modules.getWSO2 import *

urllib3.disable_warnings()
db = GetDataBase()
ws = WSO2()

datetime_format = "%d/%m/%Y - %H:%M:%S"

sysdate = datetime.now().strftime('%d/%m/%Y')
sysdateWSO2 = datetime.now().strftime('%m%Y')
sysdateWSO2month = datetime.now().strftime('%m/%Y')

print(str(datetime.now().strftime('%d/%m/%Y-%H:%M:%S')+': Inicio da atividade'))

#--------------------------- Lê arquivo de controle de transferencias já avaliadas ---------------------------
listControl = open('C:/Automations/transferences/control/Control.txt', 'r', encoding='utf-8').readlines()
list_Control = []

for n in listControl:
     list_Control.append(n.rstrip())


json_object = ws.wso2(sysdateWSO2)
blazon = db.blazon()

conta_auditavel = 'NÃO'
gerou_certif = 'NÃO'
status_certif = 'NÃO SE APLICA'

transfControl = open('C:/Automations/transferences/control/Control.txt', 'a', encoding='utf-8')

with open('C:/Automations/transferences/reports/AuditTransferencias.csv', 'a+', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')

    for transf in json_object['result']['employees']:
        if (transf['transferenceMotive'] in ('Transferir Grupo Hierárquico','Centro de Custo')) and (sysdateWSO2month in transf['transferenceStartDate'])\
                and (str(transf) not in list_Control):
            transfControl.writelines(str(transf) + "\n")

            #verifica se possui contas auditaveis
            for bl in blazon:
                if bl[4] == transf['cpf']:
                    conta_auditavel = 'SIM'
                    id_blazon = bl[0]
                    pass
            dataCertif = '01/01/1900'
            idCertif = 'NÃO SE APLICA'

            # verifica se gerou certificação
            if conta_auditavel == 'SIM' and id_blazon != 0:
                # fazendo select para certificação
                blazon_certif = db.blazoCertif(str(id_blazon))
                dataCertif = transf['transferenceStartDate'][:10]
                idCertif = ''
                for blz_cert in blazon_certif:
                    if idCertif == '':
                        idCertif = str(blz_cert[2])
                    else:
                        idCertif = str(idCertif) +' | '+ str(blz_cert[2])


                if id_blazon != 0 and blazon_certif != []:
                    gerou_certif = 'SIM'

                    if 'ERROR' in blazon_certif:
                        status_certif = 'ERRO'
                    else:
                        status_certif = 'CORRETO'

            writer.writerow([str(transf['name']).upper(), str(transf['cpf']), str(conta_auditavel), str(gerou_certif),str(status_certif),str(dataCertif),str(idCertif),str(transf['transferenceMotive'].upper()),str(sysdate)])
            id_blazon = 0

        conta_auditavel = 'NÃO'
        gerou_certif = 'NÃO'
        status_certif = 'NÃO SE APLICA'

transfControl.close()

print(str(datetime.now().strftime('%d/%m/%Y-%H:%M:%S')+': Fim da atividade'))
