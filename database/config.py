# config.py
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env
load_dotenv()

# Lee las variables de entorno para la base de datos
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "indicadores")

# Construye la URL de la base de datos de forma segura
SQL_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Opcional: imprimir la URL sin la contraseña para depuración
print(f"Conectando a: postgresql+psycopg2://{DB_USER}:****@{DB_HOST}:{DB_PORT}/{DB_NAME}")