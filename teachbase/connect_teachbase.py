import requests
from datetime import datetime, timedelta, timezone

from teachbase_drf.teachbase.settings import CLIENT_ID, CLIENT_SECRET


class Connect_teachbase:
    ''' Получаем токины и подключаемся к teachbase '''

    hours_update_tocken = 2

    def __init__(self):
        self.update_at_tocken_timestamp = 0
        self.access_token = None

    def update_bearer_token(self):
        ''' Обновляем токен, для авторизации на teachbase '''

        url = 'https://go.teachbase.ru/oauth/token'
        
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials"
        }

        response = requests.post(url, json=data)

        self.access_token = response.json().get('access_token', None)

        print('!!! RECONNECT update_bearer_token')

        self.update_at_tocken_timestamp = (datetime.fromtimestamp(response.json().get('created_at', 0), tz=None) + timedelta(hours=self.hours_update_tocken)).timestamp()

        return self.access_token


    def get_bearer_token(self):
        ''' Получаем актуальный токен '''

        if self.update_at_tocken_timestamp >= self._get_datetime_timezone():
            return self.access_token

        return self.update_bearer_token()


    def add_tocken_in_header(self, header=None):
        ''' Добавляем в запрос токен авторизации '''

        if not header:
            header = {}

        header['Authorization'] = f'Bearer {self.get_bearer_token()}'

        return header


    def _get_datetime_timezone(self):
        ''' получаем воемя в без сдвига по зоне '''

        tzinfo = timezone(timedelta())
        tms = datetime.now(tzinfo).timestamp()
        return tms


if __name__ == '__main__':
    ct = Connect_teachbase()
    print(ct.get_bearer_token())
    print(ct.get_bearer_token())