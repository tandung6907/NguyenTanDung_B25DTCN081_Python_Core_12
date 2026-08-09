from fastapi import FastAPI

from library_management.database import Base, engine
from library_management.routers import author_router, book_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")

app.include_router(author_router.router)
app.include_router(book_router.router)


@app.get("/")
def root():
    return {"message": "Library Management API is running"}
