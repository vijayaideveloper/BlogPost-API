from fastapi import Depends, FastAPI
from app.routers import post, user, auth

from app.database import Base, engine



app = FastAPI(title="Social Posts API")

Base.metadata.create_all(bind=engine)




@app.get("/", tags=["Root"])
def root():
    return {"message": "Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)