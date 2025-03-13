import schedule
import time
import Update_code_logic # imported from Update_code_logic.py
from Update_code_logic import update_table

#schedule.every().day.at("17:50").do(update_table)

schedule.every(3).seconds.do(update_table)

while True:
    schedule.run_pending()
    #time.sleep(15)
