from fastapi import Depends, HTTPException, APIRouter, Response, Body
from pygments.lexers import data

from src.api.Dependencies import DBDep, UserIDDep
from src.exceptions import UserAlreadyExistsException, ObjectAlreadyExistsException
from src.models.user import Role
from src.schemas.user import UserAddRequest, UserAdd
from src.services.auth import Auth
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(db: DBDep, data: UserAddRequest):
    hashed_password = Auth().get_password_hash(data.password)
    new_user = UserAdd(email=data.email, hashed_password=hashed_password, role=Role.USER)
    try:
        await db.user.add(new_user)
        await db.commit()
    except ObjectAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail="User already exists!")
    return {"status": "ok"}


@router.post("/login")
async def login(db: DBDep, response: Response, data: UserAddRequest = Body()):
    user = await db.user.get_user_by_email(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not Auth().verify_password(plain_password=data.password, hashed_password=user.hashed_password):
       raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = Auth().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}

@router.get("/user")
async def get_user(db: DBDep, current_user: UserIDDep):
    return await db.user.get_filter_by(id=current_user)