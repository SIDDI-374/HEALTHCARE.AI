import time
from database import get_medications

def start_reminder_service():

    while True:

        current_time = time.strftime("%H:%M")

        meds = get_medications()

        for med in meds:

            name,time_med = med

            if current_time == time_med:
                print(f"Reminder: Take {name}")

        time.sleep(60)
