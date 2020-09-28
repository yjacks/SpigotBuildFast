# coding:utf8

# 一键化构建水龙头

# 文件管理/操作外部Java
import os
import os.path
import sys
# 构建GUI
import tkinter
from tkinter.messagebox import showerror, showinfo, showwarning

import wget  # wget模块,下载构建工具

# 初始化GUI
tk = tkinter.Tk()
tk.maxsize(250, 250)
tk.minsize(250, 250)
tk.title("spigot构建")


def getBuild():  # 具体的函数,利用wget模块获取最新工具,早期的遗留
    try:
        wget.download(
            url="https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar",
            out="BuildTools.jar")
    except:
        showerror("错误", "网络错误,无法获得构建工具")
        return False
    else:
        showinfo("成功", "已获取构建工具")
        return True


def setBuild():  # 生成文件
    # 用于判断字符串是否正确
    ver = EntryVer.get()
    dir = EntryDir.get()
    if os.path.exists("BuildTools.jar"):
        BuildJar=os.path.abspath("BuildTools.jar")
    else:
        s=getBuild()
        if s:
            BuildJar=os.path.abspath("BuildTools.jar")
        else:
            return False
    if dir == '':
        showwarning("警告", "将会在本目录下开服,如不需要请直接关闭程序")
    if ver == '':
        showwarning("警告", "将会生成最新版本")
    # 生成bat,次选方案,因为os.popen和os.system都不支持cd
    Command_file = open('test.bat', 'w')
    Command_file.write(r"@echo off"+"\n")
    if not dir == '':
        Command_file.write('cd /d ' + dir+"\n")  # 如果dir不是默认,就在当前目录生成
    if not ver == '':
        Command_file.write('java -jar '+str(BuildJar)+ ' --rev ' + ver)
    else:
        Command_file.write('java -jar ' + str(BuildJar))
    Command_file.write('\nexit')
    Command_file.close()
    os.popen('start test.bat')
    return [True, dir]


def HelpUse():
    showinfo('帮助', '''
    请输入版本和目录，否则默认在当前目录下生成1.7.10版本
    按构建基础环境，会在选定的目录构建环境，可以自己按test.bat二次生成
    ''')


# 生成组件
LableVer = tkinter.Label(tk, text="版本输入")
LableDir = tkinter.Label(tk, text="路径输入")
EntryVer = tkinter.Entry(tk)
EntryDir = tkinter.Entry(tk)
ButtonChangeDir = tkinter.Button(tk, text="一键构建基础环境", command=setBuild)  # 生成文件,对应setBuild函数
ButtonHelp = tkinter.Button(tk, text='帮助', command=HelpUse)  # 帮助
ButtonExit = tkinter.Button(tk, text='退出', command=sys.exit)  # 退出

# 放置组件
LableVer.pack()
EntryVer.pack()
LableDir.pack()
EntryDir.pack()
ButtonChangeDir.pack()
ButtonHelp.pack()
ButtonExit.pack()

# 条件循环
tk.mainloop()
