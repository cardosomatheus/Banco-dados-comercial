import requests
from conexao_origem import ConexaoBancoOrigem
from psycopg2.errors import UniqueViolation

class Estados:
    def __init__(self):
        self.url_get = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
        self.conexao = ConexaoBancoOrigem().conectar_banco_origem()
    


    def busca_estados(self) -> dict:
        response = requests.get(self.url_get) 
        if response.status_code != 200:
            raise ('falha na requisicao, Eror: ', response.content)            
    
        return response.json()

    
    def inserir_estados(self) -> None:
        # Id_pais vai ser estatico no brasil, pois só vou inserir UFs do brasil por enquanto.
        estados_json = self.busca_estados()
        id_pais = self.buscar_id_pais()
        
        with self.conexao.cursor() as cursor:
            for row in estados_json:
                nome = row.get('nome')
                sigla = row.get('sigla')

                
                try:
                    cursor.execute("""INSERT INTO TB_ESTADO(NOME, SIGLA, ID_PAIS)
                                        VALUES(%s,%s,%s)""", (nome, sigla, id_pais))
                    self.conexao.commit()
                    
                    print(f'Estado {nome+'-'+sigla} inserido com sucesso')
                except UniqueViolation as iq_estado:
                    print(f'Estado {nome+'-'+sigla} Já existe')
                                        
                    self.conexao.rollback()
                    continue     
        print('LOG: Inserção de estados finalizada.')       


    def buscar_id_pais (self) -> int:
        with self.conexao.cursor() as cursor:
            cursor.execute( """SELECT ID 
                                FROM TB_PAIS 
                               WHERE NOME = 'Brasil' 
                                AND CONTINENTE = 'América' 
                            """)
            return cursor.fetchone()[0]

estados =  Estados()
#print(estados.busca_estados())
estados.inserir_estados()
