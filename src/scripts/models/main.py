from pais    import Pais
from estados import Estados
from cidade  import Cidade
from regiao  import Regiao
from cliente import Cliente
from time    import sleep


if __name__ == '__main__':
    print('O processo do main.py foi Iniciado!')
    sleep(10) # 10 sec para banco do docker se configurar e termos conexao.
    Pais().inserir_paises()
    Estados().inserir_estados()
    Cidade().Inserir_cidades_por_uf()
    Regiao().inserir_regiao()
    Cliente().inserir_clientes(quantidade=150)

    print('O processo do main.py foi executado!')