from fastapi import FastAPI
from rag.api.endpoints import router

app = FastAPI()

# Register the router
app.include_router(router)
