import configparser
import os
import sys

print(sys.argv[0])
print(sys.path[0])
ddir = sys.path[0]
filen = ''
if os.path.isfile(ddir):
    ddir,filen = os.path.split(ddir)
print(ddir)
print(filen)
os.chdir(ddir)
print('================================================')
print(os.getcwd()) #获取当前工作目录路径
print(os.path.abspath('.')) #获取当前工作目录路径
print(os.path.abspath('RuleSettings.txt')) #获取当前目录文件下的工作目录路径
print(os.path.abspath('..')) #获取当前工作的父目录 ！注意是父目录路径
print(os.path.abspath(os.curdir)) #获取当前工作目录路径
print(os.path.abspath("config.ini"))
print(os.path.dirname(os.path.abspath("config.ini")))
print(os.path.dirname(os.path.dirname(os.path.abspath("config.ini"))))

dir_now = os.path.dirname(os.path.abspath("testConfigIni.py"))
conf = configparser.ConfigParser()
conf.read(dir_now+'/config.ini')  # 读config.ini文件
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 使用mysql这样写就行了，是指明引擎的
        'NAME': conf.get('global', 'table'),  # 库名
        'USER': conf.get('global', 'uname'),  # 用户名
        'PASSWORD': conf.get('global', 'passwd'),  # 密码
        'HOST': conf.get('global', 'ip'),  # 数据库主机ip
        'PORT': conf.get('global', 'port'),  # 数据库端口号
    }
}