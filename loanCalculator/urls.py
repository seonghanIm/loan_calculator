from django.urls import path
from .views import create_bank, create_loan_product, get_loan_product, calculate_schedule,main_page

urlpatterns = [
    path('banks/', create_bank, name='create_bank'),  # 은행 등록 API
    path('loans/', create_loan_product, name='create_loan_product'), # 대출 상품 등록 API
    path('loans/list/', get_loan_product, name='get_loan_product'), # 대출 상품 조회 API
    path('calculate/schdeule/', calculate_schedule, name='calculate_schedule'), # 대출 상품 조회 API
    path('',main_page, name='main')
]