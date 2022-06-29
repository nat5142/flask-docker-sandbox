
# Flask Docker Sandbox


I'm a simple Flask app that runs via a docker container. Clone and use
however you want. Just don't commit to master. Or do. I don't care.

Use branches and leave them open when demoing a new concept


### Use:

Build docker image:
```
$ > docker build -t flask-docker-sandbox:latest .
```

And run:
```
$ > docker run -p 5000:5000 flask-docker-sandbox
```


Config settings stored in `src/config_local.py`. To be overridden later.


### TODO:

- Add compose file to orchestrate additional microservices
- Deploy to AWS via ECR. Mount as subdomain.
