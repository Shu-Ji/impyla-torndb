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
print(db.query(sql, sets))

# or if you have not sets:
# db.query(sql)

# using iter
for row in db.iter(sql, sets):
    print(row)
