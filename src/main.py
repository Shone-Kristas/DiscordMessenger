import sys
import os

# Добавьте корневую директорию в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal, init_db
from models.models import bots_accounts, user_accounts
import pandas as pd

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application. Use /upload-sending-accounts/ to upload sending accounts and /upload-recipient-accounts/ to upload recipient accounts."}

@app.post("/upload-sending-accounts/")
async def upload_sending_accounts(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        # Чтение данных из файла
        df = pd.read_csv(file.file)
        # Удаление всех текущих записей
        await db.execute(bots_accounts.delete())
        # Формирование новых записей для вставки
        accounts = [
            {
                "login": row["login"],
                "password": row["password"]
            }
            for index, row in df.iterrows()
        ]
        # Вставка новых записей
        await db.execute(bots_accounts.insert().values(accounts))
        # Подтверждение изменений
        await db.commit()
        return {"status": "sending accounts uploaded", "count": len(accounts)}
    except Exception as e:
        # В случае ошибки откатываем транзакцию
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upload-recipient-accounts/")
async def upload_recipient_accounts(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        # Чтение данных из файла
        df = pd.read_csv(file.file)
        # Удаление всех текущих записей
        await db.execute(user_accounts.delete())
        # Формирование новых записей для вставки
        accounts = [
            {
                "user_id": row["user_id"]
            }
            for index, row in df.iterrows()
        ]
        # Вставка новых записей
        await db.execute(user_accounts.insert().values(accounts))
        # Подтверждение изменений
        await db.commit()
        return {"status": "sending accounts uploaded", "count": len(accounts)}
    except Exception as e:
        # В случае ошибки откатываем транзакцию
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sending-accounts/")
async def get_sending_accounts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(bots_accounts))
    accounts = result.scalars().all()
    return accounts

@app.get("/recipient-accounts/")
async def get_recipient_accounts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(user_accounts))
    accounts = result.scalars().all()
    return accounts