import cv2
import unwrap
import os
import stitch
import ocr
import pytesseract


for filename in os.listdir("./images"):
    # do something with each file
    print("Working on " + filename)
    unwrapped = unwrap.unwrap("./images/" + filename)
    cv2.imwrite("./unwrapped/unwrapped_" + filename, unwrapped)
    
list = os.listdir("./unwrapped") 
for i in range(len(list)):   
    list[i] = "./unwrapped/" + list[i]
    
print(list)
result = stitch.stitch(list)
cv2.imwrite("fullLabel.jpg", result)

# Perform OCR
result_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
text = pytesseract.image_to_string(result_gray)
print(text)

o = ocr.OCR()
o.analyze("fullLabel.jpg")