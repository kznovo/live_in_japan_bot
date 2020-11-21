import os
from datetime import datetime

import gspread
import pandas as pd
import tweepy
from dotenv import load_dotenv

load_dotenv()
DEBUG = os.getenv('DEBUG')
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

tauth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
tauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tapi = tweepy.API(tauth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

gc = gspread.service_account()
sh = gc.open('japan_addresses')
worksheet = sh.sheet1
data = pd.DataFrame.from_dict(worksheet.get_all_records())
post_data = data.loc[data['posted'] == 'FALSE'].sample(1)

print(post_data)
if not DEBUG:
    print('Posting...')
    tapi.update_status(post_data['content'].values[0])

    print('Updating gspreadsheet...')
    index = int(post_data.index.values[0]) + 2
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    worksheet.update(f'B{index}', 'TRUE')
    worksheet.update(f'C{index}', timestamp)

print('DONE')
