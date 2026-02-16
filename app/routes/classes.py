from fastapi import APIRouter, Depends, HTTPException, Request
from app.database import get_db
from app.security import get_current_user

# Router for class management endpoints
router = APIRouter()


@router.post("/classes")
async def create_class(
    request: Request,
    user=Depends(get_current_user),  # Inject authenticated user from JWT
    db=Depends(get_db)               # Inject database connection
):
    # Allow only admin users to create classes
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    # Parse JSON payload from request body
    data = await request.json()

    # Create database cursor for executing SQL commands
    cur = db.cursor()

    # Insert new class record into the classes table
    cur.execute(
        """
        INSERT INTO classes
        (name, date_time, instructor, available_slots)
        VALUES (%s, %s, %s, %s)
        """,
        (
            data["name"],             # Class name
            data["dateTime"],         # Class date & time
            data["instructor"],       # Instructor name
            data["availableSlots"],   # Number of available slots
        )
    )

    # Commit transaction to persist changes
    db.commit()

    # Close cursor to free resources
    cur.close()

    # Return success response
    return {"message": "Class created"}


@router.get("/classes")
def get_classes(db=Depends(get_db)):
    # Create cursor to fetch class data
    cur = db.cursor()

    # Retrieve all class records
    cur.execute(
        "SELECT id, name, date_time, instructor, available_slots FROM classes"
    )

    # Fetch all rows from query result
    rows = cur.fetchall()

    # Close cursor after fetching data
    cur.close()

    # Convert DB rows into JSON-friendly format
    return [
        {
            "id": r[0],
            "name": r[1],
            "dateTime": r[2],
            "instructor": r[3],
            "availableSlots": r[4]
        }
        for r in rows
    ]