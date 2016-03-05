import mysql.connector, functools, threading, logging

class Dict(dict):
    '''
    Simple dict but support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    >>> d3 = Dict(('a', 'b', 'c'), (1, 2, 3))
    >>> d3.a
    1
    >>> d3.b
    2
    >>> d3.c
    3
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value
#engine = None
#_db_ctx = _DbCtx()
#
#class _Engine(object):
#    def __init__(self, connect):
#        self._connect = connect
#    def connect(self):
#        return self._connect()
#
#class _DbCtx(threading.local):
#    def __init__(self):
#        self.connection = None
#        self.transactions = 0
#    def is_init(self):
#        return not self.connection is None
#    def init(self):
#        self.connec

_connector = None

def create_connector(user, passwd, database, host='127.0.0.1', port = 3306, **kw):
    global _connector
    params = dict(user = user, passwd = passwd, database = database, host = host, port = port)
    defaults = dict(use_unicode = True, charset = 'utf8', collation = 'utf8_general_ci', autocommit = False)
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
    params.update(kw)
    params['buffered'] = True
    _connector =  lambda: mysql.connector.connect(**params) 

def update(sql, *params):
    conn = _connector()  
    cursor = conn.cursor()
    cursor.execute(sql, params)
    print cursor.fetchall()
    cursor.close()
    conn.close()

def _select(sql, *params):
    pass

#@with_connection
def select_one(sql, *params):
    conn = _connector()  
    cursor = conn.cursor()
    cursor.execute(sql, params)
    cols = [seq[0] for seq in cursor.description]
    values = cursor.fetchone() 
    cursor.close()
    conn.close()
    if not values:
        return values 
    else:
        return Dict(cols, values)

def insert(table, **kw):
    cols, values = zip(*kw.iteritems())
    sql = 'insert into `%s` (%s) values (%s)' % (table, ','.join(['`%s`' % col for col in cols]), ','.join(['%s' for i in range(len(cols))])) 
    print sql, values
    conn = _connector()  
    cursor = conn.cursor()
    cursor.execute(sql, values)
    cursor.close()
    conn.close()
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    create_connector('www-data', 'www-data', 'test')
    update("select * from user") 
    print select_one("select * from user where id = 101")
    print select_one("select * from user where id = 1101")
