from fastapi import FastAPI

from app.routes import auth, cart, products, ratings, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(ratings.router)
app.include_router(cart.router)
