from urllib.request import urlopen
import os
fileData = urlopen("https://visioattend.onrender.com/Files/temp.py")

print(fileData.readlines()[1])
# under construction

app_name = "VisioAttend"
root_path = "D:/Temp/"
required_folders = ["Codes","Data","TrainSets","TestSets"]

# creates list of folders in a given path
def create_folders(path, folders): # <str, list>
    if not os.path.exists(path):
        print('Path not found')
        root_path = input("Enter again:")
        return create_folders(root_path, ["VisioAttend"])
    log = dict()
    for folder in folders:
        folder_path = path+folder
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            log[folder] = 0
        else:
            log[folder] = 1
    return log

# prints whether the folder is created or already exists
def folder_status_log(logs): # <dict>
    for folder_log in logs:
        status = 'already exist' if logs[folder_log] else 'created'
        print(folder_log,'folder',status)

foundation = create_folders(root_path, [app_name])
folder_status_log(foundation)
sub_folders_path = root_path+'/'+app_name+'/'
sub_folders = create_folders(sub_folders_path, required_folders)
folder_status_log(sub_folders)

