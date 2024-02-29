import cv2

def capture(port = 0, step=(0, 500000), threshold = 'auto', memory = 200, kernel = 5):
    if threshold == 'auto':
        threshold = 100000
    preFrame = None
    cap = cv2.VideoCapture(port)
    count = 0
    history = []
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
                if len(history) > memory:
                    history.pop(0)
                motionMean =sum(history)/len(history)
                threshold = round(motionMean * 2.5)
                if ((motion > threshold) or (count >= step[1]))and count >= step[0]:
                    # print(count '     ' threshold  '     '  motion)
                    count = 0
                    cv2.imwrite('output_image.jpg', frame)
                    print('Running')
            # Update the previous frame
            preFrame = gray
        # cv2.imshow('Frame'  frame)
    cap.release()
capture(port = "http://192.168.101.176:8080/video")