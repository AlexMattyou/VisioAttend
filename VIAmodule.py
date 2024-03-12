import cv2
import face_recognition as face
import os
import pandas as pd
from time import sleep
from datetime import datetime, time
import json
import threading
import shutil

rootLoc = os.path.dirname(os.path.realpath(__file__))


# modify the config.json file
def settings(option, store=0):
    with open("config.json", "r") as file:
        data = json.load(file)
    if store:
        data[option] = store
    else:
        return data[option]
    with open("config.json", "w") as file:
        json.dump(data, file, indent=4)


# capture the current scene
def capture(port=0, interval=60, imageNumber=0, obj=None):
    if obj.stop:
        return 1
    port = "http://192.168.189.4:8080/video"
    cap = cv2.VideoCapture(port)
    success, frame = cap.read()
    print('ready')
    if success:
        imageNumber += 1
        print("Running")
        cv2.imwrite(rootLoc + "\\images\\captured\\" + f"{imageNumber}.png", frame)
        obj.addLog(f'Image captured [{imageNumber}.png]')
    cap.release()
    sleep(interval)
    capture(port, interval, imageNumber, obj)


def encodeFace(frame):
    encoded = face.face_encodings(frame)
    return encoded


def compareFace(x, y):
    distance = face.face_distance(x, y)
    match = face.compare_faces(x, y)
    return (distance, match)


# encodes faces from students folder
def createFaceMesh(obj=None):
    pandasData = []
    faceList = os.listdir(rootLoc + "\\images\\students")
    print("Images in folder:", faceList)
    for file in faceList:
        sID, sName = file.split(".")[0].split("_")
        print(sID, sName)
        face = cv2.imread(rootLoc + "\\images\\students\\" + file)
        encode = encodeFace(face)
        pandasData.append((sID, sName, encode))
        obj.addLog(f"Encoded [{sName}]")
    dataframe = pd.DataFrame(pandasData)
    dataframe.columns = ["ID", "Name", "FaceData"]
    dataframe.to_json(rootLoc + "\\faceMesh.json")
    students = dataframe.loc[:, ["ID", "Name"]]
    students.to_csv(rootLoc + "\\Data\\template\\students.csv", index=False)
    createTemplate()
    obj.addLog("Encoding completed ✅")
    return 1


# returns list of faces in given image(frame)
def predictFace(frame, bgProcess=0, obj=None):
    imageNumber = 0
    import numpy as np
    capturedFaces = np.array(encodeFace(frame))
    encodedFaces = pd.read_json(rootLoc + "\\faceMesh.json")
    predictedFaces = []
    names = []
    if not bgProcess:
        loc = face.face_locations(frame)
        print(len(loc))
    name = None
    for i in range(capturedFaces.shape[0]):
        lowestDistance = 1
        matchValue = False
        predictedID = None
        for j in range(encodedFaces.shape[0]):
            distance, match = compareFace(
                capturedFaces[i], np.array(encodedFaces.loc[j]["FaceData"])
            )
            print(distance, match)
            if distance < lowestDistance:
                lowestDistance = distance
                matchValue = match
                predictedID = encodedFaces.loc[j]["ID"]
                name = encodedFaces.loc[j]["Name"]
        if matchValue and predictedID != None and lowestDistance < 0.55:
            predictedFaces.append(predictedID)
            names.append(name)
            print(name, lowestDistance)
        else:
            name = "Unknown"
        if not bgProcess:
            import random

            cv2.rectangle(
                frame,
                (loc[i][3], loc[i][0]),
                (loc[i][1], loc[i][2]),
                (
                    random.randint(150, 255),
                    random.randint(150, 255),
                    random.randint(150, 255),
                ),
                4,
            )
            cv2.putText(
                frame,
                name,
                (loc[i][3] + 6, loc[i][2] + 6),
                cv2.FONT_HERSHEY_COMPLEX,
                2,
                (255, 255, 255),
                3,
            )
    if not bgProcess:
        frame = cv2.resize(frame, (600, 270))
        imageNumber += 1
        cv2.imwrite(rootLoc + "\\images\\predicted\\" + "predicted.png", frame)
        obj.updateImage()
    obj.addLog("Names predicted: "+ str(list(set(names))))
    return tuple(set(predictedFaces))


