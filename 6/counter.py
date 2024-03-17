import numpy as np
import math as m
import new_main as mn
import warnings
warnings.filterwarnings('ignore')


def hemming_distance(x: np.array, y: np.array) -> np.array:
    """Counting Hemming distance (sum of non-equal elements)"""
    return sum(x != y)


def true_max(kk: list[tuple], elem: tuple):
    res1, res2 = kk[0]
    if res1 <= elem[0] and res2 <= elem[1]:
        return [elem]
    else:
        return kk


def Defo(r):
    """Вспомогательная функция для красоты"""
    return r * np.log2(r)


def Kulbak(I, K2, K3, r):
    """Критерий Кульбака"""
    CKK = K2 + K3
    FKK = m.floor(CKK)
    return (1/I) * np.log2((2*I+m.pow(10, r)-FKK)/(FKK+m.pow(10,r))) * (I-CKK)


def Shennon(a, b, d1, d2):
    """Функция нахождения критерия Шеннона"""
    if (a + d2) != 0:
        r12 = a / (a + d2)
    else:
        r12 = 0
    if (b + d1) != 0:
        r21 = b / (b + d1)
    else:
        r21 = 0
    if (d1 + b)  != 0:
        r11 = d1 / (d1 + b)
    else:
        r11 = 0
    if (d2 + a) != 0:
        r22 = d2 / (d2 + a)
    else:
        r22 = 0
    return 0.5 * (Defo(r12) + Defo(r21) + Defo(r11) + Defo(r22)) + 1


def params(SK_1, SK_2, r):
    """Расчёт критериев"""
    T1, T2, alpha_arr, betta_arr = [], [], [], []
    for i in range(1,101):
        K1, K2, K3, K4 = 0, 0, 0, 0
        # Находим K1
        for j in SK_1:
            if j <= i:
                K1+=1
        # Находим K3
        for j in SK_2:
            if j <= i:
                K3+=1
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
        if (D1 >= 0.5 and D2 >= 0.5):
            # Запись значений критерия Кульбака
            T1.append(Kulbak(len(SK_1), K2, K3, r))
        else:
            T1.append(0)
        # Запись значений критерия Шенона
        T2.append(Shennon(alpha, betta, D1, D2))
        # Заменяем все nan на 0
    T2 = [0 if i != i else i for i in T2]
    return T1, T2, alpha_arr, betta_arr


def criteria_grid(filename1="image1.png", filename2="image2.png"):
    image1 = mn.ImageToAI(filename1)
    image2 = mn.ImageToAI(filename2)
    res = [(0, 0)]
    for p in np.arange(0.1, 0.9, 0.05):
        for deltt in np.arange(20, 80):
            for r in [0,-1, -2]:
                image1.create_bin_matrix(delta=deltt, flg=False, p=p)
                image2.create_bin_matrix(delta=deltt, flg=False, p=p)
                EV1, bin1 = image1.EV, image1.bin_matrix
                bin2 = image2.bin_matrix
                SK_1 = [hemming_distance(elem, EV1) for elem in bin1]
                SK_2 = [hemming_distance(elem, EV1) for elem in bin2]
                EK, ES, alphaa, betaa = params(SK_1, SK_2, r)
                newres = true_max(res, (max(EK), max(ES)))
                if newres != res:
                    params_res = (deltt, p, r)
                    resES = ES
                    resEK = EK
                    resalpha = alphaa
                    resbetaa = betaa
                    res = newres
    return res, list(map(lambda x: round(x,2), params_res)), (resEK, resES, resalpha, resbetaa)

# print(criteria_grid())
