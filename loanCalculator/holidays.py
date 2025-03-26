from datetime import datetime
from loanCalculator.models import Holidays
import requests

from loanCalculator.serializer import HolidaysSerializer
from pfct.settings import PUBLIC_HOLIDAY_API_KEY, PUBLiC_HOLIDAY_API_URL


def fetch_holidays_from_api(date_str):
    date = datetime.strptime(date_str, "%Y%m")

    url = PUBLiC_HOLIDAY_API_URL
    params = {'serviceKey': PUBLIC_HOLIDAY_API_KEY,
              'pageNo': '1',
              'numOfRows': '31',
              'solYear': date.strftime("%Y"),
              'solMonth': date.strftime("%m"),
              '_type': 'json'
              }
    response = requests.get(url, params=params)
    holidays = []

    data = response.json()
    response_body_data = data.get("response").get("body")

    if "item" not in response_body_data.get("items"):
        return holidays

    items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
    if not isinstance(items, list):
        raw = str(items["locdate"])
        formatted = datetime.strptime(raw, "%Y%m%d").strftime("%Y-%m-%d")
        holidays.append(formatted)
    else:
        for item in items:
            raw = str(item["locdate"])
            formatted = datetime.strptime(raw, "%Y%m%d").strftime("%Y-%m-%d")
            holidays.append(formatted)

    ## 저장
    input_data = [
        {"yearMonth": date.strftime("%Y%m"), "holiday": holiday}
        for holiday in holidays
    ]

    save_holiday(input_data)
    return holidays


def get_holidays_from_db(year_month: str):
    holidays = Holidays.objects.filter(yearMonth=year_month)
    return {h.holiday.strftime("%Y-%m-%d") for h in holidays}


def save_holiday(input_data: list):
    serializer = HolidaysSerializer(data=input_data, many=True)
    saved = []
    for item in input_data:
        holiday = item["holiday"]
        if isinstance(holiday, str):
            datetime.strptime(holiday, "%Y-%m-%d").date()

        obj, created = Holidays.objects.get_or_create(
            yearMonth=item["yearMonth"],
            holiday=holiday
        )

        if created:
            saved.append(obj)

    return {
        "saved": saved
    }
