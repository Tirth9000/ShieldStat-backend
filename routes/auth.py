from fastapi import APIRouter, Depends, HTTPException,status
from database.database import get_user_collection
from services.auth import hash_password, verify_password, create_access_token
from models.User import User
from database.schemas import SignupRequest, SigninRequest
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Auth"]
)

@router.post("/signup")
async def signup(payload: SignupRequest, users=Depends(get_user_collection)):
    data = payload.dict()
    data["password"] = hash_password(payload.password)
    user = User(**data)
    await users.insert_one(user.to_dict())
    return {"message": "Registration completed successfully"}

@router.post("/authorize")
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    users=Depends(get_user_collection)
):
    user = await users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token({"sub": str(user["_id"])})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/signin")
async def login_json(
    payload: SigninRequest,
    users=Depends(get_user_collection)
):
    user = await users.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["_id"])})
    return {
        "access_token": token,
        "token_type": "bearer"
    }