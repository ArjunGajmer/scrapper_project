from fastapi import FastAPI
from app.api import user_routes, scrap_request_routes
from app.db.sql import create_database

app = FastAPI()
create_database()

app.include_router(user_routes.router)
app.include_router(scrap_request_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
