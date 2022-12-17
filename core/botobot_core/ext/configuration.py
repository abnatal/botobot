from importlib import import_module
from dynaconf import FlaskDynaconf

def load_extensions(app):
    for extension in app.config.EXTENSIONS:
        module_name, factory = extension.split(":")
        ext = import_module(module_name)
        getattr(ext, factory)(app)

def init_app(app):
    FlaskDynaconf(app, settings_files=["settings.toml"])
    load_extensions(app)