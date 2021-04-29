import requests
import json


class WSO2():
    def __init__(self):
        pass

    def wso2(self, sysdateWSO2):
        #----------------- fazendo pesquisa no WSO2 para buscar admitidos do dia -----------------
        newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post('https://wso2-am-gw.algarnet.com.br/employees/transferences',
                                 data="{'date': '"+sysdateWSO2+"'}",
                                 headers=newHeaders,
                                 verify=False)

        response_Json = json.dumps(response.json())
        return json.loads(response_Json)