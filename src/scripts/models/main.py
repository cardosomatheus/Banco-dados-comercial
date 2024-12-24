from pais    import Pais
from estados import Estados
from cidade  import Cidade
from regiao  import Regiao
from cliente import Cliente
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


if __name__ == '__main__':
    Pais().inserir_paises()
    Estados().inserir_estados()
    Cidade().Inserir_cidades_por_uf()
    Regiao().inserir_regiao()
    Cliente().inserir_clientes(quantidade=150)
