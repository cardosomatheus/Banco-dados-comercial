from faker import Faker
from conexao_bd import conexao_bd
from psycopg2.errors import UniqueViolation
from regiao import Regiao

class Cliente:
    def __init__(self):
        self.faker = Faker('pt_BR')
        self.conexao = conexao_bd()
        self.dict_clientes = {}
        self.regiao = Regiao()
        
    
    def obter_dict_clientes(self,quantidade:int=100) -> dict:
        if isinstance(quantidade, int):
            for row in range(1,quantidade+1):
                nome = self.faker.name()
                cpf  = self.faker.ssn()
                self.dict_clientes.update({cpf: nome})                

            return self.dict_clientes      
              
        else:
            raise ('Informe um valor Inteiro na obter_dict_clientes()')



    def inserir_clientes(self,quantidade:int=100) -> None:
        clientes = self.obter_dict_clientes(quantidade)
                
        with self.conexao.cursor() as cursor:
            print('Iniciando inserção de cliente')
            for cpf,nome in clientes.items():
                try:
                    id_regiao = self.regiao.busca_regiao_ramdomica()                    
                    cursor.execute("""INSERT INTO TB_CLIENTE (NOME, DOCUMENTO, ID_REGIAO)
                                            VALUES (%s, %s, %s);""", (nome,cpf,id_regiao))
                    self.conexao.commit()

                except UniqueViolation as iq_pais:
                    self.conexao.rollback()
                    continue        
            print('processo finalizado')


cliente = Cliente()
print(cliente.inserir_clientes(150))