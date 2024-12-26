import psycopg2
import os
import sys
from contextlib import contextmanager
sys.path.insert(0,os.path.abspath('.'))

from src.config.config import DATABASE, DB_HOST, DB_PORT, DB_SENHA, DB_USUARIO

@contextmanager
def conexao_bd():
    try:
        conn = psycopg2.connect(database= DATABASE,
                                host    = DB_HOST,
                                user    = DB_USUARIO,
                                password= DB_SENHA,
                                port    = DB_PORT)
        yield conn
        
    except Exception as e:
        print(e)
    
    finally:
        if conn:
            conn.close()