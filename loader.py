import csv
from dotenv import load_dotenv
from elasticsearch import NotFoundError

from config.settings import logger, setting
from db.es import es_conn

load_dotenv()

def _load_data():
    try:
        with open('db/faker_employee_salary.csv', 'r') as f:
            reader = csv.reader(f)
            # logger.info(f'{next(reader)=}')

            for i, line in enumerate(reader):
                document = {
                    "Employee_ID": line[0],
                    "Name": line[2] + ' ' + line[1],
                    "Department": line[3],
                    "Salary": line[4],
                    "Joining_Date": line[5],
                    "Email_ID": line[6],
                    "Address": line[7]
                }
                # logger.info(f'{document=}')
                res = es.index(index=index_name, document=document)
                # logger.info(f'{res=}')
        _doc_count = es.count(index=index_name)['count']
        logger.info(f'В базу добавлено {_doc_count} документов')
    except FileNotFoundError as err:
        logger.error(f'{err=}')


if __name__ == '__main__':
    es = es_conn()
    index_name = setting["index_name"]

    try:
        doc_count = es.count(index=index_name)['count']
    except NotFoundError as err:
        logger.error(f'doc_count {err}')
        _load_data()
    except AttributeError as err:
        logger.error(f'doc_count {err}')
    else:
        if not doc_count:
            _load_data()
        else:
            logger.info(f'База уже содержит {doc_count} документов')
