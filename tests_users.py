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
        sid = 'oradb'
        host = '10.200.0.204'
        mustByConnection = estabConnection(user,pwd,sid,host,True)
        self.assertIsInstance(mustByConnection,cx_Oracle.Connection)
        user = 'system'
        mustByConnection = estabConnection(user,pwd,sid,host,False)
        self.assertIsInstance(mustByConnection,cx_Oracle.Connection)

    def test_get_my_query(self):
        query = get_my_query('SYSTEM',False)
        should_be = "set head off \n \
                set feedback off \n \
                set pagesize 999 \n \
                set long 999 \n \
                select decode(COUNT(*),1,0,count(*)),username from \
             dba_users left outer join v$session using (username) \
              where username in ('SYSTEM')\
             group by username;"
        self.assertEqual(should_be,query)
        query = get_my_query('SYSTEM,LB2APP',False)
        should_be = "set head off \n \
                set feedback off \n \
                set pagesize 999 \n \
                set long 999 \n \
                select decode(COUNT(*),1,0,count(*)),username from \
             dba_users left outer join v$session using (username) \
              where username in ('SYSTEM','LB2APP')\
             group by username;"
        self.assertEqual(should_be,query)
        query = get_my_query(None,False)
        self.assertNotEqual(query,should_be)
        should_be = "set head off \n \
                set feedback off \n \
                set pagesize 999 \n \
                set long 999 \n \
               select count(*) from \
             dba_users inner join v$session using (username) \
              where username not in ('MGMT_VIEW','SYS','SYSTEM','DBSNMP','SYSMAN','OUTLN','FLOWS_FILES'\
,'MDSYS','WMSYS','APPQOSSYS','FLOWS_030000','APEX_030200','APEX_040200','APEX_050200','OWBSYS_AUDIT'\
,'OWBSYS','ORDDATA','ANONYMOUS','EXFSYS','XDB','ORDSYS','CTXSYS','ORDPLUGINS','OLAPSYS'\
,'SI_INFORMTN_SCHEMA','SCOTT','XS$NULL','MDDATA','ORACLE_OCM'\
,'DIP','APEX_PUBLIC_USER','SPATIAL_CSW_ADMIN_USR','SPATIAL_WFS_ADMIN_USR');"
        query = get_my_query(None,True)
        self.assertEqual(should_be,query)

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