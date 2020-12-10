import tkinter as tk
import tkinter.messagebox
import pandas as pd
import cx_Oracle
import datetime
import re

def keyPress1(e):
    entry1.delete(0,len(entry1.get()))
    #print('entry1')
def keyPress2(e):
    entry2.delete(0,len(entry2.get()))
    #print('entry2')

def checkV():
    if v.get()<4:
        entry1.delete(0,len(entry1.get()))
        entry1.insert(0,'yyyymm')
        entry2.delete(0,len(entry2.get()))
        entry2.insert(0,'yyyymm')
    elif v.get()==4:
        entry1.delete(0,len(entry1.get()))
        entry1.insert(0,'yyyy-mm-dd')
        entry2.delete(0,len(entry2.get()))
        entry2.insert(0,'yyyy-mm-dd')
    else:
        entry1.delete(0,len(entry1.get()))
        entry1.insert(0,'yyyymmdd')
        entry2.delete(0,len(entry2.get()))
        entry2.insert(0,'yyyymmdd')
  
def excute1(st, et):

    host = "10.1.1.200"  #数据库ip
    port = "1521"  #端口
    sid = "drgs"  #数据库名称
    dsn = cx_Oracle.makedsn(host, port, sid)

    #   scott是数据用户名，tiger是登录密码（默认用户名和密码）
    try:
        conn = cx_Oracle.connect("drgs_fund_his", "drgs_fund_his", dsn)

        #    SQL语句，可以定制，实现灵活查询
        sql = (
            "select a.合计,case a.yq when '0' then '全院' when '1' then '总院' else '十梓' end 院区，"
            + "a.科室,a.统筹区,a.医疗总费用,a.总病例数,a.平均费用,a.正常分组病例数,a.高倍率病例数," +
            "a.低倍率病例数,a.拨付点数,a.拨付金额,a.拨付差额,a.预算金额,a.预算超额,a.超额比例" + " from(" +
            "select '合计' 合计," + "'0' yq," + "ksbq.dept_name 科室," +
            "dzr.region_name 统筹区," + "round(sum(bwm.total_amount),2) 医疗总费用," +
            "sum(sfm.total_medical_count) 总病例数," +
            "round(sum(bwm.total_amount) / sum(sfm.total_medical_count), 2) 平均费用,"
            + "sum(sfm.gp_count) 正常分组病例数," + "sum(sfm.high_rate_count) 高倍率病例数," +
            "sum(sfm.low_rate_count) 低倍率病例数," +
            "round(sum(sfm.score_value),2) 拨付点数," +
            "round(sum(sfm.allot_money),2) 拨付金额," +
            "round(sum(sfm.allot_differ_money),2) 拨付差额," +
            "round(sum(bwm.budget_money),2) 预算金额," +
            "round(sum(bwm.total_amount)-sum(bwm.budget_money),2) 预算超额," +
            "round((sum(bwm.total_amount)-sum(bwm.budget_money))/sum(bwm.budget_money)*100,2)||'%' 超额比例"
            + "  from budget_ward_month bwm" +
            "  join budget_dept_month bdm on bwm.f_dept_id = bdm.id" +
            "  join budget_month bm on bwm.f_id = bm.id " +
            "  join ksbq_yb ksbq on bwm.ward_code = ksbq.ward_code " +
            "  join dw_zd_region dzr on bm.bmi_code = dzr.region_id" +
            "  left join Sta_Finance_Month sfm on bwm.ward_code = sfm.ward_code and bm.year_month = sfm.year_month and bm.bmi_code = sfm.bmi_code"
            + "  where 1 = 1 and bwm.budget_money > 0" +
            "   and bm.year_month >=  '" + st + "'   and bm.year_month <=  '" +
            et + "'   and bm.bmi_code IN" +
            "   ('320506', '320507', '320509', '32058401', '32058402', '320599')" +
            "  group by ksbq.dept_name,dzr.region_id,dzr.region_name" +
            "  union all " + "select '' 合计," + "ksbq.yq yq," +
            "ksbq.dept_name 科室," + "dzr.region_name 统筹区," +
            "round(sum(bwm.total_amount),2) 医疗总费用," +
            "sum(sfm.total_medical_count) 总病例数," +
            "round(sum(bwm.total_amount) / sum(sfm.total_medical_count), 2) 平均费用,"
            + "sum(sfm.gp_count) 正常分组病例数," + "sum(sfm.high_rate_count) 高倍率病例数," +
            "sum(sfm.low_rate_count) 低倍率病例数," +
            "round(sum(sfm.score_value),2) 拨付点数," +
            "round(sum(sfm.allot_money),2) 拨付金额," +
            "round(sum(sfm.allot_differ_money),2) 拨付差额," +
            "round(sum(bwm.budget_money),2) 预算金额," +
            "round(sum(bwm.total_amount)-sum(bwm.budget_money),2) 预算超额," +
            "round((sum(bwm.total_amount)-sum(bwm.budget_money))/sum(bwm.budget_money)*100,2)||'%' 超额比例"
            + "  from budget_ward_month bwm" +
            "  join budget_dept_month bdm on bwm.f_dept_id = bdm.id" +
            "  join budget_month bm on bwm.f_id = bm.id " +
            "  join ksbq_yb ksbq on bwm.ward_code = ksbq.ward_code " +
            "  join dw_zd_region dzr on bm.bmi_code = dzr.region_id" +
            "  left join Sta_Finance_Month sfm on bwm.ward_code = sfm.ward_code and bm.year_month = sfm.year_month and bm.bmi_code = sfm.bmi_code"
            + "  where 1 = 1 and bwm.budget_money > 0" +
            "   and bm.year_month >= '" + st + "'   and bm.year_month <= '" + et +
            "'   and bm.bmi_code IN" +
            "   ('320506', '320507', '320509', '32058401', '32058402', '320599')" +
            "   group by ksbq.yq,ksbq.dept_name,dzr.region_id,dzr.region_name) a" +
            "   order by a.科室,a.统筹区,a.yq")
        #  使用pandas 的read_sql函数，可以直接将数据存放在dataframe中
        results = pd.read_sql(sql, conn)
        dateStr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        results.to_csv('月度科室财务报表'+dateStr+'.csv', index=False, header=True,encoding="gbk")
        conn.close()
    except cx_Oracle.DatabaseError as msg:
        conn.close
        print(msg)
        

