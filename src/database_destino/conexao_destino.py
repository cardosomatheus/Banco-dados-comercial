import os
from dotenv import load_dotenv
import psycopg2



class ConexaoBancoDestino:
    load_dotenv()
    
    def __init__(self):
        self.usuario = os.getenv("POSTGRES_USER_ORIGEM")
        self.senha   = os.getenv("POSTGRES_PASSWORD_ORIGEM")

    def conectar_banco_destino(self):
        return psycopg2.connect(database="postgresql",
                                host="localhost",
                                user=self.usuario,
                                password=self.senha,
                                port="5432")    