'''Initialize the database connection'''
from os import getenv
from dotenv import load_dotenv
from pymysql import connect

load_dotenv()
conn = connect(getenv('DB_HOST'), getenv('DB_USER'),
               getenv('DB_PASSWORD'), getenv('DB_NAME'), charset='utf8', autocommit=True)
