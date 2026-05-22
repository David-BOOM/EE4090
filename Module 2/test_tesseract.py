import pytesseract, cv2, glob, os
img_path = glob.glob("OCR/M2-Images/*.*")[0]
img = cv2.imread(img_path)
config = '--tessdata-dir /home/ee4090/Desktop/Day2/OCR/tessdata --dpi 300 --psm 0 --oem 1'
try:
    print(pytesseract.image_to_osd(img, config=config))
except Exception as e:
    print("Error:", e)
