from django.db import models

class Loan(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    term = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.id}: {self.amount}원 , {self.term}개월, {self.interest_rate}%"

class Bank(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class LoanProduct(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    min_term = models.IntegerField()
    max_term = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.bank.name} - {self.name}"

class Holidays(models.Model):
    yearMonth = models.CharField(max_length=6)
    holiday = models.DateField()

    def __str__(self):
        return f"{self.year} : {self.holiday}"
