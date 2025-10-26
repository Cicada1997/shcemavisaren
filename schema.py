from datetime import datetime
import requests
import json

debug = False

def fetch_schema():
    url_1 = "https://web.skola24.se/api/get/timetable/render/key"

    headers_1 = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "X-Scope": "8a22163c-8662-4535-9050-bc5e1923df48",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-GPC": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0"
    }

    print(f"fetching data from server {url_1}")
    response_1 = requests.post(url_1, headers=headers_1) #, cookies={'session': 'your_session_here'})  # Insert session cookie if required

# Check if the first request was successful and extract the key
    if response_1.status_code == 200:
        response_json = response_1.json()
        key = response_json.get("data", {}).get("key")
        
        if not key:
            print("No key found in the response.")
        else:
            # Second fetch
            url_2 = "https://web.skola24.se/api/render/timetable"

            headers_2 = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "application/json",
                "X-Scope": "8a22163c-8662-4535-9050-bc5e1923df48",
                "X-Requested-With": "XMLHttpRequest",
                "Sec-GPC": "1",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin"
            }

            week = datetime.now().isocalendar()[1]

            week_request_data = {
                "renderKey": key,
                "host": "nacka.skola24.se",
                "unitGuid": "YWE2NDNjMWItNDBhMC1mZDc0LWFiZGQtNTllZTYzMGJjYTJl",
                "schoolYear": "cd04382d-0e07-4bfc-ae84-59ee04bc07c7",
                "startDate": None,
                "endDate": None,
                "scheduleDay": 0,
                "blackAndWhite": False,
                "width": 717,
                "height": 1050,
                "selectionType": 0,
                "selection": "ZDlkOTg3YjYtYmFjMS1mNmFlLWI0ZWQtMjA3YjBkZjliY2M4",
                "showHeader": False,
                "periodText": "",
                "week": week,
                "year": 2025,
                "privateFreeTextMode": None,
                "privateSelectionMode": False,
                "customerKey": "",
                "personalTimetable": False
            }

            
            week_data = requests.post(url_2, headers=headers_2, json=week_request_data, cookies={'session': 'your_session_here'})  # Insert session cookie if required
            json_data = json.loads(week_data.text)
            lesson_info = json_data["data"]["lessonInfo"]
            return lesson_info
    else:
        print(f"Error in the first request: {response_1.status_code} - {response_1.text}")


class Lesson:
    def __init__(self, lesson):
        texts        = lesson["texts"]
        self.name    = texts[0]
        if len(texts) > 1:
            self.teacher = texts[1] # Unknown
            self.room    = texts[2]

        self.start   = lesson["timeStart"]
        self.end     = lesson["timeEnd"]

    def start_time_in_min(self):
        hours_in_min = int(self.start[0:2]) * 60
        min          = int(self.start[3:5])

        sum = hours_in_min + min

        return sum


class Day:
    def __init__(self, name: str = ""):
        self.name = name
        self.lessons = []

    def append(self, lesson):
        self.lessons.append(lesson)

    def sort(self):
        self.lessons = sorted(self.lessons, key=lambda lesson: lesson.start_time_in_min())

week = {
    0: "Måndag" ,
    1: "Tisdag" ,
    2: "Onsdag" ,
    3: "Torsdag" ,
    4: "Fredag" ,
    5: "Lördag" ,
    6: "Söndag" 
}


def get_schema():
    formatted = []
    for d_num in range(7):
        formatted.append(Day(week[d_num]))

    json_schema = fetch_schema()

    for lesson in json_schema:
        weekday_index = lesson["dayOfWeekNumber"] -1
        
        formatted[weekday_index].append(Lesson(lesson))


    for day in formatted:
        day.sort()
        if debug: print(day.name)
        for less in day.lessons:

            if debug: print(less.start)

    return formatted

    # for lesson in json_schema:
    #     new_weekday_index = lesson["dayOfWeekNumber"]
    #
    #     if weekday_index != new_weekday_index:
    #         for diff in range(new_weekday_index - weekday_index):
    #             day = Day()
    #             day.name = week[diff + weekday_index]
    #             formatted.append(day)
    #
    #         weekday_index = new_weekday_index
    #
    #     print(formatted)
    #     print(weekday_index - 1)
    #
    #     formatted[weekday_index -1].append(Lesson(lesson))
    #
    #
    # return formatted

# json_schema = fetch_schema()
#
#
# cur_day = ""
# cur_day_num = 0
# last_day_num = 0
#
# for lesson in json_schema:
#     cur_day_num = lesson["dayOfWeekNumber"]
#
#     if cur_day_num != last_day_num and cur_day_num:
#         print()
#         print(f"{ WEEK[cur_day_num -1] }")
#
#     last_day_num = cur_day_num
#
#     print(f" │")
#     print(f" ├──{ lesson["texts"][0] }\t{ "in" if lesson["texts"][2] != "" else "" } { lesson["texts"][2] }")
#     print(f" │  ├──starts\tat { lesson["timeStart"] }")
#     print(f" │  └──ends  \tat { lesson["timeEnd"] }")
