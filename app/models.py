from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class EspecificacionesIn(BaseModel):
    dias_cosecha_promedio: Optional[int] = Field(None, example=90, description="Días promedio para cosechar")
    kg_n_ha: Optional[float] = Field(None, example=120.0, description="Kilogramos de Nitrógeno por hectárea")
    kg_p_ha: Optional[float] = Field(None, example=40.0, description="Kilogramos de Fósforo por hectárea")
    kg_k_ha: Optional[float] = Field(None, example=80.0, description="Kilogramos de Potasio por hectárea")
    densidad_recomendada_ha: Optional[int] = Field(None, example=30000)
    msnm_optimo_min: Optional[int] = Field(None, example=0)
    msnm_optimo_max: Optional[int] = Field(None, example=1000)
    tolerancia_salinidad_ce: Optional[float] = Field(None, example=2.0)
    rendimiento_estimado_ton_ha: Optional[float] = Field(None, example=25.5)

class RegistroPlantaCompleto(BaseModel):
    nombre_comun: str = Field(..., example="Arándano Biloxi", description="Nombre común de la planta")
    nombre_cientifico: Optional[str] = Field(None, example="Vaccinium corymbosum")
    latitud: Optional[float] = Field(None, example=-13.16)
    longitud: Optional[float] = Field(None, example=-74.22)
    necesidad_agua: Optional[str] = Field(None, example="Frecuente")
    temperatura_min: Optional[float] = Field(None, example=10.0)
    temperatura_max: Optional[float] = Field(None, example=25.0)
    tipo_tierra: Optional[str] = Field(None, example="Orgánico/Ácido")
    ph_suelo: Optional[float] = Field(None, example=5.5)
    especificaciones: Optional[EspecificacionesIn] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre_comun": "Arándano Biloxi",
                "nombre_cientifico": "Vaccinium corymbosum",
                "latitud": -13.16,
                "longitud": -74.22,
                "necesidad_agua": "Frecuente",
                "temperatura_min": 10.0,
                "temperatura_max": 25.0,
                "tipo_tierra": "Orgánico/Ácido",
                "ph_suelo": 5.5,
                "especificaciones": {
                    "dias_cosecha_promedio": 90,
                    "kg_n_ha": 120.0,
                    "kg_p_ha": 40.0,
                    "kg_k_ha": 80.0,
                    "densidad_recomendada_ha": 30000,
                    "msnm_optimo_min": 0,
                    "msnm_optimo_max": 1000,
                    "tolerancia_salinidad_ce": 2.0,
                    "rendimiento_estimado_ton_ha": 25.5
                }
            }
        }
    )
