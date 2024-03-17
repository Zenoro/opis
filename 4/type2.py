import numpy as np
import main as mn
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from PIL import Image, ImageTk


def hemming_distance(x: np.array, y: np.array) -> np.array:
    """Counting Hemming distance (sum of non-equal elements)"""
    return sum(x != y)


def dict_key_from_value(myDict: dict, myValue):
    """Find key value in dictionary according to value"""
    for key, value in myDict.items():
        if value == myValue:
            return key


# def ask_image_filename(lbl, catcher_btn):
#     filetypes = (("Изображение", "*.jpg *.gif *.png"),
#                  ("Любой", "*"))
#     filename = fd.askopenfilename(title="Открыть файл",
#                                   initialdir="/",
#                                   filetypes=filetypes)
#     if filename:
#         lbl.config(text="✅")
#         filename_list.append(filename)
#         catcher_btn.config(state='disabled')

deltaa = 34


def delta_inputter():
    # global deltaa
    # deltaa = eval(delta_entry.get())
    # print(deltaa, "in function")
    delta_btn.config(state='disabled')
    # delta_entry.config(state='readonly')
    matrix_of_images.pack()
    SK_Frame.pack()


root = tk.Tk()
root.title("Массив кодовых расстояний")

delta_catcher = tk.Frame(root)
delta_catcher.pack()
# delta_txt = tk.Label(delta_catcher, text="Введите значение delta для подсчета EV")
delta_txt = tk.Label(delta_catcher, text="Запустить программу")
delta_txt.grid(row=0, column=0, sticky=tk.W)
# delta_entry = tk.Entry(delta_catcher, width=10)
# delta_entry.grid(row=0, column=1, sticky=tk.E, padx=10)
delta_btn = tk.Button(delta_catcher, text='Старт', command=delta_inputter)
delta_btn.grid(row=0, column=2, sticky=tk.W, pady=16, padx=8)

matrix_of_images = tk.Frame(root)
# matrix_of_images.grid(row=0, column=0)
# matrix_of_images.pack()

"""Takes images"""
image1 = mn.ImageToAI('image1.png')
image2 = mn.ImageToAI('image2.png')
image3 = mn.ImageToAI('image3.png')
image4 = mn.ImageToAI('image4.png')
ttk_image1 = ImageTk.PhotoImage(image1.IMAGE)
ttk_image2 = ImageTk.PhotoImage(image2.IMAGE)
ttk_image3 = ImageTk.PhotoImage(image3.IMAGE)
ttk_image4 = ImageTk.PhotoImage(image4.IMAGE)

empty_cell_put = tk.Label(matrix_of_images,
                          borderwidth=3,
                          relief="solid")
empty_cell_put.grid(row=0, column=0, sticky="nsew")

"""Insert images into frame by row"""
image1_row_put = tk.Label(matrix_of_images,
                          borderwidth=3,
                          relief="solid")
image1_row_put.config(image=ttk_image1)
image1_row_put.grid(row=0, column=1)

image2_row_put = tk.Label(matrix_of_images,
                          borderwidth=3,
                          relief="solid")
image2_row_put.config(image=ttk_image2)
image2_row_put.grid(row=0, column=2)

image3_row_put = tk.Label(matrix_of_images,
                          borderwidth=3,
                          relief="solid")
image3_row_put.config(image=ttk_image3)
image3_row_put.grid(row=0, column=3)

image4_row_put = tk.Label(matrix_of_images,
                          borderwidth=3,
                          relief="solid")
image4_row_put.config(image=ttk_image4)
image4_row_put.grid(row=0, column=4)

"""Insert images into frame by column"""
image1_col_put = tk.Label(matrix_of_images, borderwidth=3, relief="solid")
image1_col_put.config(image=ttk_image1)
image1_col_put.grid(row=1, column=0)

image2_col_put = tk.Label(matrix_of_images, borderwidth=3, relief="solid")
image2_col_put.config(image=ttk_image2)
image2_col_put.grid(row=2, column=0)

image3_col_put = tk.Label(matrix_of_images, borderwidth=3, relief="solid")
image3_col_put.config(image=ttk_image3)
image3_col_put.grid(row=3, column=0)

image4_col_put = tk.Label(matrix_of_images, borderwidth=3, relief="solid")
image4_col_put.config(image=ttk_image4)
image4_col_put.grid(row=4, column=0)

"""Input '-' in diagonal cells"""
image1_image1_txt = tk.Label(matrix_of_images, text='—',
                             font=("Arial Bold", 18),
                             borderwidth=3, relief="solid")
image1_image1_txt.grid(row=1, column=1, sticky="nsew")

image2_image2_txt = tk.Label(matrix_of_images, text='—',
                             font=("Arial Bold", 18),
                             borderwidth=3, relief="solid")
image2_image2_txt.grid(row=2, column=2, sticky="nsew")

image3_image3_txt = tk.Label(matrix_of_images, text='—',
                             font=("Arial Bold", 18),
                             borderwidth=3, relief="solid")
image3_image3_txt.grid(row=3, column=3, sticky="nsew")

