from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import uuid
from app.api.auth.scheams import RegisterRequest, LoginRequest
from app.db.base import getCursor
from app.api.auth.helper_functions import hashPassword, verifyPassword, generateToken
from app.core.middleware import protect

router = APIRouter()


# new user registration
@router.post('/register')
async def register(req: RegisterRequest):
    username = req.username
    email = req.email
    password = req.password

    if not username or not email or not password:
        raise HTTPException(status_code=400, detail="Please fill all the fields")

    try: 
        cursor = getCursor()

        # check if the user exists
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )
        if cursor.fetchone():
            cursor.close()
            raise HTTPException(status_code=400, detail="User already exists")
            
        hashedPassword = hashPassword(password)
        user_id = str(uuid.uuid4())

        # insert user in db
        cursor.execute(
            """
            INSERT INTO users(id, username, email, password)
            VALUES(%s, %s, %s, %s)
            RETURNING id, username, email
            """,
            (user_id, username, email.lower(), hashedPassword)
        )

        result = cursor.fetchone()
        cursor.close()

        if result:
            user_id, user_username, user_email = result
            return JSONResponse(
                status_code=201,
                content={
                    "id": str(user_id),
                    "username": user_username,
                    "email": user_email,
                    "token": generateToken(str(user_id)) 
                }
            )
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Invalid User data"
                }
            )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server Error")


# user login
@router.post('/login')
async def login(req: LoginRequest):
    
    email = req.email
    password = req.password

    if not email or not password:
        raise HTTPException(status_code=400, detail="Please fill all the fields")
    
    try:
        cursor = getCursor()
        cursor.execute(
            """
            SELECT id, username, email, password FROM users WHERE email = %s
            """,
            (email.lower(),)
        )

        userFound = cursor.fetchone()
        cursor.close()

        if userFound:
            hashedPassword = userFound[3]

        if userFound and verifyPassword(password, hashedPassword):
            user_id, user_username, user_email, _ = userFound
            return JSONResponse(
                status_code=200,
                content={
                    'id': user_id,
                    'username': user_username,
                    'email': user_email,
                    'token': generateToken(str(user_id))
                }
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server Error")


# get current user (protected route)
@router.get('/me')
async def getUser(user: dict = Depends(protect)):
    return JSONResponse(status_code=200, content=user)


# user profile data
@router.get('/profile/{id}')
async def getProfile(id: str):
    try:
        cursor = getCursor()
        
        cursor.execute(
            """
            SELECT id, username, email FROM users WHERE id = %s
            """,
            (id,)
        )

        user = cursor.fetchone()
        cursor.close()

        if user:
            user_id, user_username, user_email = user
            return JSONResponse(
                status_code=200,
                content={
                    "_id": str(user_id),
                    "username": user_username,
                    "email": user_email
                }
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server Error")
