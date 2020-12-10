import configparser
import codecs

# 实例化 ConfigParser 并加载配置文件
cp = configparser.ConfigParser()
# cp.read('app.conf')
# 配置文件如果包含 Unicode 编码的数据，需要使用 codecs 模块以合适的编码打开配置文件
with codecs.open('app.conf', 'r', encoding='utf-8') as f:
    cp.read_file(f)

# 获取 section 列表、option 键列表和 option 键值元组列表 
print('all sections:', cp.sections())        # sections: ['db', 'ssh']
print('options of [db]:', cp.options('db'))  # options of [db]: ['host', 'port', 'user', 'pass']
print('items of [ssh]:', cp.items('ssh'))    # items of [ssh]: [('host', '192.168.1.101'), ('user', 'huey'), ('pass', 'huey')]

# 读取指定的配置信息
print('host of db:', cp.get('db', 'host'))     # host of db: 127.0.0.1
print('host of ssh:', cp.get('ssh', 'host'))   # host of ssh: 192.168.1.101

# 按类型读取配置信息：getint、 getfloat 和 getboolean
print(type(cp.getint('db', 'port')))        # <type 'int'>

print(cp.get('msg', 'hello'))