image4_image4_txt = tk.Label(matrix_of_images, text='—',
                            font=("Arial Bold", 18),
                            borderwidth=3, relief="solid")
image4_image4_txt.grid(row=4, column=4, sticky="nsew")

"""Finds EVs and count Hemming distance"""
image1.create_bin_matrix(delta=41, flg=False)
image2.create_bin_matrix(delta=51, flg=False)
image3.create_bin_matrix(delta=41, flg=False)
image4.create_bin_matrix(delta=40, flg=False)
EV_image1, EV_image2, EV_image3, EV_image4 = image1.EV, image2.EV, image3.EV, image4.EV
image1_image2 = hemming_distance(EV_image1, EV_image2)
image2_image3 = hemming_distance(EV_image2, EV_image3)
image1_image3 = hemming_distance(EV_image1, EV_image3)
image4_image1 = hemming_distance(EV_image1, EV_image4)
image4_image2 = hemming_distance(EV_image2, EV_image4)
image4_image3 = hemming_distance(EV_image3, EV_image4)
distances = {image1: {image2: image1_image2, image3: image1_image3},
             image2: {image1: image1_image2, image3: image2_image3},
             image3: {image1: image1_image3, image2: image2_image3}}
# print('distances: ', image1_image2, image2_image3, image1_image3)

"""Insert Hemming distances"""
image1_image2_put = tk.Label(matrix_of_images, text=str(image1_image2),
                             font=("Arial Bold", 18),
                             borderwidth=3, relief='solid')
image1_image2_put.grid(row=1, column=2, sticky='nsew')
image2_image1_put = tk.Label(matrix_of_images, text=str(image1_image2),
                             font=("Arial Bold", 18),
                             borderwidth=3, relief='solid')
image2_image1_put.grid(row=2, column=1, sticky='nsew')

image1_image3_put = tk.Label(matrix_of_images, text=str(image1_image3),
                             font=("Arial Bold", 18),
                             borderwidth=3, relief='solid')
image1_image3_put.grid(row=1, column=3, sticky='nsew')
image3_image1_put = tk.Label(matrix_of_images, text=str(image1_image3),
                             font=("Arial Bold", 18),
                             borderwidth=3, relief='solid')
image3_image1_put.grid(row=3, column=1, sticky='nsew')

image2_image3_put = tk.Label(matrix_of_images, text=str(image2_image3),
                             font=("Arial Bold", 18),
                             borderwidth=3, relief='solid')
image2_image3_put.grid(row=2, column=3, sticky='nsew')
image3_image2_put = tk.Label(matrix_of_images, text=str(image2_image3),
                             font=("Arial Bold", 18),
                             borderwidth=3, relief='solid')
image3_image2_put.grid(row=3, column=2, sticky='nsew')
"""For 4 images"""
image1_image4_put = tk.Label(matrix_of_images, text=str(image4_image1),
                        font=("Arial Bold", 18),
                        borderwidth=3, relief='solid')
image1_image4_put.grid(row=1, column=4, sticky='nsew')

image4_image1_put = tk.Label(matrix_of_images, text=str(image4_image1),
                    font=("Arial Bold", 18),
                    borderwidth=3, relief='solid')
image4_image1_put.grid(row=4, column=1, sticky='nsew')
image2_image4_put = tk.Label(matrix_of_images, text=str(image4_image2),
                            font=("Arial Bold", 18),
                            borderwidth=3, relief='solid')
image2_image4_put.grid(row=2, column=4, sticky='nsew')

image4_image2_put = tk.Label(matrix_of_images, text=str(image4_image2),
                            font=("Arial Bold", 18),
                            borderwidth=3, relief='solid')
image4_image2_put.grid(row=4, column=2, sticky='nsew')

image3_image4_put = tk.Label(matrix_of_images, text=str(image4_image3),
                            font=("Arial Bold", 18),
                            borderwidth=3, relief='solid')
image3_image4_put.grid(row=3, column=4, sticky='nsew')

image4_image3_put = tk.Label(matrix_of_images, text=str(image4_image3),
                            font=("Arial Bold", 18),
                            borderwidth=3, relief='solid')
image4_image3_put.grid(row=4, column=3, sticky='nsew')

"""Find SK matrix"""
SK_image1 = [hemming_distance(elem, EV_image1) for elem in image1.bin_matrix]
SK_image2 = [hemming_distance(elem, EV_image2) for elem in image2.bin_matrix]
SK_image3 = [hemming_distance(elem, EV_image3) for elem in image3.bin_matrix]
"""Counting SK to neighbour"""
SK_neighbours = []
SK_para2 = []
SK_para1 = []
for choosen_image in list(distances.keys()):
    neighbour = dict_key_from_value(distances[choosen_image],
                                    min(distances[choosen_image].values()))
    SK_neighbours.append([hemming_distance(choosen_image.EV, elem)
                          for elem in neighbour.bin_matrix])
    neighbour_of_neighbour = dict_key_from_value(distances[neighbour],
                                                 min(distances[choosen_image].values()))
    SK_para1.append([hemming_distance(neighbour.EV, elem)
                     for elem in neighbour.bin_matrix])
    SK_para2.append([hemming_distance(neighbour.EV, elem)
                     for elem in neighbour_of_neighbour.bin_matrix])

