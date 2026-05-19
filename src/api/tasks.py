import logging
from fastapi import APIRouter, Depends
from src.api.Dependencies import get_role
from src.models.user import Role
from src.task.tasks import send_reminder

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/reminder", dependencies=[Depends(get_role(Role.ADMIN))])
def reminder():
    try:
        send_reminder.delay()
    except Exception as e:
        logging.info(e)
    return {"message": "reminder sent"}

