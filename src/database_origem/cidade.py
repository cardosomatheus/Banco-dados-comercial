from conexao_origem import ConexaoBancoOrigem
from psycopg2.errors import UniqueViolation
from requisicao import Requisicao


class Cidade(Requisicao):
    def __init__(self):
        super().__init__()
        self.url_get = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/' #{UF}/municipios'         
        self.conexao = ConexaoBancoOrigem().conectar_banco_origem()

  
    def lista_estados(self) -> dict:
        with self.conexao.cursor() as cursor:
            cursor.execute(""" SELECT JSON_AGG(JS)::JSONB 
                                    FROM (SELECT ID, SIGLA 
                                            FROM TB_ESTADO) JS ;
                           """ )
            
            return cursor.fetchall()[0][0]
    
    
    def Inserir_cidades_por_uf(self) -> None:
        estados_json = self.lista_estados()
        
        for row in estados_json:
            sigla = row.get('sigla')
            url_cidade_por_estado = self.url_get+sigla+'/municipios'
            cidades_por_uf = super().retorna_requisicao_json(url_cidade_por_estado)
                     
            print('Cidades da uf: ',sigla)
            self.__inserir_cidades(row.get('id'), cidade=cidades_por_uf)
            
        
        
        
    def __inserir_cidades(self, id_estado, cidade) -> dict:
        with self.conexao.cursor() as cursor:
            for row in cidade:
                try:
                    cursor.execute("""INSERT INTO TB_CIDADE (NOME,ID_IBGE, ID_ESTADO)
                                        VALUES(%s,%s,%s)""", (row.get('nome'),row.get('id'), id_estado))
                    self.conexao.commit()
                    
                except UniqueViolation as iq_estado:                                      
                    self.conexao.rollback()
                    continue 

                

    

if __name__ == '__main__':
    cidade = Cidade()
    cidade.Inserir_cidades_por_uf()

    