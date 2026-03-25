import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from supabase import create_client, Client
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURACIÓN ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
MASTER_KEY = os.getenv("MASTER_KEY", "Agro2024") # Clave secreta para registrar

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="🌱 ECO_STREAM BIOTECH",
    description="### Sistema de Inteligencia Agrícola\nGestión avanzada de cultivos y suelos.",
    version="2.5.1",
    docs_url=None, 
    redoc_url=None
)

# --- MODELOS ---
class EspecificacionesIn(BaseModel):
    dias_cosecha_promedio: Optional[int] = Field(None, example=90)
    kg_n_ha: Optional[float] = Field(None, example=120.0)
    kg_p_ha: Optional[float] = Field(None, example=40.0)
    kg_k_ha: Optional[float] = Field(None, example=80.0)
    densidad_recomendada_ha: Optional[int] = Field(None, example=30000)
    msnm_optimo_min: Optional[int] = Field(None, example=0)
    msnm_optimo_max: Optional[int] = Field(None, example=1000)
    tolerancia_salinidad_ce: Optional[float] = Field(None, example=2.0)
    rendimiento_estimado_ton_ha: Optional[float] = Field(None, example=25.5)

class RegistroPlantaCompleto(BaseModel):
    nombre_comun: str = Field(..., example="Arándano Biloxi")
    nombre_cientifico: Optional[str] = Field(None, example="Vaccinium corymbosum")
    latitud: Optional[float] = Field(None, example=-13.16)
    longitud: Optional[float] = Field(None, example=-74.22)
    necesidad_agua: Optional[str] = Field(None, example="Frecuente")
    temperatura_min: Optional[float] = Field(None, example=10.0)
    temperatura_max: Optional[float] = Field(None, example=25.0)
    tipo_tierra: Optional[str] = Field(None, example="Orgánico/Ácido")
    ph_suelo: Optional[float] = Field(None, example=5.5)
    especificaciones: Optional[EspecificacionesIn] = None

# --- INTERFAZ (COLOR BLANCO) ---
@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return HTMLResponse("""
    <!doctype html>
    <html>
      <head>
        <title>ECO_STREAM | Docs</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style> body { margin: 0; } </style>
      </head>
      <body>
        <script 
          id="api-reference" 
          data-url="/openapi.json"
          data-configuration='{
            "theme": "eco",
            "forceDarkModeState": "light", 
            "showSidebar": true,
            "customCss": ":root { --scalar-color-accent: #2ecc71; }"
          }'>
        </script>
        <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
      </body>
    </html>
    """)

# --- ENDPOINTS ---

@app.post("/registrar-total", tags=["Privado"], summary="🔐 Registro Solo Admin")
async def registrar_total(
    datos: RegistroPlantaCompleto, 
    x_api_key: str = Header(None, description="Clave maestra para autorizar el registro")
):
    if x_api_key != MASTER_KEY:
        raise HTTPException(status_code=403, detail="No autorizado.")

    try:
        planta_dict = datos.model_dump(exclude={'especificaciones'})
        res_planta = supabase.table("plantas").insert(planta_dict).execute()
        
        id_n = res_planta.data[0]['id']

        res_espec = "Sin datos técnicos"
        if datos.especificaciones:
            espec_dict = datos.especificaciones.model_dump()
            espec_dict['planta_id'] = id_n
            res_op = supabase.table("especificaciones_agricolas").insert(espec_dict).execute()
            res_espec = res_op.data[0]

        tipo = "Neutro"
        if datos.ph_suelo and datos.ph_suelo < 6.5: tipo = "Ácido"
        elif datos.ph_suelo and datos.ph_suelo > 7.5: tipo = "Alcalino"

        return {"mensaje": f"¡Éxito! Suelo {tipo}", "id": id_n, "datos": res_espec}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/inventario", tags=["Público"], summary="🌍 Listado Abierto")
async def inventario():
    res = supabase.table("plantas").select("*, especificaciones_agricolas(*)").execute()
    return res.data