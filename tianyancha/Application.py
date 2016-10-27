# coding = utf-8

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import TianYanCha
import threading

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def __del__(self):
        print('del tianyanche')
        root.destroy

    def createWidgets(self):
        self.labelDest = tk.Label(self)
        self.labelDest["text"] = '来源路径:'
        self.labelDest.grid(row=0, column=0)

        self.contentDest = tk.StringVar()
        self.contentDest.set('./work/all.txt')
        self.entryDest = tk.Entry(self)
        self.entryDest["textvariable"] = self.contentDest
        self.entryDest.grid(row=0, column=1)

        self.labelSuc = tk.Label(self)
        self.labelSuc["text"] = '成功路径:'
        self.labelSuc.grid(row=1, column=0)

        self.contentSuc = tk.StringVar()
        self.contentSuc.set('./work/suc.txt')
        self.entrySuc = tk.Entry(self)
        self.entrySuc["textvariable"] = self.contentSuc
        self.entrySuc.grid(row=1, column=1)

        self.labelFail = tk.Label(self)
        self.labelFail["text"] = '失败路径:'
        self.labelFail.grid(row=2, column=0)

        self.contentFail = tk.StringVar()
        self.contentFail.set('./work/fail.txt')
        self.entryFail = tk.Entry(self)
        self.entryFail["textvariable"] = self.contentFail
        self.entryFail.grid(row=2, column=1)

        self.buttonStart = tk.Button(self, text = '开始')
        self.buttonStart['command'] = self.start
        self.buttonStart['fg'] = 'green'
        self.buttonStart.grid(row=3, column=0)

        self.quit = tk.Button(self, text="停止", fg="red",
                              command=self.quit)
        self.quit.grid(row=3, column=1)

        self.text = ScrolledText(self)
        self.text.grid(row=4, columnspan=2)

    def start(self):
        self.running = True
        self.text.insert('end', '来源：' + self.contentDest.get() + "\r\n")
        self.text.insert('end', '成功：' + self.contentSuc.get() + "\r\n")
        self.text.insert('end', '失败：' + self.contentFail.get() + "\r\n")
        self.tianyancha = TianYanCha.TianYanCha(self.contentSuc.get(), self.contentFail.get())
        self.tianyancha.setOutput(self.text)
        self.td = threading.Thread(target=self.startThread)
        self.td.setDaemon(True)
        self.td.start()

    def quit(self):
        self.running = False
        del self.tianyancha
        print('quit')

    def startThread(self):
        self.text.delete(0.0, 'end')
        file = open(self.contentDest.get())
        for line in file.readlines():
            if self.running == True:
               self.tianyancha.getCompanyByName(line.strip('\n'))
            else:
                print('停止')
                break;


root = tk.Tk()
app = Application(master=root)
app.mainloop()