def excute2(st, et):
    host = "10.1.1.200"  #数据库ip
    port = "1521"  #端口
    sid = "drgs"  #数据库名称
    dsn = cx_Oracle.makedsn(host, port, sid)

    # scott是数据用户名，tiger是登录密码（默认用户名和密码）
    conn = cx_Oracle.connect("cisda", "cisda", dsn)

    #SQL语句，可以定制，实现灵活查询

    c = conn.cursor()
    V_SQLCODE = ' '
    V_SQLERR = ' '
    try:
        c.callproc('prc_depart_month_ybyq', [st, et, V_SQLCODE, V_SQLERR])

        #     使用pandas 的read_sql函数，可以直接将数据存放在dataframe中
        sql = "select name 科室名称,CALENDAR_ID 月份,CASE_COUNT 例数,CMI,WEIGHT 权重,DRG_GROUPS 分组,DAY_EFF 时间消耗指数,COST_EFF 费用消费指数,SYNTHESIS_SCORE 综合得分 from ZHFX_SJWDFX"
        results = pd.read_sql(sql, conn)
    except:
        print('请确认输入数据格式是否有问题')
        pass
    conn.close()
    #   file2=open('时间维度综合分析.csv','w')
    dateStr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    results.to_csv('时间维度综合分析(科室)'+dateStr+'.csv', index=False, header=True,encoding="gbk")

