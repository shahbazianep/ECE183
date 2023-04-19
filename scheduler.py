from crontab import CronTab
import os.path
import time

class Scheduler():
    def run(self, quantity, daily_dose, name):
        num_days = quantity/daily_dose
        dose_hours = [] # List of Hours of when to take pill each day
        match (daily_dose):
            case 1:
                dose_hours.append(9) # Take pill at 9 AM each day
            case 2:
                dose_hours += [9, 21]
            case 3:
                dose_hours += [9, 14, 21]
            case 4:
                dose_hours += [9, 13, 17, 21]
            case 5:
                dose_hours += [5, 9, 13, 17, 21]
            case default:
                assert(False)
        local_time = time.localtime(time.time())
        hour = local_time.tm_hour
        # maybe needed depending on how we want to handle pills being put in the machine in the middle of the day
        # hours_missed = [i for i in dose_hours if i <= hour]
        # if hours_missed:
        #     num_days +=1
        self.schedule(dose_hours)
    
    def schedule(self, dose_hours):
        cron = CronTab(user=True)
        cron.remove_all()
        current_path = os.path.dirname(os.path.abspath(__file__))
        job = cron.new(command="python3 " + current_path + "Controller.py")
        job.day.every(1)
        for hour in dose_hours:
            job.hour.also.on(hour)
        cron.write()