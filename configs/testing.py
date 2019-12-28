from configs.default import *

TESTING = True
PW_DB_URL = "mysql+pool://127.0.0.1"
PW_CONN_PARAMS.update({"database": "quatrains_test"})
