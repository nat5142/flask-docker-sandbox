from src.main import make_celery

app = make_celery()
app.conf.imports = app.conf.imports + ('src.tasks.example',)