"""Insert SK into the window"""
SK_Frame = tk.Frame(root)
SK_title = tk.Label(SK_Frame, text="SK & SK_PARA", font=("Arial Bold", 18))
SK_title.grid(row=0, column=0, columnspan=4)
# image 1
image1_txt = tk.Label(SK_Frame, text='Картинка 1', font=("Arial Bold", 12))
image1_txt.grid(row=1, column=0, sticky='nsew')

SK_image1_txt = tk.Label(SK_Frame, text="SK")
SK_image1_txt.grid(row=2, column=0, rowspan=2, sticky='nsew', padx=8)
SK_image1_entry1 = tk.Entry(SK_Frame, width=40)
SK_image1_entry1.insert(tk.END, ' '.join([str(i) for i in SK_image1]))
SK_image1_entry1.config(state='readonly')
SK_image1_entry1.grid(row=2, column=1, sticky=tk.W, padx=4)
SK_image1_entry2 = tk.Entry(SK_Frame, width=40)
SK_image1_entry2.insert(tk.END, ' '.join([str(i) for i in SK_neighbours[0]]))
SK_image1_entry2.config(state='readonly')
SK_image1_entry2.grid(row=3, column=1, sticky=tk.W, padx=4)

SK_PARA_image1_txt = tk.Label(SK_Frame, text='SK_PARA')
SK_PARA_image1_txt.grid(row=2, column=2, rowspan=2, sticky='nsew', padx=8)
SK_PARA_image1_entry1 = tk.Entry(SK_Frame, width=40)
SK_PARA_image1_entry1.insert(tk.END, ' '.join([str(i) for i in SK_para1[0]]))
SK_PARA_image1_entry1.config(state='readonly')
SK_PARA_image1_entry1.grid(row=2, column=3, padx=4)
SK_PARA_image1_entry2 = tk.Entry(SK_Frame, width=40)
SK_PARA_image1_entry2.insert(tk.END, ' '.join([str(i) for i in SK_para2[0]]))
SK_PARA_image1_entry2.config(state='readonly')
SK_PARA_image1_entry2.grid(row=3, column=3, padx=4)

"""
# image 2
image2_txt = tk.Label(SK_Frame, text='Картинка 2', font=("Arial Bold", 12))
image2_txt.grid(row=4, column=0, sticky='nsew')

SK_image2_txt = tk.Label(SK_Frame, text="SK")
SK_image2_txt.grid(row=5, column=0, rowspan=2, sticky='nsew')
SK_image2_entry1 = tk.Entry(SK_Frame, width=40)
SK_image2_entry1.insert(tk.END, ' '.join([str(i) for i in SK_image2]))
SK_image2_entry1.config(state='readonly')
SK_image2_entry1.grid(row=5, column=1, sticky=tk.W)
SK_image2_entry2 = tk.Entry(SK_Frame, width=40)
SK_image2_entry2.insert(tk.END, ' '.join([str(i) for i in SK_neighbours[1]]))
SK_image2_entry2.config(state='readonly')
SK_image2_entry2.grid(row=6, column=1, sticky=tk.W)

SK_PARA_image2_txt = tk.Label(SK_Frame, text='SK_PARA')
SK_PARA_image2_txt.grid(row=5, column=2, rowspan=2, sticky='nsew', padx=5)
SK_PARA_image2_entry1 = tk.Entry(SK_Frame, width=40)
SK_PARA_image2_entry1.insert(tk.END, ' '.join([str(i) for i in SK_para1[1]]))
SK_PARA_image2_entry1.config(state='readonly')
SK_PARA_image2_entry1.grid(row=5, column=3, sticky=tk.W, padx=5)
SK_PARA_image2_entry2 = tk.Entry(SK_Frame, width=40)
SK_PARA_image2_entry2.insert(tk.END, ' '.join([str(i) for i in SK_para2[1]]))
SK_PARA_image2_entry2.config(state='readonly')
SK_PARA_image2_entry2.grid(row=6, column=3, sticky=tk.W, padx=5)

# # image 3
# SK_image3_txt = tk.Label(SK_Frame, text='Картинка 3')
# SK_image3_txt.grid(row=5, column=0, sticky=tk.E, rowspan=2)
# SK_image3_entry1 = tk.Entry(SK_Frame, width=50)
# SK_image3_entry1.insert(tk.END, ' '.join([str(i) for i in SK_image3]))
# SK_image3_entry1.config(state='readonly')
# SK_image3_entry1.grid(row=5, column=1, sticky=tk.W)
# SK_image3_entry2 = tk.Entry(SK_Frame, width=50)
# SK_image3_entry2.insert(tk.END, ' '.join([str(i) for i in SK_neighbours[2]]))
# SK_image3_entry2.config(state='readonly')
# SK_image3_entry2.grid(row=6, column=1, sticky=tk.W)
"""


root.mainloop()
