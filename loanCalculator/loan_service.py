from calendar import monthrange
from datetime import datetime
from decimal import Decimal

from loanCalculator.models import LoanProduct
from loanCalculator.utils import get_next_business_day, loan_validate


def calculate_schedule_func(product: LoanProduct, amount: Decimal, term: int, start_date):
    monthly_rate = float(product.interest_rate) / 100 / 12
    amount = float(amount)
    term = int(term)

    # validate = loan_validate(amount, term, product)
    # if validate:
    #     return {"error": validate}

    if monthly_rate == 0:
        monthly_payment = float(amount) / term
    else:
        monthly_payment = float(amount) * monthly_rate / (1 - (1 + monthly_rate) ** - term)

    total_payment = monthly_payment * term
    total_interest = total_payment - float(amount)

    today = datetime.today()

    base_day = int(start_date)
    schedule = []
    principal_balance = amount
    for i in range(term):
        month = today.month + i + 1
        year = today.year + (month - 1) // 12
        month = (month - 1) % 12 + 1

        _, last_day = monthrange(year, month)

        day = min(base_day, last_day)
        raw_pay_date = datetime(year, month, day)
        pay_date = get_next_business_day(raw_pay_date)

        interest = principal_balance * monthly_rate
        principal_payment = monthly_payment - interest
        principal_balance -= principal_payment

        schedule.append({
            "count": str(i + 1) + "회차",
            "date": pay_date.strftime("%Y-%m-%d"),
            "amount": "{:,}".format(round(int(monthly_payment), -1)),
            "remaining_principal": "{:,}".format(round(max(principal_balance, 0)))
        })

    return {
        "interest_rate": product.interest_rate,
        "monthly_payment": "{:,}".format(round(int(monthly_payment), -1)),
        "total_payment": "{:,}".format(round(int(total_payment), -1)),
        "total_interest": "{:,}".format(round(int(total_interest), -1)),
        "schedule": schedule
    }
