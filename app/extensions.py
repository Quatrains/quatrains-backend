from flasgger import Swagger
from peeweext.flask import Peeweext


swagger = Swagger(template_file="docs/openapi_template.yml")

pwdb = Peeweext()
