from pymysql import connect
from dotenv import load_dotenv
from os import getenv

load_dotenv()
conn = connect(getenv('DB_HOST'), getenv('DB_USER'),
               getenv('DB_PASSWORD'), getenv('DB_NAME'), charset='utf8', autocommit=True)
