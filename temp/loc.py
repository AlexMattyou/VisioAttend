import os

# Get the directory of the current Python file
rootLoc = os.path.dirname(os.path.realpath(__file__))
imgList = []
for root, dirs, files in os.walk("D:\Projects\VisioAttend\images\students"):
    imgList = [f.split('.')[0] for f in files]
    # images\students



print(imgList)