import psycopg2
from src.config import DATABASE, DB_HOST, DB_PORT, DB_SENHA, DB_USUARIO



def conectar_banco_origem():
    try:
        print(f"Conectando ao banco {DB_HOST} com o usuário {DB_USUARIO}...")
        #return psycopg2.connect(database= DATABASE,
        #                    host    = DB_HOST,
        #                    user    = DB_USUARIO,
        #                    password= DB_SENHA,
        #                    port    = DB_PORT)
    except Exception as e:
        print('Erro ao se conectar com o banoc: ', e)
        return None


#with conectar_banco_origem().cursor() as cursor:
#    cursor.execute('Select count(*) from TB_PAIS')
#    print(cursor.fetchone())

