############# Importation 
from ast import arg
from concurrent.futures import process
from tabnanny import verbose
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL
from os import listdir
from glob import glob
import os
from turtle import update
from PIL import Image, ImageTk
from DicomRTTool import DicomReaderWriter
import SimpleITK as sitk
import pydicom as dicom
import pandas as pd
import glob
from tqdm import tqdm
import cv2
from PIL import Image
import csv as csv_lib
import pydicom
import threading
import sys
import multiprocessing 
from multiprocessing import Process
import joblib
from joblib import Parallel, delayed
from tqdm.gui import tqdm_gui
from tkinter import ttk
import threading
from tkinter import _tkinter


global in_path_dicom_nifti
global convert_save
global root
############# page 1 : Home page 
def call_home_page():
    root.geometry('600x750')
    home_page = Frame(root, bg=bg)
    home_page.grid(row=0, column=0, sticky='nsew')
    title = Label(home_page, text='Abys Medical Converter', bg=bg, fg='Black', font='Arial 30 ')
    title.pack(pady=(20,0))
    image = Image.open('utils/image.png')
    image=image.resize((350,150))
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image = photo)
    label.image = photo
    #root.configure(background='white')
    label.grid(row=1,column=0)
    buttons_frame = Frame(home_page, bg=bg)
    buttons_frame.pack( padx=10,pady=40)

    dicom_to_nifti_button = Button(buttons_frame, text='Dicom\nto\nNIfTI', font='none 20 bold', width=15, bg='black',fg='white', command=dicom_to_nifti_page)
    dicom_to_nifti_button.pack(pady=(80,0))

############# page 2 : Dicom to nifti page 
def dicom_to_nifti_page():
    global text_message_d_n
    global convert_save
    global progress_bar
    root.geometry('600x750')
    dicom_to_nifti = Frame(root, bg=bg)
    dicom_to_nifti.grid(row=0, column=0, sticky='nsew')

    title = Label(dicom_to_nifti, text='Dicom to Nifti', bg='black',fg='white', font='Arial 15 bold')
    title.pack()

    open_buttons = Frame(dicom_to_nifti, bg=bg)
    open_buttons.pack(pady=(30,0))

    open_file = Button(open_buttons, text='Open file', font='none 20 bold', width=10, bg='coral',fg='black', command=call_open_file_dicom_to_nifti)
    open_file.grid(row=0, column=0, padx=(0,20))

    open_dir = Button(open_buttons, text='Open Dirs', font='none 20 bold', width=10, bg='coral',fg='black', command=call_open_dir_dicom_to_nifti)
    open_dir.grid(row=0, column=1, padx=(20,0))

    convert_save = Button(dicom_to_nifti, text='Convert & Save', state = NORMAL , font='none 20 bold', bg='coral',fg='black', command=call_convert_save_dicom_to_nifti)
    convert_save.pack(pady=(40,0))


    text_message_d_n = Label(dicom_to_nifti,text='Choose file or dir', font='none 9', bg='coral',fg='black')
    text_message_d_n.pack(pady=(20,0))

    progress_bar = ttk.Progressbar(root, mode='determinate', length=260)
    progress_bar.place(x=170, y=350)

    home_button = Button(dicom_to_nifti, text='Home', command=call_home_page, font='none 20 bold', width=15, bg='black',fg='white')
    home_button.place(x=170, y=450)

    home_button = Button(dicom_to_nifti, text='Restart', command=restart, font='none 20 bold', width=15, bg='black',fg='white')
    home_button.place(x=170, y=510)
    #home_button.pack(pady=(60,0))

############# page 2 : Functions to open dicom files            



# def _start_thread():
#           p1 = threading.Thread(target=call_convert_save_dicom_to_nifti())
#           p1.start()
  

def call_open_file_dicom_to_nifti():
    global flag_dicom_nifti
    global in_path_dicom_nifti
    global text_message_d_n
    in_path_dicom_nifti = filedialog.askdirectory()
    if in_path_dicom_nifti: 
        flag_dicom_nifti = 1
        text_message_d_n.config(text='You opened: \n' + in_path_dicom_nifti)
    else:
       messagebox.showerror("Error", "try again")

def call_open_dir_dicom_to_nifti():
    global flag_dicom_nifti 
    global in_path_dicom_nifti
    global text_message_d_n
    global file
    in_path_dicom_nifti = filedialog.askdirectory()
    # in_path_dicom_nifti=manager.Value(any,in_path_dicom_nifti)
    if in_path_dicom_nifti:
        flag_dicom_nifti = 2
        text_message_d_n.config(text='You opened: \n' + in_path_dicom_nifti) 
    else:
        messagebox.showerror("Error", "try again")    
 
