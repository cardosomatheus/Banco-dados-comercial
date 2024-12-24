from conexao_bd import conexao_bd
from psycopg2.errors import UniqueViolation
from requisicao import Requisicao
from estados import Estados
from cidade import Cidade
import pandas as pd



class Regiao():
    def __init__(self) -> None:
        super().__init__()
        self.estados = Estados()
        self.cidade  = Cidade()
        self.conexao = conexao_bd()
    
    def busca_regiao_ramdomica(self) -> int:
        sql = """SELECT id
                    FROM tb_regiao
                   ORDER BY RANDOM()
                   LIMIT 1;"""
                   
        with self.conexao.cursor() as cursor:
            cursor.execute(sql)
            
            return cursor.fetchone()[0]
    
    def leitura_json(self) -> pd.DataFrame:
        df = pd.read_json(r'src\fonte_dados\_bairros_brasil.json', orient='records', encoding='utf-8')
        return df


    def inserir_regiao(self):
        df_pandas = self.leitura_json()

        print('Inciando inserção de regiões.')        
        with self.conexao.cursor() as cursor:
            
            for row in df_pandas.to_records(index=False):
                id_estado = self.estados.buscar_id_estado(row['estado'])
                id_cidade = self.cidade.buscar_id_cidade(row['cidade'], id_estado)
                
                if id_estado is not None and id_cidade is not None:
                    try:
                        cursor.execute("""INSERT 
                                            INTO TB_REGIAO (LATITUDE, LONGITUDE, BAIRRO, ID_CIDADE)
                                           VALUES (%s, %s, %s,%s);
                                        """, (str(row['latitude']), str(row['longitude']), row['bairro'], id_cidade))
                        self.conexao.commit()

                    except UniqueViolation as id_regiao:
                        self.conexao.rollback()
                        continue            

        print('LOG: Inserção de Regiões finalizada.\n')    

if __name__ == '__main__':
    regiao = Regiao()
    regiao.inserir_regiao()
 