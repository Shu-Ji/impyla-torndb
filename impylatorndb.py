# coding: u8

import logging

from impala.dbapi import connect


class Row(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, key, value):
        self[key] = value


class Connection(object):

    def __init__(self,
            host='localhost', port=10000, auth_mechanism="PLAIN",
            zookeeper_address_str=None, **kwargs):

        # zookeeper_address_str = 'zk1.example.com:2181,zk2.example.com:2182'
        self.connection_params = Row(**kwargs)
        self.connection_params.host = host
        self.connection_params.port = port
        self.connection_params.auth_mechanism = auth_mechanism

        self.zookeeper_address_str = zookeeper_address_str

        self.conn = None

    def reconnect(self):
        kwargs = self.connection_params

        if self.zookeeper_address_str:
            kwargs.host, kwargs.port = self.get_hs2_server_address()

        self.close(self.conn)
        self.conn = connect(**kwargs)

    def get(self, sql, sets=None):
        """
        sets can be list:

        sets = [
            'SET mapred.job.name = myjobname',
            'set mapreduce.job.queuename=root.offline.myhadoop.queue',
        ]

        or string:

        sets = 'SET mapred.job.name = myjobname'
        """

        rows = self.query(sql, sets)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for get() query")
        else:
            return rows[0]

    def iter(self, sql, sets=None):
        cursor = self.set_hiveconf_and_get_cursor(sets)
        self._execute(cursor, sql)
        column_names = [i[0] for i in cursor.description]

        for row in cursor:
            yield Row(zip(column_names, row))

        self.close(cursor)

    def query(self, sql, sets=None):
        return list(self.iter(sql, sets))

    def execute(self, sql, sets=None):
        cursor = self.set_hiveconf_and_get_cursor(sets)
        self._execute(cursor, sql)
        self.close(cursor)

    def _execute(self, cursor, sql):
        try:
            return cursor.execute(sql)
        except Exception as e:
            self.close(self.conn)
            logging.error(sql)
            raise(e)

    def set_hiveconf_and_get_cursor(self, sets=None):
        self.reconnect()

        sets = sets or []
        if not isinstance(sets, list):
            sets = [sets]

        cursor = self.conn.cursor()
        for set_statement in sets:
            self._execute(cursor, set_statement)
        return cursor

    def close(self, what):
        try:
            what.close()
        except:
            pass

    def __del__(self):
        self.close(self.conn)

    def get_hs2_server_address(self):
        import random
        from kazoo.client import KazooClient

        logging.basicConfig()
        zk = KazooClient(hosts=self.zookeeper_address_str, read_only=True)
        zk.start()

        address = random.choice(zk.get_children('/hiveserver2'))
        host, port = address.split(';')[0].split('=')[-1].split(':')
        return host, int(port)
