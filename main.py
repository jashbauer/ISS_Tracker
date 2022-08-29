import time
from mail_manager import Mailer
from api_extractor import Requester

MY_LATITUDE = -22.345524
MY_LONGITUDE = -48.764423

MY_LOCATION = (MY_LONGITUDE, MY_LATITUDE)

TOLERANCE = 5.0  # Tolerance rate for changes in ISS movement


MY_EMAIL = "your_gmail@gmail.com"
PASSWORD = "xxxxxxxxxxxxxxxxx"

REFRESH_TIME = 30

# DEFINING OBJECTS
request_manager = Requester(longitude=MY_LONGITUDE, latitude=MY_LATITUDE, tolerance=TOLERANCE)
mail_sender = Mailer(email=MY_EMAIL, password=PASSWORD)

# Run for every [REFRESH TIME] amount of time
while True:
    iss_long = request_manager.iss_position_now["longitude"]
    iss_lat = request_manager.iss_position_now["latitude"]
    current_hour = request_manager.hour_now
    visibility_hour = request_manager.day_data["sunset"]

    if request_manager.condition_checker():
        message = "It's time to check the sky! ISS in range and nighttime!"
        print(message)
        mail_sender.send_mail(message=message)
    else:
        print("ISS not in range or daytime.")
        print(f"Current hour in your location (24h format): {current_hour}h")
        print(f"Current hour must be >= {visibility_hour} for ISS to be visible.")
        print(f"Your position: (long = {MY_LONGITUDE}, lat = {MY_LATITUDE})")
        print(f"ISS Position: (long = {iss_long}, lat = {iss_lat})")

    print()
    time.sleep(REFRESH_TIME)
