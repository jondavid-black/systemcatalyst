from fastapi import FastAPI

app = FastAPI(title="System Gantry API")


@app.get("/")
def read_root():
    return {"message": "Welcome to System Gantry API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
