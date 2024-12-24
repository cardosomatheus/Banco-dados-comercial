import os
from dotenv import load_dotenv


load_dotenv()
# dados de conexao do banco
DB_USUARIO = os.getenv("POSTGRES_USER_ORIGEM")
DB_SENHA   = os.getenv("POSTGRES_PASSWORD_ORIGEM")
DATABASE   = "origem"
DB_HOST    = "localhost"
DB_PORT    = "5432"

DATA_DIR = "./data"