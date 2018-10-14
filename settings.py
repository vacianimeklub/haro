import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))
LIST_OF_ADMINS = [ADMIN_USER_ID]

SQLITE_PATH = 'haro.sqlite'