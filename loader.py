import csv
from dotenv import load_dotenv
from elasticsearch import NotFoundError

from config.settings import logger, setting
from db.es import es_conn

load_dotenv()


def _load_data():
    try:
        with open(setting["csv_file"], 'r') as f:
            reader = csv.reader(f)
            logger.info(f'{next(reader)=}') #пропуск первой строки с заголовками
            for i, line in enumerate(reader):
                # logger.info(f"Loading row {i}: {line}")
                try:
                    salary1 = int(line[4]) % 1000  # less 1000
                    salary2 = int(line[4]) // 1000 % 1000  # less 1mln, gt 1000
                    salary3 = int(line[4]) // 1000000  # gt 1mln
                    salary = f"""$ {salary3 if salary3 > 0 else ''}{"'" if salary3 > 0 else ''}{salary2 if salary2 > 0 else ''}{"'" if salary2 > 0 else ''}{salary1}.00"""
                except ValueError as err:
                    logger.error(f"{line[4]=}, {err=}")  # , {salary1=}, {salary2=}, {salary3=}
                    salary = line[4]
                document = {
                    "Employee_ID": line[0],
                    "Name": line[2] + ' ' + line[1],
                    "Department": line[3],
                    "Salary": salary,
                    "Joining_Date": line[5],
                    "Email_ID": line[6],
                    "Address": line[7]
                }
                # logger.info(f'{document=}')
                res = es.index(index=index_name, document=document)
                # if res:
                #     logger.info(f"Loaded row {i}")
                # else:
                #     logger.error(f"loading failed {i}")
                # logger.info(f'{res=}')
    except FileNotFoundError as err:
        logger.error(f'CAN FIND {setting["csv_file"]}, {err=}')
    else:
        _doc_count = es.count(index=index_name)['count']
        logger.info(f'В базу добавлено {_doc_count} документов')


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
