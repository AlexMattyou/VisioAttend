import cv2
from time import sleep as s
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

previous_frame = None
motion_threshold = 1200000 # Adjust this threshold based on your requirements

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # Apply Gaussian blur
    # absolute difference between the current and previous frame
    if previous_frame is not None:
        frame_diff = cv2.absdiff(previous_frame, gray)
        motion_value = cv2.sumElems(frame_diff)[0]
        # If the motion value exceeds the threshold  save the frame
        # print(motion_value)
        if motion_value > motion_threshold:
            print(motion_value)
            out.write(frame)
            print("Motion detected!")
    # Update the previous frame
    previous_frame = gray
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
