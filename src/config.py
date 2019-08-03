import os
import logging

DEBUG = True
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '5000'))

POSTGRES = {
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'pw': os.getenv('POSTGRES_PW', ''),
    'host': os.getenv('POSTGRES_HOST', os.getenv('DB_PORT_5432_TCP_ADDR')),
    'port': os.getenv('POSTGRES_PORT', os.getenv('DB_PORT_5432_TCP_PORT')),
    'db': os.getenv('POSTGRES_DB', 'postgres'),
}
DB_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'server.log'),
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s pid:%(process)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)

ICEFIRE_API_URL = "https://www.anapioficeandfire.com/api/books"
ICEFIRE_API_TIMEOUT = 10
