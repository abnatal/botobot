from botobot_whatsapp.ext.database import db

def create_db():
    """ Creates the database and required records. """
    db.create_all()

def drop_db():
    """ Drops the entire database """
    db.drop_all()

def init_app(app):
    for command in [create_db, drop_db]:
        app.cli.add_command(app.cli.command()(command))
