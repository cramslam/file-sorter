### Liam Shaw
### 1/11/2024

import os, shutil, customtkinter, json
from customtkinter import *
from PIL import Image

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")



#root and actual main window

root = customtkinter.CTk()
root.geometry("600x365")
root.title("Gangsta File Sorter")
root.resizable(False, False)



#functions
#save function

def save_checkboxes():
    states = {f"checkbox_{i}": var.get() for i, var in enumerate(checkbox_vars)}
    with open("config.json", "w") as file:
        json.dump(states, file)
    save_button_text.set("Saved!")

def load_checkboxes():
    try:
        with open("config.json","r") as file:
            states = json.load(file)
            for i, var in enumerate(checkbox_vars):
                state = states.get(f"checkbox_{i}", False)
                var.set(state)
    except FileNotFoundError:
        pass

#file button function

def filepath(entry1):
    button_path = filedialog.askdirectory()
    entry_path = entry1.get()

    sort_button_text.set ("Sort")

    if len(entry_path) == 0:
        path = button_path
        entry1.insert(0,path)
    else:
        entry1.delete(0, "end")
        path = button_path
        entry1.insert(0,path)

#sort button function

def sort(entry1,textbox,checkbox_vars):
    entry_path = entry1.get()
    
    #input validation

    create_files = False

    if len(entry_path) != 0:
        if os.path.exists(entry_path):
            create_files = True
            path = entry_path
            sort_button_text.set ("Sorted!")

            textbox.configure(state=NORMAL)
            textbox.delete("1.0", "end")
            textbox.configure(state=DISABLED)

        else:
            create_files = False
            entry1.delete(0, "end")
            entry1.insert(0,"Invalid Path")
            sort_button_text.set ("Error!")

            textbox.configure(state=NORMAL)
            textbox.delete("1.0", "end")
            textbox.insert ("0.0", "- Enter or choose a valid file path.")
            textbox.configure(state=DISABLED)
    else:
        create_files = False
        sort_button_text.set ("No File Chosen")

        textbox.configure(state=NORMAL)
        textbox.delete("1.0", "end")
        textbox.insert ("0.0", "- Enter or choose a valid file path.")
        textbox.configure(state=DISABLED)

    #sorting

    if create_files:
        path = (path + "/")
        current_files = (os.listdir(path))
        print("Current files:", current_files)

        textbox.configure(state=NORMAL)

        for filename in file_types.items():
            folder_name = (filename[0])
            folder_path = path + folder_name
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                textbox.insert ("0.0", f"- Folder Created: {folder_name}\n")
            else:
                textbox.insert ("0.0", f"- Folder already exists: {folder_name}\n")

        textbox.configure(state=DISABLED)
 
        # Flatten file_types into a list of (folder_name, extension)
        all_extensions = [(folder, ext) for folder, exts in file_types.items() for ext in exts]

        # Get the selected extensions
        selected_extensions = [ext for (ext), ck_selected in zip(all_extensions, checkbox_vars) if ck_selected.get()]

        textbox.configure(state=NORMAL)
        # Process each file in the directory
        for file in current_files:
            for folder_name, ext in selected_extensions:
                if file.lower().endswith(ext):
                    source_path = os.path.join(path, file)
                    destination_path = os.path.join(path, folder_name, file)

                    shutil.move(source_path, destination_path)
                    textbox.insert("end", f"- Moved {ext} file: {os.path.basename(file)} to {folder_name}\n")
                    break  # Break the loop once the file is moved

        textbox.configure(state=DISABLED)
                    
          

#left panel 

frame = customtkinter.CTkFrame(master=root)
frame.grid(row= 0, column= 0, pady=(10,0), padx=(15,0), sticky = "N")

#logo
img1 = customtkinter.CTkImage(Image.open("logo1.png"), size=(175,100))
label = customtkinter.CTkLabel(master=frame, text= "", image= img1)
label.grid(row= 0, column= 0, padx=(60,0),pady= (5,0))

#text entry
entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="File Path", width=367)
entry1.grid(row= 1, column= 0, padx=(12,5), pady= (22,6))

#file button
img2 = customtkinter.CTkImage(Image.open("file3.png"), size=(20,20))
file_button = customtkinter.CTkButton(master=frame, image= img2, text="", width=1, command=lambda: filepath(entry1))
file_button.grid(row= 1, column= 1, padx=(0,12), pady= (22,6), sticky= "W")

#sort button
sort_button_text = customtkinter.StringVar()
sort_button = customtkinter.CTkButton(master=frame, textvariable=sort_button_text, command=lambda: sort(entry1,textbox,checkbox_vars))
sort_button_text.set ("Sort")
sort_button.grid(row= 2, column= 0, pady=(0,12), padx=(60,0), sticky = "N")



#right side filetype scrollbar

frame2 = customtkinter.CTkFrame(master=root)
frame2.grid(row= 0, column= 1, pady=(10,6), padx=(5,15), sticky = "N")

