from fastapi import APIRouter, Depends, HTTPException, Request
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.database import get_db
from app.security import ALGORITHM, SECRET_KEY, verify_password

# Create router instance for authentication routes
router = APIRouter()

# Password hashing context (bcrypt algorithm)
pwd_context = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def login(request: Request, db=Depends(get_db)):
    # Parse JSON body from incoming request
    data = await request.json()

    # Extract login credentials
    email = data.get("email")
    password = data.get("password")

    # Create a database cursor to execute SQL queries
    cur = db.cursor()

    # Fetch user credentials using email
    cur.execute(
        "SELECT id, password_hash, role FROM users_data WHERE email=%s",
        (email,)
    )

    # Fetch one matching user record
    user = cur.fetchone()

    # Close cursor after query execution
    cur.close()

    # If no user found, credentials are invalid
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Unpack user details from query result
    user_id, hashed, role = user

    # Verify provided password against stored hashed password
    if not verify_password(password, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT access token with user details and expiry time
    token = jwt.encode(
        {
            "user_id": user_id,        # User identifier
            "email": email,            # User email
            "role": role,              # User role for authorization
            "exp": datetime.utcnow() + timedelta(hours=24)  # Token expiration
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # Return JWT token to client
    return {"access_token": token}