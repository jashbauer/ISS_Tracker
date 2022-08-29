import requests
import datetime as dt


class Requester:

    def __init__(self, longitude, latitude, tolerance):
        self.longitude = longitude
        self.latitude = latitude
        self.tolerance = tolerance
        self.iss_position_now = self.iss_data()
        self.hour_now = self.time_now()
        self.day_data = self.sunset_time()

    def time_now(self):
        now = dt.datetime.now()
        hour_now = now.hour
        self.hour_now = hour_now
        return hour_now

    def sunset_time(self):
        parameters = {
            "lat": self.latitude,
            "lng": self.longitude,
            "formatted": 0

        }

        response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()
        data = response.json()

        sunrise = data["results"]["sunrise"]
        sunset = data["results"]["sunset"]

        sunrise_hour = int(sunrise.split(sep="T")[1].split(sep=":")[0])
        sunset_hour = int(sunset.split(sep="T")[1].split(sep=":")[0])

        day_data = {"sunrise": sunrise_hour, "sunset": sunset_hour}
        self.day_data = day_data
        return day_data

    def iss_data(self):
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()

        data = response.json()

        longitude = float(data["iss_position"]["longitude"])
        latitude = float(data["iss_position"]["latitude"])

        iss_position = {"longitude": longitude, "latitude": latitude}

        self.iss_position_now = iss_position
        return iss_position

    def condition_checker(self):
        iss_info = self.iss_data()
        iss_long = iss_info["longitude"]
        iss_lat = iss_info["latitude"]

        sunset_here = self.sunset_time()["sunset"]

        lower_lat = iss_lat - self.tolerance
        upper_lat = iss_lat + self.tolerance
        lower_log = iss_long - self.tolerance
        upper_long = iss_long + self. tolerance

        hour_now = self.hour_now

        if (lower_lat <= self.latitude <= upper_lat)\
                and (lower_log <= self.longitude <= upper_long) \
                and hour_now >= sunset_here:
            return True
        else:
            return False
