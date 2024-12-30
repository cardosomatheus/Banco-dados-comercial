import psycopg2
from conexao_bd import conexao_bd
from requisicao import Requisicao
from pais import Pais

class Estados(Requisicao):
    def __init__(self):
        """
        Inicializa a classe Estados, herda de Requisicao e configura a URL da API do IBGE para obtenção de dados dos estados.
        """
        super().__init__()
        self.url_get = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
        self.pais = Pais()


    def inserir_estados(self) -> None:
        """
        Insere os estados obtidos da API do IBGE no banco de dados. 
        Realiza inserções em batch para melhorar a performance.
        """
        estados_json = super().retorna_requisicao_json(url_get=self.url_get)
        id_pais = self.pais.buscar_id_pais(nome_pais= 'Brasil', continente= 'América')

        # Preparar os dados para inserção em batch
        data = [(row.get('nome'), row.get('sigla'), id_pais) for row in estados_json]

        with conexao_bd() as conexao:
            with conexao.cursor() as cursor:
                # Inserção em batch
                query = """INSERT 
                            INTO TB_ESTADO(NOME, SIGLA, ID_PAIS) VALUES (%s, %s, %s)
                            ON CONFLICT DO NOTHING;
                        """
                            
                psycopg2.extras.execute_batch(cursor, query, data)
                conexao.commit()


        print('Log: Processo de Estados finalizado.\n')


    def buscar_id_estado(self, sigla: str) -> int:
        """
        Busca o ID de um estado específico no banco de dados, com base na sigla.

        :param sigla: Sigla do estado.
        :return: ID do estado.
        :raises ValueError: Se o estado não for encontrado no banco de dados.
        """
        #sigla = sigla.upper()

        with conexao_bd() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""SELECT ID FROM TB_ESTADO WHERE SIGLA = %s""", (sigla,))
                resultado = cursor.fetchone()

                if resultado:
                    return resultado[0]
                else:
                    raise ValueError(f"Estado com sigla '{sigla}' não encontrado.")


    def lista_estados(self) -> dict:
        """
        Lista todos os estados no banco de dados em formato JSON.

        :return: Dicionário contendo os dados de todos os estados.
        """
        try:
            with conexao_bd() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""SELECT JSON_AGG(JS)::JSONB 
                                      FROM (SELECT ID, SIGLA FROM TB_ESTADO) JS;""")
                    return cursor.fetchall()[0][0]
        except psycopg2.DatabaseError as e:
            return {}



 