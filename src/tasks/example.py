import logging

from src.extensions import celery

log = logging.getLogger('tasks.example')


@celery.task
def example_task():
    return 'OK'


@celery.task
def logging_task(value):
    log.info('Logging task value: {}'.format(value))
    return
