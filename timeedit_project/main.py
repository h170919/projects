import requests
from datetime import datetime, timedelta

urls = [
    "https://cloud.timeedit.net/hvl/web/pen/ri102v5y6867Z6QY57Q07YgXZQ0168Y660Q5.json",  # 1093
    "https://cloud.timeedit.net/hvl/web/pen/ri102v5y6867Z6QY37Q47YgXZQ0968Y660Q5.json",  # 1090
    "https://cloud.timeedit.net/hvl/web/pen/ri102v5y6867Z6QY47Q47YgXZQ0968Y660Q5.json",  # 1091
    "https://cloud.timeedit.net/hvl/web/pen/ri102v5y6867Z6QY07Q07YgXZQ0168Y660Q5.json",  # 1092
    "https://cloud.timeedit.net/hvl/web/pen/ri102v5y6867Z6QY57Q57YgXZQ0168Y660Q5.json",  # 1094
    "https://cloud.timeedit.net/hvl/web/pen/ri102v5y6867Z6QY47Q67YgXZQ0168Y660Q5.json",  # AUD G
    "https://cloud.timeedit.net/hvl/web/pen/ri102v5y6867Z6QY27Q67YgXZQ0168Y660Q5.json",  # AUD E
    "https://cloud.timeedit.net/hvl/web/pen/ri102v5y6867Z6QY37Q67YgXZQ0168Y660Q5.json",  # AUD F
    "https://cloud.timeedit.net/hvl/web/pen/ri102v5y6867Z6QY47Q57YgXZQ0168Y660Q5.json",  # 2083
    "https://cloud.timeedit.net/hvl/web/pen/ri102v5y6867Z6QY57Q67YgXZQ0168Y660Q5.json", # 2085
    "https://cloud.timeedit.net/hvl/web/pen/ri102v5y6867Z6QY77Q57YgXZQ0168Y660Q5.json"   # 2008
]

current_time_obj = datetime.now()
next_hour_time_obj = current_time_obj + timedelta(hours=1)

free_rooms = []

print("Checking availability...")

for url in urls:
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        reservations = data["reservations"]
        current_time_obj = datetime.now()
        todays_date = current_time_obj.strftime("%d.%m.%Y")

        room_name = reservations[0]["columns"][3] if reservations else "Unknown Room"

        room_is_free = True
        next_reservation = None

        for reservation in reservations:
            startdate = reservation["startdate"]

            if startdate == todays_date:
                starttime_str = reservation["starttime"]
                endtime_str = reservation["endtime"]

                start_time_obj = datetime.strptime(starttime_str, "%H:%M")
                end_time_obj = datetime.strptime(endtime_str, "%H:%M")

                if start_time_obj.time() <= current_time_obj.time() <= end_time_obj.time():
                    room_is_free = False
                    break

                elif current_time_obj.time() < start_time_obj.time():
                    if next_reservation is None or start_time_obj < next_reservation['start_time_obj']:
                        next_reservation = {
                            'start_time_obj': start_time_obj,
                            'starttime_str': starttime_str,
                            'endtime_str': endtime_str
                        }

        if room_is_free:
            if next_reservation:
                time_until_next_reservation = next_reservation['start_time_obj'] - current_time_obj
                free_rooms.append({
                    'room_name': room_name,
                    'current_time': current_time_obj.strftime('%H:%M'),
                    'next_reservation': f"{next_reservation['starttime_str']} to {next_reservation['endtime_str']}",
                    'available_for': f"{time_until_next_reservation.seconds // 60} minutes"

                })
            else:
                free_rooms.append({
                    'room_name': room_name,
                    'current_time': current_time_obj.strftime('%H:%M'),
                    'next_reservation: ': "no more reservations today",
                    'available_for: ': "rest of the day"
                })
    else:
        print(f"Failed to retrieve data for {url}. Status code: {response.status_code}")

if free_rooms:
    print("\nRooms ready:")
    for room in free_rooms:
        print(f"- Room {room['room_name']} is free as of {room['current_time']}.")
        print(f"  It will be available until {room['next_reservation']}, for {room['available_for']}.\n")
        if(next_reservation):
            print(f"  It will be available until {next_reservation['starttime_str']} ({room['available_for']} remaining).")
else:
    print("\nNo rooms are free right now.")
