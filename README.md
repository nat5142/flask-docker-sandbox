
# Flask Docker Sandbox


I'm a simple Flask app that runs via a docker container. Clone and use
however you want. Just don't commit to master. Or do. I don't care.

Use branches and leave them open when demoing a new concept


### Use:

Build and run docker image:
```
$ > docker compose up --build --remove-orphans
```


Config settings stored in `src/config_local.py`. Create a values for the following keys: 

- `SECRET_KEY` 
- `SECURITY_PASSWORD_SALT`
- `PASSWORD_RESET_SALT`

Easiest to generate these by running the following in an interpreter
```python
import uuid ; uuid.uuid4().hex
```

### Flask-Mail configuration:

Best way to set up a simple email service for the project is to create a new Google account, set up 2FA, and create an App Password for it. The App Password can stand in for your login password in the `MAIL_PASSWORD` flask config variable.

To do this go to your account > "Security" tab (left) > Section "Signing In To Google" > App passwords. After this, a google mail config will look like this:

```python
# Flask-Mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = '<mailbox>x@gmail.com'
MAIL_PASSWORD = '<your-app-password>'
```


## Database:

Default installation is Postgres.


### TODO:

- Add compose file to orchestrate additional microservices
- Deploy to AWS via ECR. Mount as subdomain.
