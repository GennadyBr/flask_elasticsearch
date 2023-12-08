import logging

from elasticsearch import Elasticsearch
import csv
import os
from dotenv import load_dotenv
from settings import logger, index_name

load_dotenv()


def flog(value):
    """Выводит переменную в лог в виде f{variable=} строки"""
    logger.info(f"{value=}")


url = f"http://{os.getenv('ES_HOST')}:9200"
es = Elasticsearch(hosts=[url])
logger.info(f'Connecting to Elasticsearch cluster `{es.info().body["cluster_name"]}`')


doc_count = es.count(index=index_name)['count']
if not doc_count:
    with open('Car_details_v3.csv', 'r') as f:
        reader = csv.reader(f)
        flog(next(reader))

        for i, line in enumerate(reader):
            document = {
                "name": line[0],
                "engine": line[9],
                "year": line[1],
                "price": line[2]
            }
            flog(document)
            res = es.index(index=index_name, document=document)
            flog(res)
    doc_count = es.count(index=index_name)['count']
    logger.info(f'В базу добавлено {doc_count} документов')
else:
    logger.info(f'База уже содержит {doc_count} документов')