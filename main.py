import auth_token
from fastapi import FastAPI
import tasks
import users

#Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth_token.router)
