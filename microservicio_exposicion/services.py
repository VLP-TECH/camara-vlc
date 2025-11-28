from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, extract, or_, distinct
from collections import defaultdict
from database.modelos import (
    ResultadoIndicador, ComponenteIndicador, DefinicionIndicador, 
    Subdimension, Dimension, ProcessedDatoCrudo, DatoCrudo
)

def obtener_filtros_unicos(db: Session, columna):
    """
    Helper genérico para sacar valores únicos de una columna de ResultadoIndicador
    """
    return db.query(distinct(columna)).order_by(columna.asc()).all()

def obtener_filtros_disponibles(
    db: Session, 
    pais: str = None, 
    periodo: int = None, 
    sector: str = None, 
    tamano: str = None,
    nombre_indicador: str = None
):
    # 1. Preparamos los alias
    IndicadorDesdeComponente = aliased(DefinicionIndicador)
    IndicadorDesdeCrudo = aliased(DefinicionIndicador)
    
    # 2. Definimos la columna consolidada del nombre
    nombre_consolidado = func.coalesce(IndicadorDesdeComponente.nombre, IndicadorDesdeCrudo.nombre)

    # 3. Función interna que construye la query CORRECTAMENTE con los JOINS
    def get_distinct_values(target_col):
        # IMPORTANTE: Empezamos seleccionando desde la tabla principal
        q = db.query(distinct(target_col)).select_from(ResultadoIndicador)
        
        # --- APLICAR JOINS SIEMPRE QUE HAYA FILTRO DE NOMBRE ---
        # Sin esto, el filtro where no funciona porque no conoce las tablas unidas
        if nombre_indicador:
            q = q.outerjoin(ResultadoIndicador.componente)\
                 .outerjoin(IndicadorDesdeComponente, ComponenteIndicador.indicador)\
                 .outerjoin(ResultadoIndicador.origen_crudo)\
                 .outerjoin(ProcessedDatoCrudo.dato_crudo_origen)\
                 .outerjoin(IndicadorDesdeCrudo, DatoCrudo.indicador)
            
            q = q.filter(nombre_consolidado == nombre_indicador)

        # --- FILTROS DE CASCADA (Contexto) ---
        q = q.filter(target_col != None) # Nunca devolver nulos

        # Aplicamos filtros cruzados (si selecciono País, filtra Sectores, etc.)
        if pais and target_col != ResultadoIndicador.pais:
            q = q.filter(ResultadoIndicador.pais == pais)
            
        if periodo and target_col != extract('year', ResultadoIndicador.periodo):
            q = q.filter(extract('year', ResultadoIndicador.periodo) == periodo)
            
        if sector and target_col != ResultadoIndicador.sector:
            q = q.filter(ResultadoIndicador.sector == sector)

        if tamano and target_col != ResultadoIndicador.tamano_empresa:
            q = q.filter(ResultadoIndicador.tamano_empresa == tamano)

        # Ordenar resultados
        return q.order_by(target_col.asc()).all()

    # 4. Ejecutar consultas
    paises_res = get_distinct_values(ResultadoIndicador.pais)
    sectores_res = get_distinct_values(ResultadoIndicador.sector)
    tamanos_res = get_distinct_values(ResultadoIndicador.tamano_empresa)
    provincias_res = get_distinct_values(ResultadoIndicador.provincia) # <--- ESTO AHORA DEVOLVERÁ DATOS

    # 5. Lógica especial para años (por el extract)
    col_anio = extract('year', ResultadoIndicador.periodo)
    q_anios = db.query(distinct(col_anio)).select_from(ResultadoIndicador).filter(ResultadoIndicador.periodo != None)
    
    # Repetimos los Joins para años también
    if nombre_indicador:
        q_anios = q_anios.outerjoin(ResultadoIndicador.componente)\
                 .outerjoin(IndicadorDesdeComponente, ComponenteIndicador.indicador)\
                 .outerjoin(ResultadoIndicador.origen_crudo)\
                 .outerjoin(ProcessedDatoCrudo.dato_crudo_origen)\
                 .outerjoin(IndicadorDesdeCrudo, DatoCrudo.indicador)\
                 .filter(nombre_consolidado == nombre_indicador)
    
    if pais: q_anios = q_anios.filter(ResultadoIndicador.pais == pais)
    
    anios_res = q_anios.order_by(col_anio.desc()).all()

    return {
        "paises": [r[0] for r in paises_res],
        "sectores": [r[0] for r in sectores_res],
        "tamanos_empresa": [r[0] for r in tamanos_res],
        "provincias": [r[0] for r in provincias_res], # Ahora sí lleva datos
        "anios": [int(r[0]) for r in anios_res]
    }

