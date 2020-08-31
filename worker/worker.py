from raven import Client

from core.celery_app import celery_app
# from core.config import settings
SENTRY_DSN = None
client_sentry = Client(SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"
