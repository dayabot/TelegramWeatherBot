# -*- coding: utf-8 -*-
import sys

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from loguru import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from telegram_bot.database import models
from telegram_bot.database.database import engine
from telegram_bot.routers import webhook, cron
from telegram_bot.settings import settings

logger.remove()
FORMAT = "<level>{level: <6}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{message}</level>"
logger.add(sys.stdout, colorize=True, format=FORMAT)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(webhook.router)
app.include_router(cron.router)

# sentry middleware
if settings.SENTRY_URL:
    sentry_sdk.init(dsn=settings.SENTRY_URL, environment=settings.ENV)
    app = SentryAsgiMiddleware(app)

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=5000, log_level="info", reload=True)