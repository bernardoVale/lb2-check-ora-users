--BY USER
select count(*),username
from v$session
  where username not in ('SYS','SYSTEM')
  group by username;

--TOTAL
select count(*)
from v$session
  where username not in ('SYS','SYSTEM');

select NULLIF(COUNT(*),0),username
from v$session
  where username in ('LB2APP')
  group by username;

select decode(COUNT(*),1,0,count(*)),username from
  dba_users left outer join v$session using (username)
  where username in ('APPQOSSYS','HELPDESK')
group by username;

set head off
set feedback off
set pagesize 999
set long 999
select decode(COUNT(*),1,0,count(*)),username from
  dba_users left outer join v$session using (username)
  where username not in ('SYS','SYSTEM')
group by username;