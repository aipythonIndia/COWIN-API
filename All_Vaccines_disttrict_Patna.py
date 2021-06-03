"""
Developer: aipython
Email: aipython.india@gmail.com
website: www.aipython.in
"""

import requests
from datetime import datetime, timedelta
import pytz
import time
from os import environ

# Authentication and Telegram group detail
tele_auth_token = environ['Tele_auth_tok']
tel_group_id = "cowin_danapur_vaccine"
Dist_ID = "097" # For Patna (Bihar)

# Date calculation - Today and tomorrow
time_interval = 30 # (in seconds) Specify the frequency of code execution
header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}

def update_date_time():
    print ("Updating date and Time ..")
    IST = pytz.timezone('Asia/Kolkata')
    raw_TS = datetime.now(IST) + timedelta(days=1) # One day ahead
    tomorrow_date = raw_TS.strftime("%d-%m-%Y")
    today_date = datetime.now(IST).strftime("%d-%m-%Y") #Current Date
    curr_time = (datetime.now(IST).strftime("%H:%M:%S")) # Current time
    return today_date, tomorrow_date, curr_time

def refresh_api_call(Dist_ID, tomorrow_date):
    print ("Refreshing API call with updated parameters ...")
    request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={Dist_ID}&date={tomorrow_date}"
    # print (request_link)
    response = requests.get(request_link, headers = header)
    raw_JSON = response.json()
    return raw_JSON

sent_dates_record  = [] # List of dates for age group 45+ for which one round of message has been sent
num_times_msg_sent = 0  # Number of times messages has been sent on Telegram

def send_msg_on_telegram(msg, today_date):
    print ("Sending Messege of Telegram ....")
    telegram_api_url = f"https://api.telegram.org/bot{tele_auth_token}/sendMessage?chat_id=@{tel_group_id}&text={msg}"
    
    tel_response = requests.get(telegram_api_url)
    if tel_response.status_code == 200:
        print (f"[{today_date}-{curr_time}] : Notification has been sent on Telegram")
    else:
        print ("Could not send Message .. some problem while sending msg on Telegram")
    # add_dates_in_record(today_date)

    
def get_availability_for_45(age_limit, available_capacity):
    # print ("Checking availability for Age 45 and above")
    if (age_limit == 45) and (available_capacity > 0):
        msg = f"""Vaccine AVAILABLE\n[For age 45+] at Pincode: {pincode}\nCenter: {center_name} on {slot_date}\nVaccine: {vaccine_name}\nDose_1: {qnty_dose_1}\nDose_2: {qnty_dose_2}\n\nRegistration link: https://selfregistration.cowin.gov.in/"""
        
        if str(today_date) not in sent_dates_record:
            send_msg_on_telegram(msg, today_date)
            # print (msg) # For local testing
        else:
            print (f"One round of messages has already been sent for age 45+ today {today_date}")
    # else:
        # print (f"Checked at [{today_date}-{curr_time}] : No Vaccine Slots for 45+ available for {tomorrow_date}")
        
        
def get_availability_for_18(age_limit, available_capacity):
    # print ("Checking availability for Age 18 to 44")
    if (age_limit == 18) and (available_capacity > 0):
        msg = f"""Vaccine AVAILABLE\n[For age 18+] at Pincode: {pincode}\nCenter: {center_name} on {slot_date}\nVaccine: {vaccine_name}\nDose_1: {qnty_dose_1}\nDose_2: {qnty_dose_2}\n\nRegistration link: https://selfregistration.cowin.gov.in/"""
        
        if str(today_date) not in sent_dates_record:
            send_msg_on_telegram(msg,today_date)
            # print (msg) # For local testing
        else:
            print (f"One round of messages has already been sent for age 18+ today {today_date}")
    # else:
        # print (f"Checked at [{today_date}-{curr_time}] : No Vaccine Slots for 18+ available for {tomorrow_date}")

num_iterations = 0
while True:
    num_iterations += 1
    today_date, tomorrow_date, curr_time = update_date_time()
    raw_JSON = refresh_api_call(Dist_ID, tomorrow_date)
    sess_len = len(raw_JSON['sessions'])
    print (f"INFO [{today_date}-{curr_time}] : Checking for VACCINES availabilities on the Portal")
    # print (f"Total {len(raw_JSON['sessions'])} centers found")
    if sess_len > 0:
        for sess in raw_JSON['sessions']:
            age_limit           = sess['min_age_limit']
            center_name         = sess['name']
            pincode             = sess['pincode']
            vaccine_name        = sess['vaccine']
            available_capacity  = sess['available_capacity']
            qnty_dose_1         = sess['available_capacity_dose1']
            qnty_dose_2         = sess['available_capacity_dose2']
            slot_date           = sess['date']
            
            get_availability_for_45(age_limit, available_capacity)
            get_availability_for_18(age_limit, available_capacity)
            
        # Update the dates in the list after sending one complete round of messages
        if str(today_date) not in sent_dates_record:
            sent_dates_record.append(str(today_date))
        # sent_dates_record_18.append(str(today_date))
        
        time.sleep(time_interval)
    else:
        print (f"ERROR [{today_date}-{curr_time}] : No Information available on COWIN server.. looks like no Sessions")
        # print (f"One message has already been sent Today {today_date}")
        # print (f"Total message sent is {num_times_msg_sent}")
        
    print (f"INFO : Total Number of times this code has checked CoWIN portal is: {num_iterations}")