import cv2
import face_recognition as face
import os
import pandas as pd
from datetime import datetime,time
import json

rootLoc = os.path.dirname(os.path.realpath(__file__))

# modify the config.json file
def settings(option, store = 0):
    with open('config.json', 'r') as file:
        data = json.load(file)
    if store:
        data[option] = store
    else:
        return data[option]
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)
        
# returns list of files in a folder(path)
def listFile(path, obj = None):
    return os.listdir(path)

# capture the current scene
def capture(port = 0, threshold = 100000, obj=None):
    step = settings('captureMaxMin')
    kernel = settings('captureKernel')
    historyLimit = settings('captureHistoryLimit')
    savePath="images/before"
    
    preFrame = None
    cap = cv2.VideoCapture(port)
    count = 0
    history = []
    imgList = os.listdir(rootLoc+savePath)
    imgList = [int(i.split('.')[0]) for i in imgList] if imgList else [0]
    nextImage = max(imgList) + 1
    while True:
        success, frame = cap.read()
        global image
        count+= 1
        if success:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (kernel, kernel), 0)
            if preFrame is not None:
                frameDiff = cv2.absdiff(preFrame, gray)
                motion = round(cv2.sumElems(frameDiff)[0])
                if motion == 0:
                    count  = 1
                    continue
                history.append(motion)
                if len(history) > historyLimit:
                    history.pop(0)
                motionMean =sum(history)/len(history)
                threshold = round(motionMean * 2)
                if ((motion > threshold) or (count >= step[1]))and count >= step[0]:
                    # print(count '     ' threshold  '     '  motion)
                    count = 0
                    cv2.imwrite(rootLoc+savePath+ f'/{nextImage}.png', frame)
                    nextImage += 1
                    print('Running')
            # Update the previous frame
            preFrame = gray
        # cv2.imshow('Frame'  frame)
    cap.release()
def encodeFace(frame):
    encoded = face.face_encodings(frame)
    print(len(encoded))
    return encoded
def compareFace(x, y):
    distance = face.face_distance(x, y)
    match = face.compare_faces(x, y)
    return (distance, match)

# encodes faces from students folder
def createFaceMesh(x, obj=None):
    if not obj.stop:
        if obj: obj.addLog("<  Encoding Started  >")
        if obj: obj.addLog("Encoding...")
        pandasData = []
        faceList = os.listdir(rootLoc+"Students")
        print("Images in folder:", faceList)
        for file in faceList:
            sID, sName = file.split('.')[0].split('_')
            face = cv2.imread(rootLoc+"Students"+'/'+file)
            encode = encodeFace(face)
            pandasData.append((sID, sName, encode))
            if obj: obj.addLog("Face encoded: "+str(sName), 0)
        # print(pandasData)
        dataframe = pd.DataFrame(pandasData)
        dataframe.columns = ['ID', 'Name', 'FaceData']
        dataframe.to_json(rootLoc+"faceMesh.json")
        students = dataframe.loc[: ['ID', 'Name']]
        students.to_csv(rootLoc+'Data/Template/students.csv', index=False)
        # print(students)
        # print("Encoding Successful!")
        if obj: obj.addLog("<  Encoding Success ✅  >", 0)
    else:
        if obj: obj.addLog("<  Process Stopped  >")
        return 0
def returnFaceMesh():
    return pd.read_json(rootLoc+'faceMesh.json')

# returns list of faces in given image(frame)
def predictFace(frame, obj=None):
    showBox = 1
    import numpy as np
    capturedFaces = np.array(encodeFace(frame))
    encodedFaces = returnFaceMesh()
    predictedFaces = []
    names = []
    if showBox:
        loc = face.face_locations(frame)
        print(len(loc))
    name = None
    print(capturedFaces.shape[0])
    for i in range(capturedFaces.shape[0]):
        lowestDistance = 1
        matchValue = False
        predictedID = None
        for j in range(encodedFaces.shape[0]):
            print(encodedFaces.shape[0])
            print()
            # if encodedFaces.loc[j]['ID'] in predictedFaces: continue # ignore duplicates
            distance, match  = compareFace(capturedFaces[i], np.array(encodedFaces.loc[j]['FaceData']))
            print(distance, match)
            if distance < lowestDistance:
                print(lowestDistance)
                lowestDistance = distance
                matchValue = match
                predictedID = encodedFaces.loc[j]['ID']
                name = encodedFaces.loc[j]['Name']
        if matchValue and predictedID != None and lowestDistance < 0.55:
            predictedFaces.append(predictedID)
            names.append(name)
            print(name, lowestDistance)
        else:
            name = 'Unknown'
        if showBox:
            import random
            cv2.rectangle(frame, (loc[i][3], loc[i][0]), (loc[i][1], loc[i][2]), (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)), 4)
            cv2.putText(frame, name, (loc[i][3]+6, loc[i][2], 6), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 3)
    if showBox:
        frame = cv2.resize(frame, (0, 0), fx=0.4, fy=0.4)
        cv2.imshow('FaceBox', frame)
        cv2.waitKey(0)
        cv2.destroyWindow("FaceBox")
    print("Names predicted:", tuple(set(names)))
    return tuple(set(predictedFaces))

