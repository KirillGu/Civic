from PIL import Image
import pytesseract
import cv2
import os
from skimage.filters import threshold_local

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

base_dir = os.path.dirname(os.path.abspath(__file__))
image = base_dir + r'/tmp/233.jpg'
d = Image.open(image)
preprocess = "thresh"

# загрузить образ и преобразовать его в оттенки серого
image = cv2.imread(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


#проверьте, следует ли применять пороговое значение для предварительной обработки изображения

if preprocess == "thresh":
    gray = cv2.threshold(gray, 100, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #gray = threshold_local(gray, 25, offset=195, method="gaussian")
    gray = cv2.adaptiveThreshold(gray, 155, 1, 1, 7, 2)
    gray = cv2.bitwise_not(gray)
    gray = cv2.medianBlur(gray, 3)

    # cv2.imshow("Contour Outline", gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

# если нужно медианное размытие, чтобы удалить шум
elif preprocess == "blur":
    gray = cv2.medianBlur(gray, 3)

    # gray = threshold_local(image, 25, offset=15, method="gaussian")
    # cv2.imshow("Contour Outline", gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

# сохраним временную картинку в оттенках серого, чтобы можно было применить к ней OCR
filename_dir = base_dir +"\gray\{}.png".format(os.getpid())
cv2.imwrite(filename_dir, gray)


# загрузка изображения в виде объекта image Pillow, применение OCR, а затем удаление временного файла
config_ru = r' -c tessedit_char_whitelist=АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
config_eng = r''
text = pytesseract.image_to_string(Image.open(filename_dir), lang='rus', config=config_ru).replace('\n\x0c', '')
print(text)
os.remove(filename_dir)

# показать выходные изображения
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.imshow("Output", gray)
cv2.waitKey(0)
