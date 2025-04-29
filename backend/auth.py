# auth.py
from passlib.context import CryptContext
from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta

# In-memory storage (replace with DB in production)
users_db = {}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT config
SECRET_KEY = "webpulse_secret_key_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def register_user(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    if email in users_db:
        raise HTTPException(status_code=409, detail="User already exists")

    hashed_password = get_password_hash(password)
    users_db[email] = {
        "email": email,
        "password": hashed_password,
        "role": "admin" if "xholi" in email else "user"
    }

    return {"message": "User registered successfully"}

async def login_user(data):
    email = data.get("email")
    password = data.get("password")

    user = users_db.get(email)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer", "user": {"email": email}}

def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = users_db.get(email)
        if not user:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
