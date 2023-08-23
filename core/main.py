from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.assistant.assistant_controller import controller as AssistantAudioController
from core.bot.bot import setup_bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    application = setup_bot()
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    yield
    await application.stop()


app = FastAPI(lifespan=lifespan)

connected_clients = []

origins = [
    "http://localhost",
    "http://localhost:3000",
    "ws://localhost:3000",
    "*"
]

app.include_router(AssistantAudioController, tags=['assistant'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
