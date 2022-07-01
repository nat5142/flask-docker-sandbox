from src.extensions import db


def init_db(flask_app):
    db.init_app(flask_app)


def commit_db_session():
    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        raise exc


class CommonModel(object):
    """ A database model that I've found to be particularly useful. """

    def save(self, commit=True, *args, **kwargs):
        """ Add the records to the database session and COMMIT transaction """
        db.session.add(self)
        if commit:
            commit_db_session()

    def delete(self, commit=True, *args, **kwargs):
        db.session.delete(self)
        if commit:
            commit_db_session()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def as_dict(self):
        """ Represent the object as a dictionary without the `_sa_instance_state` key. """
        _dict = {}
        for key, value in self.__dict__.items():
            if key == '_sa_instance_state':
                continue
            else:
                _dict[key] = value

        return _dict
