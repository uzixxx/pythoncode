def exchange(s, a, b):
    st1 = s[0:b]+s[a] + s[b+1:]
    st2 = st1[0:a]+s[b]+st1[a+1:]
    return st2

s1 = 'sabcdbsd'
print(exchange(s1,5,5))
