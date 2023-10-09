from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import task, token, auth, users

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*'],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(task.router)
app.include_router(token.router)
app.include_router(auth.router)
app.include_router(users.router)
