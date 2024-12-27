from conexao_bd import conexao_bd
from psycopg2.errors import UniqueViolation
from requisicao import Requisicao
from estados import Estados
from cidade import Cidade
import pandas as pd


class Regiao:
    """
    Classe para gerenciar operações relacionadas a regiões, incluindo inserção no banco de dados e busca de regiões aleatórias.

    Atributos:
        estados (Estados): Instância da classe Estados para busca de informações relacionadas a estados.
        cidade (Cidade): Instância da classe Cidade para busca de informações relacionadas a cidades.
        conexao (function): Função para gerenciar a conexão com o banco de dados.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe Regiao, configurando as dependências necessárias.
        """
        self.estados = Estados()
        self.cidade = Cidade()
        self.file_bairros_brasil =  r'src\fonte_dados\_bairros_brasil.json'

    def busca_regiao_aleatoria(self) -> int:
        """
        Busca uma região aleatória no banco de dados.
        Returns:
            int: ID de uma região selecionada aleatoriamente.
        """
        sql = """ SELECT id FROM tb_regiao ORDER BY RANDOM() LIMIT 1;"""
        with conexao_bd() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(sql)
                resultado = cursor.fetchone()
                if resultado:
                    return resultado[0]
                return None


    def leitura_json(self) -> pd.DataFrame:
        """
        Lê um arquivo JSON e converte os dados em um DataFrame do pandas.
        Returns:
            pd.DataFrame: DataFrame contendo os dados do JSON.
        """
        try:
            df =  pd.read_json(self.file_bairros_brasil, orient='records', encoding='utf-8')
            df["id_cidade"] = ''   
            
            if df.empty:
                raise Exception("O arquivo JSON não contém dados.")   
                             
            print('LOG: Adicinando id_cidade no Dataframe, aguarde...')                             
            for index, row in df.iterrows():
                id_estado = self.estados.buscar_id_estado(sigla=row[0])
                id_cidade = self.cidade.buscar_id_cidade(nome=row[1], id_estado=id_estado)
                df.at[index,"id_cidade"] = id_cidade
                
            print('LOG: Finalizado dataframe, partiu inserção')                             
            return df
        
        except Exception as e:
            raise Exception(f"Erro ao ler o arquivo JSON: {e}")
        

    def inserir_regiao(self) -> None:
        """
        Insere as regiões no banco de dados, utilizando os dados de um arquivo JSON.
        Realiza a inserção para cada registro, associando a região com o estado e a cidade correspondente.
        Ignora duplicidades utilizando o tratamento de exceções.
        """
        df_pandas = self.leitura_json()

        data = ((str(row['latitude']), str(row['longitude']), row['bairro'], row["id_cidade"]) for row in df_pandas.to_records(index=False))
        
        print('LOG: Processo de regiões Inicializado.')
        query = """
                 INSERT INTO TB_REGIAO (LATITUDE, LONGITUDE, BAIRRO, ID_CIDADE)
                    VALUES (%s, %s, %s, %s)
                   ON CONFLICT (LATITUDE, LONGITUDE) DO NOTHING;
                """
                
        with conexao_bd() as conexao:
            with conexao.cursor() as cursor:                        
                try:
                    psycopg2.extras.execute_batch(cur=cursor, sql=query, argslist= data)   
                    conexao.commit()
                except Exception as e:
                    conexao.rollback()

        print('LOG: Processo de regiões Finalizado.')





