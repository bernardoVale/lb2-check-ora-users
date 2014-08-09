**Check Oracle Users**
Counts users sessions.

**Usage:**

```
    ./check_ora_users --sid orateste --user sys --pwd mypasswd --warning 50 --schemas MYSCHEMA1,MYSHEMA2 
```

**HELP**:

    usage: check_ora_users [-h] --sid SID --user USER --pwd PWD --warning WARNING
                       [--schemas SCHEMAS]
    
    optional arguments:
      -h, --help         show this help message and exit
      --sid SID          SID do banco de produção. Checar tnsnames.ora!
      --user USER        Usuário do banco: sys,system etc..
      --pwd PWD          Senha do usuário especificado!
      --warning WARNING  Quantidade de usuarios para alertar WARNING.
      --schemas SCHEMAS  Lista de usuários que devem ser analisados.
                         Caso não exista irá contabilizar todos.Com exceção dos usuários do sistema. SYS,SYSTEM, etc..
