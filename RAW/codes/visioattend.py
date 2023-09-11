import mattcode
mattcode.p = '🟢' # symbol to mark present
mattcode.a = '🔴' # symbol to mark absent
attend = mattcode.VisioAttend("C:/Users/alexm/OneDrive/Desktop/VisioAttend",600,True)

# attend.newSpace()
# from datetime import date
# attend.addDates(date(2023,7,15),date(2023,7,19))

attend.webcapture(port = "C:/Users/alexm/OneDrive/Desktop/VisioAttend/videos/v6.mp4",count = 4,left=2)
attend.recognize()
# "http://192.168.182.187:8080/video"
# "C:/Users/alexm/OneDrive/Desktop/VisioAttend/videos/v6.mp4"