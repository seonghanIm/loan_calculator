from datetime import date

from django.test import TestCase
from django.urls import reverse

from loanCalculator.holidays import fetch_holidays_from_api
from loanCalculator.models import LoanProduct, Bank
from loanCalculator.utils import is_holiday
from loanCalculator.views import get_loan_product


class HolidayFunctionTest(TestCase):
    def test_fetch_march_2025(self):
        holidays = fetch_holidays_from_api("202325")
        print("function res :", holidays)

        self.assertIsInstance(holidays,list)
        self.assertTrue(all(isinstance(date, str) for date in holidays))
        self.assertTrue(any("2025-04") in date for date in holidays)

    def test_is_holiday(self):
        res = is_holiday(date(2025,1,27))
        print("is_holiday res:", res)

        self.assertIsInstance(res, bool)
        self.assertTrue(res)

    def setUp(self):
        bank = Bank.objects.create(name="신한은행")
        LoanProduct.objects.create(
            bank=bank,
            name="신한 마이카 대출",
            min_amount=1000000,
            max_amount=50000000,
            min_term=12,
            max_term=60,
            interest_rate=4.2
        )

    def test_get_loan_products(self):
        url = reverse('get_loan_product')
        res = self.client.get(url)

        print('test_get_loan_products : ',res.data)

        self.assertEqual(res.status_code,200)
        self.assetIsInstance(res,list)
