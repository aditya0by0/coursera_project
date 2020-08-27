import zipfile
from PIL import Image,ImageDraw
import pytesseract
import cv2 as cv
import numpy as np
import math
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
#pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def search_text(filename,value):
    list_info=[]
    with zipfile.ZipFile(filename) as zp:
        for name in zp.namelist():
            img=Image.open(zp.open(name))
            img_str=pytesseract.image_to_string(img.convert('L'))
            if not value in img_str : continue
            dictionary={'name':name,'image':img,'text':img_str}
            list_info.append(dictionary)
    return list_info

def extract_faces(image_d,scale_factor):

    array_img=np.array(image_d.convert('L'))
    faces=face_cascade.detectMultiScale(array_img,scale_factor)

    face_img=[]
    for x,y,w,h in faces:
        face_img.append(image_d.crop((x,y,x+w,y+h)))

    col_len=5
    row_len=math.ceil(len(faces)/col_len)

    list_contact_sheet=[]
    contact_sheet=Image.new(image_d.mode,(550,110*row_len))
    x,y=0,0
    for face in face_img:
        face.thumbnail((110,110))
        contact_sheet.paste(face,(x,y))
        if x+110 >= contact_sheet.width:
            x=0
            y+=110
        else: x+=110
    return contact_sheet

def output_screen(value,zip_name,scale_factor):
    for element in search_text(zip_name,value):
        if value in element['text']:
            print(f"Results found in file {element['name']}")
            img=element['image']
            contact_sheet_ul=extract_faces(img,scale_factor)
            if contact_sheet_ul is not None:
                display(contact_sheet_ul)
            else:
                print('But there was no faces in that file')

output_screen('Mark','readonly/images.zip',1.15)
