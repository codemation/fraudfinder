import os
from fastapi import FastAPI
from easyauth.client import EasyAuthClient
from models import Person
from models.db import db_setup
from app import compare_persons
from app.api import api_setup
from app.frontend import frontend_setup

server = FastAPI(title='Fraud Detection')

TOKEN_SERVER_PATH = os.environ.get('TOKEN_SERVER_PATH')
assert TOKEN_SERVER_PATH, f"missing required environment variable 'TOKEN_SERVER_PATH'"

@server.on_event('startup')
async def startup():
    server.auth = await EasyAuthClient.create(
        server, 
        TOKEN_SERVER_PATH, # Should be a running EasyAuthServer
    )
    await db_setup(server.auth)
    await api_setup(server.auth)
    await frontend_setup(server.auth)

@server.on_event('shutdown')
async def shutdown():
    await server.auth.db.close()

