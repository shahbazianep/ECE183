import ocr
import scheduler
import sys

# o = ocr.OCR()
# s = scheduler.Scheduler()
# if len(sys.argv) > 2:
#     sys.exit()
# m = o.analyze(sys.argv[1])
# s.run(m.quantity, m.dosage * m.dosage_time, m.name)
# m.print()

med_name = sys.argv[1]

file = open("Counter.txt", "r")


file_contents = file.readlines()
for i in range(len(file_contents)):
    if med_name in file_contents[i]:
        quantity = int(file_contents[i].split()[1])
        new_line = f"{med_name} {quantity-1}\n"
        file_contents[i] = new_line

write_file = open("Counter.txt", "w")
write_file.writelines(file_contents)
file.close()
