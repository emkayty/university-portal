"""Finance App - Fees, Payments, Payroll Models"""
import uuid
from django.db import models
from django.conf import settings
from apps.academic.models import Programme, AcademicSession


class FeeItem(models.Model):
    """Fee Item"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_compulsory = models.BooleanField(default=True)
    programme = models.ForeignKey(
        Programme,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='fee_items'
    )
    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name='fee_items'
    )
    level = models.IntegerField(default=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fee_items'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.amount}"


class StudentFee(models.Model):
    """Student Fee Record"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_fees'
    )
    fee_item = models.ForeignKey(
        FeeItem,
        on_delete=models.CASCADE,
        related_name='student_fees'
    )
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        db_table = 'student_fees'
        unique_together = ['student', 'fee_item']
    
    def __str__(self):
        return f"{self.student.email} - {self.fee_item.name}"
    
    @property
    def balance(self):
        return self.amount_due - self.amount_paid
    
    @property
    def is_fully_paid(self):
        return self.amount_paid >= self.amount_due


class Payment(models.Model):
    """Payment Record"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_ref = models.CharField(max_length=50, unique=True)
    gateway = models.CharField(max_length=20)  # paystack, flutterwave
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)
    invoice_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.payment_ref} - {self.amount}"


class Scholarship(models.Model):
    """Scholarship"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scholarships'
    )
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    awarded_by = models.CharField(max_length=255)
    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name='scholarships'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'scholarships'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.student.email}"


class PayrollRecord(models.Model):
    """Payroll Record"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payroll_records'
    )
    month = models.CharField(max_length=7)  # YYYY-MM
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'payroll_records'
        unique_together = ['staff', 'month']
        ordering = ['-month', '-generated_at']
    
    def __str__(self):
        return f"{self.staff.email} - {self.month}"
    
    def save(self, *args, **kwargs):
        self.net_pay = self.basic_salary + self.allowances - self.deductions
        super().save(*args, **kwargs)