#file types header
label2 = customtkinter.CTkLabel(master=frame2, text="File Types", font=("Arial", 16, "bold"))
label2.grid(row= 0, column= 0, pady=(12,6), padx=12)

scrollableframe = customtkinter.CTkScrollableFrame(master=frame2, width= 103, height= 227)
scrollableframe.grid(pady=(0,6),padx= 6)

#save button
save_button_text = customtkinter.StringVar()
button2 = customtkinter.CTkButton(master=root, textvariable=save_button_text, width=135, command=save_checkboxes)
button2.grid(row= 2, column= 1, pady=(0,12), padx=(3,12), sticky= "N")
save_button_text.set("Save")



#output panel

frame3 = customtkinter.CTkFrame(master=root, width= 400, height= 75)
frame3.grid(row= 1, column= 0, padx=(15,0), sticky = "N")
frame3.place(x=15, y=216)

#log header
label3 = customtkinter.CTkLabel(master=frame3, text="Log:", font=("Arial", 12, "bold"))
label3.grid(row= 0, column= 0, padx=12, sticky = "W")

#output textbox
textbox = customtkinter.CTkTextbox(master= frame3,fg_color="#292929", width= 413, height = 83)
textbox.grid(row= 1, column= 0, padx=10, pady=(0,10), sticky = "N")
textbox.insert("insert", "- Wsg playa welcome 2 tha gangsta file sorter type shit.\n- How to use: Choose or enter the file path that you want to sort\n- Select which file type(s) you want to sort\n- Click sort and watch real gangsta shit go down")
textbox.configure(state = DISABLED)



#credit label
label4 = customtkinter.CTkLabel(master=root, text="Version 1.01 - Created by Liam Shaw", font=("Arial", 10, "bold"))
label4.grid(row= 2, column= 0, padx=12, sticky = "W")
label4.place(x=18, y=336)

#file strings

file_types = {
"Image Files": (".png",".jpg",".jpeg",".gif",".bmp",".heif",".heic",".pdn",".psd",".svg",".tif",".tiff"),
"Document Files": (".doc",".docx",".txt",".pdf",".md",".odt",".ppt",".pptx",".rtf",".xls",".xlsx"),
"Audio Files": (".mp3",".wav",".wave",".wma",".ogg",".aac",".flac"),
"Video Files": (".avi",".flv",".mov",".mp4"),
"System Files": (".dll",".drv",".ini",".tmp"),
"Compressed Files": (".zip",".rar",".jar",".7z"),
"Executable Files": (".bat",".com",".exe")
}



#checkbox stuff right side panel

checkboxes = []
checkbox_vars = []
checkbox_functions = {}
checkbox_identifiers = {}
row_number = 1
updating_checkboxes = False

#checkbox function

def checkbox_function(file_type, ck_selected):
    def inner():
        pass
    return inner

for file_label, file_extensions in file_types.items():

    #'file label' header in scrollable frame
    file_label = customtkinter.CTkLabel(master=scrollableframe, text=file_label, font=("Arial", 11, "bold"))
    file_label.grid(row=row_number, pady=(6, 0), sticky="W")

    # row_number increases for as many file extensions in tuple
    row_number += 1 + len(file_extensions)

    for file_extension in file_extensions:
        ck_selected = BooleanVar()

        #individual file extension checkbox in scrollable frame
        ckbox = customtkinter.CTkCheckBox(master=scrollableframe, text=file_extension, variable=ck_selected)
        ckbox.grid(pady=(6, 0), padx=4, sticky="W")
        checkboxes.append(ckbox)
        checkbox_vars.append(ck_selected)

        unique_key = f"{file_label}_{file_extension}"
        checkbox_identifiers[ckbox] = unique_key
        func = checkbox_function(file_extension, ck_selected)
        checkbox_functions[unique_key] = func
        ckbox.configure(command=lambda f=func: (f(), update_select_all()))

load_checkboxes()

#select all functions
        
def update_select_all():
    all_checked = all(ck_selected.get() for ck_selected in checkbox_vars)
    select_all.set(all_checked)
    save_button_text.set("Save")

def selectall():
    global updating_checkboxes
    updating_checkboxes = True
    for ckbox, ck_selected in zip(checkboxes, checkbox_vars):
        ck_selected.set(True)
        unique_key = checkbox_identifiers[ckbox]
        checkbox_functions[unique_key]()
    select_all.set(True)
    updating_checkboxes = False

def deselectall():
    global updating_checkboxes
    updating_checkboxes = True
    for ckbox, ck_selected in zip(checkboxes, checkbox_vars):
        ck_selected.set(False)
        unique_key = checkbox_identifiers[ckbox]
        checkbox_functions[unique_key]()
    select_all.set(False)
    updating_checkboxes = False

#select all checkbox
select_all = BooleanVar()
label3 = customtkinter.CTkCheckBox(master=scrollableframe, text= "Select All", variable= select_all)
label3.grid(row= 0, column= 0, pady=(6,0), padx=4)
label3.configure(command=lambda: selectall() if select_all.get() else deselectall())

root.mainloop()
