import os

from flask import Flask, request
from dotenv import load_dotenv
from werkzeug.exceptions import BadRequestKeyError

from db.es import es_conn, get_payload
from logger.settings import logger
load_dotenv()

app = Flask(__name__)

max_size = 100


@app.route('/search')
def search_autocomplete():
    try:
        query = request.args["q"].lower()
        logger.info(f'{query=}')
        tokens = query.split(" ")
        logger.info(f'{tokens=}')
        payload = get_payload(tokens)
        logger.info(f'{payload=}')
        es = es_conn()

        response = es.search(index="cars", query=payload, size=max_size)
        logger.info(f"{response['hits']['hits']=}")
        return [result['_source']['name'] for result in response['hits']['hits']]
    except BadRequestKeyError:
        return "Please provide an autocomplete query"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('FLASK_PORT'), debug=True)
