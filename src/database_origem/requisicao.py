import requests


class Requisicao:
    def __init__(self):
        pass
    
    def retorna_requisicao_json(self, url_get) -> dict:
        
        response = requests.get(url_get) 
        if response.status_code != 200:
            raise ('falha na requisicao, Eror: ', response.content)            
    
        return response.json()
    
    
    def retorna_requisicao_texto(self, url_get) -> dict:
        response = requests.get(url_get) 
        if response.status_code != 200:
            raise ('falha na requisicao, Eror: ', response.content)            
    
        return response.content
