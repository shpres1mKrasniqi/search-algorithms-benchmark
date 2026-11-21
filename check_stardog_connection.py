import os

import stardog
from dotenv import load_dotenv

load_dotenv()

connection_details = {
    "endpoint": os.environ["STARDOG_ENDPOINT"],
    "username": os.environ["STARDOG_USERNAME"],
    "password": os.environ["STARDOG_PASSWORD"],
}

database = os.environ["STARDOG_DATABASE"]

with stardog.Connection(database, **connection_details) as conn:
    result = conn.select("SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }")
    print(result)