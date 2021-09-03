import cv2
import pytesseract
import skimage.exposure
import numpy as np

# Подключение фото
img = cv2.imread('12.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
img = cv2.filter2D(img, -1, kernel)


cv2.imshow('12', img)
cv2.waitKey(0)
cv2.imwrite('12.jpg', img)

# Будет выведен весь текст с картинки
config = r'--oem 3 --psm 6'
print(pytesseract.image_to_string(img, lang='rus', config=config))