def dayTimeStamp(currentTime):
    # if time(9, 0) >= currentTime or time(16, 30) <= currentTime: return  0
    if time(9, 0) <= currentTime <= time(9, 50):
        return 1
    elif time(9, 50) <= currentTime <= time(10, 40):
        return 2
    # elif time(10, 40) <= currentTime <= time(10, 55): return 0
    elif time(10, 55) <= currentTime <= time(11, 45):
        return 3
    elif time(11, 45) <= currentTime <= time(12, 35):
        return 4
    # elif time(12, 35) <= currentTime <= time(13, 20): return 0
    elif time(13, 20) <= currentTime <= time(14, 10):
        return 5
    elif time(14, 10) <= currentTime <= time(15, 0):
        return 6
    # elif time(15, 0) <= currentTime <= time(15, 10): return 0
    elif time(15, 10) <= currentTime <= time(16, 0):
        return 7
    elif time(16, 0) <= currentTime <= time(16, 30):
        return 8
    else:
        return 0


# create a template file
def createTemplate(default="daily"):
    students = os.listdir(rootLoc + "\\images\\students")
    if default == "daily":
        columns = ["ID", "Name", "1", "2", "3", "4", "5", "6", "7", "8"]
        df = pd.DataFrame(columns=columns)
        for file in students:
            sID, sName = file.split(".")[0].split("_")
            dataRow = {
                "ID": sID,
                "Name": sName,
                "1": " ",
                "2": " ",
                "3": " ",
                "4": " ",
                "5": " ",
                "6": " ",
                "7": " ",
                "8": " ",
            }
            df.loc[len(df)] = dataRow
        df.to_csv(rootLoc + "\\Data\\Template\\dailyRecord.csv", index=False)


def createRegister(type = 'D'):
    if type == "D":
        date = datetime.now().date()
        if date.strftime("%A") == "Sunday":
            print(" SUNDAY is a holiday ")
            return 0
        register = pd.read_csv(rootLoc + "\\Data\\Template\\dailyRecord.csv")
        fileName = f"{date.year}-{date.month}-{date.day}.csv"
        register.to_csv(rootLoc + "\\Data\\DayRecord\\" + fileName, index=False)


def fileSearch(fileName, path):
    for root, dirs, files in os.walk(path):
        if fileName in files:
            # File found
            filePath = f"{root}/{fileName}"
            return filePath
    return 0  # No file found


# put present to given name
def putAttendence(names=[]):
    date = datetime.now()
    fileName = f"{date.year}-{date.month}-{date.day}.csv"
    path = rootLoc + "\\Data\\DayRecord\\"
    filePath = fileSearch(fileName, path)
    if filePath == 0:
        createRegister("D")
        return putAttendence(names)
    period = dayTimeStamp(date.time())
    if period == 0 or period == 1:
        return period
    register = pd.read_csv(filePath)
    OD, Leave = [], []
    # OD  Leave = informed()
    for i in range(register.shape[0]):
        target = register.loc[i]["ID"]
        print(target)
        if (target in names) or (target in OD):
            s = "P"
        elif target in Leave:
            s = "L"
        else:
            s = "A"
        print(register.iloc[i])
        if register.loc[i, str(period)] != "P":
            register.loc[i, str(period)] = s
    print(register)
    register.to_csv(filePath, index=False)
    return filePath



#!/usr/bin/python3
from PIL import Image
import tkinter as tk
from customtkinter import (
    CTkImage,
    CTkButton,
    CTkCheckBox,
    CTkEntry,
    CTkFont,
    CTkFrame,
    CTkLabel,
    CTkScrollableFrame,
    CTkTabview,
    CTk
)