############# page 2 : Functions to convert dicom files
def call_convert_save_dicom_to_nifti():
    global progress_bar
    global image
    global images
    global out_path
    global file
    global convert_save
    global root
    global num_files
    global text_message_d_n
    if flag_dicom_nifti == 1 and in_path_dicom_nifti:
        out_path = filedialog.asksaveasfilename()
        text_message_d_n.config(text='Conversion...')
        if out_path:
            reader = DicomReaderWriter()
            reader.walk_through_folders(in_path_dicom_nifti)
            reader.get_images()
            sitk.WriteImage(reader.dicom_handle, out_path + '.nii.gz')
            text_message_d_n.config(text='Conversion is finished\n'+'File saved at\n' + out_path + '.nii.gz')
            
    if flag_dicom_nifti == 2 and in_path_dicom_nifti:
        images =[f.path for f in os.scandir(in_path_dicom_nifti) if f.is_dir()]
        out_path = filedialog.askdirectory()
        print (out_path)
        num_files = sum([True for f in os.scandir(in_path_dicom_nifti) if f.is_dir()])
        print(num_files)
        if out_path : 
            convert_save['state'] = DISABLED             
            def pa():
              nonlocal result
              result=Parallel(n_jobs=-2, backend='threading')(delayed(fonct)(image, out_path) for i, image in (enumerate(images))) 
            
            result = None
            progress_bar['maximum'] = num_files  # number of items that loops in Parallel
            
            process = threading.Thread(target=pa)
            process.start()
            """
            update progress bar
            """

            while progress_bar['value'] < num_files+1:
               progress_bar['value'] = n
               percentage = round(float(float(n)/float(num_files)*100), 2) #calculate the percentage
               t = "Converting..."+" | Progress: "+str(n)+"/"+str(num_files)+" | Percentage: "+str(percentage)+"%"
               progr = tk.Label(root, text=t, font='none 12', bg='black',fg='white')
               progr.grid(row=0, column=0)
               root.update_idletasks()
            # root.update()# prevent freezin
            # process.join()
            # progr.destroy()
            text_message_d_n.config(text='Conversion is finished\n'+'Files saved at\n' + out_path)
            progress_bar.destroy()
            convert_save['state'] = NORMAL
            # process.join()
        else:
                 messagebox.showerror("Error", "try again")
n=0
def fonct(k, out_path):
    global n
    reader = DicomReaderWriter()
    reader.walk_through_folders(k)
    reader.get_images()
    sitk.WriteImage(reader.dicom_handle, out_path + '/' + os.path.basename(k) + '.nii.gz') 
    n=n+1      

def restart():
    os.execv(sys.executable, ['python'] + sys.argv)

############# page 2 : Function to extract csv file                
# def meta () :
#     folder_path = in_path_dicom_nifti
#     out_path = filedialog.asksaveasfilename()
#     images_path = os.listdir(folder_path)
#     metadata=[]
#     data = []
#     columns_list = ['Patient_ID' , 'Sex' , 'Birth_date' , 'Age' , 'Modality' , 'Manufacturer' , 'Institution_Name' , 'Study_Description' , 'Slice_Thickness']
#     text_message_d_n.config(text='Extracting...')
#     for i in tqdm(range(len(images_path))):
#        t = os.listdir(folder_path+'/'+images_path[i])
#        img_path = folder_path+'/'+images_path[i]+'/'+t[1]
#        ds = pydicom.filereader.dcmread(img_path)
#        print(ds)
#        data.append([ds.PatientID, ds.PatientSex, ds.PatientBirthDate, ds.PatientAge[:-1], ds.Modality, ds.Manufacturer.replace(" ","_"), ds.InstitutionName.replace(" ","_"), ds.StudyDescription.replace(" ","_"), ds.SliceThickness])
#     with open(out_path, 'w', encoding='UTF8', newline='') as f:
#        writer = csv_lib.writer(f, delimiter = ";")
#        writer.writerow(columns_list)
#        writer.writerows(data) 
#        text_message_d_n.config(text='Files saved at\n' + out_path)


############# The main function 
if __name__ == '__main__':
    multiprocessing .freeze_support()
    bg = 'white'
    root = Tk()
    root.geometry('600x750')
    root.title('Abys Converter')
    root.iconbitmap('utils/logo.ico')
    root.resizable(width=0, height=0)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    call_home_page()
    root.mainloop()
    
    
