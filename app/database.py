import psycopg2

def get_db():
     # Create a new connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="fitness_studio_db",   # Database name
        user="postgres",              # Database user
        password="Lijygrdwa@74",       # Database password
        host="localhost",              # Database host (local machine)
        port=5432                      # PostgreSQL default port
    )

    try:
        # This is commonly used with dependency injection in FastAPI to provide a database connection for each request
        yield conn
    finally:
        # Ensure the database connection is always closed
        # This runs after the request is completed or if an error occurs
        conn.close()