import requests
from requests.exceptions import RequestException


class Requisicao:
    def __init__(self, timeout: int = 10):
        """
        Classe para lidar com requisições HTTP.
        :param timeout: Tempo máximo de espera para resposta, em segundos.
        """
        self.timeout = timeout
    
    
    def _execulta_requisicao(self, url_get: str, headers: dict = None, params: dict = None) -> requests.Response:
        """
        Realiza uma requisição GET e retorna a resposta em formato JSON.
        :param url_get: URL para a requisição GET.
        :param headers: Headers adicionais para a requisição (opcional).
        :param params: Parâmetros para a URL (opcional).
        :return: Retor o responde da requisiçãp 
        :raises: Exception em caso de erro na requisição.
        """
        try:
            response = requests.get(url_get, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()  # Levanta um erro se o status HTTP não for 2xx
            return response
        
        except RequestException as e:
            raise Exception(f"Falha na requisição para {url_get}. Erro: {e}")
        
        
    def retorna_requisicao_json(self, url_get: str, headers: dict = None, params: dict = None) -> dict:
        """
        Realiza uma requisição GET e retorna a resposta em formato JSON.
        :param url_get: URL para a requisição GET.
        :param headers: Headers adicionais para a requisição (opcional).
        :param params: Parâmetros para a URL (opcional).
        :return: Resposta da requisição em formato JSON.
        :raises: Exception em caso de erro na requisição.
        """
        response = self._execulta_requisicao(url_get, headers=headers, params=params)
        return response.json()


    def retorna_requisicao_texto(self, url_get: str, headers: dict = None, params: dict = None) -> str:
        """
        Realiza uma requisição GET e retorna a resposta como texto.
        :param url_get: URL para a requisição GET.
        :param headers: Headers adicionais para a requisição (opcional).
        :param params: Parâmetros para a URL (opcional).
        :return: Resposta da requisição em formato texto.
        :raises: Exception em caso de erro na requisição.
        """
        response = self._execulta_requisicao(url_get, headers=headers, params=params)
        return response.content
