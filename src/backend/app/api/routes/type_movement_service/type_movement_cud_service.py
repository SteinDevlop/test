import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.type_movement import TypeMovementCreate,TypeMovementOut
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/typemovement", tags=["typemovement"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    current_user: dict = Security(
        get_current_user,
        scopes=["system", "administrador"]
    )
):
    logger.info(f"[GET /crear] Usuario: {current_user['user_id']} - Mostrando formulario de creación de tipo de movimiento")
    return templates.TemplateResponse("CrearTipoMovimiento.html", {"request": request})

@app.get("/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[GET /actualizar] Usuario: {current_user['user_id']} - Mostrando formulario de actualización de tipo de movimiento")
    return templates.TemplateResponse("ActualizarTipoMovimiento.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[GET /eliminar] Usuario: {current_user['user_id']} - Mostrando formulario de eliminación de tipo de movimiento")
    return templates.TemplateResponse("EliminarTipoMovimiento.html", {"request": request})

#
@app.post("/create")
async def create_typemovement(
    id: int = Form(...),
    type: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /create] Usuario: {current_user['user_id']} - Intentando crear tipo de movimiento {type}")

    try:
        # Verificar si el rol de usuario ya existe
        existing_user = controller.get_by_column(TypeMovementOut, "type", type)  
        if existing_user:
            logger.warning(f"[POST /create] Error de validación: El tipo de movimiento ya existe con id {id}")
            raise HTTPException(400, detail="El tipo de movimiento ya existe con la misma identificación.")

        # Crear tipo de movimiento
        new_typemovement = TypeMovementCreate(id=id, type=type)
        logger.info(f"Intentando insertar rol de usuario con datos: {new_typemovement.model_dump()}")
        controller.add(new_typemovement)
        logger.info(f"Rol de Usuario insertado con ID: {new_typemovement.id}")  # Verifica si el ID se asigna
        logger.info(f"[POST /create] Rol de Usuario creado exitosamente con identificación {id}")
        return {
            "operation": "create",
            "success": True,
            "data": TypeMovementOut(id=new_typemovement.id, type=new_typemovement.type).model_dump(),
            "message": "TypeMovement created successfully."
        }
        
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_typemovement(
    id: int = Form(...),
    type: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /update] Usuario: {current_user['user_id']} - Actualizando tipo de movimiento id={id}")
    try:
        existing = controller.get_by_id(TypeMovementOut, id)
        if existing is None:
            logger.warning(f"[POST /update] Rol de Usuario no encontrada: id={id}")
            raise HTTPException(404, detail="TypeMovement not found")

        updated_typemovement = TypeMovementOut(id=id, type=type)
        controller.update(updated_typemovement)
        logger.info(f"[POST /update] TipoMovimiento actualizada exitosamente: {updated_typemovement}")
        return {
            "operation": "update",
            "success": True,
            "data": TypeMovementOut(id=id, type=updated_typemovement.type).model_dump(),
            "message": f"TypeMovement {id} updated successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_roluser(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /delete] Usuario: {current_user['user_id']} - Eliminando tipo de movimiento con id={id}")
    try:
        existing = controller.get_by_id(TypeMovementOut, id)
        if not existing:
            logger.warning(f"[POST /delete] Tipo de Movimiento no encontrado en la base de datos: id={id}")
            raise HTTPException(404, detail="TypeMovement not found")

        logger.info(f"[POST /delete] Eliminando tipo de movimiento con id={id}")
        controller.delete(existing) 
        logger.info(f"[POST /delete] Tipo de Movimiento eliminada exitosamente: id={id}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"TypeMovement {id} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
