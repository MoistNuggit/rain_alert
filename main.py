import requests
from twilio.rest import Client
import smtplib
import os

# BELOW ARE ACCOUNT INFO RELATED TO OPENWEATHERMAP
OPENWEATHER_ENDPOINT = 'https://api.openweathermap.org/data/3.0/onecall'

API_KEY1 = os.environ.get('OPENWEATHER_API_KEY')
# API_KEY2 = 'f680a3968a9d6f5ccfc14825eab9b61a'
# ANGELA_API_KEY = '69f04e4613056b159c2761a9d9e664d2'

parameters = {
    'lat': float(os.environ.get('MY_LAT')),
    'lon': float(os.environ.get('MY_LON')),
    'appid': API_KEY1,
    'excluse': 'current,minutely,daily'
}

# BELOW ARE ACCOUNT INFO RELATED TO TWILIO
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
RECEIVER_PHONE_NUMBER = os.environ.get('RECEIVER_PHONE_NUMBER')

# BELOW IS TO GET A JSON CONTAINING A LIST OF FORECAST OF NEXT 12 HOURS
response = requests.get(url=OPENWEATHER_ENDPOINT, params=parameters)
response.raise_for_status()
weather_data = response.json()
# print(weather_data)
hourly = weather_data['hourly']
# print(hourly)

def send_notification_email():
    my_email = "owenpythontest@gmail.com"
    # MY_PASSWORD IS APP PASSWORD
    my_password = os.environ.get('YAHOO_APP_PASSWORD')

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs="owenthatasian@yahoo.com",
                            msg="Subject:It's going to rain today! \n\n"
                                "Well, it's going to rain today. I don't know what else to write here, uhhhh"
                                " I guess bring an umbrella? Who uses umbrellas nowadays anyway? This isn't even"
                                " supposed to be a legit notification anyway I'm just using this to test out my"
                                " stupid Python codes. So yeah, it'll rain. I guess...BTW the part about it raining"
                                " is true. Like it's actually going to rain according to the weather forecast. "
                                "Just keep that in mind. Yeah that's all I guess.")


def will_rain():
    for hour in hourly[:13]:
        if hour['weather'][0]['id'] < 700:
            return True

if will_rain():
    # print('Bring an umbrella')
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body= "Guess what. It's going to rain today. Bring an umbrella.",
        from_= TWILIO_PHONE_NUMBER,
        to = RECEIVER_PHONE_NUMBER
    )
    print(message.status)

    send_notification_email()

