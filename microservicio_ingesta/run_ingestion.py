from microservicio_ingesta.scripts.ingestion.collect_eurostat.collect_data import collector_eurostat
from microservicio_ingesta.scripts.ingestion.collect_ine.collect_data import collector_ine
from microservicio_ingesta.scripts.ingestion.collect_cnmc.collect_data import collector_cnmc
from microservicio_ingesta.scripts.ingestion.collect_base.collect_macro import collect_renta_per_capita
from microservicio_ingesta.scripts.ingestion.collect_digital_decade.collect_data import collector_digital_decade

def collecting():
    print('[1/5] -- Recogiendo datos de rpc...')
    collect_renta_per_capita()

    print('[2/5] -- Recogiendo datos de eurostat...')
    collector_eurostat()

    print('[3/5] -- Recogiendo datos de ine...')
    collector_ine()

    print('[4/5] -- Recogiendo datos de cnmc...')
    collector_cnmc()

    print('[5/5] -- recogiendo datos de digital-decade...')
    collector_digital_decade()

if __name__ == '__main__':
    collecting()