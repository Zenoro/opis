import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import new_main as mn
__import__("warnings").filterwarnings('ignore')

"""Интерфейс"""
window_frame = tk.Tk()

tk.Label(window_frame, text="Первое изображение:").grid(column=0, row=0, sticky=tk.E)
tk.Label(window_frame, text="Второе изображение:").grid(column=0, row=1, sticky=tk.E)

im_name_1 = tk.Entry(window_frame)
im_name_1.grid(column=1, row=0)
im_name_1.insert(tk.END, "image4.png")

im_name_2 = tk.Entry(window_frame)
im_name_2.grid(column=1, row=1)
im_name_2.insert(tk.END, "image3.png")

# tk.Label(window_frame, text="Введите Δ:").grid(column=0, row=2, sticky=tk.E)
# delta_name = tk.Entry(window_frame)
# delta_name.grid(column=1, row=2)
# delta_name.insert(tk.END, "22")

# tk.Label(window_frame, text="Введите p:").grid(column=0, row=3, sticky=tk.E)
# p_name = tk.Entry(window_frame)
# p_name.grid(column=1, row=3)
# p_name.insert(tk.END, "0.5")

my_img_1 = mn.ImageToAI(im_name_1.get())
my_img_1.create_bin_matrix(40, 0.6, False)
my_img_2 = mn.ImageToAI(im_name_2.get())
my_img_2.create_bin_matrix(41, 0.5, False)

first_table = tk.Frame(window_frame)
second_table = tk.Frame(window_frame)

first_table.grid(row=5, column=0, columnspan=2)
second_table.grid(row=5, column=2, columnspan=2)
"""конец описания интерфейса"""

# Список для критерия Кульбака
EK = []
# Список для критерия Шенона
ES = []

EKT = []
EST = []


# Расстояние по Хэмингу
def hemming_distance(x: np.array, y: np.array) -> np.array:
    """Counting Hemming distance (sum of non-equal elements)"""
    return sum(x != y)


# Вспомогательная функция для красоты
def Defo(r):
    return r*float(np.log2(r))


# Критерий Кульбака
def Kulbak(I, K2, K3):
    CKK = K2 + K3
    FKK = np.floor(CKK)
    return (1/I) * np.log2((2*I+10**(0)-FKK) / (FKK+10**(0))) * (I-CKK)


# Функция нахождения критерия Шеннона
def Shennon(a, b, d1, d2):
    if a + d2 != 0:
        r12 = a / (a + d2)
    else:
        r12 = 0
    if b + d1 != 0:
        r21 = b / (b + d1)
    else:
        r21 = 0
    if d1 + b != 0:
        r11 = d1 / (d1 + b)
    else:
        r11 = 0
    if d2 + a != 0:
        r22 = d2 / (d2 + a)
    else:
        r22 = 0
    return 0.5 * (Defo(r12) + Defo(r21) + Defo(r11) + Defo(r22)) + 1


def params(SK_1, SK_2):
    """Расчёт критериев"""
    T1, T2, alpha_arr, betta_arr = [], [], [], []
    for i in range(1, 101):
        K1, K2, K3, K4 = 0, 0, 0, 0
        # Находим K1
        for j in SK_1:
            if j <= i:
                K1 += 1
        # Находим K3
        for j in SK_2:
            if j <= i:
                K3 += 1
        # К2, К4
        K2 = len(SK_1) - K1
        K4 = len(SK_2) - K3
        # Прочие параметры
        alpha = K2 / len(SK_1)
        betta = K3 / len(SK_1)
        alpha_arr.append(alpha)
        betta_arr.append(betta)
        D1 = K1 / len(SK_1)
        D2 = K4 / len(SK_1)
        if D1 >= 0.5 and D2 >= 0.5:
            # Запись значений критерия Кульбака
            T1.append(Kulbak(len(SK_1), K2, K3))
        else:
            T1.append(0)
        # Запись значений критерия Шенона
        T2.append(Shennon(alpha, betta, D1, D2))
        # Заменяем все nan на 0
    T2 = [0 if i != i else i for i in T2]
    return T1, T2, alpha_arr, betta_arr


