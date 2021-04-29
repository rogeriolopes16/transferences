import mysql.connector
from settings.credentials import *
from settings.parameters import *
from settings.db import *

# --------------------------- Abrindo conexão com MYSql Blazon ---------------------------
db = mysql.connector.connect(user=CRD_USER_DB_BLAZON, passwd=CRD_PWD_DB_BLAZON, host=PAR_BLAZON_IP, db=PAR_BLAZON_DB_NAME)
cursor_blazon = db.cursor()

class GetDataBase():
    def __init__(self):
        pass

    def blazon(self):
        # fazendo select para encontrar usuarios no blazon
        cursor_blazon.execute(SELECT_USERS_ACTIVES_BLAZON)
        return cursor_blazon.fetchall()

    def blazoCertif(self,id_blazon):
        # fazendo select para certificação
        cursor_blazon.execute(SELECT_CERTIFICACAO_BLAZON, (id_blazon,))
        return cursor_blazon.fetchall()