def dayTimeStamp(currentTime):
    if time(9, 0) >= currentTime or time(16, 30) <= currentTime: return  1
    elif time(9, 0) <= currentTime <= time(9, 50): return 1
    elif time(9, 50) <= currentTime <= time(10, 40): return 2
    # elif time(10, 40) <= currentTime <= time(10, 55): return 0
    elif time(10, 55) <= currentTime <= time(11, 45): return 3
    elif time(11, 45) <= currentTime <= time(12, 35): return 4
    # elif time(12, 35) <= currentTime <= time(13, 20): return 0
    elif time(13, 20) <= currentTime <= time(14, 10): return 5
    elif time(14, 10) <= currentTime <= time(15, 0): return 6
    # elif time(15, 0) <= currentTime <= time(15, 10): return 0
    elif time(15, 10) <= currentTime <= time(16, 0): return 7
    elif time(16, 0) <= currentTime <= time(16, 30): return 8
    else: return 0

# create a template file
def createTemplate(default='daily'):
    register = pd.read_csv(rootLoc+"Data/Template/"+default+"Record.csv")
    students = os.listdir(rootLoc+"Students")
    if default == 'daily':
        columns = ['ID', 'Name', '1', '2', '3', '4', '5', '6', '7', '8']
        df = pd.DataFrame(columns=columns)
        for file in students:
            sID, sName = file.split('.')[0].split('_')
            dataRow = {'ID': sID, 'Name': sName, '1': ' ', '2': ' ', '3': ' ', '4': ' ', '5': ' ', '6': ' ', '7': ' ', '8': ' '}
            df.loc[len(df)] = dataRow
        df.to_csv(rootLoc+'Data/Template/dailyRecord.csv', index=False)    

def createRegister(type, obj=None):
    if type == "D":
        date = datetime.now().date()
        if date.strftime("%A") == 'Sunday':
            print(' SUNDAY is a holiday ')
            return 0
        register = pd.read_csv(rootLoc+"Data/Template/dailyRecord.csv")
        fileName = f"{date.year} {date.month} {date.day}.csv"
        register.to_csv(rootLoc+'Data/DayRecord/'+fileName, index=False)
def fileSearch(fileName, path):
    for root, dirs, files in os.walk(path):
        if fileName in files:
            # File found
            filePath = f"{root}/{fileName}"
            return filePath
    return 0 # No file found

# retrive additional information
def informed():
    import json
    with open(rootLoc+"received/informed.json", 'r') as f:
        data = json.load(f)
        return (data['OD'], data['Leave'])
    


# put present to given name
def putAttendence(names=[], obj=None):
        date = datetime.now()
        fileName = f"{date.year} {date.month} {date.day}.csv"
        # path = rootLoc+"Data/DayRecord"
        path = "D:/Data/Apps/XAMPP/htdocs"
        filePath = fileSearch(fileName, path)
        if filePath == 0:
            createRegister('D')
            return putAttendence(names)
        period = dayTimeStamp(date.time())
        if period == 0 or period ==  1: return period
        register = pd.read_csv(filePath)
        OD, Leave = [], []
        # OD  Leave = informed()
        for i in range(register.shape[0]):
            target = register.loc[i]['ID']
            print(target)
            if (target in names) or (target in OD):s = 'P'
            elif (target in Leave):s = 'L'
            else:s = 'A'
            print(register.iloc[i])
            if register[str(period)].iloc[i] != 'P':
                register[str(period)].iloc[i] = s
        print(register)
        register.to_csv(filePath, index=False)
        return filePath

# local run
def fileRun(imgList, obj=None):
    for img in imgList:
        frame = cv2.imread(img)
        names = predictFace(frame, obj) # list of (IDs) predicted
        if obj and not obj.stop: obj.addLog(f'predicted IDs from {img.split("/")[ 1]} [{names}]')
        register = putAttendence(names, obj)
        if register == 0:
            return 0
    if obj: obj.addLog(f"<  Attendence Saved  >")

# ip run
def ipRun(port, obj=None):
    imgList = capture(3, port, obj)
    for img in range(len(imgList)):
        try:
            names = predictFace(imgList[img], obj) # list of (ID  Names) predicted
        except Exception as e:
            if obj and not obj.stop: obj.addLog(f'ERROR Code: 197\n  Camera IP not found  ')
        if obj and not obj.stop: obj.addLog(f'predicted IDs from capture {img} [{names}]')
        register = putAttendence(names, obj)
    if obj: obj.addLog(f"<  Attendence Saved  >")
    if register == 0: # stop processing
        return 0
    else: ipRun(port, obj) # repeat
    
def testRun(port, obj=None):
    pass

def run(port, obj=None):
    pass