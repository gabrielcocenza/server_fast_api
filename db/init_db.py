from sqlalchemy.orm import Session

import crud, schemas
# from core.config import settings
from db.base import Base
from db.session import engine

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email="superuser_1@gmail.com")
    if not user:
        user_in = schemas.UserCreate(
            email="superuser_1@gmail.com",
            password="password",
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)
