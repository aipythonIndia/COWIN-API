
""" 
Developer: aipython on [29-05-2021]
website: www.aipython.in

Sends Notifications on a Telegram channel , whenever the vaccine slot is available at the given PINCODE 
"""

import requests #can be installed using:  pip install requests
from datetime import date

raw_TS = date.today()
formatted_date = raw_TS.strftime("%d-%m-%Y")
PINCODE = "802128"

msg = "Blank"
auth_token = "1802553040:AAEJOBYkPpvJuHxveA4Fs5C5OLIAQhbwGTI"
tel_group_id = "cowin_danapur_vaccine"

request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={formatted_date}"
header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}

response = requests.get(request_link, headers = header)
raw_JSON = response.json()

slot_found =  False

def get_availability_45(age = 45):
    for cent in raw_JSON['centers']:
        for sess in cent["sessions"]:
            if sess["min_age_limit"] == age and sess["available_capacity"] > 0:
                slot_found =  True
                msg = f"""For age 45+ [Vaccine Available]\n\tCenter : {cent["name"]}\n\tVaccine: {sess["vaccine"]}\n\tDose_1: {sess["available_capacity_dose1"]}\n\tDose_2: {sess["available_capacity_dose2"]}"""
            else:
                slot_found =  False
                msg = f" For Age category 45+  >> No slot Available at PINCODE: {PINCODE}"
    
    send_msg_on_telegram(msg)
        
def get_availability_18(age = 18):
    for cent in raw_JSON['centers']:
        for sess in cent["sessions"]:
            if sess["min_age_limit"] == age and sess["available_capacity"] > 0:
                slot_found =  True
                msg = f"""For age 18+ [Vaccine Available]\n\tCenter : {cent["name"]}\n\tVaccine: {sess["vaccine"]}\n\tDose_1: {sess["available_capacity_dose1"]}\n\tDose_2: {sess["available_capacity_dose2"]}"""
            else:
                slot_found =  False
                msg = f" For Age category 18+  >> No slot Available at PINCODE: {PINCODE}"
    
    send_msg_on_telegram(msg)

def send_msg_on_telegram(msg):
    telegram_api_url = f"https://api.telegram.org/bot{auth_token}/sendMessage?chat_id=@{tel_group_id}&text={msg}"
    tel_resp = requests.get(telegram_api_url)

    if tel_resp.status_code == 200:
        print ("Notification has been sent on Telegram")
    else:
        print ("Could not send Message")
        
        
get_availability_45()
get_availability_18()

