from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Routes
from routes import job

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware, allow_origins="*", allow_methods="*", allow_headers="*"
)


app.include_router(job.router)


@app.get("/")
def root():
    return {"message": "Daggle flask server⚡"}
