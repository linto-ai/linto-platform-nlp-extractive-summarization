import os
from celery import Celery

from extsumm import logger

celery = Celery(__name__, include=['celery_app.tasks'])
service_name = os.environ.get("SERVICE_NAME", "extsumm")
broker_url = os.environ.get("SERVICES_BROKER")
if os.environ.get("BROKER_PASS", False):
    components = broker_url.split('//')
    broker_url = f'{components[0]}//:{os.environ.get("BROKER_PASS")}@{components[1]}'
celery.conf.broker_url = "{}/0".format(broker_url)
celery.conf.result_backend = "{}/1".format(broker_url)
celery.conf.update(
    result_expires=3600,
    task_acks_late=True,
    task_track_started = True)

# Queues
celery.conf.update(
    {'task_routes': {
        'extsumm_task' : {'queue': 'extsumm'},}
    }
)

logger.info(
    f"Celery configured for broker located at {broker_url} with service name {service_name}"
)