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

resp_JSON = {"sessions":[{"center_id":661924,"name":"GGS Patna City (Covaxin)","address":"Ashok Rajpath","state_name":"Bihar","district_name":"Patna","block_name":"Patna Sadar","pincode":800008,"from":"09:00:00","to":"18:00:00","lat":25,"long":85,"fee_type":"Free","session_id":"44551190-6c30-4d94-9d04-9ff73e3cecce","date":"05-06-2021","available_capacity_dose1":0,"available_capacity_dose2":0,"available_capacity":0,"fee":"0","min_age_limit":45,"vaccine":"COVAXIN","slots":["09:00AM-11:00AM","11:00AM-01:00PM","01:00PM-03:00PM","03:00PM-06:00PM"]}]}

# Variables to store intermediate values
time_interval = 20 # (in seconds) Specify the frequency of code execution
vaccine_found_status_45 = False
vaccine_found_status_18 = False
sent_dates_record  = [] # List of dates for age group 45+ for which one round of message has been sent
pincodes_served_today_45 = []
pincodes_served_today_18 = []
centers_served_today_45 = []
centers_served_today_18 = []

header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}

def update_date_time():
    print ()
    print ("FUNCTION CALL: Updating date and Time ..")
    IST = pytz.timezone('Asia/Kolkata')
    raw_TS = datetime.now(IST) + timedelta(days=1) # One day ahead
    tomorrow_date = raw_TS.strftime("%d-%m-%Y")
    today_date = datetime.now(IST).strftime("%d-%m-%Y") #Current Date
    curr_time = (datetime.now(IST).strftime("%H:%M:%S")) # Current time
    return today_date, tomorrow_date, curr_time

def refresh_api_call(Dist_ID, tomorrow_date):
    print ("FUNCTION CALL: Refreshing API call with updated parameters ...")
    request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={Dist_ID}&date={tomorrow_date}"
    # print (request_link)
    response = requests.get(request_link, headers = header)
    resp_JSON = response.json()
    # print ("Size of Response in MB: ", len(response.content)/1000000)
    # print ("Response Header: ", response.headers)
    return resp_JSON


def send_msg_on_telegram(msg, today_date):
    print ("FUNCTION CALL: Sending Messege on Telegram ....")
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
        vaccine_found_status_45 = True
        msg = f"""Vaccine AVAILABLE\n[For age 45 and above] at Pincode: {pincode}\nCenter: {center_name} on {slot_date}\nVaccine: {vaccine_name}\nDose_1: {qnty_dose_1}\nDose_2: {qnty_dose_2}\n\nRegistration link: https://selfregistration.cowin.gov.in/"""
        if (pincode not in pincodes_served_today_45) or (center_name not in centers_served_today_45) or (str(today_date) not in sent_dates_record):
            pincodes_served_today_45.append(pincode)
            centers_served_today_45.append(center_name)
            send_msg_on_telegram(msg, today_date)
            # print (msg) # For local testing
        else:
            print (f"For Age 45+: Pincode {pincode} center name: {center_name} on {today_date} already served")
    else:
        vaccine_found_status_45 = False
        # print (f"Checked at [{today_date}-{curr_time}] : No Vaccine Slots for 45+ available for {tomorrow_date}")
        
        
def get_availability_for_18(age_limit, available_capacity):
    # print ("Checking availability for Age 18 to 44")
    if (age_limit == 18) and (available_capacity > 0):
        vaccine_found_status_18 = True
        msg = f"""Vaccine AVAILABLE\n[For age 18 to 44] at Pincode: {pincode}\nCenter: {center_name} on {slot_date}\nVaccine: {vaccine_name}\nDose_1: {qnty_dose_1}\nDose_2: {qnty_dose_2}\n\nRegistration link: https://selfregistration.cowin.gov.in/"""
        if (pincode not in pincodes_served_today_18) or (center_name not in centers_served_today_18) or (str(today_date) not in sent_dates_record):        
            pincodes_served_today_18.append(pincode)
            centers_served_today_18.append(center_name)
            send_msg_on_telegram(msg,today_date)
            # print (msg) # For local testing
        else:
            print (f"For Age 18+: Pincode {pincode} center name: {center_name} on {today_date} already served")
    else:
        vaccine_found_status_18 = False
        # print (f"Checked at [{today_date}-{curr_time}] : No Vaccine Slots for 18+ available for {tomorrow_date}")


num_iterations = 0
while True:
    num_iterations += 1
    today_date, tomorrow_date, curr_time = update_date_time()
    resp_JSON = refresh_api_call(Dist_ID, tomorrow_date)
    sess_len = len(resp_JSON['sessions'])
    print (f"INFO [{today_date}-{curr_time}] : Checking for VACCINES availabilities on the Portal")

    if sess_len > 0:
        for sess in resp_JSON["sessions"]:
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
            
        if vaccine_found_status_18 == False:
            print (f"INFO [{today_date}-{curr_time}] : NO Vaccine found for Age 18 to 44")
        else:
            print (f"INFO [{today_date}-{curr_time}] : Vaccine FOUND for Age 18 to 44")
            
        if vaccine_found_status_45 == False:
            print (f"INFO [{today_date}-{curr_time}] : NO Vaccine found for 45+")
        else:
            print (f"INFO [{today_date}-{curr_time}] : Vaccine FOUND for 45+")
        
        # Update the dates in the list after sending one complete round of messages
        if str(today_date) not in sent_dates_record:
            sent_dates_record.append(str(today_date))

        print (f"waiting........ for {time_interval} seconds")
        print ()
        time.sleep(time_interval)
        
    else:
        print (f"ERROR [{today_date}-{curr_time}] : No Information available on COWIN server.. looks like no Sessions for {tomorrow_date}")

        
    print (f"INFO : Total Number of times this code has checked CoWIN portal is: {num_iterations}")