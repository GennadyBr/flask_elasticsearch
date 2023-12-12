import os

from flask import Flask, request, render_template
from dotenv import load_dotenv
from werkzeug.exceptions import BadRequestKeyError
from elasticsearch import NotFoundError

from db.es import es_conn, get_payload
from config.settings import logger, setting

index_name, search_field, max_size = setting('index_name'), setting('search_field'), setting('max_size')

load_dotenv()

app = Flask(__name__)

def _search(request):
    es = es_conn()
    try:
        query = request.args["q"].lower()
        # logger.info(f'{query=}')
        tokens = query.split(" ")
        # logger.info(f'{tokens=}')
        payload = get_payload(tokens)
        # logger.info(f'{payload=}')
        response = es.search(index=index_name, query=payload, size=max_size)
        # logger.info(f"{response['hits']['hits']=}")
        sorted_response = sorted(response['hits']['hits'], key=lambda k: k['_score'], reverse=True)
        # result = [
        #     f"""{res['_score']} / {res['_source'][search_field]} dep: {res['_source']['Department']} salary: {res['_source']['Salary']}$"""
        #     for res in sorted_response]
        return sorted_response

    except BadRequestKeyError:
        return f"Please provide an query http://{os.getenv('VPS_HOST')}:{os.getenv('FLASK_PORT')}/search?q=<your request>"
    except NotFoundError:
        return f"no such index ['{index_name}'], available index {[key for key in es.indices.get_alias(index='*') if '.' not in key[0]]}"

@app.route('/')
def home():
    users = _search(request)
    return render_template("index.html", users=users)


@app.route('/search')
def search():
    users = _search(request)
    return render_template("index.html", users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('FLASK_PORT'), debug=True)
