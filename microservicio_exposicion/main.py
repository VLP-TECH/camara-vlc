from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# Importaciones locales
from database.connection import get_db
from microservicio_exposicion.schemas import ResultadoIndicadorResponse, ScoreRequest, ScoreResponse, FiltrosResponse
from microservicio_exposicion.services import obtener_data_consulta, calcular_brainnova_score, obtener_nombres_indicadores_disponibles, obtener_filtros_unicos, obtener_filtros_disponibles

from database.modelos import ResultadoIndicador
import uvicorn

app = FastAPI(title="Brainnova API")

# Configuración CORS
origins = ["http://localhost:3000", "http://localhost:5173", "http://localhost:4173", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session

@app.get("/api/v1/resultados", response_model=List[ResultadoIndicadorResponse])
def leer_resultados(
    page: int = Query(1, ge=1),
    per_page: int = Query(1000, le=5000),
    pais: Optional[str] = None,
    periodo: Optional[int] = None,
    sector: Optional[str] = None,
    tamano_empresa: Optional[str] = None, 
    provincia: Optional[str] = None,  # <--- 1. AÑADE ESTO (Faltaba recibirlo)
    nombre_indicador: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * per_page
    
    datos = obtener_data_consulta(
        db=db,
        skip=skip,
        limit=per_page,
        pais=pais,
        periodo=periodo,
        sector=sector,
        nombre_indicador=nombre_indicador,
        tamano=tamano_empresa,
        provincia=provincia  
    )
    
    return [
        {
            "nombre_indicador": row.nombre_indicador,
            "resultado": float(row.resultado) if row.resultado is not None else 0.0,
            "periodo": row.periodo,
            "pais": row.pais,
            "provincia": row.provincia,
            "sector": row.sector,
            "tamano_empresa": row.tamano_empresa
        }
        for row in datos
    ]

# --- ENDPOINT 2: Cálculo Score ---
@app.post("/api/v1/brainnova-score", response_model=ScoreResponse)
def get_brainnova_score(req: ScoreRequest, db: Session = Depends(get_db)):
    resultado = calcular_brainnova_score(
        db=db,
        pais=req.pais,
        periodo=req.periodo,
        sector=req.sector,
        tamano=req.tamano_empresa,
        provincia=req.provincia
    )
    
    if not resultado:
        raise HTTPException(status_code=404, detail="No hay datos suficientes para calcular el score")
    
    return resultado

@app.get("/api/v1/indicadores-disponibles", response_model=List[str])
def lista_indicadores_activos(db: Session = Depends(get_db)):
    """
    Devuelve la lista de indicadores que tienen datos reales asociados.
    Ideal para rellenar desplegables (Select) en el Frontend.
    """
    nombres = obtener_nombres_indicadores_disponibles(db)
    return nombres

@app.get("/api/v1/filtros-disponibles")
def obtener_filtros(db: Session = Depends(get_db)):
    """
    Devuelve todos los valores posibles para los desplegables de filtrado
    """
    return {
        "paises": [r[0] for r in obtener_filtros_unicos(db, ResultadoIndicador.pais)],
        "periodos": [r[0].year for r in obtener_filtros_unicos(db, ResultadoIndicador.periodo)], # Ojo con .year si es Date
        "sectores": [r[0] for r in obtener_filtros_unicos(db, ResultadoIndicador.sector) if r[0]], # if r[0] filtra nulos
        "tamano_empresa": [r[0] for r in obtener_filtros_unicos(db, ResultadoIndicador.tamano_empresa) if r[0]]
    }

@app.get("/api/v1/filtros-globales", response_model=FiltrosResponse)
def get_filtros_globales(
    pais: Optional[str] = None,
    periodo: Optional[int] = None,
    sector: Optional[str] = None,
    tamano: Optional[str] = None,
    nombre_indicador: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Devuelve opciones de filtrado.
    Si envías parámetros (ej: ?pais=España), las listas devueltas (provincias, sectores...)
    se filtrarán para mostrar solo lo disponible en ese contexto.
    """
    return obtener_filtros_disponibles(db, pais, periodo, sector, tamano, nombre_indicador=nombre_indicador)

def main():
    print("🚀 Levantando API para la demo...")
    # Usamos el puerto 8000 y escuchamos en todas las interfaces (0.0.0.0)
    uvicorn.run(app, host="0.0.0.0", port=8000)