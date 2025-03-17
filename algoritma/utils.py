
import cv2
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from skimage.feature import graycomatrix, graycoprops
from skimage import io, img_as_ubyte,color, transform
import skimage

def compute_gradients(image):
    """
    Menghitung gradien menggunakan Sobel operator.

    Parameters:
    - image: Citra grayscale (2D numpy array).

    Returns:
    - grad_x: Gradien di arah x.
    - grad_y: Gradien di arah y.
    - magnitude: Magnitude dari gradien.
    """
    # Menghitung gradien di arah x dan y menggunakan Sobel
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)

    # Menghitung magnitude dari gradien
    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    magnitude = np.uint8(np.clip(magnitude, 0, 255))  # Mengonversi ke uint8

    return grad_x, grad_y, magnitude

def compute_laplacian(image):
    """
    Menghitung Laplacian dari citra.

    Parameters:
    - image: Citra grayscale (2D numpy array).

    Returns:
    - laplacian: Hasil Laplacian dari citra.
    """
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    laplacian = np.uint8(np.clip(laplacian, 0, 255))  # Mengonversi ke uint8
    return laplacian

def canny_with_gradients_and_laplacian(image_path, low_threshold, high_threshold):
    """
    Menggunakan Canny Edge Detection dengan fitur gradien dan Laplacian.

    Parameters:
    - image_path: Path ke citra yang akan diproses.
    - low_threshold: Ambang batas rendah untuk Canny.
    - high_threshold: Ambang batas tinggi untuk Canny.

    Returns:
    - edges: Citra hasil deteksi tepi.
    """
    # Membaca citra dan mengonversinya menjadi grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError("Gambar tidak ditemukan di path yang diberikan.")

    # Menghitung gradien
    grad_x, grad_y, magnitude = compute_gradients(image)

    # Menghitung Laplacian
    laplacian = compute_laplacian(image)

    # Menggabungkan magnitude gradien dan Laplacian
    combined = cv2.addWeighted(magnitude, 0.5, laplacian, 0.5, 0)

    # Menggunakan Canny untuk mendeteksi tepi
    edges = cv2.Canny(combined, low_threshold, high_threshold)

    return combined, edges
  
def image_hsv(image):
  img = io.imread(image)
  hsv = color.rgb2hsv(img)
  hue, saturation, value = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
  mean_hue = np.mean(hue)
  mean_saturation = np.mean(saturation)
  mean_value = np.mean(value)

  return mean_hue,mean_saturation, mean_value



def ekstraksi_ciri(image_path):
      h, s, v = image_hsv(image_path)
      h_mean, s_mean, v_mean = np.mean(h), np.mean(s), np.mean(v)
      h_std, s_std, v_std = np.std(h), np.std(s), np.std(v)

      edges = canny_with_gradients_and_laplacian(image_path, 100, 200)[1]

      edge_count = np.sum(edges > 0)  # Jumlah piksel tepi

      # Gabungkan semua fitur menjadi satu vektor
      return [h_mean.round(2), s_mean.round(2), v_mean.round(2), h_std.round(2), s_std.round(2), v_std.round(2), edge_count]
