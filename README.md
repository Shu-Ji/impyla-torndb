Forked from https://github.com/Shu-Ji/impyla-torndb.


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

    $ pipenv install git+https://github.com/Shu-Ji/impyla-torndb.git#egg=impylatorndb


If some sasl error occurs, please uninstall sasl:

    $ pipenv uninstall sasl

Then install pure-sasl:

    $ pipenv install git+https://github.com/thobbs/pure-sasl.git#egg=puresasl

Impyla will use the pure-sasl fallback.


```python
# coding: u8

from impylatorndb import Connection


user = 'myuser'
sets = [
    'SET mapred.job.name = myjobname',
    'set mapreduce.job.queuename=myqueue',
]
# sets can be None, or strings
# e.g.
# sets = 'set mapred.job.name = myjobname'

# using zk
zookeeper_address_str = 'zk1.xx.org:2181,zk2.xx.org:2181'
db = Connection(zookeeper_address_str=zookeeper_address_str, user=user)

# connect to hs2 directly
#host = '127.0.0.1'
#port = 10000
#db = Connection(host=host, port=port, user=user)


sql = 'SELECT city_id FROM mydb.mytb LIMIT 10'
db.query(sql, sets)

# or if you have not sets:
# db.query(sql)

# using iter
for row in db.iteR(sql, sets):
    print(row)
