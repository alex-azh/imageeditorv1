from PIL import Image, ImageDraw
import numpy as np
import cv2

def I_Method(name: str):
    "I - Преобразование цветного изображения в полутоновое (по формуле I=(R+G+B)/3)"
    image = Image.open(name)
    draw = ImageDraw.Draw(image)
    w, h = image.size
    pix = image.load()
    for i in range(w):
        for j in range(h):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            draw.point((i, j), (S, S, S))
    return image


def GreyWorld(imageName):
    "GW - Автоматический баланс белого посредством алгоритма GreyWorld"
    image = cv2.imread(imageName)
    b, g, r = cv2.split(image)
    # avg calculating...
    r_avg = cv2.mean(r)[0]
    g_avg = cv2.mean(g)[0]
    b_avg = cv2.mean(b)[0]
    avg = (b_avg + g_avg + r_avg) / 3
    r_k = avg / r_avg
    g_k = avg / g_avg
    b_k = avg / b_avg
    # creating...
    r = (r * r_k).clip(0, 255)
    g = (g * g_k).clip(0, 255)
    b = (b * b_k).clip(0, 255)
    image = cv2.merge([b, g, r]).astype(np.uint8)
    return image


def HistSplit(pictureName):
    "QRGB - Эквализация гистограммы (для каждого цветового слоя независимо)"
    img = cv2.imread(pictureName)
    g = img[:, :, 0]
    b = img[:, :, 1]
    r = img[:, :, 2]
    hist_r, bins_r = np.histogram(r, 256)
    hist_g, bins_g = np.histogram(g, 256)
    hist_b, bins_b = np.histogram(b, 256)
    cdf_r = hist_r.cumsum()
    cdf_g = hist_g.cumsum()
    cdf_b = hist_b.cumsum()
    cdf_r = (cdf_r - cdf_r[0]) * 255 / (cdf_r[-1] - 1)
    cdf_r = cdf_r.astype(np.uint8)
    cdf_g = (cdf_g - cdf_g[0]) * 255 / (cdf_g[-1] - 1)
    cdf_g = cdf_g.astype(np.uint8)
    cdf_b = (cdf_b - cdf_b[0]) * 255 / (cdf_b[-1] - 1)
    cdf_b = cdf_b.astype(np.uint8)
    r2 = cdf_r[r]
    g2 = cdf_g[g]
    b2 = cdf_b[b]
    img2 = img.copy()
    img2[:, :, 0] = g2
    img2[:, :, 1] = b2
    img2[:, :, 2] = r2
    return img2
