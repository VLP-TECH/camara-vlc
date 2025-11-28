from microservicio_ingesta.run_ingestion import collecting
from microservicio_ingesta.run_processing import processing
from modelos.escribir_ficheros import FileWriter
from microservicio_ingesta.scripts.loading.load_database import loading


if __name__ == '__main__':
    collecting()
    processing()
    loading()
