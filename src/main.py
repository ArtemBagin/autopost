from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)
