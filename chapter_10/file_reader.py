# read() 返回字符串
file_path = 'pi_digits.txt'
# with open(file_path) as file_object:
#     contents = file_object.read()
#     print(contents.rstrip())

# with open(file_path) as file_object:
#     for line in file_object:
#         print(line.rstrip())

# readlines() 返回列表
with open(file_path) as file_object:
    lines = file_object.readlines()

pi_string = ''
for line in lines:
    print(line.rstrip())
    pi_string += line.strip()

print(pi_string)
print(len(pi_string))
