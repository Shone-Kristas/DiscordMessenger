import sys
import os

from trigger import schedule_message

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from sqlalchemy import insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models.models import bots_accounts, user_accounts, messages
import pandas as pd
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger


app = FastAPI()
scheduler = AsyncIOScheduler()

app.mount("/static", StaticFiles(directory="./public"))

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup_event():
    # Запуск планировщика
    scheduler.start()

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

@app.post("/upload-message/")
async def upload_message(message: str = Form(...), time: str = Form(...), db: AsyncSession = Depends(get_db)):
    try:
        # Преобразование времени в формат datetime
        time_obj = datetime.strptime(time, '%H:%M').time()
        # Удаление всех текущих записей
        await db.execute(messages.delete())
        # Создание нового сообщения
        new_message = {
            "message": message,
            "time": time_obj
        }
        # Вставка нового сообщения
        await db.execute(insert(messages).values(new_message))
        await db.commit()

        # Добавление задачи в планировщик
        send_time = datetime.combine(datetime.today(), time_obj)
        print("send_time", send_time)
        if send_time < datetime.now():
            send_time = datetime.combine(datetime.today() + timedelta(days=1), time_obj)

        scheduler.add_job(send_message, DateTrigger(run_date=send_time), args=[new_message["message"], db])

        return {"status": "message and time uploaded", "message": new_message}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def send_message(messege, db):
    # Получаем количество записей в таблице user_accounts
    count_result = await db.execute(select(func.count()).select_from(user_accounts))
    count = count_result.scalar()

    # Получаем все аккаунты bots_accounts
    bot_acc_result = await db.execute(select(bots_accounts.c.login, bots_accounts.c.password))
    bot_acc = bot_acc_result.all()
    bot_index = 0  # Индекс текущего аккаунта в bots_accounts

    # Получаем все user_id из таблицы user_accounts
    user_acc_result = await db.execute(select(user_accounts.c.user_id))
    user_acc = user_acc_result.all()
    user_index = 0  # Индекс текущего user_id в user_accounts

    # Итерируем по количеству записей в таблице user_accounts
    for i in range(count):
        login = bot_acc[bot_index][0]  # Получаем login текущего аккаунта bots_accounts
        password = bot_acc[bot_index][1]  # Получаем password текущего аккаунта bots_accounts
        user_id = user_acc[user_index][0]  # Получаем user_id текущей записи из user_accounts

        schedule_message(login, password, user_id, messege)

        bot_index += 1

        # Если достигли конца списка аккаунтов в bots_accounts, сбрасываем индекс и начинаем сначала
        if bot_index >= len(bot_acc):
            bot_index = 0
        user_index += 1