def obtener_data_consulta(
    db: Session, 
    skip: int = 0, 
    limit: int = 1000,
    pais: str = None,
    periodo: int = None,
    sector: str = None,
    nombre_indicador: str = None,
    tamano: str = None,
    provincia: str = None # <--- 1. ARGUMENTO NUEVO
):
    IndicadorDesdeComponente = aliased(DefinicionIndicador)
    IndicadorDesdeCrudo = aliased(DefinicionIndicador)

    query = db.query(
        func.coalesce(
            IndicadorDesdeComponente.nombre, 
            IndicadorDesdeCrudo.nombre, 
            "Indicador Desconocido"
        ).label('nombre_indicador'),
        ResultadoIndicador.valor_calculado.label('resultado'),
        ResultadoIndicador.periodo,
        ResultadoIndicador.pais,
        ResultadoIndicador.provincia,
        ResultadoIndicador.sector,
        ResultadoIndicador.tamano_empresa
    )

    # Joins
    query = query.outerjoin(ResultadoIndicador.componente)\
                 .outerjoin(IndicadorDesdeComponente, ComponenteIndicador.indicador)\
                 .outerjoin(ResultadoIndicador.origen_crudo)\
                 .outerjoin(ProcessedDatoCrudo.dato_crudo_origen)\
                 .outerjoin(IndicadorDesdeCrudo, DatoCrudo.indicador)

    # --- FILTROS ---
    if pais:
        query = query.filter(ResultadoIndicador.pais == pais)
    
    if provincia:
        query = query.filter(ResultadoIndicador.provincia == provincia)

    if sector:
        query = query.filter(ResultadoIndicador.sector.ilike(f"%{sector}%"))

    if tamano:
        query = query.filter(ResultadoIndicador.tamano_empresa == tamano)

    if periodo:
        query = query.filter(extract('year', ResultadoIndicador.periodo) == periodo)

    if nombre_indicador:
        busqueda = f"%{nombre_indicador}%"
        query = query.filter(
            or_(
                IndicadorDesdeComponente.nombre.ilike(busqueda),
                IndicadorDesdeCrudo.nombre.ilike(busqueda)
            )
        )

    query = query.order_by(ResultadoIndicador.periodo.asc())

    return query.offset(skip).limit(limit).all()
