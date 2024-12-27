import psycopg2
from faker import Faker
from conexao_bd import conexao_bd
from regiao import Regiao


class Cliente:
    def __init__(self) -> None:
        """
        Inicializa a classe Cliente com a biblioteca Faker e instância de Região.
        """
        self.faker = Faker('pt_BR')
        self.regiao = Regiao()


    def obter_dict_clientes(self, quantidade: int = 100) -> dict:
        """
        Gera um dicionário com CPFs e nomes fictícios.
        Args:    quantidade (int): Número de clientes a serem gerados. Default é 100.
        Returns: dict: Dicionário com CPFs como chaves e nomes como valores.
        Raises:  ValueError: Caso o argumento `quantidade` não seja um número inteiro.
        """
        if not isinstance(quantidade, int):
            raise ValueError("Informe um valor inteiro para 'quantidade'.")

        clientes = {self.faker.ssn(): self.faker.name() for i in range(quantidade+1)}
        return clientes


    def inserir_clientes(self, quantidade: int = 100) -> None:
            """
            Insere clientes no banco de dados com dados gerados aleatoriamente.
            Args:
                quantidade (int): Número de clientes a serem inseridos. Default é 100.
            Raises:
                Exception: Caso ocorra algum erro durante a execução.
            """
            
            clientes = self.obter_dict_clientes(quantidade)
            dados_clientes = [(nome, cpf, self.regiao.busca_regiao_aleatoria()) for cpf, nome in clientes.items()]
            
            print('Log: Processo de Clientes Inicializado.\n')            
            with conexao_bd() as conexao:
                with conexao.cursor() as cursor:                    
                    query ="""INSERT INTO TB_CLIENTE (NOME, DOCUMENTO, ID_REGIAO) 
                                VALUES (%s, %s, %s)
                               ON CONFLICT (DOCUMENTO) DO NOTHING;
                            """
                    psycopg2.extras.execute_batch(cur=cursor,sql=query, argslist=dados_clientes)
                    conexao.commit()
            print('Log: Processo de Clientes finalizado.\n')
                    