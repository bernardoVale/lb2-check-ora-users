#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import re
import sys
import cx_Oracle

__author__ = 'Bernardo Vale'
__copyright__ = 'LB2 Consultoria'
import argparse

def parse_args():
    """
    Método de analise dos argumentos do software.
    Qualquer novo argumento deve ser configurado aqui
    :return: Resultado da analise, contendo todas as variáveis resultantes
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--sid', required=True, action='store',
                        dest='sid',
                        help='SID do banco de produção. Checar tnsnames.ora!')
    parser.add_argument('--user', required=True, action='store',
                        dest='user',
                        help='Usuário do banco: sys,system etc..')
    parser.add_argument('--pwd', required=True, action='store',
                        dest='pwd',
                        help='Senha do usuário especificado!')
    parser.add_argument('--warning', required=True, action='store',
                        dest='warning',
                        help='Quantidade de usuarios para alertar WARNING.')

    parser.add_argument('--schemas', action='store',
                        dest='schemas',
                        help='Lista de usuários que devem ser analisados. \n'
                             'Caso não exista irá contabilizar todos.'
                             'Com exceção dos usuários do sistema. SYS,SYSTEM, etc..')
    p = parser.parse_args()
    return p

def wrap_schemas(schemas):
    """
    Pega a lista de usuarios e coloca no padrão SQL
    :param schemas: Lista de usuarios
    :return:
    """
    aux = ''
    for schema in schemas.split(','):
        aux += "'" + schema + "',"
    k = aux.rfind(",")
    return ''.join((aux[:k]+""))

def get_my_query(schemas):
    """
    Retorna a query necessária para cada tipo de entrada
    Caso None deve adicionar somente os usuários do sistema
    :param schemas: Schemas a serem contados
    :return:
    """
    not_this_schemas = "'MGMT_VIEW','SYS','SYSTEM','DBSNMP','SYSMAN','OUTLN','FLOWS_FILES'\
,'MDSYS','WMSYS','APPQOSSYS','FLOWS_030000','APEX_030200','APEX_040200','APEX_050200','OWBSYS_AUDIT'\
,'OWBSYS','ORDDATA','ANONYMOUS','EXFSYS','XDB','ORDSYS','CTXSYS','ORDPLUGINS','OLAPSYS'\
,'SI_INFORMTN_SCHEMA','SCOTT','XS$NULL','MDDATA','ORACLE_OCM'\
,'DIP','APEX_PUBLIC_USER','SPATIAL_CSW_ADMIN_USR','SPATIAL_WFS_ADMIN_USR'"
    if schemas != None:
        return "set head off \n \
                set feedback off \n \
                set pagesize 999 \n \
                set long 999 \n \
                select decode(COUNT(*),1,0,count(*)),username from \
             dba_users left outer join v$session using (username) \
              where username in ("+wrap_schemas(schemas)+")\
             group by username;"
    else:
        return "set head off \n \
                set feedback off \n \
                set pagesize 999 \n \
                set long 999 \n \
               select decode(COUNT(*),1,0,count(*)),username from \
             dba_users left outer join v$session using (username) \
              where username not in ("+not_this_schemas+")\
             group by username;"
def main():
    args = parse_args()
    query = get_my_query(args.schemas)
    result = ''
    if args.user.lower() == 'sys':
        result = run_sqlplus(args.pwd, args.user, args.sid, query, True, True)
    else:
        result = run_sqlplus(args.pwd, args.user, args.sid, query, True, False)
    perf_data = ''
    total = 0
    if 'ORA-' in result:
        print 'Erro desconhecido ao executar a query:'+result
        sys.exit(3)
    # Replace 4/3/2 whitespaces devido ao resultado do sqlplus,
    # split '' serve para criar a minha lista com cada coluna em um elemnto
    #strip para tirar os whites antes e dps.
    r = result.strip().replace("    "," ").replace("   "," ").replace("  "," ").split(' ')
    it = iter(r)
    for count, schema in zip(it,it):
        perf_data += schema + '=' + count + ' '
        total += int(count)
    perf_data += 'TOTAL='+str(total)+';'+args.warning
    if total > int(args.warning):
        print 'WARNING - Sobrecarga no banco, Sessões:'+str(total)+' | ' +perf_data
        sys.exit(1)
    else:
        print 'Total de Sessões:' + str(total) + '| ' +perf_data
        sys.exit(0)

def run_sqlplus(pwd, user, sid, query, pretty, is_sysdba):
        """
        Executa um comando via sqlplus
        :param credencias: Credenciais de logon  E.g: system/oracle@oradb
        :param cmd: Query ou comando a ser executado
        :param pretty Indica se o usuário quer o resultado com o regexp
        :param Usuário é sysdba?
        :return: stdout do sqlplus
        """
        credencias = user +'/'+ pwd+'@'+sid
        if is_sysdba:
            credencias += ' as sysdba'
        session = subprocess.Popen(['sqlplus','-S',credencias], stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        session.stdin.write(query)
        stdout, stderr = session.communicate()
        if pretty:
            r_unwanted = re.compile("[\n\t\r]")
            stdout = r_unwanted.sub("", stdout)
        if stderr != '':
            print stdout
            print 'ERRO - Falha ao executar o comando:'+query
            sys.exit(2)
        else:
            return stdout

def estabConnection(user, pwd, sid, host, is_sysdba):
        """
        Tenta conectar no Oracle com as credenciais
        :param user: Usuário do banco
        :param senha: Senha do banco
        :param sid: service-name do banco
        :return: Uma conexão ativa com o banco
        """
        try:
            if is_sysdba:
                conn = cx_Oracle.connect(user + '/' + pwd + '@' + host + '/' +sid ,mode = cx_Oracle.SYSDBA)
            else:
                conn = cx_Oracle.connect(user + '/' + pwd + '@' + host + '/' +sid)
        except:
            print sys.exc_info()[1]
            print "Falha na conexao com a base, cheque os parametros!"
            sys.exit(2)
        return conn


if __name__ == '__main__':
    main()

