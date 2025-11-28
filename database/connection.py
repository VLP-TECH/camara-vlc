from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.config import SQL_DATABASE_URL

# Se crea el engine una vez en toda la aplicación
engine = create_engine(SQL_DATABASE_URL)

# Se crea la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Se crea la base declarativa que usarán todos los modelos
Base = declarative_base()

def get_db():
    """
    Generador de dependencia para FastAPI.
    Crea una sesión nueva para cada petición y la cierra al terminar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()