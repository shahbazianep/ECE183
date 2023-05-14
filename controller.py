import ocr
import scheduler
import sys
import json

# o = ocr.OCR()
# s = scheduler.Scheduler()
# if len(sys.argv) > 2:
#     sys.exit()
# m = o.analyze(sys.argv[1])
# s.run(m.quantity, m.dosage * m.dosage_time, m.name)
# m.print()

med_name = sys.argv[1]

with open("Counter.json", "r") as file:
    data = json.load(file)
    med_list = data["medications"]
    for medications in med_list:
        if medications["name"] == med_name:
            medications["quantity"] -= 1

with open("Counter.json", "w") as file:
    json.dump(data, file, indent=2, sort_keys=True)