def excute3(st, et):
    host = "10.1.1.200"  #数据库ip
    port = "1521"  #端口
    sid = "drgs"  #数据库名称
    dsn = cx_Oracle.makedsn(host, port, sid)
    
    # scott是数据用户名，tiger是登录密码（默认用户名和密码）
    conn = cx_Oracle.connect("cisda", "cisda", dsn)
    
        #SQL语句，可以定制，实现灵活查询
    
    c = conn.cursor()
    V_SQLCODE = ' '
    V_SQLERR = ' '
    try:
        c.callproc('PRC_WORD_MONTH_YBYQ', [st, et, V_SQLCODE, V_SQLERR])
        #     使用pandas 的read_sql函数，可以直接将数据存放在dataframe中
        sql = "select dept_name 科室,name 病区,CALENDAR_ID 月份,CASE_COUNT 例数,CMI,WEIGHT 权重,DRG_GROUPS 分组,DAY_EFF 时间消耗指数,COST_EFF 费用消费指数,SYNTHESIS_SCORE 综合得分 from ZHFX_SJWDFX_BQ"
        results = pd.read_sql(sql, conn)
    
    except:
        print('请确认输入数据格式是否有问题')
        pass
    conn.close()
    #   file2=open('时间维度综合分析.csv','w')
    dateStr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    results.to_csv('时间维度综合分析(病区)'+dateStr+'.csv', index=False, header=True,encoding="gbk")

def excute4(st, et):
    host = "10.1.1.200"  #数据库ip
    port = "1521"  #端口
    sid = "drgs"  #数据库名称
    dsn = cx_Oracle.makedsn(host, port, sid)
        
            # scott是数据用户名，tiger是登录密码（默认用户名和密码）
    conn = cx_Oracle.connect("cisda", "cisda", dsn)
        
            #SQL语句，可以定制，实现灵活查询
        
    c = conn.cursor()
    V_SQLCODE = ' '
    V_SQLERR = ' '
    try:
        c.callproc('prc_word_zbfx_ybyq', [st, et, V_SQLCODE, V_SQLERR])

        #     使用pandas 的read_sql函数，可以直接将数据存放在dataframe中
        sql =( "select b.dept_name 科室名称,a.name 病区名称,a.CASE_COUNT 例数,a.CMI,WEIGHT 权重,"+
          "a.DRG_GROUPS 分组,a.DAY_EFF 时间消耗指数,a.COST_EFF 费用消费指数,a.SYNTHESIS_SCORE 综合得分"+ 
          " from ZHFX_ZBFX_BQ a "+
          " left join zjk.drgs_zd_bq b on a.dept_code= b.dept_code and a.code=b.ward_code "+
          " order by b.dept_name,a.SYNTHESIS_SCORE desc")
        results = pd.read_sql(sql, conn)
    except:
        print('请确认输入数据格式是否有问题')
        pass   
    conn.close()
    #   file2=open('时间维度综合分析.csv','w')
    dateStr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    results.to_csv('综合分析指标(病区)'+dateStr+'.csv', index=False, header=True,encoding="gbk")

def excute5(st, et):
    host = "10.1.1.200"  #数据库ip
    port = "1521"  #端口
    sid = "drgs"  #数据库名称
    dsn = cx_Oracle.makedsn(host, port, sid)
        
            # scott是数据用户名，tiger是登录密码（默认用户名和密码）
    conn = cx_Oracle.connect("cisda", "cisda", dsn)
        
            #SQL语句，可以定制，实现灵活查询
        
    c = conn.cursor()
    V_SQLCODE = ' '
    V_SQLERR = ' '
    try:
        c.callproc('PRC_ZRYS_MONTH_YBYQ', [st, et, V_SQLCODE, V_SQLERR])

        #     使用pandas 的read_sql函数，可以直接将数据存放在dataframe中
        sql =( "select b.ksmc 科室名称,a.name 医师,a.CASE_COUNT 例数,a.CMI,WEIGHT 权重,"+
          "a.DRG_GROUPS 分组,a.DAY_EFF 时间消耗指数,a.COST_EFF 费用消费指数,a.SYNTHESIS_SCORE 综合得分"+ 
          " from ZHFX_ZBFX_YS a "+
          " left join zjk.drgs_zd_ks b on a.dept_code= b.bm "+
          " order by b.ksmc,a.SYNTHESIS_SCORE desc")
        results = pd.read_sql(sql, conn)
    except:
        print('请确认输入数据格式是否有问题')
        pass        
    conn.close()
    #   file2=open('时间维度综合分析.csv','w')
    dateStr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    results.to_csv('综合分析指标(医师)'+dateStr+'.csv', index=False, header=True,encoding="gbk")

