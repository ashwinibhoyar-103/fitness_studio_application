# Fitness Studio Application (FastAPI + PostgreSQL)

A backend API for a fictional **Fitness Studio** that allows users to sign up, log in, view fitness classes, book classes, and manage bookings.

Built using **FastAPI**, **PostgreSQL**, **JWT authentication**, and **bcrypt-based password hashing**.

---

## 📌 Project Overview

### 🚀 Features
- User Signup & Login (JWT-based authentication)
- Secure password hashing with bcrypt
- Create fitness classes (authenticated users)
- View all upcoming classes
- Book a class (with slot validation & race-condition safety)
- View user bookings
- PostgreSQL transactions to prevent overbooking

### 🛠 Tech Stack
- **Backend:** FastAPI  
- **Database:** PostgreSQL  
- **Authentication:** JWT (`python-jose`)  
- **Password Hashing:** bcrypt  
- **DB Driver:** psycopg2  
- **Server:** Uvicorn  

### 📁 Project Structure
```
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
```
## Setup Instructions

### Prerequisites

Make sure you have installed:
- Python 3.11+
- PostgreSQL 14+
- pip & virtualenv

### Clone the Repository
```bash
git clone https://github.com/your-username/fitness-studio-app.git
cd fitness-studio-app
```

### Create & Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Create Database Tables
```sql
CREATE TABLE users_data (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'user'
);

CREATE TABLE classes (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100),
    date_time TIMESTAMP,
    instructor VARCHAR(100),
    total_slots INT,
    available_slots INT
);

CREATE TABLE bookings (
    id BIGSERIAL PRIMARY KEY,
    class_id BIGINT REFERENCES classes(id) ON DELETE CASCADE,
    client_id BIGINT REFERENCES users_data(id) ON DELETE CASCADE,
    client_email VARCHAR(255)
);
```

## How to Run Locally

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

Server will run at: **http://127.0.0.1:8000**

## API Usage (Postman)

### Signup

**POST** `/auth/signup`

**Body:**
```json
{
    "name": "Alice",
    "email": "alice@example.com",
    "password": "password123",
    "role": "admin"
}
```

**Example 2:**
```json
{
    "name": "Ashwini",
    "email": "ashwini@gmail.com",
    "password": "Ash@123",
    "role": "user"
}
```

### Login

**POST** `/auth/login`

**Body:**
```json
{
    "email": "alice@example.com",
    "password": "password123"
}
```

**Response:**
```json
{
    "access_token": "JWT_TOKEN_HERE"
}
```

### Create Class (Authenticated)

**POST** `/classes`

**Headers:**
```
Authorization: Bearer JWT_TOKEN_HERE
```

**Body:**
```json
{
    "name": "Morning Yoga",
    "date_time": "2025-06-20 07:00:00",
    "instructor": "John Doe",
    "total_slots": 20
}
```

### View Classes

**GET** `/classes`
```
http://127.0.0.1:8000/classes
```

### Book a Class (Authenticated)

**POST** `/book`

**Headers:**
```
Authorization: Bearer JWT_TOKEN_HERE
```

**Body:**
```json
{
    "class_id": 1,
    "client_id": 2,
    "client_email": "ashwini@gmail.com"
}
```

### View My Bookings

**GET** `/bookings`

**Headers:**
```
Authorization: Bearer JWT_TOKEN_HERE
```

---
