from fastapi import APIRouter, HTTPException
from ..database import supabase

router = APIRouter(tags=["Público"])

@router.get("/inventario")
async def inventario():
    res = supabase.table("plantas").select("*, especificaciones_agricolas(*)").execute()
    return res.data

# --- ESTO ES LO QUE DEBES AGREGAR ---
@router.get("/planta/{nombre}")
async def obtener_planta(nombre: str):
    # El select con (*) en ambos lados es lo que trae "TODO"
    res = supabase.table("plantas")\
        .select("*, especificaciones_agricolas(*)")\
        .ilike("nombre", f"{nombre}")\
        .execute()
    
    if not res.data:
        raise HTTPException(status_code=404, detail="Planta no encontrada")
    
    return res.data[0] # Retorna el objeto completo con sus relaciones
