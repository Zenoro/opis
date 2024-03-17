import tkinter as tk
import tkinter.filedialog as fd
from PIL import Image, ImageTk
import numpy as np
from tkinter import messagebox
import os
# [::10,::10]


def txt_maker(arr: list, tk_text_obj: tk.Text):
    for elem in arr:
        tk_text_obj.insert(tk.END, ' '.join([str(i) for i in elem])+'\n')


class ImageToAI():
    def __init__(self, path_name, cropsize=(100, 100)) -> None:
        """Create class' object with image matrix"""
        self.PATH = path_name
        self.IMAGE = Image.open(self.PATH).resize((cropsize))
        self.image_matrix = np.array(self.IMAGE.convert('L'))  # .T

    def create_bin_matrix(self, delta: float, p: float, flg: bool) -> tuple[int]:
        """Create binary matrix and VDK/NDK according to input delta"""
        self.VDK = np.round(np.mean(self.image_matrix, axis=0) + abs(delta), 5)
        self.NDK = np.round(self.VDK - 2 * abs(delta), 5)
        self.NDK[np.where(self.NDK < 0)] = 0
        vm, nm = self.image_matrix <= self.VDK, self.image_matrix >= self.NDK
        self.bin_matrix = np.array(vm * nm).astype(int)
        self.EV = (np.mean(self.bin_matrix, axis=0) >= p).astype(int)
        if flg:
            return self.VDK, self.NDK

    def image_from_bin_matrix(self, file_name='out.png', is_saving=1) -> None:
        """Create binary image from binary matrix"""
        img = Image.new('1', (100, 100))
        pixels = img.load()
        for i in range(100):
            for j in range(100):
                pixels[i, j] = int(self.bin_matrix[i, j])
        img.save(file_name)


class Ex(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ОПИС")
        initial_frame = tk.Frame(self)
        initial_frame.grid(row=0, column=0, columnspan=2)
        self.btn_file = tk.Button(initial_frame, text="Выбрать файл",
                                  command=self.choose_file)
        self.btn_file.grid(row=0, column=0, padx=10, pady=10)
        self.del_but = tk.Button(initial_frame, text="Удалить фото",
                                 command=self.deleter)
        self.del_but.grid(row=0, column=1, padx=10, pady=10)

    def choose_file(self):
        """Выбор файла"""
        filetypes = (("Изображение", "*.jpg *.gif *.png"),
                     ("Любой", "*"))
        self.filename = fd.askopenfilename(title="Открыть файл",
                                           initialdir="/",
                                           filetypes=filetypes)
        if self.filename:
            self.create_img_matrix()

    def create_img_matrix(self):
        """Отображение изображения и матрицы этого изображения"""
        self.btn_file.config(state='disabled')
        self.input_image = ImageToAI(self.filename)
        # вставка изображения
        self.image = ImageTk.PhotoImage(self.input_image.IMAGE)
        self.first_task = tk.Frame(self)
        self.first_task.grid(row=1, column=0, padx=10)
        self.image_sprite = tk.Label(self.first_task)
        self.image_sprite.configure(image=self.image, pady=16)
        self.image_sprite.grid(row=0, column=0, columnspan=2)
        # вставка чисел
        image_matrix_text = tk.Text(self.first_task, wrap=tk.WORD, width=39, height=10)
        image_matrix_text.grid(row=1, column=0, columnspan=2, )
        txt_maker(self.input_image.image_matrix[::10, ::10], image_matrix_text)
        self.binary_matrix()

    def binary_matrix(self):
        """Запрос ввода delta, ввод кнопки подсчета бинарной матрицы и изображения"""
        self.second_task = tk.Frame(self)
        self.second_task.grid(row=1, column=1, padx=10)
        delta_txt = tk.Label(self.second_task, text="delta:")
        delta_txt.grid(row=0, column=0, sticky=tk.E)
        self.delta_ctch = tk.Entry(self.second_task, width=10)
        self.delta_ctch.grid(row=0, column=1, sticky=tk.W)
        start_btn = tk.Button(self.second_task, text="Построить бинарную матрицу \nи отображение",
                              command=self.create_binary_matrix)
        start_btn.grid(row=1, column=0, columnspan=2)

    def create_binary_matrix(self):
        """Отображение бинарного изображения и бинарной матрицы"""
        try:
            delta = eval(self.delta_ctch.get())
        except:
            messagebox.showinfo('Ошибка',
                                "Вы не ввели необходимые параметры или передали их неверно.")
            return
        VDK, NDK = self.input_image.create_bin_matrix(delta, flg=True)
        """Добавляем VDK"""
        VM_txt = tk.Label(self.second_task, text="Матрица значений VDK")
        VM_txt.grid(row=2, column=0, columnspan=2)
        VM_values = tk.Entry(self.second_task, width=50)
        VM_values.insert(tk.END, ' '.join([str(i) for i in VDK[::10]]))
        VM_values.config(state='readonly')
        VM_values.grid(row=3, column=0, columnspan=2)
        """Добавляем NDK"""
        NM_txt = tk.Label(self.second_task, text="Матрица значений NDK")
        NM_txt.grid(row=4, column=0, columnspan=2)
        NM_values = tk.Entry(self.second_task, width=50)
        NM_values.insert(tk.END, ' '.join([str(i) for i in NDK[::10]]))
        NM_values.config(state='readonly')
        NM_values.grid(row=5, column=0, columnspan=2)
        """Добавляем бинарную матрицу"""
        bin_shower = tk.Text(self.second_task, width=20, height=10)
        bin_shower.grid(row=6, column=0, columnspan=2)
        txt_maker(self.input_image.bin_matrix[::10, ::10], bin_shower)
        """Добавляем бинарное изображение"""
        self.input_image.image_from_bin_matrix()
        new_image = Image.open('out.png')

        self.bin_image = ImageTk.PhotoImage(new_image)
        self.bin_img_put = tk.Label(self.second_task)
        self.bin_img_put.configure(image=self.bin_image, pady=16)
        self.bin_img_put.grid(row=7, column=0, columnspan=2)
        """Добавляем эталонный вектор"""
        EV_shower_txt = tk.Label(self.second_task, text="Эталонный вектор")
        EV_shower_txt.grid(row=8, column=0, columnspan=2)

        EV_shower_entry = tk.Entry(self.second_task, width=17)
        EV_shower_entry.grid(row=9, column=0, columnspan=2)
        EV_shower_entry.insert(tk.END, ' '.join(map(str, self.input_image.EV[::10])))
        EV_shower_entry.config(state='readonly')

    def deleter(self):
        """Удаление всех окон"""
        self.btn_file.config(state='normal')
        self.first_task.destroy()
        self.second_task.destroy()
        try:
            os.remove('out.png')
        except:
            pass


if __name__ == "__main__":
    main = Ex()
    main.mainloop()
