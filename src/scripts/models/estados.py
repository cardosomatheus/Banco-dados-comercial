from conexao_bd import conexao_bd
from psycopg2.errors import UniqueViolation
from requisicao import Requisicao
from pais import Pais


class Estados(Requisicao):
    def __init__(self):
        super().__init__()
        self.url_get = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
        self.conexao = conexao_bd()
        self.pais    =  Pais()

    
    def inserir_estados(self) -> None:
        # Id_pais vai ser estatico no brasil, pois só vou inserir UFs do brasil por enquanto.
        estados_json = super().retorna_requisicao_json(url_get=self.url_get)
        id_pais = self.pais.buscar_id_pais()
        
        
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


    def buscar_id_estado(self, sigla:str) -> int:
        sigla = sigla.replace(' ','').upper()
        
        with self.conexao.cursor() as cursor:
            try:
                cursor.execute( """SELECT ID FROM TB_ESTADO WHERE SIGLA = %s """, (sigla,))                          
                return  cursor.fetchone()[0]
            
            except TypeError:
               return None
       
       
    def lista_estados(self) -> dict:
        with self.conexao.cursor() as cursor:
            cursor.execute(""" SELECT JSON_AGG(JS)::JSONB 
                                    FROM (SELECT ID, SIGLA 
                                            FROM TB_ESTADO) JS ;
                           """ )
            
            return cursor.fetchall()[0][0]     

if __name__ == '__main__':
    estados =  Estados()
    print(estados.buscar_id_estado('  Mg  '))
    estados.inserir_estados()
