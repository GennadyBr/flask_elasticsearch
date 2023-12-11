import os

from elasticsearch import Elasticsearch
from logger.settings import logger

def es_conn():
    url = f"http://{os.getenv('ES_HOST')}:9200"
    es = Elasticsearch(hosts=[url])
    logger.info(f'Connecting to Elasticsearch cluster `{es.info().body["cluster_name"]}`')
    return es


def get_payload(tokens: str) -> dict:
    clauses = [
        {
            "span_multi": {
                "match": {
                    "fuzzy": {
                        "name": {
                            "value": "marcides",
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
