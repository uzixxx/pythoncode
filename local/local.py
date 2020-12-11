import time
import pandas as pd
import cx_Oracle


def performance(unit):
    def perf_decorator(f):
        def wrapper(*args, **kw):
            t1 = time.time()
            r = f(*args, **kw)
            t2 = time.time()
            t = (t2 - t1) * 1000 if unit=='ms' else (t2 - t1)
            print('call %s() in %f %s' % (f.__name__, t, unit))
            return r
        return wrapper
    return perf_decorator


def log(prefix):
    def log_decorator(f):
        def wrapper(*args, **kw):
            print('[%s] %s()...' % (prefix, f.__name__))
            return f(*args, **kw)
        return wrapper
    return log_decorator


# 实现查询并返回dataframe
@log('DEBUG')
def query(sql):
    
    host = "localhost"  # 数据库ip
    port = "1521"   # 端口
    sid = "orcl"  # 数据库名称
    dsn = cx_Oracle.makedsn(host, port, sid)
    
    # scott是数据用户名，tiger是登录密码（默认用户名和密码）
    conn = cx_Oracle.connect("bmi", "bmi", dsn)  

    # 使用pandas的read_sql函数，可以直接将数据存放在dataframe中
    results = pd.read_sql(sql, conn)

    conn.close()
    return results


@log('DEBUG')
def r_sql(name, st, et):
    
    # sql文件夹路径
    sql_path = ''
 
    # sql文件名， .sql后缀的
    sql_file = name

    # 读取 sql 文件文本内容
    sql = open(sql_path + sql_file, 'r', encoding='utf-8')
    # 此时 sqltxt 为 list 类型
    sqltxt = sql.readlines()
    # sqltxt = sql.read()
    
    # 读取之后关闭文件
    sql.close()
    
    # list 转 str
    sql = "".join(sqltxt)

    sql_new = sql.replace('&begin_mon', "'"+st+"'").replace('&end_mon', "'"+et+"'")
    
    return sql_new

# print(r_sql('local.sql','20180101','20190101'))


cmd = input('请输入指令：')
if cmd == '1':
    st = input('请输入开始时间：')
    et = input('请输入结束时间：')
    sql = r_sql('local.sql', st, et)
    # print(sql)
    results = query(sql)
    results.to_csv('单据.csv', index=False, header=True,encoding="gbk")
else:
    pass


