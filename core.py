import logging
import json
from os import path, mkdir
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from source.database import Base
from aiogram import Bot
from aiogram.dispatcher import Dispatcher


if not path.exists('./logs/'):
    mkdir('./logs')

logging.basicConfig(filename='logs/pictura.log', level=logging.INFO,
                    format=u'%(asctime)-15s | [%(name)s] %(levelname)s => %(message)s')
logger = logging.getLogger('root')

# Config
config = json.load(open('config.json', 'r'))
msg = config['msg']['en']

engine = create_engine('postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'.format(
    user=config['db_user'],
    password=config['db_password'],
    host=config['db_host'],
    name=config['db_name'],
    port=config['db_port']
), echo=False)
Base.metadata.create_all(engine, checkfirst=True)




bot = Bot(token=config['tg_token'])
dp = Dispatcher(bot)

Session = sessionmaker(bind=engine)
