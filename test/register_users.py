import secrets

import pandas as pd
import requests
from tqdm import tqdm
from config import Config

TOKEN = Config.TOKEN
USER_NUMBER = Config.USER_NUMBER
API = Config.HOST

logins = []
passwords = []

for i in tqdm(range(USER_NUMBER)):
    password = secrets.token_hex(20)
    login = f"user_{secrets.token_hex(10)}"
    r = requests.post(
        f"{API}/auth/register",
        data={
            'token': TOKEN,
            'login': login,
            'password': password
        }
    )
    logins.append(login)
    passwords.append(password)

# df_old = pd.read_csv('kek.csv')
df = pd.DataFrame({'login': logins, 'password': passwords})
# df_new = pd.concat([df_old, df])
df_new = df
df_new.to_csv('users.csv', index=False)
