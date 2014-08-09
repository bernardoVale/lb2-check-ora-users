import unittest
from check_ora_users import *
__author__ = 'bernardovale'


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.schemas = 'HELPDESK,SYSTEM'

    def test_wrap_schemas(self):
        result = wrap_schemas(self.schemas)
        should_be = "'HELPDESK','SYSTEM'"
        self.assertEqual(result,should_be)
        single = wrap_schemas('HELPDESK')
        should_be = "'HELPDESK'"
        self.assertEqual(single,should_be)

    def test_conn(self):
        user = 'sys'
        pwd = 'oracle'
        sid = 'lb2app'
        host = '10.200.0.213'
        mustByConnection = estabConnection(user,pwd,sid,host,True)
        self.assertIsInstance(mustByConnection,cx_Oracle.Connection)
        user = 'system'
        mustByConnection = estabConnection(user,pwd,sid,host,False)
        self.assertIsInstance(mustByConnection,cx_Oracle.Connection)

    def test_get_my_query(self):
        query = get_my_query('SYSTEM')
        should_be = "set head off \n \
                select count(*),username \
             from v$session \
              where username in ('SYSTEM')\
             group by username;"
        self.assertEqual(query,should_be)
        query = get_my_query('SYSTEM,LB2APP')
        should_be = "set head off \n \
                select count(*),username \
             from v$session \
              where username in ('SYSTEM','LB2APP')\
             group by username;"
        self.assertEqual(query,should_be)
        query = get_my_query(None)
        self.assertNotEqual(query,should_be)

    def test_sqlplus(self):
        user = 'sys'
        pwd = 'oracle'
        sid = 'helpdesk'
        query = "set head off \n \
                select count(*),username \
             from v$session \
              where username in ('HELPDESK','SYSTEM')\
             group by username;"
        for lol in run_sqlplus(pwd,user,sid,query,True,True).strip().split(' '):
            print lol