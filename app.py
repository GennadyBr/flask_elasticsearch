import os
from urllib import request

from flask import Flask
from dotenv import load_dotenv

from db.es import es_conn, get_payload

load_dotenv()

app = Flask(__name__)

max_size = 100


@app.route('/search')
def search_autocomplete():
    query = request.args["q"].lower()
    tokens = query.split(" ")
    if len(tokens) < 2:
        return "Please provide an autocomplete query"
    else:
        payload = get_payload(tokens)
        es = es_conn()

        response = es.search(index="cars", query=payload, size=max_size)

    return [result['_source']['name'] for result in response['hits']['hits']]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('FLASK_PORT'), debug=True)
