"""Optical Character Recognition Module"""
import json
import cv2
import pytesseract

class Medication:
    def __init__(self, quantity, dosage, dosage_time, pill_type, name):
        self.name = name
        self.quantity = int(quantity)
        self.dosage = int(dosage)
        self.dosage_time = int(dosage_time)
        self.pill_type = pill_type

    def print(self):
        if self.quantity is None:
            print("QUANTITY NOT FOUND ERROR")
        else:
            print("QTY: " + self.quantity)
        print("DOSE: " + self.dosage)
        print("DAILY FREQUENCY: " + self.dosage_time)
        print("TYPE: " + self.pill_type)
        print("MEDICATION: " + self.name)


class OCR:
    def analyze(self, IMAGE_NAME):
        pytesseract.pytesseract.tesseract_cmd = \
            r'C:\Users\eshah\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

        # image = Image.open(IMAGE_NAME)
        # BW = image.convert("1", dither="None")
        img = cv2.imread("./test_images/" + IMAGE_NAME)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        string = pytesseract.image_to_string(img).lower()
        string_processed = pytesseract.image_to_string(img2).lower()

        try:
            QUANTITY = string[string.index("qty")+5:string.index("qty")+8].strip()
        except ValueError:
            try:
                QUANTITY = string[string.index("tablets")-6:string.index("tablets")-4].strip()
            except ValueError:
                QUANTITY = None
        try:
            QUANTITY = str(int(QUANTITY))
        except:
            QUANTITY = None
        if QUANTITY is None:
            try:
                QUANTITY = string_processed[string_processed.index("qty")+5:string_processed.index("qty")+8].strip()
            except ValueError:
                try:
                    QUANTITY = string_processed[string_processed.index("tablets")-6:string_processed.index("tablets")-4].strip()
                except ValueError:
                    QUANTITY = None

        for i in range(10):
            try:
                DOSAGE = string[string.index("take " + str(i)) + 5:string.index("take " + str(i))+7].strip()
            except ValueError:
                continue

        if "once" in string:
            DOSAGE_TIME = "1"
        elif "twice" in string or "2 times" in string or "two times" in string:
            DOSAGE_TIME = "2"
        elif "3 times" in string or "three times" in string:
            DOSAGE_TIME = "3"
        else:
            DOSAGE_TIME = "4"

        try:
            if string.index("tablet") > 0:
                PILL_TYPE = "tablet"
            else:
                PILL_TYPE = "capsule"
        except ValueError:
            PILL_TYPE = "unknown"

        json_file = json.load(open("database.json", encoding="UTF-8"))

        for i in json_file["results"]:
            try:
                if i["generic_name"].lower() in string_processed and \
                    string_processed[string_processed.index(i["generic_name"].lower())-1].isspace():
                    MEDICATION_NAME = i["generic_name"]
            except KeyError:
                continue

        med = Medication(quantity=QUANTITY, dosage=DOSAGE, dosage_time=DOSAGE_TIME, pill_type=PILL_TYPE, name=MEDICATION_NAME)
        return med
