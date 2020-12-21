import tkinter as tk
import tkinter.messagebox


def check():
    if v.get() < 4:
        entry1.delete(0, len(entry1.get()))
        entry1.insert(0, 'yyyymm')
        entry2.delete(0, len(entry2.get()))
        entry2.insert(0, 'yyyymm')
    elif v.get() == 4:
        entry1.delete(0, len(entry1.get()))
        entry1.insert(0, 'yyyy-mm-dd')
        entry2.delete(0, len(entry2.get()))
        entry2.insert(0, 'yyyy-mm-dd')
    else:
        entry1.delete(0, len(entry1.get()))
        entry1.insert(0, 'yyyymmdd')
        entry2.delete(0, len(entry2.get()))
        entry2.insert(0, 'yyyymmdd')


def func1():
    entry1.delete(0, len(entry1.get()))


def func2():
    entry2.delete(0, len(entry2.get()))


def click():
    value = v.get()
    print(value)
    tkinter.messagebox.showwarning(title='warning', message='请选择要导出的文件')


root = tk.Tk()
root.title("医保小工具")
root.geometry('500x300')
root.resizable(0, 0)

group = tk.LabelFrame(root, text='选择要导出的文件：', padx=5, pady=5)
group.pack(side='left', fill='both', expand='1', padx=10, pady=10)

titles = [
    ('月度科室财务报表', 1),
    ('时间维度综合分析(科室)', 2),
    ('时间维度综合分析(病区)', 3),
    ('综合分析指标(病区)', 4),
    ('综合分析指标(医师)', 5)]
v = tk.IntVar()
for title, num in titles:
    b = tk.Radiobutton(group, text=title, variable=v, value=num, command=check)
    b.pack(anchor='w')

label1 = tk.Label(text="开始时间：", width=20, height=2)
label1.pack()
entry1 = tk.Entry(width=20)
entry1.bind('<Button-1>', func1)
entry1.pack(padx=10)

label2 = tk.Label(text="结束时间：", width=20, height=2)
label2.pack()
entry2 = tk.Entry(width=20)
entry2.bind('<Button-1>', func2)
entry2.pack(padx=10)

button1 = tk.Button(text="导出", width=10, height=2, command=click)
button1.pack(side='bottom', padx=10, pady=10)

root.mainloop()
