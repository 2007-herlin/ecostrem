from fastapi import APIRouter, HTTPException, Depends
from ..database import supabase
from ..models import RegistroPlantaCompleto
from ..auth import get_api_key

router = APIRouter(tags=["Privado"])

@router.post("/registrar-total", summary="🔐 Registro Solo Admin")
async def registrar_total(
    datos: RegistroPlantaCompleto, 
    api_key: str = Depends(get_api_key)
):
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
