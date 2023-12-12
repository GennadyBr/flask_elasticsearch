import os
from typing import List

from elasticsearch import Elasticsearch
from elastic_transport import ConnectionError
from config.settings import logger, search_field


def es_conn() -> Elasticsearch:
    url = f"http://{os.getenv('ES_HOST')}:9200"
    try:
        es = Elasticsearch(url)
        # es = Elasticsearch(hosts=[url])
        logger.info(f'Connecting to Elasticsearch cluster `{es.info().body["cluster_name"]}`')
        return es
    except ConnectionError as err:
        logger.error(f'ConnectionError {err}')
        # raise ConnectionError(f'ConnectionError {err}')


def get_payload(tokens: List[str]) -> dict:
    clauses = [
        {
            "span_multi": {
                "match": {
                    "fuzzy": {
                        search_field: {
                            "value": i,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            }
        } for i in tokens
    ]

    payload = {
        "bool": {
            "must": [
                {
                    "span_near": {
                        "clauses": clauses,
                        "slop": 0,
                        "in_order": False
                    }
                }
            ]
        }
    }

    return payload
