import logging
import json
from fastapi import Request, Query, APIRouter, Security, Path
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.user import UserOut
from backend.app.logic.universal_controller_sqlserver import UniversalController

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for user-related endpoints
app = APIRouter(prefix="/user", tags=["user"])

# Initialize universal controller instance
controller = UniversalController()

# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request
):
    """
    Render the 'ConsultarUsuario.html' template for the user consultation page.
    """
    return templates.TemplateResponse("ConsultarUsuario.html", {"request": request})


@app.get("/users")
async def get_users(
):
    """
    Retrieve and return all user records from the database.
    """
    usuarios = controller.read_all(UserOut)
    return usuarios


@app.get("/usuario", response_class=HTMLResponse)
def usuario(
    request: Request,
    id: int= Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "pasajero"])
):
    """
    Retrieve a user by its ID and render the 'usuario.html' template with its details.
    If the user is not found, display 'None' for all fields.
    """
    logger.info(f"[GET /user] Usuario: {current_user['user_id']} - Consultando usuario con id={id}")
    unit_usuario= controller.get_by_id(UserOut, id)

    if unit_usuario:
        logger.info(f"[GET /user] Usuario encontrados: {unit_usuario.ID}")

    else:
        logger.warning(f"[GET /user] No se encontró usuario con id={id}")
    
    context = {
        "request": request,
        "ID": unit_usuario.ID if unit_usuario else "None",
        "Identificacion": unit_usuario.Identificacion if unit_usuario else "None",
        "Nombre": unit_usuario.Nombre if unit_usuario else "None",
        "Apellido": unit_usuario.Apellido if unit_usuario else "None",
        "Correo": unit_usuario.Correo if unit_usuario else "None",
        "Contrasena": unit_usuario.Contrasena if unit_usuario else "None",
        "IDRolUsuario": unit_usuario.IDRolUsuario if unit_usuario else "None",
        "IDTurno": unit_usuario.IDTurno if unit_usuario else "None",
        "IDTarjeta": unit_usuario.IDTarjeta if unit_usuario else "None",
    }

    return templates.TemplateResponse(request,"usuario.html", context)
