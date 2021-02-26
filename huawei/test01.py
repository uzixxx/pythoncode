# 输入一个只含有小写字母的字符串，只交换其中两个字符的位置，使字符串的值最小。


def exchange(s, a, b):
    st1 = s[0:b]+s[a] + s[b+1:]
    st2 = st1[0:a]+s[b]+st1[a+1:]
    return st2


s1 = input('输入一个只含有小写字母的字符串: ')
# s = "".join((lambda x: (x.sort(), x)[1])(list(s1)))
ls = list(s1)
ls.sort()
s2 = "".join(ls)
s3 = ""
i = 0
for i in range(len(s1)):
    if s1[i] > s2[i]:
        break
if i == len(s1)-1:
    s3 = exchange(s1, i-1, i)
else:
    s3 = exchange(s1, i, s1.rfind(s2[i]))

print(s3)
