def max_len(string):
    abba = []
    aba = []
    # 遍历寻找对称位置
    for i in range(len(string)-1):
        current = i
        next_one = i+1
        if string[current] == string[next_one]:
            abba.append(i)
        elif string[current-1] == string[next_one]:
            aba.append(i)
    length = []
    for j in abba:
        first = j
        last = j+1
        while first>=0 and last<len(string) and string[first]==string[last]:
            first+=-1
            last+=1
            # CABBA，第一循环时，符合条件的只有2个字符，而此时last-first=3,所以需要减去1
            length.append(last-first-1)
    for k in aba:
        first = k-1
        last = k+1
        while first>=0 and last<len(string) and string[first] == string[last]:
            first+=-1
            last +=1
            length.append(last-first-1)
    if len(length)==0:
        return 0
    else:
        return max(length)


while True:
    try:
        string = input()
        print(max_len(string))
    except:
        break
