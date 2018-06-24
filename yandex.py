import requests


class YaMetrikaBase:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.token)
        }


class YaMetrikaUser(YaMetrikaBase):

    @property
    def counters(self):
        headers = self.get_headers()
        response = requests.get(
            'https://api-metrika.yandex.ru/management/v1/counters',
            headers=headers
        )
        return [YaMetrikaCounter(self.token, c['id']) for c in response.json()['counters']]

    @property
    def accounts(self):
        headers = self.get_headers()
        response = requests.get(
            'https://api-metrika.yandex.ru/management/v1/accounts',
            headers=headers
        )
        return [c['id'] for c in response.json()['accounts']]


class YaMetrikaCounter(YaMetrikaBase):
    def __init__(self, token, counter_id):
        super().__init__(token)
        self.counter_id = counter_id
        self.headers = self.get_headers()

    @property
    def visits(self):
        response = requests.get('https://api-metrika.yandex.ru/stat/v1/data',
                                params=dict(
                                    ids=self.counter_id,
                                    metrics='ym:s:visits'
                                ), headers=self.headers)
        return response.json()['totals'][0]

    @property
    def pageviews(self):
        response = requests.get('https://api-metrika.yandex.ru/stat/v1/data',
                                params=dict(
                                    ids=self.counter_id,
                                    metrics='ym:s:pageviews'
                                ), headers=self.headers)
        return response.json()['totals'][0]

    @property
    def users(self):
        response = requests.get('https://api-metrika.yandex.ru/stat/v1/data',
                                params=dict(
                                    ids=self.counter_id,
                                    metrics='ym:s:users'
                                ), headers=self.headers)
        return response.json()['totals'][0]


TOKEN = 'AQAAAAAnpo6KAAUQ9dAiMjTn3EofrXcOFq4ovIM'
yametrika = YaMetrikaUser(TOKEN)
for counter in yametrika.counters:
    print(counter.counter_id, counter.visits, counter.pageviews, counter.users)
