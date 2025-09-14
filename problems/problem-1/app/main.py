from fastapi import FastAPI
from .database import test_connection, Base, engine
from . import models
from .routers import auth, users, projects, tasks

# create tables if not exist
models.Base = Base  # ensure Base is available (models already use Base import)
# Note: in production use migrations. For dev, create tables on startup.

app = FastAPI(title="Task Manager API", version="1.0.0")

@app.on_event("startup")
def startup_event():
    test_connection()
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print("Error creating tables:", e)

# include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Task Manager API is running"}