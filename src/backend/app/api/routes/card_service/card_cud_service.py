import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.card import CardCreate, CardOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/card", tags=["card"])
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.post("/create")
async def create_card(
    ID: int = Form(...),
    IDUsuario: int = Form(...),
    IDTipoTarjeta: int = Form(...)
):
    try:
        new_card = CardCreate(ID=ID, IDUsuario=IDUsuario,IDTipoTarjeta=IDTipoTarjeta, Saldo=0)
        controller.add(new_card)

        logger.info(f"[POST /create] Tarjeta creada exitosamente: {new_card}")
        return {
            "operation": "create",
            "success": True,
            "data": CardOut(ID=new_card.ID, IDUsuario=new_card.IDUsuario,IDTipoTarjeta=new_card.IDTipoTarjeta, Saldo=new_card.Saldo).model_dump(),
            "message": "Card created successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_card(
    ID: int = Form(...),
    IDUsuario: int = Form(...),
    IDTipoTarjeta: int = Form(...),
    
):
    try:
        existing = controller.get_by_id(CardOut, ID)
        if existing is None:
            logger.warning(f"[POST /update] Tarjeta no encontrada: ID={ID}")
            raise HTTPException(404, detail="Card not found")

        updated_card = CardCreate(ID=ID,IDUsuario=IDUsuario,IDTipoTarjeta=IDTipoTarjeta, Saldo=existing.Saldo)
        controller.update(updated_card)

        logger.info(f"[POST /update] Tarjeta actualizada exitosamente: {updated_card}")
        return {
            "operation": "update",
            "success": True,
            "data": CardOut(ID=updated_card.ID, IDUsuario=updated_card.IDUsuario,IDTipoTarjeta=updated_card.IDTipoTarjeta, Saldo=updated_card.Saldo).model_dump(),
            "message": f"Card {ID} updated successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_card(
    ID: int = Form(...),
    
):
    try:
        existing = controller.get_by_id(CardOut, ID)
        if not existing:
            logger.warning(f"[POST /delete] Tarjeta no encontrada: ID={ID}")
            raise HTTPException(404, detail="Card not found")

        controller.delete(existing)
        logger.info(f"[POST /delete] Tarjeta eliminada exitosamente: ID={ID}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"Card {ID} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=str(e))
