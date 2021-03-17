li = [1, 2, 5, 7, 9]
s = []
s.append(li[0])
for i in range(1, len(li)):
    if li[i] != li[i - 1] + 1:
        s.append(li[i-1])
        s.append(li[i])

# for i in range(len(s)):
#     if i % 2 == 0:
#         print(str(s[i]) + '-' + str(s[i+1]))
print(s)