def table_1():
    """Таблица значений 1"""
    global alph_a, bett_a
    data = zip(list(range(1, 101)), EK, alph_a, bett_a)

    # Создание таблицы
    table = ttk.Treeview(first_table,
                         columns=('column1', 'column2', 'column3', 'column4'),
                         show='headings')
    table.pack(side='left', expand=True, fill='both')
    # Установка заголовков столбцов
    table.heading('column1', text="d")
    table.column('column1', width=10)
    table.heading('column2', text="Kulbak")
    table.column('column2', width=50)
    table.heading('column3', text="alpha")
    table.column('column3', width=50)
    table.heading('column4', text="beta")
    table.column('column4', width=50)
    # table.heading('column5', text="beta")
    # table.column('column5', width=50)

    verscrlbar = ttk.Scrollbar(first_table,
                               orient="vertical",
                               command=table.yview)

    verscrlbar.pack(side='right', fill='y')
    table.configure(yscrollcommand=verscrlbar.set)
    # Добавление данных в таблицу
    for x, z, alph, bet in data:
        table.insert("", 'end', values=(x, z, alph, bet))


def table_2():
    """Таблица значений 2"""
    global alph_b, bett_b
    data = zip(list(range(1, 101)), EKT, EST, alph_b, bett_b)

    # Создание таблицы
    table = ttk.Treeview(second_table,
                         columns=('column1', 'column2', 'column3', 'column4', 'column5'),
                         show='headings')
    table.pack(side='left', expand=True, fill='both')
    # Установка заголовков столбцов
    table.heading('column1', text="d")
    table.column('column1', width=10)
    table.heading('column2', text="Kulbak")
    table.column('column2', width=50)
    table.heading('column3', text="Shenon")
    table.column('column3', width=50)
    table.heading('column4', text="alpha")
    table.column('column4', width=50)
    table.heading('column5', text="beta")
    table.column('column5', width=50)

    verscrlbar = ttk.Scrollbar(second_table,
                               orient="vertical",
                               command=table.yview)
    verscrlbar.pack(side='right', fill='y')
    table.configure(yscrollcommand=verscrlbar.set)
    # Добавление данных в таблицу
    for x, y, z, alph, bet in data:
        table.insert("", 'end', values=(x, y, z, alph, bet))


def start():
    """Основная функция"""
    global EK, ES, EKT, EST, first_table, second_table, alph_a, alph_b, bett_a, bett_b
    EK, ES, EKT, EST = [], [], [], []

    # Находим аргументы для SK
    EV1, Bin1 = my_img_1.EV, my_img_1.bin_matrix
    EV2, Bin2 = my_img_2.EV, my_img_2.bin_matrix

    # Находим SK для эталонного вектора и бинарной матрицы
    SK_1, SK_2 = np.sum(Bin1 ^ EV1, axis=1), np.sum(Bin2 ^ EV1, axis=1)
    SKT_1, SKT_2 = np.sum(Bin2 ^ EV2, axis=1), np.sum(Bin1 ^ EV2, axis=1)

    EK, ES, alph_a, bett_a = params(SK_1, SK_2)
    EKT, EST, alph_b, bett_b = params(SKT_1, SKT_2)

    first_table.grid_forget()
    second_table.grid_forget()

    first_table = tk.Frame(window_frame)
    second_table = tk.Frame(window_frame)

    first_table.grid(row=5, column=0, columnspan=2)
    second_table.grid(row=5, column=2, columnspan=2)

    table_1()
    table_2()


def show():
    """Отобразить график"""
    global EK, ES, canvas1, canvas2

    fig_1 = Figure(figsize=(6, 4), dpi=100)
    ax = fig_1.add_subplot(111)
    ax.plot(list(range(1, 51)), EK[:50], "r-")#, list(range(1, 101)), ES, "g-")
    ax.plot(EK.index(max(EK))+1, max(EK), 'bx')
    # ax.plot(ES.index(max(ES))+1, max(ES), 'bx')
    ax.grid()
    canvas1 = FigureCanvasTkAgg(fig_1, master=window_frame)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=4, column=0, columnspan=2)
    window_frame.after(200, None)

    fig_2 = Figure(figsize=(6, 4), dpi=100)
    ax = fig_2.add_subplot(111)
    ax.plot(list(range(1, 101)), EKT, "r-", list(range(1, 101)), EST, "g-")
    ax.plot(EKT.index(max(EKT))+1, max(EKT), 'bx')
    ax.plot(EST.index(max(EST))+1, max(EST), 'bx')
    ax.grid()
    canvas2 = FigureCanvasTkAgg(fig_2, master=window_frame)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=4, column=2, columnspan=2)
    window_frame.after(200, None)


def hide():
    """Скрыть график"""
    global canvas1, canvas2
    if canvas1:
        canvas1.get_tk_widget().destroy()
    if canvas2:
        canvas2.get_tk_widget().destroy()


main_button = tk.Button(window_frame, text="Рассчитать", command=start).grid(row=0, column=2)
show_button = tk.Button(window_frame, text="Отобразить", command=show).grid(row=1, column=2)
hide_button = tk.Button(window_frame, text="Скрыть", command=hide).grid(row=2, column=2)

window_frame.mainloop()
