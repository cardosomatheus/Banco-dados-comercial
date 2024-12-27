import pandas as pd
import psycopg2
from bs4 import BeautifulSoup
import psycopg2.extras
from conexao_bd import conexao_bd
from requisicao import Requisicao
from io import StringIO


class Pais(Requisicao):
    def __init__(self):
        """
        Inicializa a classe Pais, que herda de Requisicao e define a URL para buscar os dados de países.
        """
        super().__init__()
        self.url_get = 'https://www.sport-histoire.fr/pt/Geografia/Paises_por_ordem_alfabetica.php'


    def busca_tabela_de_paises(self) -> pd.DataFrame:
        """
        Realiza uma requisição para obter a tabela de países em formato HTML e a converte para um DataFrame.
        
        :return: Um DataFrame contendo os países, suas capitais e continentes.
        :raises Exception: Se a requisição falhar, se a tabela não for encontrada ou se ocorrer um erro no processo.
        """
        try:
            # Tentando fazer a requisição            
            response = super().retorna_requisicao_texto(self.url_get)
            if not response:
                raise Exception("Requisição vazia na url:", self.url_get)
        
            # Buscando Tabela HTML de países
            soup = BeautifulSoup(response, 'html.parser')
            table = soup.find('table')
    
            # Exceção caso a tabela esteja vazia
            if table is None:
                raise Exception("Tabela não encontrada no HTML da página.")
            
            return self._leitura_tabela_html(str(table))

        except Exception as e:
            # Captura outros erros, como de parsing ou de leitura de tabela
            raise Exception(f"Erro ao buscar tabela de países: {e}")
        


    def _leitura_tabela_html(self, tabela_pandas_html: str) -> pd.DataFrame:
        """
        Converte o conteúdo da tabela HTML para um DataFrame do pandas.

        :param tabela_pandas_html: A tabela HTML em formato string que será convertida.
        :return: Um DataFrame contendo os dados da tabela de países.
        :raises ValueError: Se a tabela contiver dados insuficientes ou estiver vazia.
        """
        # Extrai o conteúdo da tabela para um DataFrame
        df = pd.read_html(StringIO(tabela_pandas_html), skiprows=1)[0]
        if df.empty or df.shape[1] < 3:
            raise ValueError("Erro ao processar a tabela de países: dados insuficientes.")

        df.columns = ['NOME', 'CAPITAL', 'CONTINENTE']  # Renomeia colunas
        return df
    


    def inserir_paises(self) -> None:
        """
        Insere os países obtidos na tabela em um banco de dados PostgreSQL.

        Conecta ao banco de dados e insere os dados dos países, utilizando uma inserção em batch.
        Caso o país já exista (conflito), ignora a inserção para esse país.

        :raises Exception: Se ocorrer algum erro durante o processo de inserção.
        """
        df_pandas = self.busca_tabela_de_paises()
        data = [tuple(row) for row in df_pandas.to_records(index=False)]
        query = """INSERT INTO TB_PAIS (NOME, CAPITAL, CONTINENTE)
                    VALUES (%s, %s, %s)  
                ON CONFLICT DO NOTHING;
                """
        with conexao_bd() as conexao:
            with conexao.cursor() as cursor:             
                psycopg2.extras.execute_batch(cursor, query, data)
                conexao.commit()

                    

        print('Log: Processo de países finalizado.\n')


    def buscar_id_pais(self, nome_pais: str = 'Brasil', continente: str = 'América') -> int:
        """
        O valor será estático no Brasil até então.
        Busca o ID de um país específico no banco de dados, com base no nome e no continente.

        :param nome_pais: Nome do país. Padrão é 'Brasil'.
        :param continente: Nome do continente. Padrão é 'América'.
        :return: O ID do país encontrado.
        :raises ValueError: Se o país não for encontrado no banco de dados.
        """
        query = """SELECT ID FROM TB_PAIS WHERE NOME = %s AND CONTINENTE = %s;"""
        
        with conexao_bd() as conexao:
            with conexao.cursor() as cursor:  
                cursor.execute(query, (nome_pais, continente))
                resultado = cursor.fetchone()
                
                if resultado:
                    return resultado[0]
                else:
                    raise ValueError(f"País '{nome_pais}' no continente '{continente}' não encontrado.")

Pais().inserir_paises()