from fastapi import APIRouter
from ..database import supabase

router = APIRouter(tags=["Público"])

@router.get("/inventario", summary="🌍 Listado Abierto")
async def inventario():
    res = supabase.table("plantas").select("*, especificaciones_agricolas(*)").execute()
    return res.data
