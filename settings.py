import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

admin_user_id_raw = os.getenv('ADMIN_USER_ID')
if admin_user_id_raw:
    ADMIN_USER_ID = int(admin_user_id_raw)
    LIST_OF_ADMINS = [ADMIN_USER_ID]
else:
    ADMIN_USER_ID = None
    LIST_OF_ADMINS = []

SQLITE_PATH = 'haro.sqlite'
SQLALCHEMY_SQLITE_PATH = 'sqlite:///' + SQLITE_PATH
