import cv2
import numpy as np
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from matplotlib import pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import Image, ImageTk

###########################Интерфейс##################################
img_1=0
img_2=0

window = ThemedTk(theme="scidmint")
window.title("Практическая работа 8")

params_frame = ttk.Frame(window, borderwidth=1, relief=SOLID, padding=[20,43])
ttk.Label(params_frame, text="ρ:").grid(row=0, column=0, sticky=E)
ro_entery = ttk.Entry(params_frame)
ro_entery.grid(row=0, column=1)
ro_entery.insert(END, "0.45")
ttk.Label(params_frame, text="r:").grid(row=1, column=0, sticky=E)
r_entery = ttk.Entry(params_frame) 
r_entery.grid(row=1, column=1)
r_entery.insert(END, "0")
ttk.Label(params_frame, text="d:").grid(row=2, column=0, sticky=E)
d_entery = ttk.Entry(params_frame)
d_entery.insert(END, "50")
d_entery.grid(row=2, column=1)
ttk.Label(params_frame, text="Δ:").grid(row=3, column=0, sticky=E)
delta_entery = ttk.Entry(params_frame)
delta_entery.grid(row=3, column=1)
delta_entery.insert(END, "37")
ttk.Label(params_frame, text="Объект :").grid(row=4, column=0, sticky=E)
row_entery = ttk.Entry(params_frame)
row_entery.grid(row=4, column=1)
row_entery.insert(END, "[1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1]")

image_frame = ttk.Frame(window, borderwidth=1, relief=SOLID)
image_frame.pack(fill=BOTH, side=BOTTOM, expand=True)
params_frame.pack(fill=BOTH, side=TOP)

ttk.Label(image_frame, text="Первый класс").grid(row=0, column=0)
im_name_1 = ttk.Entry(image_frame)
im_name_1.grid(row=1, column=0)
im_name_1.insert(END, "image1.png")

ttk.Label(image_frame, text="Второй класс").grid(row=0, column=2)
im_name_2 = ttk.Entry(image_frame)
im_name_2.grid(row=1, column=2)
im_name_2.insert(END, "image2.png")

def image_draw():
    global img_1, img_2
    img_1 = cv2.imread(im_name_1.get(), 0) #since the image is grayscale, we need only one channel and the value '0' indicates just that
    img_2 = cv2.imread(im_name_2.get(), 0) #since the image is grayscale, we need only one channel and the value '0' indicates just that
    img_1 = cv2.resize(img_1, (100, 100))
    img_2 = cv2.resize(img_2, (100, 100))
    # cv2.imshow('Original', img)
    # cv2.waitKey(0)
    # print(img.shape[0])

    imgtk_1 = ImageTk.PhotoImage(image=Image.fromarray(img_1)) 
    imgtk_2 = ImageTk.PhotoImage(image=Image.fromarray(img_2)) 

    # Put it in the display window
    second_label = Label(image_frame, image=imgtk_1)
    second_label.image = imgtk_1
    second_label.grid(row=2, column=0, columnspan=2)

    second_label = Label(image_frame, image=imgtk_2)
    second_label.image = imgtk_2
    second_label.grid(row=2, column=2, columnspan=2)

def hamming_distance(list1, list2): 
    distance = 0
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            distance += 1
    return distance

def EV_getMax(img):
    ans = []
    for i in range(0,100):
        mat = []
        mat = list(img[:, i])
        avg_val = sum(mat)/len(mat)
        max_val = avg_val + eval(delta_entery.get()) # реализовать ввод
        min_val = avg_val - eval(delta_entery.get())
        for j in range(0, len(mat)):
            if (max_val > mat[j]) and (min_val < mat[j]):
                mat[j] = 1
            else:
                mat[j] = 0
        ans.append(mat)
    EV=[]
    p=eval(ro_entery.get())
    for i in range(0,100):
        if sum(list(ans[i]))/len(ans[i]) >= p:
            EV.append(1)
        else:
            EV.append(0)
    return EV, ans

def classifizer():
    EV1, arr1 = EV_getMax(img_1)
    EV2, arr2 = EV_getMax(img_2)
    print(arr1[4])
    ans=[]
    if (row_entery.get())!="":
        tester = eval(row_entery.get())
        mu1 = 1-(hamming_distance(tester, EV1)/eval(d_entery.get()))
        mu2 = 1-(hamming_distance(tester, EV2)/eval(d_entery.get()))
        if (max(mu1, mu2))<0:
            ans.append(0)
        elif (max(mu1, mu2)==mu1):
            ans.append(1)
        elif (max(mu1, mu2)==mu2):
            ans.append(-1)
        if sum(ans)>0:
            status_txt.configure(text="Принадлежит 1 классу")
            status_txt.grid(row=6, column=0, columnspan=2)
        elif sum(ans)<0:
            status_txt.configure(text="Принадлежит 2 классу")
            status_txt.grid(row=6, column=0, columnspan=2)
        else:
            status_txt.configure(text="Принадлежит другому классу")
            status_txt.grid(row=6, column=0, columnspan=2)
    else:
        for tester in arr1:
            mu1 = 1-(hamming_distance(tester, EV1)/eval(d_entery.get()))
            mu2 = 1-(hamming_distance(tester, EV2)/eval(d_entery.get()))
            if (max(mu1, mu2))<0:
                ans.append("0")
            elif (max(mu1, mu2)==mu1):
                ans.append("1")
            elif (max(mu1, mu2)==mu2):
                ans.append("-1")
        count_0 = 0
        for i in ans: 
            if i=="0":
                count_0+=1 
        count_1 = 0
        for i in ans: 
            if i=="1":
                count_1+=1 
        count_2 = 0
        for i in ans :
            if i=="-1":
                count_2+=1 
        if max(count_2, count_1, count_0)==count_1:
            # status_txt.destroy()
            status_txt.config(text="Принадлежит 1 классу. Точность "+str(count_1)+"%.")
            status_txt.grid(row=6, column=0, columnspan=2)            
        elif max(count_2, count_1, count_0)==count_2:
            # status_txt.destroy()
            status_txt.config(text="Принадлежит 2 классу. Точность "+str(count_2)+"%.")
            status_txt.grid(row=6, column=0, columnspan=2)
        else:
            # status_txt.destroy()
            status_txt.config(text="Принадлежит другому классу. Точность "+str(count_0)+"%.")
            status_txt.grid(row=6, column=0, columnspan=2)


img_button = ttk.Button(image_frame, text = "Выбор изображения", command=image_draw).grid(row=4, column=0)
main_button = ttk.Button(params_frame, text = "Классифицировать", command=classifizer).grid(row=5, column=0, columnspan=2)
status_txt = Label(params_frame)

window.mainloop()
