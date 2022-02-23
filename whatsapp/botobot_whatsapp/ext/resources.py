from flask_restful import Api
from importlib import import_module

def add_resources(api):
    """ Add all resources to the API.
        Configuration string: "fully_qualified_name:url_route"
    """
    for res in api.app.config.RESTAPI_RESOURCES:
        module_name, route = res.split(":")
        module = import_module('.'.join(module_name.split('.')[:-1]))
        class_ = getattr(module, module_name.split('.')[-1])
        api.add_resource(class_,route)

def init_app(app):
    add_resources(api = Api(app))
