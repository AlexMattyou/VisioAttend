from VIAmodule import *

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