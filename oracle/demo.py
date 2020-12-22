import pandas as pd
import cx_Oracle


def conn_to_oracle(username, password):
    host = "127.0.0.1"
    port = "1521"
    sid = "orcl"
    dsn = cx_Oracle.makedsn(host, port, sid)
    conn = cx_Oracle.connect(username, password, dsn)
    return conn


def read_sql(name):
    sql_path = ''
    sql_file = sql_path + name
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.readlines()
    sql = "".join(sql_content)
    # sql_new = sql.replace('&begin_mon', "'" + st + "'").replace('&end_mon', "'" + et + "'")
    return sql


def exec_sql():
    try:
        conn = conn_to_oracle('bmi', 'bmi')
        sql = read_sql('ysk.sql')
        results = pd.read_sql(sql, conn)   # 使用pandas的read_sql函数，可以直接将数据存放在dataframe中
        results.to_csv('医生库.csv', index=False, header=True, encoding="gbk")
    except cx_Oracle.DatabaseError as e:
        print(e)
    else:
        conn.close()


def exec_proc(proc_name):
    try:
        conn = conn_to_oracle('bmi', 'bmi')
        c = conn.cursor()
        c.callproc(proc_name)
    except cx_Oracle.DatabaseError as e:
        print(e)
    else:
        conn.close()


print(read_sql('dw_bill.sql'))
