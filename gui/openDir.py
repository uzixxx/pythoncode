import tkinter as tk
import configparser
import subprocess

def readconfig(filename):
    cf = configparser.ConfigParser()
    try:
        configcontent = {}
        cf.read(filename,encoding='utf-8')
        sections = cf.sections()
        for s in sections:
            configcontent.update(dict(cf.items(s)))
    except:
        print("throw a exception:\n{e}".format(e=sys.exc_info()))
        return None
    else:
        return configcontent

def clickFun(v):
    def f():
        subprocess.run(r'''start "" '''+'''"'''+v+'''"''',shell=True)
    return f

configcontent = readconfig('dir.conf')
option_name_list = configcontent.keys()

root = tk.Tk()
root.title("Small Tool")
root.geometry('300x810')
root.resizable(0,0)

frame1 = tk.Frame(root)
frame1.pack(padx=5,pady=5)
for name in option_name_list:
    button = tk.Button(frame1, text=name ,width=30, height=1, command=clickFun(configcontent[name]))
    button.pack(side='top', pady=5)

root.mainloop()

