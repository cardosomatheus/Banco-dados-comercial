from conexao_bd import conexao_bd
from psycopg2.errors import UniqueViolation
from requisicao import Requisicao
from estados import Estados


class Cidade(Requisicao):
    def __init__(self) -> None:
        super().__init__()
        self.url_get = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/' #{UF}/municipios'         
        self.conexao = conexao_bd()
        self.estado  = Estados() 
  

    
    
    def Inserir_cidades_por_uf(self) -> None:
        estados_json = self.estado.lista_estados()
        
        for row in estados_json:
            sigla = row.get('sigla')
            url_cidade_por_estado = self.url_get+sigla+'/municipios'
            cidades_por_uf = super().retorna_requisicao_json(url_cidade_por_estado)
                     
            print('Cidades da uf: ',sigla)
            self.__inserir_cidades(row.get('id'), cidade=cidades_por_uf)
            
        
        
        
    def __inserir_cidades(self, id_estado, cidade) -> None:
        with self.conexao.cursor() as cursor:
            for row in cidade:
                try:
                    cursor.execute("""INSERT INTO TB_CIDADE (NOME,ID_IBGE, ID_ESTADO)
                                        VALUES(%s,%s,%s)""", (row.get('nome'),row.get('id'), id_estado))
                    self.conexao.commit()
                    
                except UniqueViolation as iq_estado:                                      
                    self.conexao.rollback()
                    continue 
    
    def buscar_id_cidade(self, nome:str, id_estado:int) -> int:
        
        with self.conexao.cursor() as cursor:
            try:
                cursor.execute( """SELECT ID FROM TB_CIDADE WHERE UPPER(NOME) = UPPER(TRIM(%s)) AND ID_ESTADO = %s """, (nome,id_estado,))
                                
                return  cursor.fetchone()[0]
            except TypeError:
               return None

                

    

if __name__ == '__main__':
    cidade = Cidade()
    cidade.Inserir_cidades_por_uf()

    