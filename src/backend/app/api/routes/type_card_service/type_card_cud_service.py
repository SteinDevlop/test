import logging
from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.type_card import TypeCardOut, TypeCardCreate
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user
from fastapi import Security

# Initialize the controller for Tipo card

# Create a router for Tipo card-related endpoints
app = APIRouter(prefix="/typecard", tags=["Type Card"])

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Route to create a new Tipo of card

# Route to create a new Tipo of card via POST
@app.post("/create")
async def create_typecard(
    ID: int = Form(...),
    Tipo: str = Form(...)
    
):
    """
    Creates a new Tipo of card with the provided ID and Tipo.
    """
    try:
        new_typecard = TypeCardCreate(ID=ID, Tipo=Tipo)

        # Add the new Tipo of card using the controller
        controller.add(new_typecard)
        return {
            "operation": "create",
            "success": True,
            "data": TypeCardOut(ID=new_typecard.ID, Tipo=new_typecard.Tipo).model_dump(),
            "message": "Card Tipo created successfully"
        }
    except ValueError as e:
        logger.error(f"[POST /create] Error creating card Tipo: {str(e)}")
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails
    except Exception as e:
        logger.error(f"[POST /create] Internal server error: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")  # General server error


# Route to update an existing Tipo of card via POST
@app.post("/update")
async def update_typecard(
    ID: int = Form(...),
    Tipo: str = Form(...),
    
):
    """
    Updates an existing Tipo of card by its ID and new Tipo.
    If the Tipo of card does not exist, a 404 error is raised.
    """
    try:
        # Check if the Tipo of card exists
        existing = controller.get_by_id(TypeCardOut, ID)
        if not existing:
            logger.warning(f"[POST /update] Card Tipo with ID {ID} not found.")
            raise HTTPException(404, detail="Card Tipo not found")

        # Create a new instance with the updated data
        updated_typecard = TypeCardCreate(ID=ID, Tipo=Tipo)

        # Update the Tipo of card using the controller
        controller.update(updated_typecard)
        return {
            "operation": "update",
            "success": True,
            "data": TypeCardOut(ID=updated_typecard.ID, Tipo=updated_typecard.Tipo).model_dump(),
            "message": f"Card Tipo {ID} updated successfully"
        }
    except ValueError as e:
        logger.error(f"[POST /update] Error updating card Tipo: {str(e)}")
        raise HTTPException(400, detail=str(e))


# Route to delete an existing Tipo of card via POST
@app.post("/delete")
async def delete_typecard(
    ID: int = Form(...),
    
):
    """
    Deletes an existing Tipo of card by its ID.
    If the Tipo of card does not exist, a 404 error is raised.
    """
    try:
        # Check if the Tipo of card exists
        existing = controller.get_by_id(TypeCardOut, ID)
        if not existing:
            logger.warning(f"[POST /delete] Card Tipo with ID {ID} not found.")
            raise HTTPException(404, detail="Card Tipo not found")

        # Delete the Tipo of card using the controller
        controller.delete(existing)
        return {
            "operation": "delete",
            "success": True,
            "message": f"Card Tipo {ID} deleted successfully"
        }
    except HTTPException:
        raise  # Re-raise HTTPException as it is
    except Exception as e:
        logger.error(f"[POST /delete] Internal server error: {str(e)}")
        raise HTTPException(500, detail=str(e))
