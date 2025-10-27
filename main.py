from fastapi import FastAPI

from app.db import engine
from app.seed import seed_data
from app.routes.teams import router as teams_router
from app.routes.tournaments import router as tournaments_router
from app.routes.matches import router as matches_router


app = FastAPI()

app.include_router(teams_router)
app.include_router(tournaments_router)
app.include_router(matches_router)


@app.on_event("startup")
def on_startup():
    # create tables
    from sqlmodel import SQLModel, Session

    SQLModel.metadata.create_all(engine)
    # seed data
    with Session(engine) as session:
        seed_data(session)


