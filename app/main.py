from fastapi import FastAPI

from app.routes import auth, products, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
