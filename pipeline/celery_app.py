from celery import Celery

celery_app = Celery(
    "omnigen_workers",
    broker="sqla+sqlite:///celery_broker.db",
    backend="db+sqlite:///celery_results.db"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Explicitly import tasks so the worker registers them on startup
import pipeline.tasks