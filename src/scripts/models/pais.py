import pandas as pd
import psycopg2
from bs4 import BeautifulSoup
from conexao_bd import conexao_bd
from requisicao import Requisicao


class Pais(Requisicao):
    def __init__(self):
        super().__init__()
        self.conexao =  conexao_bd()
        self.url_get = 'https://www.sport-histoire.fr/pt/Geografia/Paises_por_ordem_alfabetica.php'


    def busca_tabela_de_paises(self) -> pd.DataFrame:
        response = super().retorna_requisicao_texto(self.url_get)
        soup = BeautifulSoup(response, 'html.parser')
        table = soup.find('table')
        return pd.read_html(str(table), skiprows=1)[0]
         

    def inserir_paises(self) -> None:
        df_pandas = self.busca_tabela_de_paises()
        
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


    def buscar_id_pais (self) -> int:
        with self.conexao.cursor() as cursor:
            cursor.execute( """SELECT ID  FROM TB_PAIS WHERE NOME = 'Brasil' AND CONTINENTE = 'América' """)
            return cursor.fetchone()[0]

if __name__ == '__main__':
    pais = Pais()
    pais.inserir_paises()
