
# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/flask_docker_sandbox'  # Default for docker-compose configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Celery
CELERY_CONFIG = {  # Defaults for docker-compose
    'broker_url': 'amqp://guest:guest@rabbitmq:5672/',
    'result_backend': 'db+{}'.format(SQLALCHEMY_DATABASE_URI),
    'task_annotations': {
        'tasks.add': {
            'rate_limit': '10/s'
        }
    }
}

CELERY_BROKER_URL = CELERY_CONFIG['broker_url']
