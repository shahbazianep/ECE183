import os.path
from scheduler import Scheduler

current_path = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_path, "Pill_Dosage.txt")

with open(filename) as file:

	for line in file:
		parameters = line.split()
		if len(parameters) < 3:
			print("Error: Wrong # of parameters")
		quantity = int(parameters[0])
		dosage = int(parameters[1])
		name = parameters[2]
		scheduler = Scheduler()
		scheduler.run(quantity, dosage, name)