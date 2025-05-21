from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.routers import cities, requests, feedback, masters, admin
from app.database import create_db_and_tables


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
Подключение роутеров
"""
app.include_router(cities.router)
app.include_router(requests.router)
app.include_router(feedback.router)
app.include_router(masters.router)
app.include_router(admin.router)




@app.on_event('startup')
def startup_event():
    create_db_and_tables()

