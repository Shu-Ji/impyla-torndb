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
