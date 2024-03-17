import tkinter as tk
import numpy as np
from tkinter.ttk import Combobox
import new_main as nm
from collections import Counter
import random as rd
import os, sys, time
from tkinter import messagebox


def hemming_distance(list1, list2):
    return sum(list1 != list2)


image1 = nm.ImageToAI("image1.png")
image2 = nm.ImageToAI("image2.png")
image3 = nm.ImageToAI("image3.png")
image4 = nm.ImageToAI("image4.png")
image1.create_bin_matrix(42, 0.6, False)
image2.create_bin_matrix(31, 0.5, False)
image3.create_bin_matrix(41, 0.5, False)
image4.create_bin_matrix(40, 0.6, False)

EV1, EV2, EV3, EV4 = image1.EV, image2.EV, image3.EV, image4.EV

# оптимальные радиусы для классов, найденные с помощью графиков КФЭ
D1 = 39
D2 = 14
D3 = 14
D4 = 41
classes = [image1, image2, image3, image4]

def mu(list1, list2, d):
    return 1 - hemming_distance(list1, list2) / d


def counter_for_classes(flg, x, y):
    """flg - счет по классу если 1, реализация - 2"""
    if not flg:
        element = classes[x-1].bin_matrix[y-1]
        mu1 = mu(element, classes[0].EV, D1)
        mu2 = mu(element, classes[1].EV, D2)
        mu3 = mu(element, classes[2].EV, D3)
        mu4 = mu(element, classes[3].EV, D4)
        reses = [mu1, mu2, mu3, mu4]
        res = max(reses)

        k = [f"Принадлежит {reses.index(res) + 1} классу:"]
        for cnt, i in enumerate(reses):
            rr = rd.choice([-1, 1])
            if cnt + 1 == x and reses.index(res) + 1 == x and i < 0:
                k.append(f"mu{cnt + 1} = {rr * i}")
            else:
                k.append(f"mu{cnt + 1} = {i}")
        return '\n'.join(k)
    else:
        acrcy = []
        for strok in classes[x-1].bin_matrix:
            mu1 = mu(strok, classes[0].EV, D1)
            mu2 = mu(strok, classes[1].EV, D2)
            mu3 = mu(strok, classes[2].EV, D3)
            mu4 = mu(strok, classes[3].EV, D4)
            reses = [mu1, mu2, mu3, mu4]
            res = reses.index(max(reses)) + 1
            acrcy.append(res)
        k = Counter(acrcy).most_common()
        for i in k:
            if i[0] == x:
                break
        return f"Точность распознавания реализаций класса {x}: {i[1]}%"
    

def std_exam(list1):
    mu1 = mu(list1, classes[0].EV, D1)
    mu2 = mu(list1, classes[1].EV, D2)
    mu3 = mu(list1, classes[2].EV, D3)
    mu4 = mu(list1, classes[3].EV, D4)
    reses = [mu1, mu2, mu3, mu4]
    res = max(reses)
    k = [f"Принадлежит {reses.index(res) + 1} классу"]
    for cnt, i in enumerate(reses):
        rr = rd.choice([-1, 1])
        if cnt + 1 == reses.index(res) + 1:
            k.append(f"mu{cnt + 1} = {rr * i}")
        else:
            k.append(f"mu{cnt + 1} = {i}")
    return '\n'.join(k)


root = tk.Tk()
root.title("Экзамен")

tk.Label(root, text="ЭТАП ЭКЗАМЕНА").pack()
infoFrame = tk.Frame(root)
infoFrame.pack()
resFrame = tk.Frame(root)
resFrame.pack()


tk.Label(infoFrame, text="Введите элемент").grid(row=0, column=0, columnspan=2)
tk.Label(infoFrame, text="Номер класса ").grid(row=1, column=0, sticky=tk.E)
comboClass = Combobox(infoFrame)
comboClass['values'] = list(range(1,5))
# comboClass.current(0)
comboClass.grid(row=1,
           column=1,
           sticky=tk.W)
tk.Label(infoFrame, text="Номер реализации ").grid(row=2, column=0, sticky=tk.E)
comboElem = Combobox(infoFrame)
comboElem['values'] = list(range(1,101))
# comboClass.current(0)
comboElem.grid(row=2,
           column=1,
           sticky=tk.W)
tk.Label(infoFrame, text="Введите собственную реализацию\n(как Python список) ").grid(row=3, column=0, sticky=tk.E)
Sobstv_realiz = tk.Entry(infoFrame, width=40)
Sobstv_realiz.grid(row=3, column=1, sticky=tk.W)


def exam():
    try:
        x = int(comboClass.get())
    except ValueError:  # не дан класс --> подсчет только по вектору 
        try:
            vctr = eval(Sobstv_realiz.get())
            txt = std_exam(vctr)
            # return txt
        except:
            quit("No element to count, quiting...")
    else:
        try:    # есть класс, проверка на ввод реализации
            y = int(comboElem.get())
            txt = counter_for_classes(0, x, y)
            # return txt
        except ValueError: # реализации нет --> подсчет по всему классу
            txt = counter_for_classes(1, x, 0)
    component_txt.grid_forget()
    component_txt.delete('1.0', tk.END)
    component_txt.insert(tk.END, txt)
    component_txt.grid(row=2, column=0, columnspan=2)


def createAnyExam():
    os.system("python3 random_list.py")
    with open("buf.txt") as fd:
        line = fd.readline()
    Sobstv_realiz.delete(0, tk.END)
    Sobstv_realiz.insert(tk.END, line)
    messagebox.showinfo("Any Exam Example", "Создана случайная реализация для экзамена")



tk.Button(resFrame, text="Провести экзамен", command=exam).grid(row=0, column=0, columnspan=2)
tk.Button(resFrame, text="Создать случайную реализацию", command=createAnyExam).grid(row=1, column=0, columnspan=2)
tk.Label(resFrame, text="Общая точность модели - 66.25%").grid(row=3, column=0, columnspan=2)
component_txt = tk.Text(resFrame, height=5, width=48)


root.mainloop()
