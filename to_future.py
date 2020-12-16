import datetime
import tkinter as tk
import tkinter.messagebox
import os
import yaml


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        error = True
        event = "做啥"
        title = "标题人"
        next_time = "2100/1/1 0:00:00"
        geometry = "220x80"
        try:
            if(os.path.exists("nextdate.yaml")):
                with open("nextdate.yaml", 'r', encoding="UTF-8") as fs:
                    datas = yaml.load(fs, Loader=yaml.FullLoader)
                    master.title(datas["title"])
                    self.next_time = datetime.datetime.strptime(datas["next_time"], "%Y/%m/%d %H:%M:%S")
                    master.geometry(datas["geometry"])
                    tk.Label(self, text="还有多久就可以{}了？".format(datas["event"])).pack()
            else:
                tkinter.messagebox.showinfo("提示","没有找到配置文件，创建初始魔怔人配置："+os.getcwd()+"\\nextdate.yaml")
                error = False
                raise BaseException
        except:
            if error: tkinter.messagebox.showwarning("错误", "配置文件出错，使用初始魔怔人配置："+os.getcwd()+"\\nextdate.yaml")
            with open("nextdate.yaml", 'w', encoding="UTF-8") as fs:
                fs.write("title: {}}\nnext_time: {}\ngeometry: {}\nevent: {}".format(title, next_time, geometry, event))
            self.next_time = datetime.datetime.strptime(next_time, "%Y/%m/%d %H:%M:%S")
            master.title(title)
            master.geometry(geometry)
            tk.Label(self, text="还有多久就可以{}了？".format(event)).pack()

        self.display = tk.StringVar()
        tk.Label(self, textvariable=self.display).pack()
        grid = tk.Frame(self)
        grid.pack()
        # prompts = ["年", "月","天","小时","分钟","秒"]
        prompts = ["天", "小时", "分钟", "秒"]
        # self.ivs = [tk.IntVar() for i in range(6)]
        self.ivs = [tk.IntVar() for i in range(4)]
        # for i in range(6):
        for i in range(4):
            tmp = tk.Checkbutton(grid, text=prompts[i], variable=self.ivs[i])
            tmp.select()
            tmp.grid(row=0, column=i)
        self.pack()
        self.refresh()
        self.mainloop()

    def refresh(self):
        now_time = datetime.datetime.now()
        # year = now_time.year - self.last_talk.year
        # month = now_time.month - self.last_talk.month
        timechange = self.next_time - now_time
        day = timechange.days
        second = timechange.seconds
        text = ""
        if self.ivs[0].get():
            text += "{}天".format(day)
            day = 0
        if self.ivs[1].get():
            hour = int(day * 24 + second / 60 / 60)
            text += "{}小时".format(hour)
            second = second % (60 * 60)
            day = 0
        if self.ivs[2].get():
            minute = int(day * 24 * 60 + second / 60)
            text += "{}分钟".format(minute)
            second = second % 60
            day = 0
        if self.ivs[3].get():
            second = int(day * 24 * 60 * 60 + second)
            text += "{}秒".format(second)
        if timechange < datetime.timedelta(0,0,0,0,0,0,0):
            text = "在？时间到了，快去"
        # if self.ivs[4]:
        # if self.ivs[5]:
        # text = "{}天{}小时{}分钟{}秒".format(time_elapsed.days, int(time_elapsed.seconds/3600), int((time_elapsed.seconds%3600)/60), time_elapsed.seconds%60)
        self.display.set(text)
        self.after(100, self.refresh)


if __name__ == "__main__":
    app = Application(tk.Tk())
