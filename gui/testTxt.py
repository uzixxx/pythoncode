import numpy as np
filename = 'RuleSettings.txt' # txt文件和当前脚本在同一目录下，所以不用写具体路径
L1 = []
with open(filename, 'r', encoding = 'utf8') as file_to_read:
    while True:
        lines = file_to_read.readline() # readline()整行读取数据,返回字符串
        if not lines:
            break
        L2 = []
        for i in lines.split('\t'):
            L2.append(i)
        L1.append(L2)
    print(L1)
    print(len(L1))
