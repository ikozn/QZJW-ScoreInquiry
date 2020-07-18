import requests
import json
import Settings


class Qzapi():
    def __init__(self):
        self.url = Settings.url
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36'
        }

    def is_valid(self, token):
        self.headers['token'] = token
        params = {
            'method': 'getStudentIdInfo'
        }
        response = requests.get(self.url,
                                headers=self.headers,
                                params=params
                                )
        if response.status_code == 200:
            try:
                if json.loads(response.content)['flag'] == '0':
                    return True
            except(KeyError):
                return False

    # 登录换取 token
    def get_token(self):
        params = {
            'method': 'authUser',
            'xh': Settings.account,
            'pwd': Settings.password
        }
        response = requests.get(Settings.url,
                                headers=self.headers,
                                params=params
                                )
        if response.status_code == 200:
            res_json = json.loads(response.content)
            if res_json['success']:
                return res_json['token']

    # 获取当前学期学年
    def getXnxq(self):
        params = {
            'method': 'getXnxq',
            'xh': Settings.account
        }
        response = requests.get(self.url,
                                headers=self.headers,
                                params=params
                                )
        if response.status_code == 200:
            res_json = json.loads(response.content)
            for i in range(len(res_json)):
                for flag in res_json[i]['isdqxq']:
                    if flag == '1':
                        return res_json[i]['xnxq01id']

    # 成绩查询（当前学期学年）
    def getCjcx(self):
        result_list = []
        params = {
            'method': 'getCjcx',
            'xh': Settings.account,
            'xqxnid': self.getXnxq()
        }
        response = requests.get(self.url,
                                headers=self.headers,
                                params=params
                                )
        if response.status_code == 200:
            res_json = json.loads(response.content)['result']
            for v in res_json:
                result_list.append({
                    'kcmc': v['kcmc'],
                    'zcj': v['zcj']
                })
        return result_list
