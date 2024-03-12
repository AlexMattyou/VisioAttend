#!/usr/bin/python3
import tkinter as tk
from threading import Thread
from customtkinter import (
    CTk, 
    CTkButton, 
    CTkEntry, 
    CTkFrame, 
    CTkLabel, 
    CTkSwitch, 
    set_appearance_mode, 
    set_default_color_theme, 
)


class App:
    def __init__(self, master=None):

        # meta
        self.root = CTk(None)
        set_appearance_mode("dark")
        set_default_color_theme("blue")
        self.root.geometry("640x480")
        self.root.resizable(False, False)
        self.root.title("Visio Attend 2.03")

        #global variables
        self.rootLoc = '../'
        self.stop = 0
        # input variables
        self.IPaddress = tk.StringVar()
        self.inputMode = tk.StringVar()
        self.log_1 = tk.StringVar(value="Logs will be displayed here")
        self.log_2 = tk.StringVar(value=" ")
        self.log_3 = tk.StringVar(value=" ")
        self.log_4 = tk.StringVar(value=" ")
        self.log_5 = tk.StringVar(value=" ")
        self.log_6 = tk.StringVar(value=" ")

        # UI
        self.menu_frame = CTkFrame(self.root)
        self.menu_frame.configure(height=250, width=200)
        self.menu_label = CTkLabel(self.menu_frame)
        self.menu_label.configure(text="Menu")
        self.menu_label.pack(fill="x", padx=5, pady=5, side="top")
        self.key_frame = CTkFrame(self.menu_frame)
        self.key_frame.configure(height=90)
        self.start_button = CTkButton(self.key_frame)
        self.start_button.configure(compound="bottom", text="Start")
        self.start_button.pack(padx=5, pady="10 5", side="top")
        self.start_button.configure(command=self.startKey)
        self.stop_button = CTkButton(self.key_frame)
        self.stop_button.configure(compound="bottom", text="Stop")
        self.stop_button.pack(padx=5, pady="10 5", side="top")
        self.stop_button.configure(command=self.stopKey)
        self.key_frame.pack(padx=10, pady=10, side="top")
        self.key_frame.pack_propagate(0)
        self.attend_folder_button = CTkButton(self.menu_frame)
        self.attend_folder_button.configure(text="Attendence Folder")
        self.attend_folder_button.pack(padx=10, pady=10, side="top")
        self.attend_folder_button.configure(command=self.openAttend)
        self.today_button = CTkButton(self.menu_frame)
        self.today_button.configure(text="Today's Record")
        self.today_button.pack(padx=10, pady=10, side="top")
        self.today_button.configure(command=self.openTodays)
        self.menu_frame.grid(column=0, padx="20 10", pady="20 10", row=0, sticky="ew")
        self.menu_frame.pack_propagate(0)
        self.config_frame = CTkFrame(self.root)
        self.config_frame.configure(height=250, width=390)
        self.config_label = CTkLabel(self.config_frame)
        self.config_label.configure(text="Configure")
        self.config_label.pack(fill="x", padx=5, pady=5, side="top")
        self.config_inner_frame = CTkFrame(self.config_frame)
        self.config_inner_frame.configure(height=205, width=370)
        self.ip_label = CTkLabel(self.config_inner_frame)
        self.ip_label.configure(text="Camera IP address:")
        self.ip_label.pack(anchor="w", padx=35, pady="10 0", side="top")
        self.ip_input = CTkEntry(self.config_inner_frame)
        self.ip_input.configure(corner_radius=2, textvariable=self.IPaddress, width=320)
        self.ip_input.pack(side="top")
        self.input_mode_label = CTkLabel(self.config_inner_frame)
        self.input_mode_label.configure(text="Input Mode:")
        self.input_mode_label.pack(anchor="w", padx=35, pady="10 0", side="top")
        self.input_mode_switch = CTkSwitch(
            self.config_inner_frame, onvalue='1', offvalue='0'
        )
        self.input_mode_switch.configure(
            text="IP camera mode", variable=self.inputMode
        )
        self.input_mode_switch.pack(anchor="w", padx=35, pady=0, side="top")
        self.files_frame = CTkFrame(self.config_inner_frame)
        self.files_frame.configure(height=80, width=350)
        self.students_button = CTkButton(self.files_frame)
        self.students_button.configure(text="Students")
        self.students_button.pack(
            anchor="center", ipadx=5, ipady=5, padx=15, pady=10, side="left"
        )
        self.students_button.configure(command=self.openStudents)
        self.img_folder_button = CTkButton(self.files_frame)
        self.img_folder_button.configure(text="Encode")
        self.img_folder_button.pack(
            anchor="center", ipadx=5, ipady=5, padx=15, pady=10, side="left"
        )
        self.img_folder_button.configure(command=self.encodeStudents)
        self.files_frame.pack(padx=10, pady=10, side="top")
        self.files_frame.pack_propagate(0)
        self.config_inner_frame.pack(side="top")
        self.config_inner_frame.pack_propagate(0)
        self.config_frame.grid(column=1, padx="10 20", pady="20 10", row=0)
        self.config_frame.pack_propagate(0)
        self.log_frame = CTkFrame(self.root)
        self.log_frame.configure(height=180, width=600)
        self.log_label_1 = CTkLabel(self.log_frame)
        self.log_label_1.configure(
            text="Logs will be displayed here", textvariable=self.log_1
        )
        self.log_label_1.pack(anchor="w", fill="x", side="bottom")
        self.log_label_2 = CTkLabel(self.log_frame)
        self.log_label_2.configure(text=" ", textvariable=self.log_2)
        self.log_label_2.pack(anchor="w", fill="both", side="bottom")
        self.log_label_3 = CTkLabel(self.log_frame)
        self.log_label_3.configure(text=" ", textvariable=self.log_3)
        self.log_label_3.pack(anchor="w", fill="both", side="bottom")
        self.log_label_4 = CTkLabel(self.log_frame)
        self.log_label_4.configure(text=" ", textvariable=self.log_4)
        self.log_label_4.pack(anchor="w", fill="both", side="bottom")
        self.log_label_5 = CTkLabel(self.log_frame)
        self.log_label_5.configure(text=" ", textvariable=self.log_5)
        self.log_label_5.pack(anchor="w", fill="both", side="bottom")
        self.log_label_6 = CTkLabel(self.log_frame)
        self.log_label_6.configure(text=" ", textvariable=self.log_6)
        self.log_label_6.pack(anchor="w", fill="both", side="bottom")
        self.log_frame.grid(column=0, columnspan=2, padx=20, pady="10 20", row=1)
        self.log_frame.pack_propagate(0)
        self.root.grid_propagate(0)

        load_thread = Thread(target=load_visioattend)
        load_thread.start()

        # Main widget
        self.mainwindow = self.root

    def run(self):
        self.mainwindow.mainloop()

    def startKey(self):
        self.stop = 0
        if self.inputMode.get() == '1':
            import VIAmodule as via
            port = self.IPaddress.get()
            if port == '0':
                self.addLog('  Using WebCam  ')
                thread = Thread(target=via.ipRun, args=(0, self))
                thread.start()
            else: 
                self.addLog('  Using IP Camera  ')
                via.settings('cameraIP',port)
                thread = Thread(target=via.ipRun, args=(port, self))
                thread.start()
        else:
            self.addLog('  Using Pre Image Mode  ')
            import VIAmodule as via
            imgList = via.fileList(self.rootLoc+"received/images", self)
            thread = Thread(target=via.fileRun, args=(imgList, self))
            thread.start()

    def stopKey(self):
        self.stop = 1

    def openAttend(self):
        import os
        path = self.rootLoc+"Data/DayRecord"
        path = os.path.realpath(path)
        self.addLog(f'opened [{path}]')
        os.startfile(path)

    def openTodays(self):
        import os
        from datetime import datetime
        date = datetime.now().date()
        fileName = f"{date.year}-{date.month}-{date.day}.csv"
        path = self.rootLoc+"Data/DayRecord/"+fileName
        path = os.path.realpath(path)
        self.addLog(f'opened [{path}]')
        os.startfile(path)

    def openStudents(self):
        import os
        path = self.rootLoc+"Students"
        path = os.path.realpath(path)
        self.addLog(f'opened [{path}]')
        os.startfile(path)

    def encodeStudents(self):
        import VIAmodule as via
        self.stop = 0
        encode_thread = Thread(target=via.createFaceMesh, args=(0, self))
        encode_thread.start()
        via.createTemplate()

    def addLog(self, content, level = 'new'):
        if len(content) > 80:
            self.addLog(content[:80], level)
            self.addLog(content[80:], level)
            return 0
        if level == 'new':
            self.log_6.set(self.log_5.get())
            self.log_5.set(self.log_4.get())
            self.log_4.set(self.log_3.get())
            self.log_3.set(self.log_2.get())
            self.log_2.set(self.log_1.get())
            self.log_1.set(content)
        else:
            self.log_1.set(content)

def load_visioattend():
    import VIAmodule as via
    app.addLog('<  visioattend loaded ✅  >', 0)
    ipAdd = via.settings("cameraIP")
    app.IPaddress.set(ipAdd)
    app.rootLoc = via.rootLoc
    app.addLog(f'Root Location: {app.rootLoc}')
    app.addLog(f'Selected IP address: {ipAdd}')

if __name__ == "__main__":
    app = App()
    app.addLog('loading visioattend (please wait)')
    load_thread = Thread(target=load_visioattend)
    load_thread.start()
    try:
        app.run()
    except Exception as e:
        app.addLog(f'ERROR Code: 231\n  Something went wrong  ')