class App:
    def __init__(self, master=None):
        
        # build ui
        self.ctktoplevel1 = CTk()
        self.ctktoplevel1.geometry("760x574")
        self.ctktoplevel1.resizable(False, False)
        self.ctktoplevel1.title("VisioAttend")
        
        #variables:
        self.ipAddressStr = tk.StringVar(value=settings("cameraIP"))
        self.captureInterval = tk.IntVar(value=settings("captureInterval"))
        self.bgProcess = tk.IntVar(value=settings("bgProcess"))
        self.aboutStr = tk.StringVar(value="👆\nThis page can give you a grasp of what's happening here\n\nThis is VisioAttend\nAn Automated face-recognigation attendence system")
        self.startOrStop = tk.StringVar(value="Start")
        self.stop = 0
        
        self.viewFrame = CTkFrame(self.ctktoplevel1)
        self.viewFrame.configure(
            corner_radius=10, fg_color="#474965", height=340, width=760
        )
        self.tabView = CTkTabview(self.viewFrame)
        self.tabView.configure(
            anchor="w",
            fg_color="#191C24",
            height=320,
            segmented_button_selected_color="#EE6352",
            segmented_button_selected_hover_color="#BB4E3F",
            width=730,
        )
        cameraTab = self.tabView.add("Camera")
        self.image = CTkLabel(cameraTab)
        self.image.configure(corner_radius=5, height=270, width=600)
        self.image.pack(side="top")
        aboutTab = self.tabView.add("About")
        self.aboutFrame = CTkScrollableFrame(aboutTab, orientation="vertical")
        self.aboutFrame.configure(
            fg_color="#191C24", height=257, scrollbar_button_color="#191C24", width=690
        )
        self.aboutLabel = CTkLabel(self.aboutFrame)
        self.aboutLabel.configure(
            text="This is Visio Attend", textvariable=self.aboutStr
        )
        self.aboutLabel.pack(side="top")
        self.aboutFrame.pack(side="top")
        self.tabView.pack(padx=10, pady=10, side="top")
        self.viewFrame.grid(
            column=0, columnspan=2, padx="10 5", pady="10 5", row=0, sticky="nw"
        )
        self.ipFrame = CTkFrame(self.ctktoplevel1)
        self.ipFrame.configure(
            corner_radius=10, fg_color="#262933", height=220, width=470
        )
        self.ipLabel = CTkLabel(self.ipFrame)
        self.ipLabel.configure(
            font=CTkFont("Candara", 14, "bold", "roman", False, False),
            justify="left",
            text="Camera IP address:",
        )
        self.ipLabel.pack(anchor="w", padx=10, pady="5 0", side="top")
        self.ipEntry = CTkEntry(self.ipFrame)
        self.ipEntry.configure(
            fg_color="#191C24",
            font=CTkFont("system", None, None, "roman", False, False),
            justify="left",
            show="•",
            text_color="#EE6352",
            textvariable=self.ipAddressStr,
            width=467,
        )
        self.ipEntry.pack(anchor="e", padx="5 10", pady="0 10", side="top")
        self.startBtn = CTkButton(self.ipFrame)
        self.startBtn.configure(
            fg_color="#EE6352",
            font=CTkFont("Candara", 14, "bold", "roman", False, False),
            hover_color="#BB4E3F",
            text="Start",
            text_color="#000000",
            textvariable=self.startOrStop,
        )
        self.startBtn.pack(padx="10 10", pady="0 20", side="right")
        self.startBtn.configure(command=self.btnStart)
        self.ipFrame.grid(column=0, padx="10 5", pady="5 5", row=1, sticky="nw")
        self.optionsFrame = CTkFrame(self.ctktoplevel1)
        self.optionsFrame.configure(
            corner_radius=10, fg_color="#262933", height=216, width=260
        )
        self.optionsLabel = CTkLabel(self.optionsFrame)
        self.optionsLabel.configure(
            anchor="w",
            font=CTkFont("Candara", 14, "bold", "roman", False, False),
            justify="left",
            text="Options:",
        )
        self.optionsLabel.pack(anchor="w", padx=10, side="top")
        self.bg_process = CTkCheckBox(self.optionsFrame, onvalue=1, offvalue=0)
        self.bg_process.configure(
            fg_color="#EE6352",
            hover_color="#BB4E3F",
            text="Background Process",
            variable=self.bgProcess,
            width=250,
        )
        self.bg_process.pack(padx=5, pady=10, side="top")
        self.ctkframe2 = CTkFrame(self.optionsFrame)
        self.ctkframe2.configure(fg_color="#262933")
        self.ctklabel6 = CTkLabel(self.ctkframe2)
        self.ctklabel6.configure(text="Frame Interval")
        self.ctklabel6.pack(padx="10 5", pady=10, side="left")
        self.ctkentry2 = CTkEntry(self.ctkframe2)
        self.ctkentry2.configure(
            fg_color="#191C24",
            font=CTkFont("system", None, None, "roman", False, False),
            justify="left",
            textvariable=self.captureInterval,
            width=80,
        )
        self.ctkentry2.pack(padx=5, pady=10, side="left")
        self.ctkframe2.pack(side="left")
        self.optionsFrame.grid(
            column=1, padx="5 10", pady="5 10", row=1, rowspan=2, sticky="nw"
        )
        self.dataFrame = CTkFrame(self.ctktoplevel1)
        self.dataFrame.configure(
            corner_radius=10, fg_color="#474965", height=110, width=470
        )
        self.registerFrame = CTkFrame(self.dataFrame)
        self.registerFrame.configure(fg_color="#262933")
        self.registerLabel = CTkLabel(self.registerFrame)
        self.registerLabel.configure(
            font=CTkFont("Candara", 14, "bold", "roman", False, False),
            justify="left",
            text="Stored Register:",
        )
        self.registerLabel.pack(anchor="w", padx=10, pady="5 0", side="top")
        self.viewAll = CTkButton(self.registerFrame)
        self.viewAll.configure(
            fg_color="#EE6352",
            font=CTkFont("Tahoma", 12, "bold", "roman", False, False),
            hover_color="#BB4E3F",
            text="View All",
            text_color="#000000",
            width=100,
        )
        self.viewAll.pack(padx="10 5", pady=10, side="left")
        self.viewAll.configure(command=self.btnViewAll)
        self.viewToday = CTkButton(self.registerFrame)
        self.viewToday.configure(
            fg_color="#EE6352",
            font=CTkFont("Tahoma", 12, "bold", "roman", False, False),
            hover_color="#BB4E3F",
            text="View Today",
            text_color="#000000",
            width=100,
        )
        self.viewToday.pack(padx="5 10", pady=10, side="left")
        self.viewToday.configure(command=self.btnViewToday)
        self.registerFrame.pack(padx="10 5", pady=10, side="left")
        self.trainFrame = CTkFrame(self.dataFrame)
        self.trainFrame.configure(fg_color="#262933")
        self.trainLabel = CTkLabel(self.trainFrame)
        self.trainLabel.configure(
            font=CTkFont("Candara", 14, "bold", "roman", False, False),
            justify="left",
            text="Prelude Data:",
        )
        self.trainLabel.pack(anchor="w", padx=10, pady="5 0", side="top")
        self.students = CTkButton(self.trainFrame)
        self.students.configure(
            fg_color="#EE6352",
            font=CTkFont("Tahoma", 12, "bold", "roman", False, False),
            hover_color="#BB4E3F",
            text="Students Image",
            text_color="#000000",
            width=100,
        )
        self.students.pack(padx="10 5", pady=10, side="left")
        self.students.configure(command=self.btnStudents)
        self.encode = CTkButton(self.trainFrame)
        self.encode.configure(
            fg_color="#EE6352",
            font=CTkFont("Tahoma", 12, "bold", "roman", False, False),
            hover_color="#BB4E3F",
            text="Start Learning",
            text_color="#000000",
            width=100,
        )
        self.encode.pack(padx="5 10", pady=10, side="left")
        self.encode.configure(command=self.btnEncode)
        self.trainFrame.pack(padx="5 10", pady=10, side="left")
        self.dataFrame.grid(column=0, padx="10 5", pady="5 10", row=2, sticky="nw")

        # Main widget
        self.mainwindow = self.ctktoplevel1
        
        imgThread = threading.Thread(target=self.updateImage)
        imgThread.start()

    def run(self):
        self.mainwindow.mainloop()
        
    def addLog(self, log):
        old = self.aboutStr.get()
        new = log + '\n' + old
        self.aboutStr.set(new)
        
    def updateImage(self):
        imgLoc = rootLoc + "\\images\\predicted\\"
        if os.path.exists(imgLoc + "predicted.png"):
            light_image = Image.open(imgLoc + "predicted.png")
            dark_image = Image.open(imgLoc + "predicted.png")
        else:
            light_image = Image.open(imgLoc + "empty.png")
            dark_image = Image.open(imgLoc + "empty.png")
        
        my_image = CTkImage(light_image=light_image, dark_image=dark_image, size=(600, 270))
        self.image.configure(self, image = my_image, text=' ')
    
    def preStart(self):
        settings("cameraIP", str(self.ipAddressStr.get()))
        settings("captureInterval", int(self.captureInterval.get()))
        settings("bgProcess", int(self.bgProcess.get()))
        cameraLoop = threading.Thread(target=capture, args=(self.ipAddressStr.get(), self.captureInterval.get(), 0, self))
        cameraLoop.start()
        startLoop = threading.Thread(target=self.startLoop)
        startLoop.start()
        
    def preStop(self):
        path = rootLoc + "\\images\\captured"
        shutil.rmtree(path)
        os.makedirs(path)
        
    def startLoop(self):
        if self.stop:
            self.addLog('< VisioAttend stopped >')
            return 0
        path = rootLoc + "\\images\\captured\\"
        imgList = []
        for root, dirs, files in os.walk(path):
            imgList = [int(f.split('.')[0]) for f in files]
        if len(imgList) == 0:
            sleep(3)
            self.startLoop()
            return
        img = path +  str(min(imgList)) + ".png"
        frame = cv2.imread(img)
        if self.stop:
            self.addLog('< VisioAttend stopped >')
            return 0
        names = predictFace(frame, self.bgProcess.get(), self)
        if self.stop:
            self.addLog('< VisioAttend stopped >')
            return 0
        putAttendence(names)
        self.addLog('----------------------------------------------  Attendance updated  ----------------------------------------------')
        os.remove(img)
        self.startLoop()

    def btnStart(self):
        type = self.startOrStop.get()
        if type == "Start":
            self.stop = 0
            self.startOrStop.set("Stop")
            self.addLog('VisioAttend started')
            start = threading.Thread(target=self.preStart)
            start.start()
        else:
            self.stop = 1
            self.startOrStop.set("Start")
            self.addLog('Stopping process...')
            self.preStop()
            
    def btnViewAll(self):
        path = rootLoc+"\\Data\\DayRecord"
        path = os.path.realpath(path)
        os.startfile(path)

    def btnViewToday(self):
        date = datetime.now().date()
        fileName = f"{date.year}-{date.month}-{date.day}.csv"
        path = rootLoc+"\\Data\\DayRecord\\"+fileName
        if not os.path.exists(path):
            createRegister()
        path = os.path.realpath(path)
        os.startfile(path)

    def btnStudents(self):
        path = rootLoc+"\\images\\Students"
        path = os.path.realpath(path)
        os.startfile(path)

    def btnEncode(self):
        encode_thread = threading.Thread(target=createFaceMesh, args=(self,))
        encode_thread.start()

from flask import Flask, render_template, request, jsonify, send_file, Response
web = Flask(__name__)

@web.route("/visioattend/register.csv") 
def sendRegister():
    date = datetime.now()
    fileName = f"{date.year}-{date.month}-{date.day}.csv"
    path = rootLoc + "\\Data\\DayRecord\\"
    fileExist = fileSearch(fileName, path)
    if not fileExist:
        path = rootLoc + "\\Data\\Template\\"
        fileName = "dailyRecord.csv"
    with open(path + fileName, 'r') as file:
        csv_content = file.read()
    return Response(csv_content, mimetype='text/plain')

@web.route("/visioattend/edit") 
def edit():
    return render_template('index.html')

@web.route('/visioattend', methods=['POST'])
def receive_json():
    data = request.json  # Get JSON data sent from the client
    print('Received JSON data:', data)
    # Process the data as needed
    print("yeay")
    response_data = {'message': 'Data received successfully'}
    return jsonify(response_data)

def run_flask():
    web.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    app = App()
    app.run()
