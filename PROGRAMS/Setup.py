from urllib.request import urlopen
import customtkinter as ctk
from PIL import Image
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()

width, height = 600, 400
x_center = int((window.winfo_screenwidth() / 2) - (width / 2))
y_center = int((window.winfo_screenheight() / 2) - (height / 2))
window.geometry(f'{width}x{height}+{x_center}+{y_center}')

window.title("Setup Visio-Attend")
window.resizable(1,1)

# frame = ctk.CTkFrame(window, width=1500, height=650, fg_color='red')
# frame.place(anchor='center')

img = Image.open("C:/Users/alexm/OneDrive/Desktop/logo/dark0020.png")
photo = ctk.CTkImage(dark_image=img, light_image=img,size=(width, height - 100))
label = ctk.CTkLabel(window, image = photo, width = 2000, height = 0, text='')
label.pack(anchor=ctk.N)


setup_box = ctk.CTkFrame(window, width = 580, height=90, fg_color="transparent")
setup_box['padding'] = 10
setup_box.columnconfigure(0, weight=2)
setup_box.columnconfigure(1, weight=10)
setup_box.pack()

def open_file_manager():
    folder_selected = ctk.filedialog.askdirectory()
    print(folder_selected)

b2 = ctk.CTkButton(setup_box,border_width= 0, text ='Choose',font = ("Helvetica",15),width = 30, height = 30, command=open_file_manager, corner_radius = 3)
b2.grid(column = 0, row= 0)
install_path = ctk.StringVar()
install_path.set(os.getcwd())
path_entry = ctk.CTkEntry(setup_box, textvariable=install_path, corner_radius = 3,height = 30, width=300)
path_entry.grid(column = 1, row= 0)
path_entry.focus()
b = ctk.CTkButton(window, text ='Download',font = ("Helvetica",25), command=lambda: print(install_path.get()), corner_radius = 5)
b.pack(pady = 10)


window.mainloop()
