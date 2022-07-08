

def register_jinja(flask_app):
    flask_app.jinja_env.add_extension('jinja2.ext.do')
    flask_app.jinja_env.add_extension('jinja2.ext.loopcontrols')
