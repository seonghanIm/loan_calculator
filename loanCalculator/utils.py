from calendar import monthrange
from datetime import timedelta, datetime
from decimal import Decimal

from loanCalculator.holidays import get_holidays_from_db, fetch_holidays_from_api

# db 먼저 조회 후 없으면 API 요청 하여 DB 저장하고 확인까지
from loanCalculator.models import LoanProduct


def is_holiday(date):
    holidays = get_holidays_from_db(date.strftime("%Y%m"))
    if not holidays:
        holidays = fetch_holidays_from_api(date.strftime("%Y%m"))
    if date.strftime("%Y-%m-%d") in holidays:
        return True
    return False


# 주말이나 공휴일이면 다음 영업일로
def get_next_business_day(date: datetime) -> datetime:
    while date.weekday() >= 5 or is_holiday(date):
        date += timedelta(days=1)
    return date


def loan_validate(amount, term, product) -> str:
    amount = Decimal(amount)
    term = int(term)


    if term < product.min_term:
        return f"대출 기간이 너무 짧습니다. 최소 대출 기간은 {product.min_term}개월입니다."

    if term > product.max_term:
        return f"대출 기간이 너무 깁니다. 최대 대출 기간은 {product.max_term}개월입니다."

    if amount < product.min_amount:
        min_amount = "{:,}".format(int(product.min_amount))
        return f"대출 금액이 너무 적습니다. 최소 대출 금액은 {min_amount}원 입니다."

    if amount > product.max_amount:
        max_amount = "{:,}".format(int(product.max_amount))
        return f"대출 금액이 너무 많습니다. 최대 대출 금액은 {max_amount}원 입니다."

    return ""
