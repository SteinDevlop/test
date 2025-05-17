from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.payments import Payment
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/payments", tags=["payments"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_pagos(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "finanzas", "operador"])
):
    """
    Lista todos los pagos.
    """
    try:
        pagos = controller.read_all(Payment)
        return templates.TemplateResponse("ListarPago.html", {"request": request, "pagos": pagos})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{IDMovimiento}", response_class=HTMLResponse)
def detalle_pago(
    IDMovimiento: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "finanzas", "operador"])
):
    """
    Obtiene el detalle de un pago por su IDMovimiento.
    """
    try:
        pago = controller.get_by_id(Payment, IDMovimiento)
        if not pago:
            raise HTTPException(status_code=404, detail="Pago no encontrado")
        return templates.TemplateResponse("DetallePago.html", {"request": request, "pago": pago.to_dict()})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))