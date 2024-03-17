import tkinter as tk
from tkinter import ttk
import counter as ct
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 
from tkinter import messagebox
import new_main as mn
# import tkinter.filedialog as fd


def info_adder(object:tk.Entry, some_str:str):
    object.config(state='normal')
    object.delete(0, tk.END)
    object.insert(tk.END, some_str)
    object.config(state='readonly')


def count_optimal():
    fn1 = img1_name.get()
    fn2 = img2_name.get()
    try:
        res, (delta, p, r), (EK, ES, alphaa, betaa)  = ct.criteria_grid(fn1, fn2)
    except FileNotFoundError:
        messagebox.showinfo('FileNotFoundError',
                                "Не был найден файл картинки!\nПопробуйте изменить папку запуска или измените имя текста")
    info_adder(optimal_delta, str(delta))
    info_adder(optimal_p, str(p))
    info_adder(optimal_res, "; ".join(map(str, map(lambda x: round(x, 4), *res))))
    info_adder(optimal_r, str(r))
    # show_table(EK, ES, alphaa, betaa, r)


def show_table(EK, ES, alphaa, betaa, r):
    first_table.grid(row=1, column=0, columnspan=2)
    table1(EK, ES, alphaa, betaa)
    show1(EK, ES)
    second_table.grid(row=1, column=2, columnspan=2)
    show2(r)


def table1(EK, ES, alph_a, bett_a):
    """Таблицы значений"""
    data = zip([*range(1,101)], EK, ES, alph_a, bett_a)

    # Создание таблицы
    table = ttk.Treeview(first_table,
                         columns=('column1', 'column2', 'column3', 'column4', 'column5'),
                         show='headings')
    table.pack(side='left',expand=True, fill='both')
    # Установка заголовков столбцов
    table.heading('column1', text="d")
    table.column('column1', width=25)
    table.heading('column2', text="Kulbak")
    table.column('column2', width=50)
    table.heading('column3', text="Shenon")
    table.column('column3', width=50)
    table.heading('column4', text="alpha")
    table.column('column4', width=50)
    table.heading('column5', text="beta")
    table.column('column5', width=50)

    verscrlbar = ttk.Scrollbar(first_table,
                               orient="vertical",
                               command=table.yview) 
  
    verscrlbar.pack(side='right', fill='y')   
    table.configure(yscrollcommand=verscrlbar.set) 
    # Добавление данных в таблицу
    for x, y, z, alph, bet in data:
        table.insert("", 'end',
                     values=(x, y, z, alph, bet))


def show1(EK, ES):
    """Отображение графика"""
    fig_1 = Figure(figsize=(6, 4), dpi=80)
    ax = fig_1.add_subplot(111)
    ax.plot([*range(1,101)], EK, "r-", [*range(1,101)], ES, "g-")
    ax.plot(EK.index(max(EK))+1, max(EK), 'bx')
    ax.plot(ES.index(max(ES))+1, max(ES), 'bx')
    ax.grid()
    canvas1 = FigureCanvasTkAgg(fig_1, master=root)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=2, column=0, columnspan=2, pady=8)
    root.after(200, None)


def show2(r):
    image1 = mn.ImageToAI(img1_name.get())
    image2 = mn.ImageToAI(img2_name.get())
    delt, pp = int(optimal_delta.get()), float(optimal_p.get())
    image1.create_bin_matrix(delta=delt, flg=False, p=pp)
    image2.create_bin_matrix(delta=delt, flg=False, p=pp)
    EV2 = image1.EV
    bin1, bin2 = image1.bin_matrix, image2.bin_matrix
    SKT_1 = [ct.hemming_distance(elem, EV2) for elem in bin2]
    SKT_2 = [ct.hemming_distance(elem, EV2) for elem in bin1]
    EKT, EST, alphT, betT = ct.params(SKT_1, SKT_2, r)
    fig_2 = Figure(figsize=(6, 4), dpi=80)
    ax = fig_2.add_subplot(111)
    ax.plot([*range(1,101)], EKT, "r-", [*range(1,101)], EST, "g-")
    ax.plot(EKT.index(max(EKT))+1, max(EKT), 'bx')
    ax.plot(EST.index(max(EST))+1, max(EST), 'bx')
    ax.grid()
    canvas2 = FigureCanvasTkAgg(fig_2, master=root)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=2, column=2, columnspan=2, pady=8)
    table2(EKT, EST, alphT, betT)
    root.after(200, None)


def table2(EKT, EST, alphT_a, bettT_a):
    """Таблицы значений"""
    data = zip([*range(1,101)], EKT, EST, alphT_a, bettT_a)

    # Создание таблицы
    table = ttk.Treeview(second_table,
                         columns=('column1', 'column2', 'column3', 'column4', 'column5'),
                         show='headings')
    table.pack(side='left',expand=True, fill='both')
    # Установка заголовков столбцов
    table.heading('column1', text="d")
    table.column('column1', width=25)
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
        table.insert("", 'end',
                     values=(x, y, z, alph, bet))


root = tk.Tk()
root.title("Практическая работа 6")

infobox = tk.Frame(root)
infobox.grid(row=0, column=0)
first_table = tk.Frame(root)
second_table = tk.Frame(root)


tk.Label(infobox, text="Первое изображение: ").grid(row=0, column=0, sticky=tk.E)
tk.Label(infobox, text="Второе изображение: ").grid(row=1, column=0, sticky=tk.E)
img1_name = tk.Entry(infobox, width=14)
img1_name.insert(tk.END, "image11.png")
img1_name.grid(row=0, column=1)
img2_name = tk.Entry(infobox, width=14)
img2_name.insert(tk.END, "image22.png")
img2_name.grid(row=1, column=1)

tk.Label(infobox, text="Оптимальное значение delta:").grid(row=2, column=0, sticky=tk.E)
tk.Label(infobox, text="Оптимальное значение p:").grid(row=3, column=0, sticky=tk.E)
tk.Label(infobox, text="Оптимальное значение ro:").grid(row=4, column=0, sticky=tk.E)
optimal_delta = tk.Entry(infobox, width=8, state='readonly')
optimal_delta.grid(row=2, column=1)
optimal_p = tk.Entry(infobox, width=8, state='readonly')
optimal_p.grid(row=3, column=1)
optimal_r = tk.Entry(infobox, width=8, state='readonly')
optimal_r.grid(row=4, column=1)

tk.Label(infobox, text="Полученные максимальные\nпараметры (Kulbak; Shennon):").grid(row=6,
                                                                    column=0,
                                                                    sticky=tk.E,
                                                                    pady=8)
optimal_res = tk.Entry(infobox, width=15)
optimal_res.grid(row=6, column=1, sticky=tk.W, pady=8)

count_btn = tk.Button(infobox, text= "\n".join(["Рассчитать", "оптимальные", "значения"]),
                      command=count_optimal)
count_btn.grid(row=5, column=0, columnspan=2, pady=8)

root.mainloop()
