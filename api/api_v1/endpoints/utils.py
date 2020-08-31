import logging
from typing import Any

from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic.networks import EmailStr

import models, schemas
from api import deps
from core.celery_app import celery_app
from utils import send_test_email
# from worker.celery_worker import test_celery

from worker.celery_app import celery_app

log = logging.getLogger(__name__)

router = APIRouter()


def celery_on_message(body):
    log.warn(body)

def background_on_message(task):
    log.warn(task.get(on_message=celery_on_message, propagate=False))


@router.get("/test-celery/{word}", status_code=201)
async def test_celery(
    word: str,
    background_task: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    task_name = "worker.celery_worker.test_celery"
    task = celery_app.send_task(task_name, args=[word])
    print(task)
    background_task.add_task(background_on_message, task)
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
