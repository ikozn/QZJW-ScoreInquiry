import Qzapi
import sqlite3
import requests
import os
from Settings import ServerChan_URL


class Work(Qzapi.Qzapi):
    def __init__(self, db_path):
        self.db_connect = sqlite3.connect(db_path)
        self.jw_connect = super(Work, self).__init__()
        self.db_cursor = self.db_connect.cursor()

    def get_token(self):
        self.db_cursor.execute("SELECT token FROM jwxt_token WHERE id='1'")
        query_set = self.db_cursor.fetchone()
        if query_set is None:
            token = super(Work, self).get_token()
            self.db_cursor.execute(
                "INSERT INTO jwxt_token VALUES(1, '%s')" % token
            )
            self.db_connect.commit()
            return token
        # 数据库里有可用的 token
        elif query_set is not None and self.is_valid(query_set[0]):
            token = query_set[0]
            return token
        # 数据库中的 token 不可用
        else:
            token = super(Work, self).get_token()
            self.db_cursor.execute(
                "UPDATE jwxt_token SET token = '%s' WHERE id = 1" % token
            )
            return token

    def get_sql_kcmc_list(self):
        sql_kcmc_list = []
        temp = self.db_cursor.execute(
            "SELECT kcmc FROM jwxt_result"
        )
        for v in temp:
            sql_kcmc_list.append(v[0])
        return sql_kcmc_list

    def server_chan(self, text, inform_list):
        desp = ''
        for v in inform_list:
            desp += '***\n### ' + v['kcmc'] + '\n#### 总成绩' + v['zcj'] + '\n***'
        params = {
            'text': text,
            'desp': desp
        }
        requests.get(
            ServerChan_URL,
            headers=self.headers,
            params=params
        )

    def start(self):
        inform_list = []
        self.headers['token'] = self.get_token()
        api_result_list = self.getCjcx()
        sql_kcmc_list = self.get_sql_kcmc_list()
        for v in api_result_list:
            if not v['kcmc'] in sql_kcmc_list:
                inform_list.append({
                    'kcmc': v['kcmc'],
                    'zcj': v['zcj']
                })
                self.db_cursor.execute(
                    "INSERT INTO jwxt_result VALUES('%s', '%s')" % (
                        v['kcmc'], v['zcj'])
                )
        self.db_connect.commit()
        if len(inform_list) > 0:
            self.server_chan('成绩更新', inform_list)


if __name__ == "__main__":
    abs_path = os.getcwd() + '/'
    work = Work(abs_path + 'QZJW.db')
    work.start()
