
""" 
Developer: aipython on [12-05-2021]
website: www.aipython.in

This Programe demonstrates the use case of  COWIN API (available in public domain) to view the the availability of 
vaccin type, Minimum eligible age, Available slot for a particular date and pincode.

Check for COVID vaccine availability near you using Python | covid vaccine registration India | Python api
"""

import requests #can be installed using:  pip install requests

PINCODE = "0"
while len(PINCODE) != 6:
    PINCODE = input("Enter the pincode for which you want the status => ")
    if len(PINCODE) < 6:
        print (f"{PINCODE} is shorter than the actual length")
    elif len(PINCODE) > 6:
        print (f"{PINCODE} is longer than the actual length")
    
REQ_DATE = input ("Enter the Date to get status (Date format: DD-MM-YYYY) => ")

request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={REQ_DATE}"
header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}
response = requests.get(request_link, headers = header)
raw_JSON = response.json()

Total_centers = len(raw_JSON['centers'])
print ()
print ("                        *>>>>>>    RESULTS   <<<<<<<*                                ")
print ("-------------------------------------------------------------------------------------")
print (f"Date: {REQ_DATE} | Pincode: {PINCODE} ")

if Total_centers != 0:
    print (f"Total centers in your area is: {Total_centers}" )
else:
    print (f"Unfortunately !! Seems like no center in this area / Kindly re-check the Pincode" )

print ("------------------------------------------------------------------------------------")
print ()

for cent in range(Total_centers):
    print ()
    print (f"[{cent+1}] Center Name:", raw_JSON['centers'][cent]['name'])
    print ("------------------------------------------------------------")
    print ("   Date      Vaccine Type    Minimum Age    Available ")
    print ("  ------     -------------   ------------   ----------")
    this_session = raw_JSON['centers'][cent]['sessions']
    
    for _sess in range(len(this_session)):
        print ( "{0:^12} {1:^12} {2:^14} {3:^16} ".format(this_session[_sess]['date'], this_session[_sess]['vaccine'], this_session[_sess]['min_age_limit'], this_session[_sess]['available_capacity']))
