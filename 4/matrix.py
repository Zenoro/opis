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

image1 = mn.ImageToAI("image1.png")
image1.create_bin_matrix(42, 0.6, False)
image2 = mn.ImageToAI("image2.png")
image2.create_bin_matrix(31, 0.5, False)
image3 = mn.ImageToAI("image3.png")
image3.create_bin_matrix(41, 0.5, False)
image4 = mn.ImageToAI("image4.png")
image4.create_bin_matrix(40, 0.6, False)


root = tk.Tk()
root.title("Массив кодовых расстояний")
matrix_of_images = tk.Frame(root)
matrix_of_images.pack()

"""Takes images"""
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
image4_col_put.config(image=ttk_image3)
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
EV_image1, EV_image2, EV_image3, EV_image4 = image1.EV, image2.EV, image3.EV, image4.EV
image1_image2 = hemming_distance(EV_image1, EV_image2)
image2_image3 = hemming_distance(EV_image2, EV_image3)
image1_image3 = hemming_distance(EV_image1, EV_image3)
image4_image1 = hemming_distance(EV_image1, EV_image4)
image4_image2 = hemming_distance(EV_image2, EV_image4)
image4_image3 = hemming_distance(EV_image3, EV_image4)

# distances = {image1: {image2: image1_image2, image3: image1_image3},
#             image2: {image1: image1_image2, image3: image2_image3},
#             image3: {image1: image1_image3, image2: image2_image3}}
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

image1_image4_put = tk.Label(matrix_of_images, text=str(image4_image1),
                        font=("Arial Bold", 18),
                        borderwidth=3, relief='solid')
image1_image4_put.grid(row=1, column=4, sticky='nsew')

image4_image1_put = tk.Label(matrix_of_images, text=str(image4_image1),
                    font=("Arial Bold", 18),
                    borderwidth=3, relief='solid')
image4_image1_put.grid(row=4, column=1, sticky='nsew')

image2_image3_put = tk.Label(matrix_of_images, text=str(image2_image3),
                            font=("Arial Bold", 18),
                            borderwidth=3, relief='solid')
image2_image3_put.grid(row=2, column=3, sticky='nsew')
image3_image2_put = tk.Label(matrix_of_images, text=str(image2_image3),
                            font=("Arial Bold", 18),
                            borderwidth=3, relief='solid')
image3_image2_put.grid(row=3, column=2, sticky='nsew')

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

root.mainloop()
