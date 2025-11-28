import shutil
from pathlib import Path

def recrear_carpeta_vacia(ruta_carpeta: str):
    """
    Comprueba si una carpeta existe. Si existe, la elimina junto con
    todo su contenido y luego la vuelve a crear vacía.
    """
    path_obj = Path(ruta_carpeta)

    # 1. Si la carpeta existe, eliminarla recursivamente
    if path_obj.exists():
        print(f"Directorio '{ruta_carpeta}' encontrado. Eliminando...")
        shutil.rmtree(path_obj)
    
    # 2. Crear la carpeta vacía (y sus padres si es necesario)
    path_obj.mkdir(parents=True)
    print(f"Directorio '{ruta_carpeta}' creado vacío.")

def configurar_entorno():
    """Crea toda la estructura de directorios necesaria para el proyecto."""
    print("Limpiando y re-configurando la estructura de directorios del proyecto...")
    RUTAS = [
        'data/raw/ine',
        'data/raw/eurostat',
        'data/raw/WorldBank',
        'data/raw/digital_decade',
        'data/raw/cnmc/compressed',
        'data/raw/cnmc/uncompressed',
        'data/processed/eurostat/unfiltered',
        'data/processed/eurostat/filtered/resultado',
        'data/processed/eurostat/filtered/crudo',
        'data/processed/ine/unfiltered',
        'data/processed/ine/filtered/resultado',
        'data/processed/ine/filtered/crudo',
        'data/processed/cnmc/unfiltered',
        'data/processed/cnmc/filtered/resultado',
        'data/processed/cnmc/filtered/crudo',
        'data/processed/WorldBank/filtered/crudo',
        'data/processed/digital_decade/filtered/resultado',
        'data/processed/digital_decade/filtered/crudo',
        'data/processed/digital_decade/unfiltered'
    ]

    for ruta in RUTAS:
        recrear_carpeta_vacia(ruta)
    
    print("\nEstructura de directorios configurada con éxito.")

if __name__ == '__main__':
    # Pequeña confirmación del usuario antes de la operación destructiva
    confirmacion = input("Este script eliminará y recreará las carpetas de datos. ¿Estás seguro? (s/N): ")
    if confirmacion.lower() == 's':
        configurar_entorno()
    else:
        print("Operación cancelada.")