import tkinter as tk

root = tk.Tk()
root.title("Small Calculator")
root.geometry('500x300')

var1 = tk.DoubleVar()
label1 = tk.Label(text="The First Number", width=20, height=2)
label1.pack()
entry1 = tk.Entry(width=20)
entry1.pack()

var2 = tk.StringVar()
label2 = tk.Label(text="The Operator", width=20, height=2)
label2.pack()
entry2 = tk.Entry(width=20)
entry2.pack()

var3 = tk.DoubleVar()
label3 = tk.Label(text="The Second Number", width=20, height=2)
label3.pack()
entry3 = tk.Entry(width=20)
entry3.pack()

var4 = tk.DoubleVar()
label4 = tk.Label(text="The Solution", width=20, height=2)
label4.pack()
label5 = tk.Label(textvar=var4, width=20, height=1)
label5.pack()

def clickFun():
    global var1
    global var2
    global var3
    global var4
    var1 = int(entry1.get())
    var2 = entry2.get()
    var3 = int(entry3.get())
    if var2 == '+':
        var4.set(int(var1+var3))
    elif var2 == '-':
        var4.set(int(var1-var3))
    elif var2 == '*':
        var4.set(int(var1*var3))
    elif var2 == '/':
        if var3 == 0:
            var4.set("请重新输入数据")
        else:
            var4.set(int(var1/var3))
    else:
        var4.set("运算符出错，请重新输入数据")

button1 = tk.Button(text="Deal" ,width=10, height=2, command=clickFun)
button1.pack()
root.mainloop()