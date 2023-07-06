from fastapi import FastAPI
from pymongo import MongoClient
from database.db import db, connection

# Routes
from routes import user

app = FastAPI(debug=True)


@app.on_event("startup")
def startup_db_client():
    db.user.create_index([("address")], unique=True)


@app.on_event("shutdown")
def shutdown_db_client():
    connection.close()
    print("Closed MongoDB database!")


app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Daggle flask server⚡"}
