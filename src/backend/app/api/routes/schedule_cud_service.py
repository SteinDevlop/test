from fastapi import APIRouter, Form, HTTPException, Security, Request
from backend.app.models.schedule import Schedule
from backend.app.logic.universal_controller_sqlserver import UniversalController
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/schedules", tags=["schedules"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_horario_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Renderiza el formulario para crear un horario.
    """
    return templates.TemplateResponse("CrearHorario.html", {"request": request})

@app.post("/create")
def crear_horario(
    ID: int = Form(...),  # Asegúrate de que el nombre sea 'ID'
    Llegada: str = Form(...),  # Asegúrate de que el formato sea 'HH:MM:SS'
    Salida: str = Form(...),  # Asegúrate de que el formato sea 'HH:MM:SS'
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Endpoint para crear un horario.
    """
    schedule = Schedule(ID=ID, Llegada=Llegada, Salida=Salida)
    try:
        controller.add(schedule)
        return {"message": "Horario creado exitosamente.", "data": schedule.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_horario_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Renderiza el formulario para actualizar un horario.
    """
    return templates.TemplateResponse("ActualizarHorario.html", {"request": request})

@app.post("/update")
def actualizar_horario(
    id: int = Form(...),
    Llegada: str = Form(...),
    Salida: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Endpoint para actualizar un horario existente.
    """
    existing_schedule = controller.get_by_id(Schedule, id)
    if not existing_schedule:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    updated_schedule = Schedule(ID=id, Llegada=Llegada, Salida=Salida)
    try:
        controller.update(updated_schedule)
        return {"message": "Horario actualizado exitosamente.", "data": updated_schedule.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_horario_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Renderiza el formulario para eliminar un horario.
    """
    return templates.TemplateResponse("EliminarHorario.html", {"request": request})

@app.post("/delete")
def eliminar_horario(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Endpoint para eliminar un horario por su ID.
    """
    existing_schedule = controller.get_by_id(Schedule, id)
    if not existing_schedule:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    try:
        controller.delete(existing_schedule)
        return {"message": "Horario eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
