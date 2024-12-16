import requests
import pandas as pd
import psycopg2
from bs4 import BeautifulSoup
from conexao_origem import ConexaoBancoOrigem
from requisicao import Requisicao

class Pais(Requisicao):
    def __init__(self):
        self.conexao = ConexaoBancoOrigem().conectar_banco_origem()
        super().__init__()


    def busca_tabela_de_paises(self, url_site: str) -> pd.DataFrame:
        response = super().retorna_requisicao_texto(url_site)
        soup = BeautifulSoup(response, 'html.parser')
        table = soup.find('table')
        return pd.read_html(str(table), skiprows=1)[0]
         


    def inserir_paises(self, url_site:str ) -> None:
        df_pandas = self.busca_tabela_de_paises(url_site)
        
        with self.conexao.cursor() as cursor:
            for row in df_pandas.to_records(index=False):
                try:
                    cursor.execute("""INSERT INTO TB_PAIS (NOME, CAPITAL, CONTINENTE)
                                    VALUES (%s, %s, %s);
                                   """, row)
                    self.conexao.commit()

                except psycopg2.errors.UniqueViolation as iq_pais:
                    self.conexao.rollback()
                    continue

        print('Paises inseridos com sucesso.')



if __name__ == '__main__':
    pais = Pais()
    pais.inserir_paises(url_site='https://www.sport-histoire.fr/pt/Geografia/Paises_por_ordem_alfabetica.php')
