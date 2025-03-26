from rest_framework import serializers
from .models import Bank, LoanProduct, Holidays


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class LoanProductSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='bank.name')

    class Meta:
        model = LoanProduct
        fields = [
            'id',
            'name',
            'min_amount',
            'max_amount',
            'min_term',
            'max_term',
            'interest_rate',
            'bank_name'
        ]
        extra_kwargs = {'bank': {'read_only': True}}

    def create(self, validated_data):
        bank_name = validated_data.pop('bank_name')
        try:
             bank = Bank.objects.get(name=bank_name)
        except Bank.DoesNotExist:
             raise serializers.ValidationError({"bank_name": "해당 은행이 존재하지 않습니다."})

        loan_product = LoanProduct.objects.create(bank=bank, **validated_data)
        return loan_product


class HolidaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holidays
        fields = '__all__'


