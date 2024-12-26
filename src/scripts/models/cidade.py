from conexao_bd import conexao_bd
import psycopg2
from requisicao import Requisicao
from estados import Estados

class Cidade(Requisicao):
    """
    Classe para gerenciar operações relacionadas a cidades, incluindo inserção de dados no banco de dados e busca de IDs de cidades.
    Herda de: Requisicao: Classe base para gerenciar requisições à API.
    Atributos:
      url_get (str): URL base da API do IBGE para obter dados das cidades por estado.
      estado (Estados): Instância da classe Estados para auxiliar no gerenciamento de estados.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe Cidade, configurando a URL base e instanciando dependências necessárias.
        """
        super().__init__()
        self.url_get = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/'  # {UF}/municipios
        self.estado = Estados()

    def __inserir_cidades(self, id_estado: int, cidade: list[dict]) -> None:
        """
        Insere as cidades de um estado específico no banco de dados.
        Insere os dados em batch para melhorar a performance e utiliza ON CONFLICT para evitar duplicidade.
        Args:
            id_estado (int): ID do estado ao qual as cidades pertencem.
            cidade (list[dict]): Lista de dicionários com os dados das cidades obtidas da API.
        Raises:
            Exception: Se ocorrer um erro ao inserir os dados no banco de dados.
        """
        data = [(row.get('nome'), row.get('id'), id_estado) for row in cidade]
    
        with conexao_bd() as conexao:
            with conexao.cursor() as cursor:
                try:
                    query = """INSERT INTO TB_CIDADE (NOME, ID_IBGE, ID_ESTADO) 
                                VALUES (%s, %s, %s) 
                                ON CONFLICT (ID_IBGE) DO NOTHING"""
                    
                    psycopg2.extras.execute_batch(cursor, query, data)
                    conexao.commit()
                except Exception as e:
                    conexao.rollback()
                    raise Exception(f"Erro ao inserir cidades no estado {id_estado}: {e}")
           
    def Inserir_cidades_por_uf(self) -> None:
        """
        Insere as cidades de todos os estados no banco de dados.
        Para cada estado, realiza uma requisição à API do IBGE para obter os dados das cidades e os insere no banco.
        Raises:
            Exception: Se a lista de estados estiver vazia.
        """
        estados_json = self.estado.lista_estados()
        
        if estados_json is None:
            raise Exception("Lista de estados vazia.")
        
        print('LOG: Processo de Cidades Iniciado.\n') 
        for row in estados_json:
            sigla = row.get('sigla')
            url_cidade_por_uf = self.url_get + sigla + '/municipios'
            cidades_por_uf = super().retorna_requisicao_json(url_cidade_por_uf)
            
            if not cidades_por_uf:
                continue
            self.__inserir_cidades(row.get('id'), cidade=cidades_por_uf)
            
        print('LOG: Processo de Cidades Finalizado.\n') 
            
    def buscar_id_cidade(self, nome: str, id_estado: int) -> int:
        """
        Busca o ID de uma cidade específica no banco de dados, com base no nome e no estado.
        Args:
          nome (str): Nome da cidade a ser buscada.
          id_estado (int): ID do estado ao qual a cidade pertence.
        Returns:
            int: ID da cidade se encontrada, ou None caso não exista.
        """
        query = """SELECT ID FROM TB_CIDADE WHERE NOME= %s AND ID_ESTADO = %s"""
        with conexao_bd() as conexao:
            with conexao.cursor() as cursor:
                try:
                    cursor.execute(query, (nome, id_estado))
                    resultado = cursor.fetchone()
                    
                    if resultado:
                        return resultado[0]
                    return None
                except TypeError:
                    return None