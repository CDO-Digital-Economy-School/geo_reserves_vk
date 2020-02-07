
import requests
import json
import pandas as pd

vk_api = 'https://api.vk.com/method/'
token = '(╯°□°）╯︵ ┻━┻'


class Params:

    def __init__(self, **kwargs):
        self.params_dict = {
            'v': '5.7',
            'filter': 'all',
            'access_token': token}
        for key, value in kwargs.items():
            self.params_dict[key] = str(value)

    def get_dict(self):
        return self.params_dict


method = 'photos.search'
reserves = [
    ['Земля Леопарда', 43.23994, 131.36819, 8000],
    ['Национальный парк Бикин', 46.5403, 135.36522, 3500],
    ['Удэгейская легенда', 45.75773, 135.47622, 10000],
    ['Сихотэ - Алийский заповедник', 45.3337, 136.262, 20000],
    ['Дальневосточный Морской заповедник', 43.19967, 131.92011, 300],
    ['Кедровая падь', 43.10331, 131.49025, 6000],
    ['Зов тигра', 43.55909, 134.25464, 15000],
    ['Сафари парк', 43.32466, 132.40369, 1100],
    ['Бухта петрова', 42.87271, 133.80187, 2300],
    ['Лазовский заповедник', 43.15432, 133.9992, 14000],
    ['Высота 611', 44.568938, 135.574703, 300],
    ['Владивосток', 43.111820, 131.926755, 3000]]

all_reserves = pd.DataFrame()
in_vdk = pd.DataFrame()
offs = 100

for i in range(len(reserves)):
    buf_reserve = list()
    sch = 0
    while len(buf_reserve) >= (sch * (offs * 0.9)):
        params = Params(lat=str(reserves[i][1]), long=str(reserves[i][2]),
                        radius=str(reserves[i][3]), offset=str(sch * offs)).get_dict()
        buf_reserve += json.loads(requests.get(vk_api + method, params=params).text)['response']['items']
        sch += 1

    buf_reserve = pd.DataFrame(buf_reserve).drop(columns={'text', 'user_id', 'post_id',
                                                          'id', 'album_id', 'photo_75', 'photo_130',
                                                          'photo_604', 'photo_807', 'photo_1280',
                                                          'photo_2560', 'width', 'height'})

    buf_reserve.drop_duplicates('owner_id', inplace=True)
    buf_reserve.drop(columns='owner_id').to_csv(f'csv/{reserves[i][0]}.csv', index=False)
    print(reserves[i][0], len(buf_reserve))

    if i != (len(reserves) - 1):
        all_reserves = pd.concat([all_reserves, buf_reserve], sort=False)
    else:
        print('Всего', len(all_reserves))
        all_reserves.drop_duplicates('owner_id', inplace=True)
        all_reserves.drop(columns={'owner_id'}).to_csv('csv/all reserves.csv', index=False)

        print(reserves[i][0], len(buf_reserve))
        in_vdk = buf_reserve[buf_reserve.owner_id.isin(all_reserves.owner_id)]

in_vdk.drop(columns={'owner_id'}).to_csv('csv/Places in VDK.csv', index=False)
print('Мест во Владивостоке', len(in_vdk))
