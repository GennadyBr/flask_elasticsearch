import os
from time import sleep
from typing import List

from elasticsearch import Elasticsearch
from elastic_transport import ConnectionError
from config.settings import logger, setting


def es_conn() -> Elasticsearch:
    url = f"http://{os.getenv('ES_HOST')}:9200"
    for _ in range(10):
        try:
            es = Elasticsearch(url)
            logger.info(f'Connecting to Elasticsearch cluster `{es.info().body["cluster_name"]}`')
        except ConnectionError as err:
            logger.error(f'es_conn {err}')
            sleep(5)
        else:
            return es



def get_payload(tokens: List[str]) -> dict:
    search_field = setting["search_field"]
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
