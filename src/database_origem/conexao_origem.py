import os
from dotenv import load_dotenv
import psycopg2



class ConexaoBancoOrigem:
    load_dotenv()
    
    def __init__(self):
        self.usuario = os.getenv("POSTGRES_USER_ORIGEM")
        self.senha   = os.getenv("POSTGRES_PASSWORD_ORIGEM")

    def conectar_banco_origem(self):
        return psycopg2.connect(database="origem",
                                host="localhost",
                                user=self.usuario,
                                password= self.senha,
                                port="5432")




