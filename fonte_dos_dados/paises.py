import requests
import pandas as pd
import psycopg2
from bs4 import BeautifulSoup


def conectar_banco_origem():
    return psycopg2.connect(database="user_origem",
                            host="localhost",
                            user="user_origem",
                            password="mcds123origem",
                            port="5432")


def busca_requisicao(url_site: str) -> str:
    requisicao = requests.get(url_site)

    if requisicao.status_code != 200:
        raise ('falha na requisicao, Eror: ', requisicao.content)

    return requisicao.content


def busca_tabela_de_paises(url_site: str) -> pd.DataFrame:
    response = busca_requisicao(url_site)

    soup = BeautifulSoup(response, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table), skiprows=1)[0]
    return df


def inserir_paises(df_pandas=pd.DataFrame) -> None:
    conexao = conectar_banco_origem()

    with conexao.cursor() as cursor:
        cursor.executemany("""INSERT INTO TB_PAIS (NOME, CAPITAL, CONTINENTE)
                                VALUES (%s, %s, %s);""", df_pandas.to_records(index=False))
        conexao.commit()

    print('Paises inseridos com sucesso.')


if __name__ == '__main__':
    dataframe = busca_tabela_de_paises(
        url_site='https://www.sport-histoire.fr/pt/Geografia/Paises_por_ordem_alfabetica.php')
    inserir_paises(df_pandas=dataframe)

    print('Processo finalizado.')
