from fastapi import APIRouter, Request, HTTPException, Depends
from app.database import get_db
from app.security import hash_password

# Create a router instance for authentication-related endpoints
router = APIRouter()


@router.post("/signup")
async def signup(request: Request, db=Depends(get_db)):
    # Parse JSON body from the incoming request
    data = await request.json()

    # Extract required fields from request body
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    # Validate required fields
    if not name or not email or not password:
        # Raise 400 Bad Request if any mandatory field is missing
        raise HTTPException(status_code=400, detail="All fields required")
    
    # Hash the plaintext password before storing it in the database
    hashed = hash_password(password)

    # Create a database cursor to execute SQL queries
    cur = db.cursor()
    try:
        # Insert new user data into the users_data table
        cur.execute(
            """
            INSERT INTO users_data (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, hashed, role)
        )

        # Commit the transaction if insertion is successful
        db.commit()

    except Exception:
        # Roll back the transaction if any error occurs (e.g., duplicate email)
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

    finally:
        # Close the cursor to free database resources
        cur.close()

    # Return success response
    return {"message": "User created"}