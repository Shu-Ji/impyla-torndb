Used like [torndb](https://github.com/bdarnell/torndb) .


zookeeper of hs2 is supported by default.

This project provides three methods: `db.query`, `db.get`, `db.execute`.

`db.query` and `db.get` are used like torndb.

Only `db.execute` will return None, while `torndb.execute` returns lastrowid.


Please read the source code, it's very simple.


支持以 zk 的方式连接 hs2。

封装一下 impyla，让其使用起来和 torndb 一样简单好用。

提供 db.query、db.get、db.execute 三个方法，用法和 torndb 完全一样。

query 和 get 返回值数据类型也完全一样; 惟一不同的是 execute 方法，torndb 中会返回 lastrowid，本文中返回 None

请仔细阅读源码，了解使用方法，不用担心，源码不到 100 行。


### Install

    $ pipenv install

If you CAN NOT use the sasl C lib, you can use the pure-sasl python lib,

else please install sasl by yourself.

    $ pipenv install sasl


And if some sasl error occurs, please uninstall sasl:

    $ pipenv uninstall sasl

Impyla will use the pure-sasl fallback.


### 安装说明

由于在我们的服务器上面安装 sasl 之后，不明原因，无法使用。

所以使用了纯 python 实现的 pure-sasl 库。

通过  pipenv install 之后，即会自动安装该库，但是，同时会安装 sasl 库。

而 sasl 库用不了，所以安装完成之后手动卸载掉即可:

pipenv uninstall sasl


如果有 sasl，impyla 会使用他，如果他找不到 sasl，就会使用 pure-sasl，所以我们要卸载。


```python
# coding: u8

from tornhivedb import Connection


user = 'myuser'
sets = [
    'SET mapred.job.name = myjobname',
    'set mapreduce.job.queuename=myqueue',
]
# sets can be None, or strings
# e.g.
# sets = 'set mapred.job.name = myjobname'

# using zk
zookeeper_hosts_str = 'zk1.xx.org:2181,zk2.xx.org:2181'
db = Connection(zookeeper_hosts_str=zookeeper_hosts_str, user=user)

# connect to hs2 directly
#host = '127.0.0.1'
#port = 10000
#db = Connection(host=host, port=port, user=user)


sql = 'SELECT city_id FROM mydb.mytb LIMIT 10'
db.query(sql, sets)

# or if you have not sets:
# db.query(sql)
```
