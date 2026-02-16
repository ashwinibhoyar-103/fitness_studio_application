from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import booking, classes, login, signup

app = FastAPI()

# Auth routes
app.include_router(signup.router, prefix="/auth", tags=["Auth"])
app.include_router(login.router, prefix="/auth", tags=["Auth"])

# Class routes
app.include_router(classes.router, tags=["Classes"])

# Booking routes
app.include_router(booking.router, tags=["Bookings"])