def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime.datetime(int(year_s), int(mon_s), int(day_s))  

def clickFun():
    value = v.get()
    st = entry1.get()
    et = entry2.get()
    #print(value,st,et)
    if value ==0:
        tkinter.messagebox.showwarning(title='warning', message='请选择要导出的文件')    # 提示信息对话窗
    elif value==1:
        if len(st)!=6 or len(et)!=6 or not re.match('[2][0-9]{3}[0-1][0-9]',st) or not re.match('[2][0-9]{3}[0-1][0-9]',et):
            tkinter.messagebox.showwarning(title='warning', message='时间格式不符合')    # 提示信息对话窗
        else:
            excute1(st,et)
    elif value==2:
        if len(st)!=6 or len(et)!=6 or not re.match('[2][0-9]{3}[0-1][0-9]',st) or not re.match('[2][0-9]{3}[0-1][0-9]',et):
            tkinter.messagebox.showwarning(title='warning', message='时间格式不符合')    # 提示信息对话窗
        else:
            excute2(st,et)
    elif value==3:
        if len(st)!=6 or len(et)!=6 or not re.match('[2][0-9]{3}[0-1][0-9]',st) or not re.match('[2][0-9]{3}[0-1][0-9]',et):
            tkinter.messagebox.showwarning(title='warning', message='时间格式不符合')    # 提示信息对话窗
        else:
            excute3(st,et)
    elif value==4:
        if len(st)!=10 or len(et)!=10 or not re.match('[2][0-9]{3}[-][0-1][0-9][-][0-3][0-9]',st) or not re.match('[2][0-9]{3}[-][0-1][0-9][-][0-3][0-9]',et):
            tkinter.messagebox.showwarning(title='warning', message='时间格式不符合')    # 提示信息对话窗
        else:
            st=parse_ymd(st)
            et=parse_ymd(et)
            excute4(st,et)
    elif value==5:
        if len(st)!=8 or len(et)!=8 or not re.match('[2][0-9]{3}[0-1][0-9][0-3][0-9]',st) or not re.match('[2][0-9]{3}[0-1][0-9][0-3][0-9]',et):
            tkinter.messagebox.showwarning(title='warning', message='时间格式不符合')    # 提示信息对话窗
        else:
            excute5(st,et)
    else:
        pass

root = tk.Tk()
root.title("医保小工具")
root.geometry('500x300')
root.resizable(0,0)

group = tk.LabelFrame(root,text='选择要导出的文件：',padx=5,pady=5)
group.pack(side='left',fill='both',expand='1',padx=10,pady=10)

LANGS = [
    ('月度科室财务报表',1),
    ('时间维度综合分析(科室)',2),
    ('时间维度综合分析(病区)',3),
    ('综合分析指标(病区)',4),
    ('综合分析指标(医师)',5)]
v = tk.IntVar()
#v.set(1)
for lang,num in LANGS:
    b = tk.Radiobutton(group,text=lang,variable=v,value=num,command=checkV)
    b.pack(anchor='w')

var1 = tk.StringVar()
label1 = tk.Label(text="开始时间：", width=20, height=2)
label1.pack()
entry1 = tk.Entry(width=20)
entry1.bind('<Button-1>',keyPress1)
entry1.pack(padx=10)

var2 = tk.StringVar()
label2 = tk.Label(text="结束时间：", width=20, height=2)
label2.pack()
entry2 = tk.Entry(width=20)
entry2.bind('<Button-1>',keyPress2)
entry2.pack(padx=10)

button1 = tk.Button(text="导出" ,width=10, height=2, command=clickFun)
button1.pack(side='bottom',padx=10,pady=10)

root.mainloop()