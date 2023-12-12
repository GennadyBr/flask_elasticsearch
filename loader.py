import csv
from dotenv import load_dotenv

from config.settings import logger, index_name

from db.es import es_conn

load_dotenv()
es = es_conn()
doc_count = es.count(index=index_name)['count']

if not doc_count:
    with open('faker_employee_salary.csv', 'r') as f:
        reader = csv.reader(f)
        logger.info(f'{next(reader)=}')

        for i, line in enumerate(reader):
            document = {
                "Employee ID": line[0],
                "First Name": line[1],
                "Last Name": line[2],
                "Department": line[3],
                "Salary": line[4],
                "Joining Date": line[5],
                "Email ID": line[6],
                "Address": line[7]
            }
            logger.info(f'{document=}')
            res = es.index(index=index_name, document=document)
            logger.info(f'{res=}')
    doc_count = es.count(index=index_name)['count']
    logger.info(f'В базу добавлено {doc_count} документов')
else:
    logger.info(f'База уже содержит {doc_count} документов')