# --- FUNCIÓN 2: Calcular Score Brainnova ---
def calcular_brainnova_score(db: Session, pais: str, periodo: int, sector: str, tamano: str, provincia: str = None):
    MAPA_IMPORTANCIA = {"Alta": 3, "Media": 2, "Baja": 1, "alta": 3, "media": 2, "baja": 1}
    
    DefinicionViaComp = aliased(DefinicionIndicador)
    DefinicionViaCrudo = aliased(DefinicionIndicador)

    # Coalesce para ID e Importancia
    importancia_final = func.coalesce(DefinicionViaComp.importancia, DefinicionViaCrudo.importancia)
    id_subdim_final = func.coalesce(DefinicionViaComp.id_subdimension, DefinicionViaCrudo.id_subdimension)

    query = db.query(
        ResultadoIndicador.valor_calculado,
        importancia_final.label('importancia_texto'),
        Subdimension.id.label('subdim_id'),
        Subdimension.nombre.label('subdim_nombre'),
        Dimension.id.label('dim_id'),
        Dimension.nombre.label('dim_nombre'),
        Dimension.peso.label('dim_peso_porcentaje')
    ).select_from(ResultadoIndicador)

    # Joins Duales (Componente y Crudo)
    query = query.outerjoin(ResultadoIndicador.componente)\
                 .outerjoin(DefinicionViaComp, ComponenteIndicador.indicador)\
                 .outerjoin(ResultadoIndicador.origen_crudo)\
                 .outerjoin(ProcessedDatoCrudo.dato_crudo_origen)\
                 .outerjoin(DefinicionViaCrudo, DatoCrudo.indicador)

    # Join Jerarquía
    query = query.join(Subdimension, Subdimension.id == id_subdim_final)\
                 .join(Dimension, Dimension.id == Subdimension.id_dimension)

    # FILTROS (CORRECCIÓN DE FECHA AQUÍ)
    # Usamos extract('year') porque en BD es DATE y 'periodo' es INT (2023)
    query = query.filter(
        ResultadoIndicador.pais == pais,
        extract('year', ResultadoIndicador.periodo) == periodo, 
        ResultadoIndicador.sector == sector,
        ResultadoIndicador.tamano_empresa == tamano
    )
    
    if provincia:
        query = query.filter(ResultadoIndicador.provincia == provincia)

    resultados = query.all()

    if not resultados:
        return None

    # --- Lógica Matemática (Pirámide) ---
    tree = defaultdict(lambda: defaultdict(list))
    dim_info = {}

    for row in resultados:
        val = float(row.valor_calculado)
        imp = row.importancia_texto if row.importancia_texto else "Baja"
        peso = MAPA_IMPORTANCIA.get(imp, 1)
        
        tree[row.dim_id][row.subdim_id].append({'val': val, 'w': peso})
        if row.dim_id not in dim_info:
            dim_info[row.dim_id] = {'nombre': row.dim_nombre, 'peso_pct': float(row.dim_peso_porcentaje)}

    # Nivel 1 y 2
    scores_dimensiones = {}
    for dim_id, subdims in tree.items():
        subdim_vals = []
        for sub_id, inds in subdims.items():
            # Media Ponderada por importancia
            num = sum(i['val'] * i['w'] for i in inds)
            den = sum(i['w'] for i in inds)
            subdim_vals.append(num / den if den > 0 else 0)
        # Media Aritmética de subdimensiones
        scores_dimensiones[dim_id] = sum(subdim_vals) / len(subdim_vals) if subdim_vals else 0

    # Nivel 3 (Global)
    brainnova_score = 0
    desglose = []
    for dim_id, score in scores_dimensiones.items():
        info = dim_info[dim_id]
        contrib = score * (info['peso_pct'] / 100.0)
        brainnova_score += contrib
        desglose.append({
            "dimension": info['nombre'],
            "score_dimension": round(score, 2),
            "peso_configurado": info['peso_pct'],
            "contribucion_al_global": round(contrib, 2)
        })

    return {
        "brainnova_global_score": round(brainnova_score, 2),
        "pais": pais, "periodo": periodo, "sector": sector,
        "desglose_por_dimension": desglose
    }

def obtener_nombres_indicadores_disponibles(db: Session):
    """
    Devuelve una lista única de nombres de indicadores que tienen 
    al menos un resultado calculado o extraído en la base de datos.
    """
    IndicadorDesdeComponente = aliased(DefinicionIndicador)
    IndicadorDesdeCrudo = aliased(DefinicionIndicador)

    # 1. Definimos la columna "Nombre Calculado" (La misma lógica que usamos antes)
    nombre_consolidado = func.coalesce(
        IndicadorDesdeComponente.nombre, 
        IndicadorDesdeCrudo.nombre
    )

    # 2. Hacemos la query buscando DISTINCT (únicos)
    query = db.query(distinct(nombre_consolidado))

    # 3. Joins (Exactamente igual que en obtener_data_consulta)
    # Camino A: Componentes
    query = query.outerjoin(ResultadoIndicador.componente)\
                 .outerjoin(IndicadorDesdeComponente, ComponenteIndicador.indicador)
    
    # Camino B: Crudos
    query = query.outerjoin(ResultadoIndicador.origen_crudo)\
                 .outerjoin(ProcessedDatoCrudo.dato_crudo_origen)\
                 .outerjoin(IndicadorDesdeCrudo, DatoCrudo.indicador)

    # 4. Filtros de limpieza
    # Excluimos los nulos (resultados huérfanos si los hubiera)
    query = query.filter(nombre_consolidado != None)
    
    # 5. Ordenamos alfabéticamente
    query = query.order_by(nombre_consolidado.asc())

    result = query.all()
    
    # result será una lista de tuplas [('PIB',), ('Desempleo',), ...]
    # Lo convertimos a una lista plana ['PIB', 'Desempleo']
    return [row[0] for row in result]