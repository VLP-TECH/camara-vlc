from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class FiltrosResponse(BaseModel):
    paises: List[str]
    provincias: List[str]  # <--- NUEVO
    sectores: List[str]
    tamanos_empresa: List[str]
    anios: List[int]

# --- SALIDA: Listado de Resultados (Endpoint GET) ---
class ResultadoIndicadorResponse(BaseModel):
    nombre_indicador: str
    resultado: float
    periodo: Optional[date] = None 
    pais: Optional[str] = None
    provincia: Optional[str] = None
    sector: Optional[str] = None
    tamano_empresa: Optional[str] = None

    class Config:
        from_attributes = True

# --- ENTRADA: Petición de Score (Endpoint POST) ---
class ScoreRequest(BaseModel):
    pais: str
    periodo: int  # El usuario envía 2023, 2024...
    sector: str
    tamano_empresa: str
    provincia: Optional[str] = None

# --- SALIDA: Respuesta del Score (Endpoint POST) ---
class DimensionOutput(BaseModel):
    dimension: str
    score_dimension: float
    peso_configurado: float
    contribucion_al_global: float

class ScoreResponse(BaseModel):
    brainnova_global_score: float
    pais: str
    periodo: int
    sector: str
    desglose_por_dimension: List[DimensionOutput]