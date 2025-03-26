from calendar import monthrange
from datetime import datetime
from decimal import Decimal

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .loan_service import calculate_schedule_func
from .models import Bank, LoanProduct
from .serializer import BankSerializer, LoanProductSerializer
from .utils import get_next_business_day, loan_validate


@api_view(['POST'])
def create_bank(request):
    serializer = BankSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_loan_product(request):
    serializer = LoanProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_loan_product(request):
    products = LoanProduct.objects.select_related('bank').all()
    serializer = LoanProductSerializer(products, many=True)
    return Response(serializer.data)


## 계산
## input 으로 대출 상품 ID, 대출 받을 금액, 대출 기간
## output 으로 월별 납입일과 납입 금액
@api_view(['POST'])
def calculate_schedule(request):
    try:
        loan_product_id = int(request.data.get("loan_product_id"))
        amount = Decimal(request.data.get("amount"))
        term = int(request.data.get("term"))
    except (TypeError, ValueError):
        return Response({"error": "입력값이 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = LoanProduct.objects.get(id=loan_product_id)
    except LoanProduct.DoesNotExist:
        return Response({"error": "해당 대출 상품이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

    result = calculate_schedule_func(product, amount, term)
    return Response(result)


def main_page(request):
    banks = Bank.objects.all()
    products = LoanProduct.objects.select_related("bank").all()
    result = None

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "bank":
            name = request.POST.get("bank_name")
            if name:
                Bank.objects.get_or_create(name=name)

        elif form_type == "loan":
            bank = Bank.objects.get(id=request.POST.get("bank_id"))
            LoanProduct.objects.create(
                bank=bank,
                name=request.POST.get("name"),
                min_amount=request.POST.get("min_amount"),
                max_amount=request.POST.get("max_amount"),
                min_term=request.POST.get("min_term"),
                max_term=request.POST.get("max_term"),
                interest_rate=request.POST.get("interest_rate"),
            )

        elif form_type == "calculate":
            product = LoanProduct.objects.get(id=request.POST.get("loan_product_id"))
            amount = request.POST.get("amount")
            term = request.POST.get("term")
            start_date = request.POST.get("start_date")
            validate_msg = loan_validate(amount, term, product)
            if validate_msg:
                return render(request, "loanCalculator/main.html", {
                    "error": validate_msg
                })

            result = calculate_schedule_func(product, amount, term,start_date)

    return render(request, "loanCalculator/main.html", {
        "banks": banks,
        "products": products,
        "result": result,
        "days": range(1,32)
    })
