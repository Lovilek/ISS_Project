import requests
import smtplib
from datetime import datetime
import time

MY_LAT = 43.660084
MY_LONG = 51.149294
email = "wingeddemon2274@gmail.com"
password = "ermwhcbqlfqecxql"

parameter = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}


def iss_is_here():
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data2 = response_iss.json()
    iss_lat = float(data2["iss_position"]["latitude"])
    iss_lng = float(data2["iss_position"]["longitude"])
    if 38 <= iss_lat <= 48 and 46 <= iss_lng <= 56:
        return True


def is_night():
    response_sunrise_sunset = requests.get(url="https://api.sunrise-sunset.org/json", params=parameter)
    response_sunrise_sunset.raise_for_status()
    data = response_sunrise_sunset.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 5
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 5
    hour_now = datetime.now().hour
    if hour_now > sunset or hour_now < sunrise:
        return True


SENT_EMAIL = True
while SENT_EMAIL:
    time.sleep(60)
    if is_night() and iss_is_here():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email, to_addrs=email, msg="Subject:ISS HERE\n\n Look up and try to find ISS")
        SENT_EMAIL = False
