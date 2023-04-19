import ocr
import scheduler
import sys

o = ocr.OCR()
s = scheduler.Scheduler()
if len(sys.argv) > 2:
    sys.exit()
m = o.analyze(sys.argv[1])
s.run(m.quantity, m.dosage * m.dosage_time, m.name)
m.print()