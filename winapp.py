# Импортируем все из библиотеки TKinter
from tkinter import *
import tkinter
from tkinter import ttk, filedialog as fd, messagebox

import cv2
from PIL import Image, ImageTk

root = Tk()

# Эта функция срабатывает при нажатии на кнопку "Посмотреть погоду"
def get_weather():
    # Получаем данные от пользователя
    pass

# Указываем фоновый цвет
root['bg'] = 'white'
# Указываем название окна
root.title('Image Editor by Alex Azh')
# Указываем размеры окна
root.geometry('680x450')
# Делаем невозможным менять размеры окна
root.resizable(width=False, height=False)


def AddImage():
    global labelImg1, imgOriginalName
    name = fd.askopenfilename()
    if not name or name == None or not name.endswith('.jpg'):
        messagebox.showerror('error', 'Ошибка, нужен файл .jpg')
        return
    if 'imgOriginalName' in globals():
        labelImg1.destroy()
    imgOriginal = Image.open(name)
    imgOriginalName = name
    newImage = imgOriginal.resize((300, 300))
    photo = ImageTk.PhotoImage(newImage)
    labelImg1 = tkinter.Label(image=photo)
    labelImg1.image = photo
    labelImg1.place(x=0, y=70)


def ApplyI():
    global labelImg2, save2Image, applyMethod
    from program import I_Method
    save2Image = I_Method(imgOriginalName)
    newImage = save2Image.resize((300, 300))
    photo = ImageTk.PhotoImage(newImage)
    if 'labelImg2' in globals():
        labelImg2.destroy()
    labelImg2 = tkinter.Label(image=photo)
    labelImg2.image = photo
    labelImg2.place(x=310, y=70)
    applyMethod = '_I'


def ApplyGreyWorld():
    global labelImg2, save2Image, applyMethod
    from program import GreyWorld,grayworld
    save2Image = Image.fromarray(cv2.cvtColor(grayworld(imgOriginalName), cv2.COLOR_BGR2RGB))
    newImage = save2Image.resize((300, 300))
    photo = ImageTk.PhotoImage(newImage)
    if 'labelImg2' in globals():
        labelImg2.destroy()
    labelImg2 = tkinter.Label(image=photo)
    labelImg2.image = photo
    labelImg2.place(x=310, y=70)
    applyMethod = '_GW'


def ApplyHist():
    global labelImg2, save2Image, applyMethod
    from program import HistSplit
    save2Image = Image.fromarray(cv2.cvtColor(HistSplit(imgOriginalName), cv2.COLOR_BGR2RGB))
    newImage = save2Image.resize((300, 300))
    photo = ImageTk.PhotoImage(newImage)
    if 'labelImg2' in globals():
        labelImg2.destroy()
    labelImg2 = tkinter.Label(image=photo)
    labelImg2.image = photo
    labelImg2.place(x=310, y=70)
    applyMethod='_QRGB'


def SaveFile():
    global save2Image, imgOriginalName, applyMethod
    if not 'save2Image' in globals() or 'imgOriginalName' not in globals():
        messagebox.showerror('error', "В памяти нет обработанного изображения")
        return
    if not save2Image:
        return
    name = imgOriginalName[imgOriginalName.rfind('/') + 1:imgOriginalName.rfind('.')]
    path = imgOriginalName[:imgOriginalName.rfind('/') + 1]
    save2Image.save(path + name + applyMethod+".jpg")


def CloseImage():
    # labelImg1: Label
    global labelImg1, labelImg2, save2Image
    if 'labelImg1' in globals():
        labelImg1.destroy()
    if 'labelImg2' in globals():
        labelImg2.destroy()
    if 'save2Image' in globals():
        del save2Image


frameBtn1 = Frame(root, bg='white', bd=0)
frameBtn1.place(relx=0, rely=0, relwidth=0.25, relheight=0.05)

frameBtn2 = Frame(root, bg='white', bd=0)
frameBtn2.place(relx=0.25, rely=0, relwidth=0.15, relheight=0.05)

btn1 = Button(frameBtn1, text='Открыть изображение', command=AddImage, bg='white')
btn1.pack()

btn2 = Button(frameBtn2, text='Закрыть', command=CloseImage, bg='white')
btn2.pack()

frameBtn3 = Frame(root, bg='white', bd=0)
frameBtn3.place(relx=0.5, rely=0, relwidth=0.15, relheight=0.05)
btn3 = Button(frameBtn3, text='Полутон', command=ApplyI, bg='white')
btn3.pack()

frameBtn4 = Frame(root, bg='white', bd=0)
frameBtn4.place(relx=0.65, rely=0, relwidth=0.15, relheight=0.05)
btn4 = Button(frameBtn4, text='GreyWorld', command=ApplyGreyWorld, bg='white')
btn4.pack()

frameBtn5 = Frame(root, bg='white', bd=0)
frameBtn5.place(relx=0.45, rely=0.05, relwidth=0.4, relheight=0.05)
btn4 = Button(frameBtn5, text='QRGB Эквализация гистограммы', command=ApplyHist, bg='white')
btn4.pack()

frameBtn6 = Frame(root, bg='white', bd=0)
frameBtn6.place(relx=0.15, rely=0.05, relwidth=0.15, relheight=0.05)
btn6 = Button(frameBtn6, text='Сохранить', command=SaveFile, bg='white')
btn6.pack()
root.mainloop()
