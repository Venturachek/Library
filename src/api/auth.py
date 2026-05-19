from fastapi import  HTTPException, APIRouter, Response, Body
from pygments.lexers import data
from src.api.Dependencies import DBDep
from src.exceptions import  ObjectAlreadyExistsException
from src.schemas.user import UserAddRequest
from src.services.auth import Auth
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(db: DBDep, data: UserAddRequest):
    try:
        await Auth(db).add_user(data)
    except ObjectAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail="User already exists!")
    return {"status": "ok"}


@router.post("/login")
async def login(db: DBDep, response: Response, data: UserAddRequest = Body()):
   access_token = await Auth(db).login_user(data)
   response.set_cookie("access_token", access_token, httponly=True)
   return {"access_token": access_token}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}

