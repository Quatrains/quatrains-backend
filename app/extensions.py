from flasgger import Swagger
from peeweext.flask import Peeweext

from app.Algs.recommend import Predict


swagger = Swagger(template_file="docs/openapi_template.yml")

pwdb = Peeweext()

predict = Predict("app/Algs/dict_SimilariyPopularityType.json")
