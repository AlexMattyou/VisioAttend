import cv2
import face_recognition as face
import os
import pandas as pd
import numpy as np
import shutil
from datetime import datetime,timedelta

print("Success!!")
p = 'P'
a = 'A'
class VisioAttend():
    def __init__(self, projectDirectory = '',quality = 500, boxFace = False):
        self.encodePath = projectDirectory+"/spreadSheets/encoded.csv"
        self.sheetPath = projectDirectory+"/spreadSheets/attendence.csv"
        self.trainImgPath = projectDirectory+"/traningImages"
        self.capturedPath = projectDirectory+"/captured"
        self.captureQuality = quality
        self.boxFace = boxFace
        self.compairImgs = []
        self.encodeImgs = []
        
    def newSpace(self):
        data = []
        imgList = os.listdir(self.trainImgPath)
        print("Images in folder:",imgList)
        for file in imgList:
            img = cv2.imread(self.trainImgPath+'/'+file)
            encode = face.face_encodings(img)
            data.append((os.path.splitext(file)[0],encode[0]))
            print("Face encoded: ",os.path.splitext(file)[0])
        dataframe = pd.DataFrame(data)
        dataframe.columns = ['Names', 'FaceData']
        dataframe.to_csv(self.encodePath, index=False)
        names = pd.DataFrame(dataframe.loc[:,"Names"])
        names.to_csv(self.sheetPath, index=False)
        print("Encoding Successful!")
        cv2.waitKey(0)
        
    def webcapture(self,port = 0,count = 200,left=30):
        if os.path.exists(self.capturedPath):
            shutil.rmtree(self.capturedPath)
            os.mkdir(self.capturedPath)
        else:
            os.mkdir(self.capturedPath)
        count *= left
        cam = cv2.VideoCapture(port)
        print("Capturing Footage")
        currentframe = 0
        currentImage = 0
        for img in range(count):
            currentframe += 1
            result,frame = cam.read()
            if currentframe % left == 0: 
                if result:
                    if frame.shape[0] > self.captureQuality:
                        gradient = frame.shape[0] / self.captureQuality
                        frame = cv2.resize(frame, (int(frame.shape[1]/gradient), int(frame.shape[0]/gradient)))
                        self.compairImgs.append(frame)
                    print ('Captured: Image ' +str(currentImage)+' - Frame '+ str(img))
                    currentImage += 1
                else:
                    print("something went wrong")
                    cam.release()
                    return
        cam.release()
    def addDates(self, sdate, edate):
        datesRange = pd.date_range(sdate,edate-timedelta(days=1),freq='d')
        sheet = pd.read_csv(self.sheetPath)
        numbers = [' ' for x in range(sheet['Names'].size)]
        for d in datesRange: sheet[str(d)[:10]] = numbers
        sheet.to_csv(self.sheetPath, index=False)
    
    def recognize(self):
        if os.path.exists(self.capturedPath):
            shutil.rmtree(self.capturedPath)
            os.mkdir(self.capturedPath)
        else:
            os.mkdir(self.capturedPath)
        staticData = pd.read_csv(self.encodePath)
        trainData = []
        for i in range(len(staticData.index)):
            data = (staticData.iloc[i][0],np.array(tuple(map(float,staticData.iloc[i][1].strip('][').split()))))
            trainData.append(data)

        present = set()
        for img in range(len(self.compairImgs)):
            loc = face.face_locations(self.compairImgs[img])
            imgsEncode = face.face_encodings(self.compairImgs[img])
            detectedNames = []
            for i in range(len(imgsEncode)):
                nameList, distList, matchList = [],[],[]
                for j in range(len(trainData)):
                    
                    nameList.append(trainData[j][0])
                    distance = face.face_distance([trainData[j][1]],imgsEncode[i])
                    distList.append(distance[0])
                    match = face.compare_faces([trainData[j][1]],imgsEncode[i])
                    matchList.append(match[0])
                    
                least = distList.index(min(distList))
                if matchList[least] == True:
                    nameOf = nameList[least]
                    detectedNames.append(nameOf)
                else:
                    nameOf = "Unknown"
                cv2.rectangle(self.compairImgs[img], (loc[i][3], loc[i][0]),(loc[i][1], loc[i][2]), (255,0,255), 2)
                cv2.putText(self.compairImgs[img],nameOf,(loc[i][3]+6,loc[i][2]-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

            if self.boxFace:
                cv2.imshow(str(img),self.compairImgs[img])
                cv2.waitKey(0)
            filename = self.capturedPath+'/image'+str(img)+'.jpg'
            cv2.imwrite(filename, self.compairImgs[img])
            for n in detectedNames:
                present.add(n)
        
        year = str(datetime.now().year)
        month = str(datetime.now().month)
        month = month if len(month) == 2 else '0'+month
        day = str(datetime.now().day)
        day = day if len(day) == 2 else '0'+day
        
        currentInterval = year+'-'+month+'-'+day
        attend = pd.read_csv(self.sheetPath)
        attend[currentInterval] = a
        for name in present:
            nameIndex = attend[attend['Names'] == name].index
            attend[currentInterval][nameIndex] = p
        attend.to_csv(self.sheetPath, index=False)


# attend = VisioAttend("D:/Projects/Git/Image-Recognition/VisioAttend")
# # attend.newSpace()
# # attend.addDates(date(2023,7,14),date(2023,8,19))

# attend.webcapture(port = "http://192.168.182.187:8080/video",count = 4,left=2)

# attend.recognize()