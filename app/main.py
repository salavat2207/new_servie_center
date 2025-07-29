from fastapi import HTTPException
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles

# from app import auth
from app.auth import authenticate_user, create_access_token
from app.routers import cities, requests, masters, admin, products, menu, register
from app.database import create_db_and_tables
import logging
from fastapi import FastAPI





import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from routers.requests import router as requests_router

from middleware.proxy_headers import ProxyHeadersMiddleware


app = FastAPI()

app.add_middleware(ProxyHeadersMiddleware)



origins = [
  "http://localhost:8000",
  "http://localhost:5173",
  "http://185.177.216.134:5173",
  "http://xn----7sbfcggdzf6eibe.xn--p1ai",
  "https://xn----7sbfcggdzf6ejbe.xn--p1ai",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



"""
Старт ТГ Бота
"""
# @app.on_event("startup")
# def start_bot():
#     threading.Thread(target=start_polling, daemon=True).start()



"""
Подключение роутеров
"""
app.include_router(cities.router)
# app.include_router(feedback.router)
app.include_router(masters.router)
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(requests.router, prefix="", tags=[""])
app.include_router(products.router, prefix="/products", tags=["products"])
# app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(menu.router, prefix="/menu", tags=["menu"])
app.include_router(register.router, prefix="/admin", tags=["auth"])
app.mount("/images", StaticFiles(directory="images"), name="images")




# @app.on_event('startup')
# def startup_event():
#     create_db_and_tables()


"""
Авторизация
"""
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверные данные")
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 FastAPI остановлен")





if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)