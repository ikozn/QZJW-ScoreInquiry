# QZJW-ScoreInquiry
使用强智教务系统APP API 获取成绩，通过 ServerChan 增量推送到微信

## 运行流程
### 获取 / 更新 / 插入 token
* 运行时，优先从数据库中查询 token，并通过Qzapi.is_valid 方法进行有效性核验。
* 如果 token 无效，通过 Qzapi.get_token 方法重新获取 token，并同步更新数据库中的 token。
* 如果数据库中没有 token（query_set 返回 None），通过 Qzapi.get_token 方法获取 token，并插入到数据库中

## 使用方法
### 运行 Models.py 创建并初始化数据库结构
运行 ``Models.py``，将创建出一个名为 ``QZJW.db`` 的 Sqlite3 数据文件。并创建两个表，详细信息如下:
* jwxt_result （存储从教务系统中获取到的成绩信息）
    - kcmc TEXT NOT NULL （课程名称）
    - zcj REAL NOT NULL (总成绩)
* jwxt_token (存储从教务系统获取到的 token)
    - id INT PRIMARY KEY NOT NULL
    - token TEXT NOT NULL

### 在 Settings.py 中写入关键信息
#### url
将 ``http://jwxt.xxxxx.edu.cn/`` 替换为学校的强智教务系统域名，最后的 ``app.do`` 为 APP API模块，不可变更。
#### account、password
登录教务系统的账号和密码
#### SCKEY
Server 酱推送消息的 token。在 [Server 酱官网](https://sc.ftqq.com) 授权使用 github 登录即可得到.
#### ServerChan_URL
结合 ``SCKEY`` 拼接得出的消息推送接口地址

### 运行
`````python
    # 获取绝对路径
    abs_path = os.getcwd() + '/'
    # 初始化一个示例并传入数据文件的路径
    work = Work(abs_path + 'QZJW.db')
    work.start()
`````
设置一个定时任务执行 ``work.py``，在获取到数据库中没有的成绩信息时，就会推送至微信。



  