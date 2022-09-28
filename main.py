import os
import smtplib
from datetime import datetime
from time import sleep
from typing import Tuple

import requests

LATITUDE = float(os.getenv("LATITUDE"))
LONGITUDE = float(os.getenv("LONGITUDE"))

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 0))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")


def get_sunrise_and_sunset_hours() -> Tuple[int, int]:
    parameters = {"lat": LATITUDE, "lng": LONGITUDE, "formatted": 0}
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    return sunrise, sunset


def is_dark_now() -> bool:
    sunrise, sunset = get_sunrise_and_sunset_hours()
    current_hour = datetime.utcnow().hour
    return current_hour < sunrise or current_hour > sunset


def get_iss_latitude_and_longitude() -> Tuple[float, float]:
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    latitude = float(data["iss_position"]["latitude"])
    longitude = float(data["iss_position"]["longitude"])
    return latitude, longitude


def is_near_iss() -> bool:
    user_lat, user_long = LATITUDE, LONGITUDE
    iss_lat, iss_long = get_iss_latitude_and_longitude()
    return abs(user_lat - iss_lat) < 5 and abs(user_long - iss_long) < 5


def notify_iss_near():
    email_subject = "The ISS is above you"
    email_text = "It is currently dark and the ISS is near your latitude and longitude. You should be able to see it " \
                 "from your location."

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
        connection.starttls()
        connection.login(user=SENDER_EMAIL, password=SENDER_EMAIL_PASSWORD)
        message = f"Subject:{email_subject}\n\n{email_text}"
        connection.sendmail(from_addr=SENDER_EMAIL, to_addrs=RECIPIENT_EMAIL, msg=message)


while True:
    if is_dark_now() and is_near_iss():
        notify_iss_near()
    sleep(60)