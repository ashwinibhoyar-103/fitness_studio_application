from fastapi import APIRouter, Depends, HTTPException, Request
from app.database import get_db
from app.security import get_current_user

# Router for booking-related endpoints
router = APIRouter()


@router.post("/book")
async def book_class(
    request: Request,
    user=Depends(get_current_user),  # Inject authenticated user from JWT
    db=Depends(get_db)               # Inject database connection
):
    # Parse JSON request body
    data = await request.json()
    class_id = data["class_id"]

    # Create database cursor
    cur = db.cursor()

    try:
        # Lock the selected class row to prevent concurrent overbooking
        cur.execute(
            "SELECT available_slots FROM classes WHERE id=%s FOR UPDATE",
            (class_id,)
        )
        slots = cur.fetchone()

        # If class does not exist or no slots left, block booking
        if not slots or slots[0] <= 0:
            raise HTTPException(status_code=400, detail="No slots available")
        
        # Extract logged-in client details from JWT
        client_id = user["user_id"]
        client_email = user["email"]
        
        # Insert booking record
        cur.execute(
            "INSERT INTO bookings (class_id, client_id, client_email) VALUES (%s, %s, %s)",
            (class_id, client_id, client_email)
        )

        # Decrease available slots for the class
        cur.execute(
            "UPDATE classes SET available_slots = available_slots - 1 WHERE id=%s",
            (class_id,)
        )

        # Commit transaction if everything succeeds
        db.commit()

    except:
        # Roll back all DB changes if any error occurs
        db.rollback()
        raise

    finally:
        # Always close cursor to release DB resources
        cur.close()

    # Return success response
    return {"message": "Booking successful"}


@router.get("/bookings")
def my_bookings(
    user=Depends(get_current_user),  # Inject authenticated user
    db=Depends(get_db)               # Inject database connection
):
    # Create cursor for database query
    cur = db.cursor()

    # Fetch bookings for the logged-in user
    cur.execute(
        """
        SELECT c.name, c.date_time
        FROM bookings b
        JOIN classes c ON b.class_id = c.id
        WHERE b.user_id = %s
        """,
        (user["user_id"],)
    )

    # Retrieve all matching booking records
    rows = cur.fetchall()

    # Close cursor after data retrieval
    cur.close()

    # Format DB rows into API-friendly response
    return [
        {"class": r[0], "dateTime": r[1]}
        for r in rows
    ]