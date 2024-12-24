import psycopg2
import os
import sys
sys.path.insert(0,os.path.abspath('.'))

from src.config.config import DATABASE, DB_HOST, DB_PORT, DB_SENHA, DB_USUARIO


def conexao_bd():
    try:
        return psycopg2.connect(database= DATABASE,
                                host    = DB_HOST,
                                user    = DB_USUARIO,
                                password= DB_SENHA,
                                port    = DB_PORT)
    except Exception as e:
        print(e)
