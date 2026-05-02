"""Library Models"""
from django.db import models

class LibraryMember(models.Model):
    student = models.OneToOneField('student.StudentProfile', on_delete=models.CASCADE)
    library_id = models.CharField(max_length=20, unique=True)
    member_since = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')

class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100, blank=True)
    copies_total = models.IntegerField(default=1)
    copies_available = models.IntegerField(default=1)

class BookIssue(models.Model):
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='issued')
