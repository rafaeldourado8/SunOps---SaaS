from celery import Celery
from celery.schedules import crontab
from decouple import config

app = Celery(
    'ops_crm',
    broker=config('CELERY_BROKER_URL', default='amqp://rabbitmq:rabbitmq_dev_password@rabbitmq:5672//'),
    backend=config('CELERY_RESULT_BACKEND', default='redis://redis:6379/1'),
    include=['celery_app.tasks.example', 'celery_app.tasks.cotacao_alert']
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
    beat_schedule={
        'alerta-cotacao-segunda': {
            'task': 'celery_app.tasks.cotacao_alert.alerta_cotacao_segunda',
            'schedule': crontab(hour=8, minute=0, day_of_week=1),  # Segunda 8h
        },
    },
)

if __name__ == '__main__':
    app.start()
