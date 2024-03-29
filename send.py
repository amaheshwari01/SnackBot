from twilio.rest import Client
import csv
from datetime import datetime, timedelta
import requests as rs
import keys


client = Client(keys.account_sid, keys.auth_token)

res = rs.get(url=(keys.sheet_url + "&output=csv"))
open("./snacks.csv", "wb").write(res.content)


def calculate_days_until_date(target_date_str):
    try:
        current_date = datetime.now().date()
        target_date = datetime.strptime(target_date_str, "%m/%d/%Y").date()
        days_until_target = (target_date - current_date).days

        return days_until_target
    except ValueError:
        return -1


def get_day_of_week(date_str):
    date_obj = datetime.strptime(date_str, "%m/%d/%Y")
    day_of_week = date_obj.strftime("%A")
    return day_of_week


try:
    with open("./snacks.csv", "r") as csvFile:
        reader = csv.reader(csvFile)
        count = 0
        for row in reader:
            daystill = calculate_days_until_date(row[1])
            if daystill >= 0 and daystill <= 3:
                print(row[0])
                message = client.messages.create(
                    to="+1" + str(row[2]),
                    from_=keys.twillio_number,
                    body="Hi {} \nThis is Aayans Very COOL bot to remind you to bring snacks to the MATE meeting in {} days it will be next {} \n\nIf you have any questions or cannot bring snacks that day pls message Aayan on teams or iMessage(5105745257)".format(
                        row[0], daystill, get_day_of_week(row[1])
                    ),
                )
                message = client.messages.create(
                    to=keys.admin_number,
                    from_=keys.twillio_number,
                    body="Sent Message to {} phone number {} will bring snacks in {} days".format(
                        row[0], row[2], daystill
                    ),
                )
except Exception as err:
    errmessage = f"Unexpected {err=}, {type(err)=}"
    message = client.messages.create(
        to=keys.admin_number,
        from_=keys.twillio_number,
        body=errmessage,
    )
