                 Fitness Studio Application (FastAPI + PostgreSQL)

A backend API for a fictional Fitness Studio that allows users to sign up, log in, view fitness classes, book classes, and manage bookings.
Built using FastAPI, PostgreSQL, JWT authentication, and bcrypt-based password hashing.

* Project Overview
    
    - Features
        User Signup & Login (JWT-based authentication)
        Secure password hashing with bcrypt
        Create fitness classes (authenticated users)
        View all upcoming classes
        Book a class (with slot validation & race-condition safety)
        View user bookings
        PostgreSQL transactions to prevent overbooking
    
    - Tech Stack
        Backend: FastAPI
        Database: PostgreSQL
        Auth: JWT (python-jose)
        Password Hashing: bcrypt
        DB Driver: psycopg2
        Server: Uvicorn

    - Project Structure
        Fitness_Studio_Application/
        │
        ├── app/
        │   ├── main.py
        │   ├── database.py
        │   ├── security.py
        │   └── routes/
        │       ├── signup.py
        │       ├── login.py
        │       ├── classes.py
        │       └── booking.py
        │
        ├── requirements.txt
        └── README.md

* Setup Instructions

    - Prerequisites
        Make sure you have installed:
        Python 3.11+
        PostgreSQL 14+
        pip & virtualenv