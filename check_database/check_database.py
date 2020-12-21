import subprocess
oracle_home = 'D:/app/Administrator/product/11.2.0/dbhome_1'
user_name = 'xxxx'
user_passwd = 'xxxx'
user_tns = '127.0.0.1:1521/orcl'
user_sqlplus = oracle_home + '/bin' + '/' + 'sqlplus'
default_shell = user_sqlplus + ' / as sysdba'
user_shell = user_sqlplus + ' ' + user_name + '/' + user_passwd + '@' + user_tns


def check_database(shell_input):
    try:
        p = subprocess.Popen(shell_input, stdin=subprocess.PIPE, shell=True)
        p.stdin.write('@check_database.sql'.encode('utf-8'))
        subprocess.Popen.communicate(p)
        print('1')
        return True
    except Exception as e:
        print('2')
        print(str(e))
        return False


if check_database(default_shell):
    print("succeed")
else:
    print("error")
