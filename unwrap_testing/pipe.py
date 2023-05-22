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
    
images = os.listdir("./unwrapped")
lists = [[] for _ in range(8)]

for i, image in enumerate(images):
    for j in range(8):
        lists[j].append("./unwrapped/" + images[(i + j) % len(images)])

results = [[] for _ in range(8)]
for i, image_list in enumerate(lists):
    results[i] = stitch.stitch(image_list)
    cv2.imwrite(f"fullLabel{i}.jpg", results[i])

for i, result_list in enumerate(results):
    # Perform OCR
    result_gray = cv2.cvtColor(results[i], cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(result_gray)
    print(text)

# o = ocr.OCR()
# o.analyze("fullLabel.jpg")